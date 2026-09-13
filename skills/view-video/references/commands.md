# Focused video inspection commands

Use these examples for transcript-only requests, narrow time ranges, selected frames, or supplied subtitles. Resolve the skill directory before running them.

Useful options:

```bash
# Fetch/read captions without extracting pictures. Remote video is not downloaded
# unless local transcription is requested and captions are missing.
python3 /absolute/path/to/view-video/scripts/view_video.py 'URL' --out /tmp/video-review --transcript-only

# Inspect an interesting passage. Times refer to the original video timeline.
python3 /absolute/path/to/view-video/scripts/view_video.py 'URL' --out /tmp/video-review --start 2:15 --end 2:45 --fps 2 --max-frames 80

# Inspect only these moments at source resolution, without another overview.
python3 /absolute/path/to/view-video/scripts/view_video.py 'URL' --out /tmp/video-review --timestamps 2:18,2:19,2:20 --width 0

# Supply captions for a local file. SRT and WebVTT are supported.
python3 /absolute/path/to/view-video/scripts/view_video.py /path/demo.mp4 --out /tmp/demo-review --subtitles /path/demo.en.vtt --language en
```
