#!/usr/bin/env python3
"""Prepare timestamped video evidence for an agent to inspect."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlparse


def run(args, timeout=900):
    result = subprocess.run([str(x) for x in args], capture_output=True,
                            text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    if result.returncode:
        raise RuntimeError(f'{args[0]} failed ({result.returncode}):\n{result.stderr[-4000:]}')
    return result


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def seconds(value):
    try:
        parts = str(value).replace(',', '.').split(':')
        if not 1 <= len(parts) <= 3:
            raise ValueError()
        total = 0.0
        for part in parts:
            n = float(part)
            if not math.isfinite(n) or n < 0:
                raise ValueError()
            total = total * 60 + n
        return total
    except ValueError:
        raise argparse.ArgumentTypeError(f'Invalid timestamp: {value}')


def stamp(t):
    ms = round(t * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02}.{ms:03}'


def parse_subtitles(path, offset=0):
    content = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    cues = []
    timing = re.compile(r'^\s*([\d:.]+)\s+-->\s+([\d:.]+)')
    # SRT uses commas for fractions; WebVTT uses dots.
    for block in re.split(r'\n\s*\n', content):
        lines = block.splitlines()
        if lines and lines[0].startswith(('NOTE', 'STYLE', 'REGION')):
            continue
        for i, line in enumerate(lines):
            match = timing.match(line.replace(',', '.'))
            if not match:
                continue
            start, end = (seconds(x) + offset for x in match.groups())
            text = html.unescape(re.sub(r'<[^>]*>', '', ' '.join(lines[i + 1:])))
            text = ' '.join(text.split())
            if text and end > start:
                cues.append({'start': start, 'end': end, 'text': text})
            break
    return sorted(cues, key=lambda cue: (cue['start'], cue['end']))


def reading_cues(cues):
    previous = None
    output = []
    for cue in cues:
        words = cue['text'].split()
        if previous and cue['start'] < previous['end']:
            old = previous['text'].split()
            for count in range(min(len(old), len(words)), 0, -1):
                if old[-count:] == words[:count]:
                    words = words[count:]
                    break
        if words:
            output.append({**cue, 'text': ' '.join(words)})
        previous = cue
    return output


def spread(items, count):
    if count <= 0:
        return []
    if len(items) <= count:
        return items
    if count == 1:
        return [items[len(items) // 2]]
    return [items[round(i * (len(items) - 1) / (count - 1))] for i in range(count)]


def select_caption(metadata, language):
    preferred = language or metadata.get('language') or 'en'
    tables = [('manual', metadata.get('subtitles') or {}),
              ('automatic', metadata.get('automatic_captions') or {})]
    def matches(code, wanted):
        return code == wanted or code.startswith(wanted + '-')
    for wanted in dict.fromkeys([preferred, *([] if language else ['en'])]):
        for kind, table in tables:
            codes = sorted(table, key=lambda code: (code != wanted, code))
            for code in codes:
                if code != 'live_chat' and matches(code, wanted) and table[code]:
                    return kind, code
    if not language:
        for kind, table in tables:
            for code in sorted(table):
                if code != 'live_chat' and table[code]:
                    return kind, code
    return None


def remote_source(args, root, warnings, force_media=False):
    if not shutil.which('yt-dlp'):
        raise RuntimeError('yt-dlp is required for URLs')
    state_path = root / 'source.json'
    if state_path.exists():
        state = json.loads(state_path.read_text())
        if state['source'] != args.source:
            raise RuntimeError('Output directory belongs to another source; choose a new --out')
    else:
        base = ['yt-dlp', '--ignore-config', '--no-playlist', '--retries', '2', '--socket-timeout', '30']
        data = json.loads(run(base + ['--dump-single-json', '--skip-download', '--', args.source]).stdout)
        if data.get('is_live') or data.get('live_status') == 'is_upcoming' or data.get('_type') == 'playlist':
            raise RuntimeError('Use a finite video or a completed recording')
        duration = float(data['duration']) if data.get('duration') else None
        if duration is not None and (not math.isfinite(duration) or duration <= 0):
            raise RuntimeError('Source has no finite duration')
        state = {'source': args.source, 'title': data.get('title'), 'duration': duration,
                 'language': data.get('language'), 'subtitles': data.get('subtitles', {}),
                 'automatic_captions': data.get('automatic_captions', {})}
        # Cache language availability, not signed caption URLs or full platform metadata.
        for key in ('subtitles', 'automatic_captions'):
            state[key] = {code: bool(formats) for code, formats in state[key].items()}
        save(state_path, state)
    base = ['yt-dlp', '--ignore-config', '--no-playlist', '--retries', '2', '--socket-timeout', '30']
    subtitle, provenance = None, {'kind': 'none', 'language': args.language}
    choice = select_caption(state, args.language)
    if choice and not args.subtitles:
        kind, language = choice
        caption_dir = root / ('captions-' + hashlib.sha256(f'{kind}:{language}'.encode()).hexdigest()[:12])
        caption_dir.mkdir(exist_ok=True)
        candidates = sorted(caption_dir.glob('captions.*.vtt')) + sorted(caption_dir.glob('captions.*.srt'))
        if not candidates:
            try:
                run(base + ['--skip-download', '--write-subs' if kind == 'manual' else '--write-auto-subs',
                            '--sub-langs', '^' + re.escape(language) + '$', '--sub-format', 'vtt/srt',
                            '-o', str(caption_dir / 'captions.%(ext)s'), '--', args.source])
            except RuntimeError as error:
                warnings.append(str(error))
            candidates = sorted(caption_dir.glob('captions.*.vtt')) + sorted(caption_dir.glob('captions.*.srt'))
        if candidates:
            subtitle = candidates[0]
            provenance = {'kind': kind, 'language': language, 'path': str(subtitle)}
        else:
            warnings.append('Selected captions could not be retrieved')
    media = Path(state['media']) if state.get('media') else None
    if (force_media or not args.transcript_only or (args.whisper_model and not subtitle and not args.subtitles)) and (not media or not media.exists()):
        result = run(base + ['--no-simulate', '-f', 'bv*[height<=?1080]+ba/b[height<=?1080]',
                            '--print', 'after_move:filepath', '-o', str(root / 'video.%(ext)s'),
                            '--', args.source], timeout=3600)
        paths = [Path(line).resolve() for line in result.stdout.splitlines() if Path(line).is_file()]
        if not paths:
            raise RuntimeError('Download completed without a media path')
        media = paths[-1]
        state['media'] = str(media)
        save(state_path, state)
    return media, state, subtitle, provenance


def probe(media):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                           '-of', 'json', media]).stdout)


def local_subtitle(args, media, info, directory, warnings):
    for path in [media.with_suffix('.srt'), media.with_suffix('.vtt')]:
        if not args.language and path.is_file():
            return path, {'kind': 'sidecar', 'language': None, 'path': str(path)}
    paths = sorted(media.parent.glob(media.stem + '.*.srt')) + sorted(media.parent.glob(media.stem + '.*.vtt'))
    for path in paths:
        language = path.name[len(media.stem) + 1:].rsplit('.', 1)[0]
        if not args.language or language == args.language:
            return path, {'kind': 'sidecar', 'language': language, 'path': str(path)}
    text_codecs = {'subrip', 'webvtt', 'ass', 'ssa', 'mov_text', 'text'}
    for stream in info['streams']:
        if stream.get('codec_type') != 'subtitle':
            continue
        language = stream.get('tags', {}).get('language')
        if args.language and language != args.language:
            continue
        if stream.get('codec_name') not in text_codecs:
            warnings.append('Bitmap subtitle stream requires visual reading or OCR')
            continue
        path = directory / 'embedded.srt'
        try:
            run(['ffmpeg', '-nostdin', '-v', 'error', '-i', media, '-map', f"0:{stream['index']}", path])
            return path, {'kind': 'embedded', 'language': language, 'path': str(path)}
        except RuntimeError as error:
            warnings.append(str(error))
    return None, {'kind': 'none', 'language': args.language}


def transcribe(args, media, directory, start, end):
    binary = shutil.which(args.whisper_bin)
    if not binary or not args.whisper_model.is_file():
        raise RuntimeError('Local transcription needs whisper-cli and an existing --whisper-model file')
    wav = directory / 'audio.wav'
    run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', start, '-i', media, '-t', end - start,
         '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', wav])
    prefix = directory / 'whisper'
    run([binary, '-m', args.whisper_model, '-f', wav, '-l', args.language or 'auto',
         '-osrt', '-of', prefix], timeout=3600)
    return prefix.with_suffix('.srt')


def scene_times(media, start, end, threshold):
    result = run(['ffmpeg', '-nostdin', '-hide_banner', '-ss', start, '-i', media,
                  '-t', end - start, '-map', '0:V:0', '-an', '-vf',
                  f"scale=320:-2,select='gt(scene,{threshold})',showinfo", '-f', 'null', '-'], timeout=3600)
    return [start + float(t) for t in re.findall(r'\bn:\s*\d+.*?pts_time:([\d.eE+\-]+)', result.stderr)]


def extract_frame(media, at, width, path):
    filters = 'showinfo'
    if width:
        filters += f",scale='min({width},iw)':-2"
    result = run(['ffmpeg', '-nostdin', '-hide_banner', '-ss', at, '-i', media, '-an',
                  '-map', '0:V:0', '-frames:v', '1', '-vf', filters, '-update', '1', path])
    match = re.search(r'\bn:\s*0\b.*?pts_time:([\d.eE+\-]+)', result.stderr)
    if not path.exists() or not match:
        raise RuntimeError(f'No decoded frame at {at:.3f} seconds')
    return at + float(match.group(1))


def contact_sheets(frames, directory):
    from PIL import Image, ImageDraw
    sheets = []
    for first in range(0, len(frames), 12):
        group = frames[first:first + 12]
        sheet = Image.new('RGB', (960, math.ceil(len(group) / 3) * 210), '#202020')
        draw = ImageDraw.Draw(sheet)
        for i, frame in enumerate(group):
            with Image.open(frame['path']) as original:
                thumb = original.convert('RGB')
                thumb.thumbnail((312, 180))
            x, y = i % 3 * 320, i // 3 * 210
            sheet.paste(thumb, (x + (320 - thumb.width) // 2, y))
            draw.text((x + 6, y + 184), stamp(frame['timestamp']), fill='white')
        path = directory / f'contact-{first // 12 + 1:03}.jpg'
        sheet.save(path)
        sheets.append(str(path))
    return sheets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', help='Video URL or local file')
    parser.add_argument('--out', type=Path, required=True, help='Cache directory for this source')
    parser.add_argument('--start', type=seconds, help='Original timeline start (SS, MM:SS, HH:MM:SS)')
    parser.add_argument('--end', type=seconds, help='Original timeline end')
    parser.add_argument('--offset', type=seconds, default=0, help='Original start time of an externally clipped local file')
    parser.add_argument('--subtitles-offset', type=seconds, help='Original start time for supplied subtitle timestamps; defaults to --offset')
    parser.add_argument('--timestamps', help='Comma-separated original timestamps; extracts only these frames')
    parser.add_argument('--fps', type=float, help='Uniform samples per second, replacing scene sampling')
    parser.add_argument('--max-frames', type=int, default=48)
    parser.add_argument('--width', type=int, default=1280, help='Maximum frame width; 0 keeps source resolution')
    parser.add_argument('--scene-threshold', type=float, default=0.25)
    parser.add_argument('--language', help='Caption language code; also used by whisper-cli')
    parser.add_argument('--subtitles', type=Path, help='Explicit SRT or WebVTT file')
    parser.add_argument('--transcript-only', action='store_true')
    parser.add_argument('--whisper-model', type=Path, help='Existing whisper.cpp model for missing captions')
    parser.add_argument('--whisper-bin', default='whisper-cli')
    parser.add_argument('--contact-sheets', action='store_true')
    args = parser.parse_args()
    if args.max_frames < 2 or args.width < 0 or not 0 <= args.scene_threshold <= 1:
        parser.error('Require --max-frames >= 2, --width >= 0, and scene threshold between 0 and 1')
    if args.fps is not None and (not math.isfinite(args.fps) or args.fps <= 0):
        parser.error('--fps must be finite and positive')
    if args.transcript_only and (args.timestamps or args.fps or args.contact_sheets):
        parser.error('--transcript-only cannot be combined with frame options')
    requested = [seconds(t) for t in args.timestamps.split(',')] if args.timestamps else []
    if len(requested) > args.max_frames:
        parser.error('Increase --max-frames to fit the requested timestamps')
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            raise RuntimeError(f'{tool} is required')
    if args.subtitles:
        args.subtitles = args.subtitles.resolve(strict=True)
    root = args.out.resolve()
    root.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix='run-', dir=root))
    warnings = []
    remote = urlparse(args.source).scheme in ('http', 'https')
    if remote:
        if args.offset:
            parser.error('--offset applies only to an externally clipped local file')
        media, metadata, subtitle, provenance = remote_source(args, root, warnings)
        info = probe(media) if media else None
    else:
        media = Path(args.source).expanduser().resolve(strict=True)
        info = probe(media)
        metadata = {'source': str(media), 'title': media.name,
                    'duration': float(info['format'].get('duration') or 0)}
        subtitle, provenance = (None, {'kind': 'none'}) if args.subtitles else local_subtitle(args, media, info, directory, warnings)
    duration = float(info['format'].get('duration') or metadata['duration']) if info else metadata['duration']
    if duration is None and subtitle:
        duration = max((c['end'] for c in parse_subtitles(subtitle)), default=0)
    if duration is None:
        raise RuntimeError('No captions or duration reported; use visual mode to download and inspect this source')
    if not math.isfinite(duration) or duration <= 0:
        raise RuntimeError('Media has no finite positive duration')
    start = args.start if args.start is not None else args.offset
    end = args.end if args.end is not None else args.offset + duration
    if not args.offset <= start < end <= args.offset + duration + 0.001:
        parser.error('Requested range is outside the source timeline')
    if any(not start <= t < end for t in requested):
        parser.error('Requested timestamps must be inside the selected range, excluding its end')
    local_start, local_end = start - args.offset, end - args.offset
    subtitle_offset = args.offset
    if args.subtitles:
        subtitle = args.subtitles
        subtitle_offset = args.subtitles_offset if args.subtitles_offset is not None else args.offset
        provenance = {'kind': 'supplied', 'language': args.language, 'path': str(subtitle)}
    cues = parse_subtitles(subtitle, subtitle_offset) if subtitle else []
    if subtitle and not cues:
        warnings.append('Subtitle file contained no readable timed cues')
    if not cues and args.whisper_model and remote and not media:
        media, _, _, _ = remote_source(args, root, warnings, force_media=True)
    if not cues and args.whisper_model and media:
        try:
            subtitle = transcribe(args, media, directory, local_start, local_end)
            cues = parse_subtitles(subtitle, start)
            provenance = {'kind': 'local-whisper', 'language': args.language or 'auto', 'path': str(subtitle)}
        except (RuntimeError, subprocess.TimeoutExpired) as error:
            warnings.append(str(error))
    cues = [cue for cue in cues if cue['end'] > start and cue['start'] < end]
    if not cues:
        warnings.append('No transcript available in this range; speech has not been assessed')
    save(directory / 'transcript.json', {'provenance': provenance, 'cues': cues})
    (directory / 'transcript.txt').write_text(''.join(
        f"[{stamp(c['start'])} --> {stamp(c['end'])}] {c['text']}\n" for c in reading_cues(cues)), encoding='utf-8')
    frames = []
    if not args.transcript_only:
        if not any(s.get('codec_type') == 'video' and not s.get('disposition', {}).get('attached_pic') for s in info['streams']):
            raise RuntimeError('Source has no video stream')
        targets = {}
        def add(t, reason):
            targets.setdefault(round(t, 6), set()).add(reason)
        if requested:
            for t in requested:
                add(t - args.offset, 'requested')
        elif args.fps:
            count = max(1, math.ceil((end - start) * args.fps))
            if count > args.max_frames:
                warnings.append(f'Requested {count} frames at {args.fps} fps; budget reduced this to {args.max_frames} samples across the range')
            indices = spread(range(count), args.max_frames)
            for i in indices:
                add(local_start + i / args.fps, 'uniform')
        else:
            try:
                scenes = [t for t in scene_times(media, local_start, local_end, args.scene_threshold) if local_start <= t < local_end]
            except (RuntimeError, subprocess.TimeoutExpired) as error:
                warnings.append(f'Scene selection failed; using uniform samples: {error}')
                scenes = []
            picked = spread(scenes, args.max_frames // 2)
            if len(picked) < len(scenes):
                warnings.append(f'Sampled {len(picked)} of {len(scenes)} scene changes')
            for t in picked:
                add(t, 'scene-change')
            count = min(args.max_frames - len(targets), max(2, math.ceil((end - start) / 5) + 1))
            last = max(local_start, local_end - min(0.1, (end - start) / 2))
            for i in range(count):
                add(local_start + (last - local_start) * i / max(1, count - 1), 'uniform')
        seen = {}
        for i, (at, reasons) in enumerate(sorted(targets.items())):
            path = directory / f'frame-{i + 1:04}.png'
            try:
                actual = extract_frame(media, at, args.width, path) + args.offset
            except RuntimeError as error:
                warnings.append(str(error))
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            frame = {'timestamp': actual, 'requested_timestamp': at + args.offset,
                     'reasons': sorted(reasons), 'path': str(path)}
            if digest in seen:
                path.unlink()
                frame['path'] = seen[digest]
                frame['identical_image'] = True
            else:
                seen[digest] = str(path)
            frames.append(frame)
        if not frames:
            raise RuntimeError('No video frames could be extracted')
    times = sorted(f['timestamp'] for f in frames)
    gaps = [b - a for a, b in zip([start] + times, times + [end])]
    max_gap = max(gaps) if gaps else end - start
    if frames and max_gap > 10:
        warnings.append(f'Sparse visual coverage: largest gap is {max_gap:.1f}s; inspect relevant intervals more closely')
    sheets = []
    if args.contact_sheets and frames:
        try:
            sheets = contact_sheets(frames, directory)
        except ImportError:
            warnings.append('Contact sheets need Pillow; individual frames are available')
    manifest = {'source': metadata['source'], 'title': metadata['title'], 'media_path': str(media) if media else None,
                'source_duration': duration, 'source_offset': args.offset, 'range': [start, end],
                'transcript': str(directory / 'transcript.txt'), 'transcript_json': str(directory / 'transcript.json'),
                'subtitle_provenance': provenance, 'frames': frames, 'contact_sheets': sheets,
                'largest_unsampled_gap_seconds': max_gap, 'warnings': warnings}
    save(directory / 'manifest.json', manifest)
    print(json.dumps({'manifest': str(directory / 'manifest.json'), 'transcript': manifest['transcript'],
                      'frames': len(frames), 'unique_images': len({f['path'] for f in frames}),
                      'warnings': warnings}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
