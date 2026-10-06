# Top-K 证据覆盖演示视频

- `demo.mp4`：可播放的 66 秒 H.264 视频，1280×720、24 fps，中文烧录字幕，无音轨。
- `poster.png`：第 42 秒的封面，强调截取线下的第 7 条。
- `captions.zh-CN.srt`：对应字幕。
- `storyboard.zh-CN.md`：分镜、讲解目标和简化假设。
- `fixture.json`：来自同一已生成 HTML 示例的固定模拟资料；记录源文件名与校验值。
- `render_demo.py`：原创、可复现的本地渲染代码。
- `verification.json`：导出参数、解码检查和画面检查记录。
- `verify_demo.py`：复查视频参数、完整解码和模拟证据覆盖。

## 复现

需要本地已安装 Python 3、Pillow、FFmpeg 和支持简体中文的字体。无需联网、API 密钥、付费服务或语音工具。

```sh
python render_demo.py
ffprobe -v error -show_streams -show_format demo.mp4
ffmpeg -v error -i demo.mp4 -f null -
```

默认使用系统 Noto Sans CJK 字体。其他系统可设置 `DEMO_FONT` 与 `DEMO_FONT_BOLD`，指向已安装的中文字体文件；TTC 文件默认选用简体中文字体面。

`python render_demo.py --frames-only` 仅输出关键画面、封面和字幕。

## 制作方法与限制

视频用 Pillow 绘制原创几何画面，通过 FFmpeg 编码。可运行 `python verify_demo.py` 重做技术检查。它是与网页使用同一教学数据的动画，不是网页录屏。网页渲染在制作环境中未能启动，因此未把任何模拟界面说成实际屏幕录制。

所有数据都是教学模拟：固定一个查询和一组排名，只改变 top-K 截取位置。A 与 B 的维护周期不是实际设备建议。这个演示不证明技能优于基线，也不测量学习效果。
