#!/usr/bin/env python3
"""Render a DID YOU KNOW?! episode from an edit list.

Usage:
    python3 tools/build_cut.py episodes/01-pool-route/edl.json \
        --media "C:/Users/JAMIE K/Downloads/poolroute_stills" --out cut.mp4

The EDL is JSON:
    {
      "title": "THE POOL ROUTE",        mission card, shown on the first shot only
      "card": "HIDDEN MISSION",         small line above the title
      "narration": "audio/narration.mp3",
      "ennui_full_at": 45.2,            second at which the ENNUI bar is full
      "segments": [
        {"at": 0.0,  "clip": "clips/hedgefront.mp4", "ss": 0.0},
        {"at": 44.15, "still": "v2/beat6b_emptyroom.png"}
      ]
    }

"at" is where the shot starts on the narration timeline. Each shot runs until
the next one starts; the last runs to the end of the narration. "ss" is the
offset into the source clip. Paths are relative to --media.

Output is 1080x1920, 30 fps, H.264 with the narration as AAC audio.
Needs ffmpeg, ffprobe and Pillow.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd) + "\n" + r.stderr[-800:])
    return r.stdout


def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", path])
    return float(out.strip())


def hud(path, level, title=None, card=None):
    """Minimal HUD: minimap, draining health bar, filling ENNUI bar."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy, r = 170, 1470, 118
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=(0, 0, 0, 150))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 52, 48, 215))

    # roads and the pool route, clipped to the minimap disc
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for a, b in [((cx - 140, cy - 40), (cx + 140, cy - 70)),
                 ((cx - 60, cy - 140), (cx - 20, cy + 140)),
                 ((cx + 50, cy - 140), (cx + 80, cy + 140)),
                 ((cx - 140, cy + 60), (cx + 140, cy + 35))]:
        ld.line([a, b], fill=(120, 135, 130, 255), width=13)
    pools = [(-70, 60), (-25, 20), (20, 35), (62, -15), (30, -62), (85, -80)]
    for k, (px, py) in enumerate(pools):
        ld.rounded_rectangle([cx + px - 13, cy + py - 9, cx + px + 13, cy + py + 9],
                             4, fill=(70, 200, 215, 255))
        if k:
            qx, qy = pools[k - 1]
            for s in range(1, 6):
                x = cx + qx + (px - qx) * s / 6
                y = cy + qy + (py - qy) * s / 6
                ld.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 225, 90, 255))
    clipped = Image.composite(lay.split()[3], Image.new("L", (W, H), 0), mask)
    im.paste(lay, (0, 0), clipped)

    d = ImageDraw.Draw(im)
    d.polygon([(cx, cy - 16), (cx - 11, cy + 12), (cx, cy + 5), (cx + 11, cy + 12)],
              fill=(255, 255, 255, 255))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(230, 230, 230, 220), width=4)

    bx, by, bw = 52, 1612, 236
    d.rectangle([bx - 3, by - 3, bx + bw + 3, by + 13], fill=(0, 0, 0, 150))
    d.rectangle([bx, by, bx + int(bw * max(0.25, 1 - 0.6 * level)), by + 10],
                fill=(96, 196, 104, 255))
    by2 = by + 26
    d.rectangle([bx - 3, by2 - 3, bx + bw + 3, by2 + 13], fill=(0, 0, 0, 150))
    d.rectangle([bx, by2, bx + max(3, int(bw * level)), by2 + 10],
                fill=(170, 120, 255, 255))
    d.text((bx + bw + 14, by2 - 8), "ENNUI", font=font(22), fill=(255, 255, 255, 235),
           stroke_width=2, stroke_fill=(0, 0, 0, 200))

    if title:
        d.rectangle([0, 150, W, 330], fill=(0, 0, 0, 120))
        if card:
            d.text((60, 170), card, font=font(30), fill=(255, 225, 90, 255),
                   stroke_width=2, stroke_fill=(0, 0, 0, 220))
        d.text((60, 214), title, font=font(54), fill=(255, 255, 255, 255),
               stroke_width=3, stroke_fill=(0, 0, 0, 220))
    im.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("edl")
    ap.add_argument("--media", required=True, help="folder the EDL paths are relative to")
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-hud", action="store_true")
    ap.add_argument("--crf", default="19")
    args = ap.parse_args()

    with open(args.edl, encoding="utf-8") as f:
        edl = json.load(f)
    segs = edl["segments"]
    narration = os.path.join(args.media, edl["narration"])
    total = duration(narration)
    full_at = edl.get("ennui_full_at", total)
    frame = lambda t: round(t * FPS)

    for a, b in zip(segs, segs[1:]):
        if b["at"] <= a["at"]:
            sys.exit(f"segments out of order at {b['at']}")

    work = tempfile.mkdtemp(prefix="dyk_")
    parts = []
    for i, seg in enumerate(segs):
        end = segs[i + 1]["at"] if i + 1 < len(segs) else total
        n = frame(end) - frame(seg["at"])
        if n <= 0:
            sys.exit(f"segment {i} has no frames")
        if "still" in seg:
            src = ["-loop", "1", "-framerate", str(FPS), "-i",
                   os.path.join(args.media, seg["still"])]
            vf = ("[0:v]scale=1188:-2:flags=lanczos,"
                  "crop=1080:1920:x='54-1.2*n':y='(ih-1920)/2'[v]")
        else:
            clip = os.path.join(args.media, seg["clip"])
            need = seg.get("ss", 0) + n / FPS
            have = duration(clip)
            if need > have + 0.05:
                sys.exit(f"segment {i}: {seg['clip']} is {have:.2f}s, needs {need:.2f}s")
            src = ["-ss", str(seg.get("ss", 0)), "-i", clip]
            vf = ("[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase:"
                  "flags=lanczos,crop=1080:1920,unsharp=5:5:0.5[v]")
        part = os.path.join(work, f"seg{i:02d}.mp4")
        cmd = ["ffmpeg", "-v", "error", "-y"] + src
        if args.no_hud:
            cmd += ["-filter_complex", vf + ";[v]format=yuv420p[o]"]
        else:
            png = os.path.join(work, f"hud{i:02d}.png")
            hud(png, min(1.0, end / full_at),
                title=edl.get("title") if i == 0 else None, card=edl.get("card"))
            cmd += ["-i", png, "-filter_complex",
                    vf + ";[v][1:v]overlay=0:0,format=yuv420p[o]"]
        cmd += ["-map", "[o]", "-frames:v", str(n), "-r", str(FPS),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", args.crf, part]
        run(cmd)
        parts.append(part)
        print(f"{i:02d}  {seg['at']:6.2f}s  {n:4d} frames  {seg.get('clip') or seg.get('still')}")

    listing = os.path.join(work, "list.txt")
    with open(listing, "w", encoding="utf-8") as f:
        for p in parts:
            f.write("file '" + p.replace("\\", "/") + "'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing,
         "-i", narration, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args.out])

    # verify what was written
    run(["ffmpeg", "-v", "error", "-i", args.out, "-f", "null", "-"])
    info = run(["ffprobe", "-v", "error", "-show_entries",
                "format=duration,size:stream=codec_name,width,height",
                "-of", "default=nw=1", args.out])
    print("\nwrote", args.out, "(decodes cleanly)")
    print(info.strip())
    print(f"narration is {total:.2f}s")


if __name__ == "__main__":
    main()
