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
      "distance_mi": 0.84,              optional starting distance on minimap
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
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30

# Shared HUD geometry (1x screen pixels) used by glass_mask, hud, and ffmpeg.
GX, GY = 48, 1280
MW, MH, MR = 344, 190, 22
GAP = 12
VH, VR = 66, 14
GW, GH = MW, MH + GAP + VH
CARD_X, CARD_Y = 48, 264
SUPERSAMPLE = 2
HUD_PAD = 24

FONT_CANDIDATES = [
    "/usr/share/fonts/TTF/DejaVuSansCondensed-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]

FONT_WEIGHTS = {
    "regular": [
        "/usr/share/fonts/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ],
    "medium": [
        "/usr/share/fonts/noto/NotoSans-Medium.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ],
    "bold": [
        "/usr/share/fonts/noto/NotoSans-Bold.ttf",
        *FONT_CANDIDATES,
    ],
    "black": [
        "/usr/share/fonts/noto/NotoSans-Black.ttf",
        "/usr/share/fonts/noto/NotoSans-Bold.ttf",
        *FONT_CANDIDATES,
    ],
}


def font(size, weight="bold"):
    """Load the best available TrueType font for the requested weight."""
    for path in FONT_WEIGHTS.get(weight, FONT_CANDIDATES) + FONT_CANDIDATES:
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


def _rounded_mask(size, rects, supersample=SUPERSAMPLE):
    """Build an anti-aliased L mask for one or more (bbox, radius) rounded rects."""
    w, h = size
    s = supersample
    hi = Image.new("L", (w * s, h * s), 0)
    d = ImageDraw.Draw(hi)
    for (x0, y0, x1, y1), rad in rects:
        d.rounded_rectangle([x0 * s, y0 * s, (x1 + 1) * s - 1, (y1 + 1) * s - 1],
                            radius=rad * s, fill=255)
    return hi.resize((w, h), Image.Resampling.LANCZOS)


def glass_mask(path):
    """Write the alpha mask matching the minimap and vitals frosted-glass rects."""
    mask = _rounded_mask(
        (GW, GH),
        [
            ((0, 0, MW - 1, MH - 1), MR),
            ((0, MH + GAP, MW - 1, GH - 1), VR),
        ],
    )
    mask.save(path)


def _lerp_color(c0, c1, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c0, c1))


def _vertical_gradient(size, top_rgba, bot_rgba):
    """Create a fast vertical RGBA gradient image."""
    w, h = size
    strip = Image.new("RGBA", (1, h))
    px = [_lerp_color(top_rgba, bot_rgba, y / max(1, h - 1)) for y in range(h)]
    strip.putdata(px)
    return strip.resize((w, h), Image.Resampling.BILINEAR)


def _horizontal_gradient(size, left_rgba, right_rgba):
    """Create a fast horizontal RGBA gradient image."""
    w, h = size
    strip = Image.new("RGBA", (w, 1))
    px = [_lerp_color(left_rgba, right_rgba, x / max(1, w - 1)) for x in range(w)]
    strip.putdata(px)
    return strip.resize((w, h), Image.Resampling.BILINEAR)


def _clip_onto(base, overlay, mask):
    """Composite overlay onto base strictly inside mask."""
    clipped = Image.composite(overlay, Image.new("RGBA", base.size, (0, 0, 0, 0)), mask)
    return Image.alpha_composite(base, clipped)


def _measure_tracked_text(draw, text, fnt, tracking):
    """Return (width, height, top_offset) for tracked single-line text."""
    if not text:
        return 0, 0, 0
    x = 0
    tops, bottoms = [], []
    for i, ch in enumerate(text):
        l, t, r, b = draw.textbbox((x, 0), ch, font=fnt)
        tops.append(t)
        bottoms.append(b)
        adv = draw.textlength(ch, font=fnt)
        x += adv + (tracking if i + 1 < len(text) else 0)
    top = min(tops)
    return round(x), round(max(bottoms) - top), top


def _draw_tracked_text(draw, pos, text, fnt, fill, tracking=0, stroke_width=0, stroke_fill=None):
    """Draw text with explicit letter tracking."""
    x, y = pos
    for i, ch in enumerate(text):
        kwargs = {"font": fnt, "fill": fill}
        if stroke_width > 0 and stroke_fill is not None:
            kwargs["stroke_width"] = stroke_width
            kwargs["stroke_fill"] = stroke_fill
        draw.text((x, y), ch, **kwargs)
        x += draw.textlength(ch, font=fnt) + (tracking if i + 1 < len(text) else 0)


def _draw_heart(draw, cx, cy, r, fill):
    """Draw a clean geometric heart icon centered at (cx, cy)."""
    lr = 0.50 * r
    lx, rx, ly = cx - 0.42 * r, cx + 0.42 * r, cy - 0.18 * r
    draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=fill)
    draw.ellipse([rx - lr, ly - lr, rx + lr, ly + lr], fill=fill)
    # Tangent 45-degree lower V connecting cleanly to both lobes.
    tx = 0.42 * r + lr * 0.7071
    ty = ly + lr * 0.7071
    by = ty + tx
    draw.polygon([(cx - tx, ty), (cx, by), (cx + tx, ty), (cx, ly)], fill=fill)


def _draw_eye(draw, cx, cy, r, fill):
    """Draw a minimalist GTA VI Focus eye icon centered at (cx, cy)."""
    pts_top = []
    pts_bot = []
    for k in range(21):
        u = -1.0 + 2.0 * k / 20
        px = cx + u * r * 1.15
        arch = (1.0 - u * u) * r * 0.66
        pts_top.append((px, cy - arch))
        pts_bot.append((px, cy + arch))
    outline_pts = pts_top + list(reversed(pts_bot))
    draw.polygon(outline_pts, fill=(14, 14, 20, 140), outline=fill, width=max(2, round(r * 0.22)))
    ir = max(2, round(r * 0.36))
    draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=fill)
    pr = max(1, round(r * 0.14))
    draw.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(24, 18, 34, 235))


def _draw_pill_bar(layer, x1, y_center, x2, h, frac, c_left, c_right=None):
    """Draw a rounded glass track and filled pill bar (solid or horizontal gradient)."""
    r = h // 2
    y1 = y_center - r
    y2 = y1 + h

    # Composite the dark translucent track cleanly onto the vitals capsule.
    track = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(track)
    td.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=(10, 10, 14, 130),
                         outline=(255, 255, 255, 28), width=max(1, r // 4))
    layer = Image.alpha_composite(layer, track)

    fw = max(h, round((x2 - x1) * max(0.0, min(1.0, frac))))
    fx2 = min(x2, x1 + fw)
    pill_mask = Image.new("L", layer.size, 0)
    ImageDraw.Draw(pill_mask).rounded_rectangle([x1, y1, fx2, y2], radius=r, fill=255)

    fill_layer = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    if c_right is None:
        ImageDraw.Draw(fill_layer).rectangle([x1, y1, fx2, y2], fill=c_left)
    else:
        grad_rect = _horizontal_gradient((max(1, fx2 - x1 + 1), h + 1), c_left, c_right)
        fill_layer.paste(grad_rect, (x1, y1))

    # Top specular sheen composited cleanly (never overwrites fill alpha).
    sheen = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sheen_h = max(2, round(h * 0.36))
    ImageDraw.Draw(sheen).rectangle([x1, y1, fx2, y1 + sheen_h], fill=(255, 255, 255, 48))
    fill_layer = Image.alpha_composite(fill_layer, sheen)
    return _clip_onto(layer, fill_layer, pill_mask)


def _draw_minimap_contents(panel, ox, oy, mw, mh, mr, level, s):
    """Draw frosted tint, 3D perspective streets, Vice-pink GPS route, and badges."""
    map_mask = Image.new("L", panel.size, 0)
    ImageDraw.Draw(map_mask).rounded_rectangle(
        [ox, oy, ox + mw - 1, oy + mh - 1], radius=mr, fill=255
    )

    # Translucent frosted tint allowing blurred background colors to read through.
    tint = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    tint_grad = _vertical_gradient((mw, mh), (68, 64, 70, 118), (34, 31, 36, 152))
    tint.paste(tint_grad, (ox, oy))
    panel = _clip_onto(panel, tint, map_mask)

    # 3D-perspective road network converging toward an upper vanishing point.
    vp_x = ox + mw * 0.50
    vp_y = oy - mh * 0.55

    def px_at(dx_bottom, y):
        t = (y - vp_y) / (oy + mh - vp_y)
        return vp_x + dx_bottom * t

    def quad(dx0, dx1, y0, y1):
        return [
            (px_at(dx0, y0), y0),
            (px_at(dx1, y0), y0),
            (px_at(dx1, y1), y1),
            (px_at(dx0, y1), y1),
        ]

    geo = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(geo)

    # Subtle coastal water sliver on the right side.
    gd.polygon(quad(126 * s, 260 * s, oy, oy + mh), fill=(82, 120, 126, 56))

    # Scrolling cross-streets and city blocks so consecutive shots feel live.
    scroll = (level * 1.35) % 1.0
    cross_offsets = [((k / 3.0 + scroll) % 1.18) - 0.10 for k in range(4)]

    # Muted architectural city block footprints flanking the avenue.
    for side in (-1, 1):
        for k in range(3):
            u0 = ((k * 0.36 + scroll) % 1.15) - 0.12
            u1 = u0 + 0.24
            y0 = oy + mh * max(0.0, u0)
            y1 = oy + mh * min(1.05, u1)
            if y1 <= y0 + 4 * s:
                continue
            bx0 = side * 66 * s
            bx1 = side * (162 * s if side < 0 else 120 * s)
            if bx0 > bx1:
                bx0, bx1 = bx1, bx0
            gd.polygon(quad(bx0, bx1, y0, y1), fill=(26, 26, 32, 46))
            # Faint sunlit roof rim for pseudo-3D elevation.
            rim_y1 = min(y1, y0 + 3 * s)
            gd.polygon(quad(bx0, bx1, y0, rim_y1), fill=(205, 205, 215, 20))

    # Cross streets.
    for u in cross_offsets:
        yc = oy + mh * u
        half_w = (12 + 8 * max(0.0, u)) * s
        gd.polygon(quad(-240 * s, 240 * s, yc - half_w * 0.5, yc + half_w * 0.5),
                   fill=(145, 140, 148, 34))

    # Central perspective avenue + faint lane curbs.
    gd.polygon(quad(-52 * s, 52 * s, oy, oy + mh), fill=(155, 150, 156, 46))
    for curb_dx in (-52 * s, 52 * s):
        gd.line([(px_at(curb_dx, oy), oy), (px_at(curb_dx, oy + mh), oy + mh)],
                fill=(215, 210, 215, 26), width=max(1, round(1.5 * s)))

    # Faint overpass / arch shadow band across the upper third (matches reference).
    overpass = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    ImageDraw.Draw(overpass).rectangle(
        [ox, oy + round(mh * 0.23), ox + mw, oy + round(mh * 0.31)],
        fill=(18, 16, 20, 48),
    )
    geo = Image.alpha_composite(geo, overpass)

    # Glowing Vice-pink GPS route tapering upward from behind the player puck.
    route_y0 = oy
    route_y1 = oy + round(mh * 0.77)

    def route_poly(w_scale):
        return quad(-11 * s * w_scale, 11 * s * w_scale, route_y0, route_y1)

    glow = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).polygon(route_poly(1.65), fill=(242, 74, 162, 130))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=4.5 * s))

    route = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(route)
    rd.polygon(route_poly(1.0), fill=(244, 88, 168, 238))
    rd.polygon(route_poly(0.42), fill=(255, 174, 218, 195))
    route = Image.alpha_composite(glow, route)

    # Fade the bottom of the GPS line softly behind the player puck.
    fade = Image.new("L", panel.size, 255)
    fade_top = oy + round(mh * 0.64)
    fade_bot = route_y1
    strip = Image.new("L", (1, fade_bot - fade_top + 1))
    strip.putdata([round(255 * (1.0 - y / max(1, fade_bot - fade_top)))
                   for y in range(fade_bot - fade_top + 1)])
    fade.paste(strip.resize((mw, fade_bot - fade_top + 1)), (ox, fade_top))
    ImageDraw.Draw(fade).rectangle([ox, fade_bot + 1, ox + mw, oy + mh], fill=0)
    route_faded = Image.composite(route, Image.new("RGBA", panel.size, (0, 0, 0, 0)), fade)
    geo = Image.alpha_composite(geo, route_faded)

    panel = _clip_onto(panel, geo, map_mask)
    return panel


def _draw_minimap_chrome(panel, ox, oy, mw, mh, mr, level, distance_mi, s):
    """Draw hairline glass border, distance text, player chevron, waypoint dot, and N badge."""
    d = ImageDraw.Draw(panel)
    # Crisp outer dark hairline + inner translucent light glass rim.
    d.rounded_rectangle([ox - s, oy - s, ox + mw - 1 + s, oy + mh - 1 + s],
                        radius=mr + s, outline=(0, 0, 0, 55), width=s)
    d.rounded_rectangle([ox, oy, ox + mw - 1, oy + mh - 1],
                        radius=mr, outline=(232, 236, 240, 150), width=round(1.5 * s))

    # Top-left distance readout ("0.69 mi" style).
    start_mi = 0.84 if distance_mi is None else float(distance_mi)
    dist = max(0.02, start_mi * (1.0 - 0.94 * level))
    dist_txt = f"{dist:.2f} mi"
    dfont = font(21 * s, weight="medium")
    d.text((ox + 14 * s, oy + 10 * s), dist_txt, font=dfont,
           fill=(250, 250, 252, 248), stroke_width=round(1.5 * s),
           stroke_fill=(12, 12, 16, 210))

    # Player puck with white notched directional chevron.
    px, py = ox + round(mw * 0.50), oy + round(mh * 0.79)
    pr = 14 * s
    d.ellipse([px - pr, py - pr, px + pr, py + pr],
              fill=(18, 20, 24, 244), outline=(235, 238, 242, 70), width=s)
    d.polygon([
        (px, py - round(7.5 * s)),
        (px - round(5.5 * s), py + round(5.5 * s)),
        (px, py + round(2.5 * s)),
        (px + round(5.5 * s), py + round(5.5 * s)),
    ], fill=(252, 252, 254, 255))

    # Right-border pink waypoint blip.
    wx, wy = ox + mw - 1, oy + round(mh * 0.42)
    wr = round(7.5 * s)
    d.ellipse([wx - wr, wy - wr, wx + wr, wy + wr],
              fill=(242, 86, 168, 255), outline=(20, 16, 22, 235), width=2 * s)

    # Bottom-right black "N" compass badge.
    nx, ny = ox + mw - 4 * s, oy + mh - 4 * s
    nr = 12 * s
    d.ellipse([nx - nr, ny - nr, nx + nr, ny + nr],
              fill=(10, 10, 14, 246), outline=(220, 224, 230, 80), width=s)
    nfont = font(13 * s, weight="black")
    l, t, r, b = d.textbbox((0, 0), "N", font=nfont)
    d.text((nx - (l + r) / 2, ny - (t + b) / 2), "N", font=nfont, fill=(255, 255, 255, 255))


def _draw_vitals_strip(panel, ox, oy, mw, mh, gap, vh, vr, level, s):
    """Draw the translucent vitals capsule (Health + ENNUI) below the minimap."""
    vx0, vy0 = ox, oy + mh + gap
    vx1, vy1 = vx0 + mw - 1, vy0 + vh - 1

    vmask = Image.new("L", panel.size, 0)
    ImageDraw.Draw(vmask).rounded_rectangle([vx0, vy0, vx1, vy1], radius=vr, fill=255)
    vtint = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    ImageDraw.Draw(vtint).rounded_rectangle([vx0, vy0, vx1, vy1], radius=vr, fill=(22, 22, 28, 152))
    panel = _clip_onto(panel, vtint, vmask)

    d = ImageDraw.Draw(panel)
    d.rounded_rectangle([vx0 - s, vy0 - s, vx1 + s, vy1 + s],
                        radius=vr + s, outline=(0, 0, 0, 50), width=s)
    d.rounded_rectangle([vx0, vy0, vx1, vy1],
                        radius=vr, outline=(232, 236, 240, 130), width=round(1.5 * s))

    ix = vx0 + 23 * s
    ry1 = vy0 + round(vh * 0.32)
    ry2 = vy0 + round(vh * 0.69)
    bh = 9 * s

    # Row 1: draining Health bar + heart icon.
    _draw_heart(d, ix, ry1, 7.5 * s, (220, 245, 224, 238))
    hp = max(0.22, 1.0 - 0.65 * level)
    panel = _draw_pill_bar(panel, vx0 + 42 * s, ry1, vx0 + 326 * s, bh, hp,
                           (102, 204, 114, 245))

    # Row 2: filling ENNUI bar (Focus purple->magenta gradient) + eye icon + label.
    d = ImageDraw.Draw(panel)
    _draw_eye(d, ix, ry2, 8 * s, (236, 218, 255, 238))
    panel = _draw_pill_bar(panel, vx0 + 42 * s, ry2, vx0 + 246 * s, bh, max(0.04, level),
                           (166, 108, 255, 245), (234, 98, 206, 245))

    d = ImageDraw.Draw(panel)
    efont = font(15 * s, weight="bold")
    elabel = "ENNUI"
    ew, eh, etop = _measure_tracked_text(d, elabel, efont, tracking=round(1.5 * s))
    ex = vx0 + 326 * s - ew
    ey = ry2 - eh / 2 - etop
    _draw_tracked_text(d, (ex + s, ey + s), elabel, efont, (0, 0, 0, 175), tracking=round(1.5 * s))
    _draw_tracked_text(d, (ex, ey), elabel, efont, (245, 238, 252, 240), tracking=round(1.5 * s))
    return panel


def _draw_mission_card(im, title, card):
    """Draw the floating GTA VI-style left-anchored mission title card."""
    s = SUPERSAMPLE
    pad = 20
    kicker_txt = card.upper() if card else ""
    title_txt = title.upper()
    kfont = font(21 * s, weight="bold")
    tfont = font(46 * s, weight="black")

    # Measure text to size the gradient scrim cleanly.
    tmp_d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    kw, kh, ktop = _measure_tracked_text(tmp_d, kicker_txt, kfont, tracking=round(2.5 * s))
    tl, tt, tr, tb = tmp_d.textbbox((0, 0), title_txt, font=tfont)
    tw, th = tr - tl, tb - tt

    cw = max(440, min(860, round(max(kw, tw) / s) + 110))
    ch = 114
    card_hi = Image.new("RGBA", ((cw + 2 * pad) * s, (ch + 2 * pad) * s), (0, 0, 0, 0))
    ox, oy = pad * s, pad * s

    # Horizontal gradient dark scrim fading smoothly to transparent on the right.
    scrim = Image.new("RGBA", (cw * s, ch * s))
    row_px = []
    for x in range(cw * s):
        u = x / max(1, cw * s - 1)
        alpha = round(176 * ((1.0 - u) ** 1.35))
        row_px.append((14, 14, 20, alpha))
    strip = Image.new("RGBA", (cw * s, 1))
    strip.putdata(row_px)
    scrim.paste(strip.resize((cw * s, ch * s), Image.Resampling.BILINEAR), (0, 0))
    scrim_mask = Image.new("L", (cw * s, ch * s), 255)
    # Round left edge only by masking left corners.
    corner = Image.new("L", (cw * s, ch * s), 0)
    cd = ImageDraw.Draw(corner)
    cd.rounded_rectangle([0, 0, cw * s - 1, ch * s - 1], radius=10 * s, fill=255)
    cd.rectangle([20 * s, 0, cw * s - 1, ch * s - 1], fill=255)
    scrim_masked = Image.composite(scrim, Image.new("RGBA", (cw * s, ch * s), (0, 0, 0, 0)), corner)
    card_hi.paste(scrim_masked, (ox, oy))

    # Crisp 5 px vertical Vice-pink accent bar with soft glow.
    bar_w = 5 * s
    bar_pad_y = 14 * s
    bar_h = ch * s - 2 * bar_pad_y
    bar_glow = Image.new("RGBA", card_hi.size, (0, 0, 0, 0))
    ImageDraw.Draw(bar_glow).rounded_rectangle(
        [ox, oy + bar_pad_y, ox + bar_w, oy + bar_pad_y + bar_h],
        radius=2 * s, fill=(242, 88, 168, 140),
    )
    bar_glow = bar_glow.filter(ImageFilter.GaussianBlur(radius=4 * s))
    card_hi = Image.alpha_composite(card_hi, bar_glow)

    bar_grad = _vertical_gradient((bar_w, bar_h), (242, 88, 168, 255), (198, 90, 230, 255))
    bar_mask = Image.new("L", (bar_w, bar_h), 0)
    ImageDraw.Draw(bar_mask).rounded_rectangle([0, 0, bar_w - 1, bar_h - 1], radius=2 * s, fill=255)
    bar_img = Image.composite(bar_grad, Image.new("RGBA", (bar_w, bar_h), (0, 0, 0, 0)), bar_mask)
    card_hi.alpha_composite(bar_img, (ox, oy + bar_pad_y))

    # Text + soft blurred drop shadow (no chunky comic outline).
    tx = ox + 22 * s
    ky = oy + 16 * s - ktop
    ty = oy + (48 * s if kicker_txt else 30 * s) - tt

    shadow = Image.new("RGBA", card_hi.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    if kicker_txt:
        _draw_tracked_text(sd, (tx, ky + 2 * s), kicker_txt, kfont,
                           (0, 0, 0, 200), tracking=round(2.5 * s))
    sd.text((tx, ty + 3 * s), title_txt, font=tfont, fill=(0, 0, 0, 215))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=2.5 * s))
    card_hi = Image.alpha_composite(card_hi, shadow)

    td = ImageDraw.Draw(card_hi)
    if kicker_txt:
        _draw_tracked_text(td, (tx, ky), kicker_txt, kfont,
                           (255, 136, 198, 248), tracking=round(2.5 * s))
    td.text((tx, ty), title_txt, font=tfont, fill=(255, 255, 255, 255))

    card_1x = card_hi.resize((cw + 2 * pad, ch + 2 * pad), Image.Resampling.LANCZOS)
    im.alpha_composite(card_1x, (CARD_X - pad, CARD_Y - pad))


def hud(path, level, title=None, card=None, distance_mi=None):
    """Minimal GTA VI-style HUD: frosted minimap, Health/ENNUI vitals, mission card."""
    s = SUPERSAMPLE
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    pw, ph = (MW + 2 * HUD_PAD) * s, (GH + 2 * HUD_PAD) * s
    ox, oy = HUD_PAD * s, HUD_PAD * s
    panel = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))

    panel = _draw_minimap_contents(panel, ox, oy, MW * s, MH * s, MR * s, level, s)
    _draw_minimap_chrome(panel, ox, oy, MW * s, MH * s, MR * s, level, distance_mi, s)
    panel = _draw_vitals_strip(panel, ox, oy, MW * s, MH * s, GAP * s, VH * s, VR * s, level, s)

    panel_1x = panel.resize((MW + 2 * HUD_PAD, GH + 2 * HUD_PAD), Image.Resampling.LANCZOS)
    im.alpha_composite(panel_1x, (GX - HUD_PAD, GY - HUD_PAD))

    if title:
        _draw_mission_card(im, title, card)

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
    mask_path = os.path.join(work, "glass_mask.png")
    if not args.no_hud:
        glass_mask(mask_path)

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
                title=edl.get("title") if i == 0 else None,
                card=edl.get("card"),
                distance_mi=edl.get("distance_mi"))
            cmd += [
                "-i", png, "-i", mask_path, "-filter_complex",
                f"{vf};"
                f"[v]split[vb][vg];"
                f"[vg]crop={GW}:{GH}:{GX}:{GY},gblur=sigma=9:steps=2,format=rgba[gblur];"
                f"[2:v]format=gray[gmask];"
                f"[gblur][gmask]alphamerge[glass];"
                f"[vb][glass]overlay={GX}:{GY}[vglass];"
                f"[vglass][1:v]overlay=0:0,format=yuv420p[o]"
            ]
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
