# Focused video inspection

Resolve the absolute skill directory before running these examples. The helper requires Python 3.10+, FFmpeg, and ffprobe; URL sources also require yt-dlp. Pillow is only needed for optional contact sheets. Use `--help` for the full option list.

```bash
# Read captions without downloading video, unless missing captions require transcription.
python3 /absolute/path/to/view-video/scripts/view_video.py 'URL' --out /tmp/video-review --transcript-only

# Inspect a passage more densely. Times refer to the original video timeline.
python3 /absolute/path/to/view-video/scripts/view_video.py 'URL' --out /tmp/video-review --start 2:15 --end 2:45 --fps 2 --max-frames 80

# Inspect only these moments at source resolution.
python3 /absolute/path/to/view-video/scripts/view_video.py 'URL' --out /tmp/video-review --timestamps 2:18,2:19,2:20 --width 0

# Supply captions for a local file.
python3 /absolute/path/to/view-video/scripts/view_video.py /path/demo.mp4 --out /tmp/demo-review --subtitles /path/demo.en.vtt --language en

# This local excerpt begins at 2:00 in the original; supplied captions already use original times.
python3 /absolute/path/to/view-video/scripts/view_video.py /path/excerpt.mp4 --out /tmp/excerpt-review --offset 2:00 --subtitles /path/original.vtt --subtitles-offset 0
```

The helper downloads a full remote source once, requesting video up to 1080p where resolution is known. `--start` and `--end` limit extraction, not download size. For a large source and narrow question, a separate [yt-dlp section download](https://github.com/yt-dlp/yt-dlp#download-options) may be worthwhile; pass the excerpt's original start through `--offset`. Subtitle offsets default to that same value unless overridden. Local source files are used in place; reuse the same source and cache directory for subsequent runs.

Prefer human captions in the relevant language, then automatic captions. Without `--language`, remote selection prefers the declared video language, then English, then an available language. Local caption lookup tries supplied SRT/WebVTT, matching sidecars, then embedded text streams. `transcript.txt` removes overlapping rolling-caption repetition; use `transcript.json` for raw cues when exact wording or timing matters.

If captions are missing and whisper.cpp and a suitable model already exist, add `--whisper-model /path/to/model.bin` (and `--whisper-bin` if needed). This transcribes the selected range locally, retaining original timestamps. The helper neither downloads models nor uploads audio. If unavailable, report that speech was not assessed and use visual evidence where useful.

On failure, read the actual error. Check existing installations and PATH first. For remote extraction errors, check `yt-dlp --version` and [official update guidance](https://github.com/yt-dlp/yt-dlp#update); update through its installation method when needed, then retry. Do not repeatedly retry a login restriction or rate limit without resolving its cause. Keep usable cached media and make a focused retry instead of rebuilding extraction machinery.
