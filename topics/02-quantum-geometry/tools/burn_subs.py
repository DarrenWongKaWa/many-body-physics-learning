"""Burn an .srt into a video without libass: every cue is drawn to a PNG with Pillow and
overlaid with ffmpeg. The picture is shrunk slightly and padded with the background colour,
so the subtitles sit in their own band below the animation instead of covering it.

    python tools/burn_subs.py in.mp4 in.srt out.mp4 [--t0 0 --dur 0]   (--dur > 0: clip for tests)
"""
import argparse, re, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
SCALE_W = 1690                  # animation width after shrinking (height follows, 950 px)
TOP = 10                        # y offset of the shrunk picture
BAND_Y, BAND_H = 960, 120       # subtitle band
BG = '0x0b0d12'
FONT = '/System/Library/Fonts/HelveticaNeue.ttc'
SIZE = 40


def parse_srt(path):
    def sec(s):
        h, m, rest = s.split(':')
        return int(h) * 3600 + int(m) * 60 + float(rest.replace(',', '.'))
    cues = []
    for block in Path(path).read_text(encoding='utf-8').strip().split('\n\n'):
        lines = block.strip().split('\n')
        a, b = lines[1].split(' --> ')
        cues.append((sec(a), sec(b), lines[2:]))
    return cues


def render_cue(lines, out):
    img = Image.new('RGBA', (W, BAND_H), (0, 0, 0, 0))
    font = ImageFont.truetype(FONT, SIZE, index=0)
    d = ImageDraw.Draw(img)
    lh = SIZE + 10
    y = (BAND_H - lh * len(lines)) // 2
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    for i, line in enumerate(lines):
        w = d.textlength(line, font=font)
        x = (W - w) / 2
        ds.text((x + 2, y + i * lh + 2), line, font=font, fill=(0, 0, 0, 220))
        d.text((x, y + i * lh), line, font=font, fill=(240, 240, 240, 255))
    shadow = shadow.filter(ImageFilter.GaussianBlur(2))
    Image.alpha_composite(shadow, img).save(out)


def duration(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                                capture_output=True, text=True).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('srt')
    ap.add_argument('out')
    ap.add_argument('--t0', type=float, default=0.0)
    ap.add_argument('--dur', type=float, default=0.0)
    a = ap.parse_args()
    total = duration(a.video)
    t_end = a.t0 + a.dur if a.dur > 0 else total
    cues = [(max(s, a.t0) - a.t0, min(e, t_end) - a.t0, l) for s, e, l in parse_srt(a.srt) if e > a.t0 and s < t_end]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        Image.new('RGBA', (W, BAND_H), (0, 0, 0, 0)).save(tmp / 'blank.png')
        entries, t = [], 0.0
        for i, (s, e, lines) in enumerate(cues):
            if s > t + 1e-3:
                entries.append(('blank.png', s - t))
            render_cue(lines, tmp / f'c{i:04d}.png')
            entries.append((f'c{i:04d}.png', e - s))
            t = e
        entries.append(('blank.png', max(0.1, (t_end - a.t0) - t)))
        lst = ''.join(f"file '{tmp / f}'\nduration {d:.3f}\n" for f, d in entries)
        lst += f"file '{tmp / entries[-1][0]}'\n"          # concat demuxer: repeat last entry
        (tmp / 'subs.txt').write_text(lst)
        clip = ['-ss', str(a.t0), '-t', str(t_end - a.t0)] if a.dur > 0 else []
        fc = (f'[0:v]scale={SCALE_W}:-2,pad={W}:{H}:{(W - SCALE_W) // 2}:{TOP}:color={BG}[bg];'
              f'[1:v]format=rgba[s];[bg][s]overlay=0:{BAND_Y}:eof_action=repeat:format=auto,format=yuv420p[v]')
        cmd = ['ffmpeg', '-y', '-v', 'error', *clip, '-i', a.video, '-f', 'concat', '-safe', '0', '-i', str(tmp / 'subs.txt'),
               '-filter_complex', fc, '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
               '-c:a', 'copy', '-movflags', '+faststart', a.out]
        subprocess.run(cmd, check=True)
    print(a.out, f'{len(cues)} cues burned')


if __name__ == '__main__':
    main()
