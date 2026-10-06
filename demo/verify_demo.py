#!/usr/bin/env python3
"""Verify the encoded demo, fixture coverage and decode representative frames."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
mp4=HERE/'demo.mp4'
fixture=json.loads((HERE/'fixture.json').read_text(encoding='utf-8'))
expected={0:set(),3:{'A'},6:{'A'},7:{'A','B'},8:{'A','B'}}
for k,want in expected.items():
    have={s for r in fixture['ranking'][:k] for s in r['slots']}
    assert have==want,(k,have,want)
assert len(fixture['ranking'])==8
assert fixture['ranking'][0]['period_months']==6
assert fixture['ranking'][6]['period_months']==12
assert [r['score'] for r in fixture['ranking']]==['0.93','0.90','0.87','0.84','0.81','0.78','0.73','0.66']
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(mp4)]))
video=[s for s in probe['streams'] if s['codec_type']=='video']
audio=[s for s in probe['streams'] if s['codec_type']=='audio']
assert len(video)==1 and len(audio)==0
v=video[0]
assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
assert (v['width'],v['height'])==(1280,720)
assert v['r_frame_rate']=='24/1'
assert float(probe['format']['duration'])==66.0
assert int(v['nb_frames'])==1584
subprocess.run(['ffmpeg','-v','error','-i',str(mp4),'-f','null','-'],check=True)
frames=HERE/'decoded-frames';frames.mkdir(exist_ok=True)
for sec in [3,11,20,26,31,42,48,52,62]:
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(sec),'-i',str(mp4),'-frames:v','1',str(frames/f'{sec:02d}s.png')],check=True)
report={
 'artifact':'demo.mp4','duration_seconds':float(probe['format']['duration']),
 'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],
 'video_codec':v['codec_name'],'pixel_format':v['pix_fmt'],'frame_count':int(v['nb_frames']),
 'audio_streams':len(audio),'audio_description':'Silent; no narration or music.',
 'size_bytes':mp4.stat().st_size,'sha256':hashlib.sha256(mp4.read_bytes()).hexdigest(),
 'source_example_file':fixture['source_file'],'source_example_sha256':fixture['source_sha256'],
 'method':'Original Pillow geometric animation with FFmpeg encoding; same fixture as the completed HTML example. Not a screen capture.',
 'passed_checks':['Fixture coverage at K=0/3/6/7/8','Exact fixed score sequence and maintenance intervals','ffprobe dimensions, duration, frame rate, frame count, codec, pixel format and silent audio state','Full video decode with ffmpeg returned exit code 0'],
 'frame_review':{'decoded_samples_seconds':[3,11,20,26,31,42,48,52,62],'visual_review':'Pending reviewer inspection of final decoded frames.'},
 'limitations':['Synthetic ranking, titles, scores and maintenance periods; not real equipment advice.','Fixed query and rank; filtering, approximate search, chunking and context truncation are not modeled.','No learning-effect or skill-superiority claim.','Companion HTML was not browser-rendered in this environment.'],
}
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
