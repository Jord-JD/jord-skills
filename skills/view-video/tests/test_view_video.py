"""Run with python3 -m unittest discover -s tests -v from the skill directory."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'view_video.py'
spec = importlib.util.spec_from_file_location('view_video', SCRIPT)
video = importlib.util.module_from_spec(spec)
spec.loader.exec_module(video)

CAPTIONS = '''WEBVTT

00:00.000 --> 00:02.000
This is red

00:01.000 --> 00:03.000
This is red then blue

00:03.000 --> 00:04.000
then blue

00:04.000 --> 00:06.000
Now green &amp; finished
'''


class SubtitleTests(unittest.TestCase):
    def test_rolling_captions_keep_separate_repetition_and_raw_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'subs.vtt'
            path.write_text(CAPTIONS)
            raw = video.parse_subtitles(path, 120)
            clean = video.reading_cues(raw)
            self.assertEqual(raw[1]['text'], 'This is red then blue')
            self.assertEqual([c['text'] for c in clean],
                             ['This is red', 'then blue', 'then blue', 'Now green & finished'])
            self.assertEqual(raw[-1]['end'], 126)
            path.write_text('1\n00:00:01,200 --> 00:00:02,300\n<b>Hello</b>\n')
            self.assertEqual(video.parse_subtitles(path)[0], {'start': 1.2, 'end': 2.3, 'text': 'Hello'})

    def test_language_and_manual_preference(self):
        metadata = {'language': 'fr', 'subtitles': {'en': True, 'fr': True},
                    'automatic_captions': {'fr': True, 'de': True}}
        self.assertEqual(video.select_caption(metadata, None), ('manual', 'fr'))
        self.assertEqual(video.select_caption(metadata, 'de'), ('automatic', 'de'))
        self.assertIsNone(video.select_caption(metadata, 'ja'))


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.media = cls.root / 'demo.mp4'
        args = ['ffmpeg', '-nostdin', '-v', 'error']
        for color in ('red', 'blue', 'green'):
            args += ['-f', 'lavfi', '-i', f'color=c={color}:s=320x180:r=10:d=2']
        args += ['-filter_complex', '[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]',
                 '-map', '[v]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(cls.media)]
        subprocess.run(args, check=True, capture_output=True)
        cls.media.with_suffix('.vtt').write_text(CAPTIONS)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def invoke(self, *flags, source=None, out=None):
        output = out or tempfile.mkdtemp(dir=self.root)
        capture = io.StringIO()
        with patch.object(sys, 'argv', [str(SCRIPT), source or str(self.media), '--out', str(output), *flags]):
            with contextlib.redirect_stdout(capture):
                video.main()
        report = json.loads(capture.getvalue())
        return json.loads(Path(report['manifest']).read_text())

    def test_scene_selection_and_exact_duplicate_reuse(self):
        manifest = self.invoke()
        scenes = [f['timestamp'] for f in manifest['frames'] if 'scene-change' in f['reasons']]
        self.assertEqual(scenes, [2, 4])
        self.assertEqual(len({f['path'] for f in manifest['frames']}), 3)
        for frame in manifest['frames']:
            self.assertTrue(Path(frame['path']).is_file())

    def test_offset_focus_and_actual_frame_timestamp(self):
        manifest = self.invoke('--offset', '120', '--start', '122', '--end', '125', '--fps', '2')
        self.assertEqual([f['timestamp'] for f in manifest['frames']], [122, 122.5, 123, 123.5, 124, 124.5])
        raw = json.loads(Path(manifest['transcript_json']).read_text())
        self.assertEqual(raw['cues'][0]['start'], 121)
        precise = self.invoke('--timestamps', '2.05', '--width', '0')
        self.assertAlmostEqual(precise['frames'][0]['timestamp'], 2.1)
        self.assertEqual(precise['frames'][0]['requested_timestamp'], 2.05)

    def test_budget_covers_range_and_reports_reduction(self):
        manifest = self.invoke('--fps', '10', '--max-frames', '4')
        self.assertEqual(len(manifest['frames']), 4)
        self.assertAlmostEqual(manifest['frames'][-1]['timestamp'], 5.9)
        self.assertTrue(any('budget reduced' in warning for warning in manifest['warnings']))
        self.assertLessEqual(len(self.invoke('--max-frames', '2')['frames']), 2)

    def test_transcript_only_and_explicit_subtitle_offset(self):
        manifest = self.invoke('--transcript-only', '--offset', '120', '--subtitles',
                               str(self.media.with_suffix('.vtt')), '--subtitles-offset', '120')
        self.assertEqual(manifest['frames'], [])
        self.assertIn('[00:02:04.000', Path(manifest['transcript']).read_text())

    def test_embedded_subtitles_and_missing_transcription_backend(self):
        media = self.root / 'embedded.mkv'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(self.media),
                        '-i', str(self.media.with_suffix('.vtt')), '-map', '0:v', '-map', '1:0',
                        '-c:v', 'copy', '-c:s', 'srt', str(media)], check=True, capture_output=True)
        manifest = self.invoke('--transcript-only', source=str(media))
        self.assertEqual(manifest['subtitle_provenance']['kind'], 'embedded')
        self.assertIn('Now green & finished', Path(manifest['transcript']).read_text())
        bare = self.root / 'bare.mp4'
        shutil.copyfile(self.media, bare)
        manifest = self.invoke('--timestamps', '1', '--whisper-model', str(self.root / 'absent.bin'),
                               source=str(bare))
        self.assertEqual(len(manifest['frames']), 1)
        self.assertTrue(any('speech has not been assessed' in w for w in manifest['warnings']))

    def test_invalid_range_fails(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.invoke('--start', '4', '--end', '2')

    def test_remote_captions_first_then_cached_download(self):
        calls = []
        real_run = video.run
        def fake_download(args, **kwargs):
            if args[0] != 'yt-dlp':
                return real_run(args, **kwargs)
            calls.append(args)
            self.assertEqual(args[-2:], ['--', 'https://example.test/video?id=1&x=2'])
            if '--dump-single-json' in args:
                result = {'title': 'Fixture', 'duration': 6, 'language': 'en',
                          'subtitles': {'en': [{'ext': 'vtt'}]}}
                return subprocess.CompletedProcess(args, 0, json.dumps(result), '')
            target = Path(args[args.index('-o') + 1])
            if '--skip-download' in args:
                target = Path(str(target).replace('%(ext)s', 'en.vtt'))
                target.write_text(CAPTIONS)
                return subprocess.CompletedProcess(args, 0, '', '')
            target = Path(str(target).replace('%(ext)s', 'mp4'))
            shutil.copyfile(self.media, target)
            return subprocess.CompletedProcess(args, 0, str(target) + '\n', '')
        cache = tempfile.mkdtemp(dir=self.root)
        which = shutil.which
        with patch.object(video, 'run', side_effect=fake_download), patch.object(video.shutil, 'which', side_effect=lambda x: '/mock/yt-dlp' if x == 'yt-dlp' else which(x)):
            first = self.invoke('--transcript-only', source='https://example.test/video?id=1&x=2', out=cache)
            self.assertIsNone(first['media_path'])
            self.assertEqual(len(calls), 2)
            second = self.invoke('--timestamps', '2', source='https://example.test/video?id=1&x=2', out=cache)
            self.assertEqual(len(calls), 3)
            third = self.invoke('--timestamps', '4', source='https://example.test/video?id=1&x=2', out=cache)
            self.assertEqual(len(calls), 3)
            self.assertEqual(second['media_path'], third['media_path'])
            self.assertEqual(second['subtitle_provenance']['kind'], 'manual')


if __name__ == '__main__':
    unittest.main()
