#!/usr/bin/env python3
"""Render the original, captioned skill demonstration from its checked fixture.

Requirements: Python 3, Pillow, ffmpeg; all used locally. No network,
voice synthesis, screen recording, or external assets. Rendered geometric
animation, not a capture of the companion HTML.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT, FPS, DURATION = 1280, 720, 24, 66
COL = {'bg':'#F5F5F0','ink':'#14293D','muted':'#536273','line':'#CDD5D7',
       'white':'#FFFFFF','teal':'#087A6D','teal_bg':'#DDF0E8',
       'amber':'#935C00','amber_bg':'#FFF0CC','purple':'#6951A0','purple_bg':'#EEE8FA',
       'navy':'#14293D','gray_bg':'#E8ECEB','blue_bg':'#E8EFF7'}
FONT_DIR = Path('/usr/share/fonts/opentype/noto')

@lru_cache(None)
def font(size=28, bold=False):
    override = __import__('os').environ.get('DEMO_FONT_BOLD' if bold else 'DEMO_FONT')
    path = Path(override) if override else FONT_DIR / ('NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc')
    if not path.exists():
        raise RuntimeError('Set DEMO_FONT and DEMO_FONT_BOLD to installed CJK font paths.')
    return ImageFont.truetype(str(path), size=size, index=2 if path.suffix=='.ttc' else 0)

def ease(v):
    v=max(0,min(1,v)); return v*v*(3-2*v)

def mix(a,b,v): return a+(b-a)*v

def text(draw, xy, value, size=28, color='ink', bold=False, anchor=None):
    draw.text(xy,str(value),font=font(size,bold),fill=COL.get(color,color),anchor=anchor)

def centered(draw, x, y, value, size=28, color='ink', bold=False):
    text(draw,(x,y),value,size,color,bold,'mm')

def box(draw, xy, fill='white', radius=18, outline=None, width=1):
    draw.rounded_rectangle(xy,radius=radius,fill=COL.get(fill,fill),outline=COL.get(outline,outline),width=width)

def line(draw,xy,fill='line',width=2): draw.line(xy,fill=COL.get(fill,fill),width=width)

def arrow(draw,xy,color='muted',width=3):
    import math
    x1,y1,x2,y2=xy
    line(draw,xy,color,width)
    ang=math.atan2(y2-y1,x2-x1)
    pts=[(x2,y2),(x2-11*math.cos(ang-.5),y2-11*math.sin(ang-.5)),(x2-11*math.cos(ang+.5),y2-11*math.sin(ang+.5))]
    draw.polygon(pts,fill=COL.get(color,color))

def pill(draw,x,y,value,fill='gray_bg',color='ink',size=22):
    w=draw.textlength(value,font=font(size,True))+28
    box(draw,(x,y,x+w,y+38),fill,19)
    centered(draw,x+w/2,y+19,value,size,color,True)
    return w

def wrap(draw,value,width,size):
    lines=[]; cur=''
    for c in value:
        if c=='\n': lines.append(cur);cur='';continue
        if draw.textlength(cur+c,font=font(size))>width and cur:
            lines.append(cur);cur=c
        else: cur+=c
    if cur: lines.append(cur)
    return lines

def wrapped(draw,x,y,value,width=600,size=28,color='ink',spacing=12,bold=False):
    for i,s in enumerate(wrap(draw,value,width,size)):
        text(draw,(x,y+i*(size+spacing)),s,size,color,bold)

# The fixture is extracted from the completed companion HTML and pinned by SHA256.

def base(t,title,chapter,caption):
    im=Image.new('RGB',(WIDTH,HEIGHT),COL['bg']);d=ImageDraw.Draw(im)
    text(d,(54,25),'清晰表达 × 可视化讲解',22,'muted',True)
    text(d,(54,67),title,36,'ink',True)
    pill(d,924,24,'模拟数据 · 非维护建议',fill='amber_bg',color='amber',size=20)
    text(d,(54,123),'固定同一问题、同一组证据，观察 K 改变后的结果。',23,'muted')
    box(d,(40,596,1240,682),'navy',20)
    for j,s in enumerate(caption.split('\n')):
        centered(d,640,624+j*33,s,26,'white',j==0)
    y=704
    for i in range(6):
        x=54+i*195
        line(d,(x,y,x+174,y),'teal' if i<=chapter else 'line',5)
    return im,d

def coverage(d,x,y,k,emphasis=False):
    text(d,(x,y-45),'模型当前能回答什么？',26,'ink',True)
    for i,model in enumerate(['A','B']):
        yy=y+i*144;present=k>=1 if i==0 else k>=7
        fill='teal_bg' if present else 'amber_bg' if k else 'gray_bg'
        box(d,(x,yy,x+506,yy+129),fill,16)
        text(d,(x+21,yy+14),f'{model} 型号 · 维护周期',25,'ink',True)
        value=('每 6 个月' if i==0 else '每 12 个月') if present else ('仍缺依据' if k else '待查证')
        text(d,(x+21,yy+51),value,31,'teal' if present else 'amber' if k else 'muted',True)
        evidence=('第 1–3 条重复支持 A' if i==0 else '第 7 条已进入上下文') if present else ('第 7 条尚未进入上下文' if i==1 and k else '需要这个型号的周期证据')
        text(d,(x+21,yy+95),evidence,20,'muted')
        pill(d,x+342,yy+53,'有证据' if present else '缺证据' if k else '待检索',fill='white',color='teal' if present else 'amber' if k else 'muted',size=20)

def ranking(d,rows,k,x=57,y=200,width=602,rowh=43,show_cut=True,emphasis_rank=None):
    text(d,(x,y-45),'相似度排序',25,'ink',True)
    text(d,(x+width-120,y-43),f'Top {int(k+0.001)}' if k else '待截取',25,'teal',True)
    for i,row in enumerate(rows):
        yy=y+i*rowh;selected=(i+1)<=k+0.001
        fill='teal_bg' if selected else 'gray_bg'
        if emphasis_rank and i+1==emphasis_rank:fill='purple_bg'
        box(d,(x,yy,x+width,yy+rowh-6),fill,9)
        text(d,(x+12,yy+4),f'{i+1:02}',20,'muted',True)
        text(d,(x+58,yy+4),row['display'],21,'ink',True)
        text(d,(x+width-88,yy+4),str(row.get('score','')),19,'muted')
    if show_cut:
        cy=y+int(k+0.001)*rowh-3
        line(d,(x-8,cy,x+width+8,cy),'teal',4)
        pointer_y=y+k*rowh-3
        d.polygon([(x-8,pointer_y),(x-21,pointer_y-7),(x-21,pointer_y+7)],fill=COL['teal'])

def covered(rows,k):
    ids=set();counts={}
    for row in rows[:k]:
        for ident in row['slots']:
            ids.add(ident);counts[ident]=counts.get(ident,0)+1
    return ids,counts

CAPTIONS=[
(0,7,'K 从 3 加到 6，仍然可能漏掉 B。','因为多取几条，不保证每个问题都有证据。'),
(7,15,'同一个问题：A、B 型号的维护周期分别是多少？','看清两个目标，再看同一组模拟排名。'),
(15,25,'K = 3：取前 3 条，它们都在回答 A。','A 有 6 个月的依据；B 的周期没有依据。'),
(25,38,'把 K 从 3 增到 6，新增条目都没有 B 的周期。','出现 B 的名称，不等于给出了 B 的维护周期。'),
(38,47,'关键证据在第 7 条，就在截取线下面。','“资料里有”与“模型已经收到”是两回事。'),
(47,57,'保持本例排名不变，把 K 增到 7，才纳入 B 的周期证据。','这解释了本例，不构成“加大 K 总能找全”的保证。'),
(57,66,'检查每个子问题的证据，而不只看返回了多少条。','可尝试按 A、B 分别检索，再核对型号和适用条件。')
]

def get_caption(t):
    for start,end,a,b in CAPTIONS:
        if start<=t<end:return a+'\n'+b
    return CAPTIONS[-1][2]+'\n'+CAPTIONS[-1][3]

def render_frame(t,fixture):
    rows=fixture['ranking']
    if t<7:
        im,d=base(t,'K 加大了，为什么还漏了 B？',0,get_caption(t))
        text(d,(68,196),'问题',24,'muted',True)
        text(d,(68,238),'A、B 型号的维护周期',42,'ink',True)
        text(d,(68,298),'分别是多少？',42,'ink',True)
        text(d,(72,379),'需要 A 的证据',27,'teal',True)
        text(d,(72,421),'也需要 B 的证据',27,'amber',True)
        arrow(d,(525,325,642,325),'muted',4)
        box(d,(690,202,1207,486),'white',23)
        text(d,(722,224),'先记住这个区别',24,'muted',True)
        centered(d,948,311,'证据条数  ≠  问题覆盖',34,'ink',True)
        centered(d,948,393,'3 → 6',70,'teal',True)
        centered(d,948,459,'条目变多，缺口可能还在。',25,'muted')
        text(d,(68,541),'独立技能示例演示 · 几何动画 · 无旁白',21,'muted')
    elif t<15:
        im,d=base(t,'先定义“答全”：A 和 B 都要有周期证据',1,get_caption(t))
        ranking(d,rows,0,show_cut=False,emphasis_rank=7)
        coverage(d,714,201,0)
        text(d,(714,501),'模拟分数只决定这里的顺序。',24,'muted')
        text(d,(714,537),'相似度不是答案正确率。',24,'muted')
    elif t<25:
        k=3*ease((t-15)/1.7)
        im,d=base(t,'K = 3：三条证据，都在回答 A',2,get_caption(t))
        ranking(d,rows,k)
        coverage(d,714,201,int(k+.01))
        pill(d,715,502,'模型只收到截取线上方的条目',fill='blue_bg',size=21)
        text(d,(714,549),'重复支持 A，不能补上 B。',25,'ink',True)
    elif t<38:
        k=3+3*ease((t-25)/2.5)
        im,d=base(t,'把 K 从 3 增加到 6：B 的周期仍然缺失',3,get_caption(t))
        ranking(d,rows,k)
        coverage(d,714,201,int(k+.01))
        for rank in [4,5,6]:
            if k>=rank:
                yy=200+(rank-1)*43
                d.rounded_rectangle((57,yy,659,yy+37),radius=9,outline=COL['amber'],width=2)
        pill(d,715,502,f'新增 {max(0,int(k+0.001)-3)} 条  /  仍只覆盖 1 个型号',fill='amber_bg',color='amber',size=20)
        text(d,(714,549),'第 5、6 条：提到 B，没有周期。',23,'ink',True)
    elif t<47:
        im,d=base(t,'第 7 条：库里有，模型却还没收到',4,get_caption(t))
        ranking(d,rows,6,emphasis_rank=7)
        coverage(d,714,201,6)
        yy=200+6*43
        d.rounded_rectangle((56,yy-1,660,yy+38),radius=9,outline=COL['purple'],width=3)
        text(d,(714,501),'B 的周期证据 = 第 7 条',26,'purple',True)
        text(d,(714,540),'K = 6 的上下文不包含它。',25,'muted')
    elif t<57:
        k=6+ease((t-47)/1.7)
        im,d=base(t,'把 K 从 6 增加到 7：纳入缺失证据',5,get_caption(t))
        ranking(d,rows,k,emphasis_rank=7 if k<7 else None)
        coverage(d,714,201,7 if k>=6.999 else 6)
        pill(d,715,502,'只在这组固定排名下成立',fill='purple_bg',color='purple',size=21)
        text(d,(714,549),'真实检索还需核对资料和适用条件。',22,'muted')
    else:
        im,d=base(t,'先检查缺哪份证据，再决定怎么补',5,get_caption(t))
        box(d,(57,198,611,474),'white',22)
        text(d,(85,220),'这组排名的结果',25,'muted',True)
        text(d,(85,276),'K = 3  →  只有 A',34,'ink',True)
        text(d,(85,335),'K = 6  →  仍只有 A',34,'ink',True)
        text(d,(85,394),'K = 7  →  A 与 B',34,'teal',True)
        text(d,(696,202),'实际排查',28,'ink',True)
        text(d,(696,258),'1  资料是否已入库？',27,'ink')
        text(d,(696,308),'2  型号与检索条件是否正确？',27,'ink')
        text(d,(696,358),'3  每个子问题都有依据吗？',27,'ink')
        text(d,(696,416),'缺 B，就针对 B 查证。',29,'teal',True)
        text(d,(58,517),'边界：只演示固定排名与 top-K 截取；不模拟过滤、近似搜索或上下文截断。',22,'muted')
        text(d,(58,553),'所有型号、分数与周期均为模拟数据；不是设备维护建议，也不是效果评测。',22,'muted')
    return im

def save_captions():
    def stamp(sec):return f'00:{int(sec)//60:02d}:{int(sec)%60:02d},000'
    content='\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{c}\n{d}' for i,(a,b,c,d) in enumerate(CAPTIONS))+'\n'
    (HERE/'captions.zh-CN.srt').write_text(content,encoding='utf-8')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--frames-only',action='store_true')
    parser.add_argument('--fixture',type=Path,default=HERE/'fixture.json')
    parser.add_argument('--output',type=Path,default=HERE/'demo.mp4')
    args=parser.parse_args()
    fixture=json.loads(args.fixture.read_text(encoding='utf-8'))
    assert len(fixture['ranking'])==8
    assert fixture['ranking'][6]['period_months']==12
    assert fixture['ranking'][0]['period_months']==6
    save_captions()
    frames_dir=HERE/'verification-frames';frames_dir.mkdir(exist_ok=True)
    for t in [3,11,20,31,42,52,62]:
        render_frame(t,fixture).save(frames_dir/f'{t:02d}s.png')
    render_frame(42,fixture).save(HERE/'poster.png')
    if args.frames_only:return
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-vcodec','rawvideo',
         '-pix_fmt','rgb24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','-',
         '-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',
         '-movflags','+faststart','-metadata','title=Top-K 增大，为什么仍会漏掉 B？',
         '-metadata','comment=Original captioned geometric animation; synthetic teaching data, not UI capture or benchmark.',str(args.output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for frame in range(DURATION*FPS):
            proc.stdin.write(render_frame(frame/FPS,fixture).tobytes())
            if frame%240==0:print(f'Rendered {frame/FPS:.0f}/{DURATION}s',flush=True)
        proc.stdin.close()
        code=proc.wait()
        if code:raise RuntimeError(f'ffmpeg exited {code}')
    except BaseException:
        proc.kill();raise
    print(f'Created {args.output.name}',flush=True)

if __name__=='__main__':main()
