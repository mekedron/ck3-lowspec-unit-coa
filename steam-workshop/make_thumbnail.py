"""Builds thumbnail.png (Workshop preview, 1024x1024) and thumbnail-200px.png (a legibility
check at Steam's listing size, not uploaded).

Same frame as the other low spec mods - title band on top, BEFORE | AFTER below - but the
halves are drawn rather than screenshotted: a heater shield in plain realm colours, as
vanilla shows it with Advanced Shaders off, next to the same shield with its coat of arms.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "thumbnail.png")
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

S, BAND, SS = 1024, 190, 4                     # SS: supersampling for the drawn shapes
GOLD = (222, 190, 120)
CREAM = (248, 242, 230)
DARK = (14, 12, 10)
RED, RED_DARK = (150, 28, 32), (96, 16, 20)    # realm colours: primary, secondary
OR = (226, 182, 64)
RIM = (58, 52, 46)


def shield_poly(cx, top, w, h, n=40):
    """Heater shield: straight top, straight sides for 40 %, curves to a point."""
    l, r = cx - w / 2, cx + w / 2
    side = top + h * 0.40
    pts = [(l, top), (r, top), (r, side)]
    for i in range(1, n + 1):                  # right flank down to the point
        t = i / n
        pts.append((r - (w / 2) * t ** 1.6, side + (h - (side - top)) * t))
    for i in range(n - 1, 0, -1):              # left flank back up
        t = i / n
        pts.append((l + (w / 2) * t ** 1.6, side + (h - (side - top)) * t))
    pts.append((l, side))
    return pts


def mask_of(size, pts):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def draw_shield(col_w, col_h, heraldry):
    W, H = col_w * SS, col_h * SS
    img = Image.new("RGB", (W, H), DARK)
    # soft vignette backdrop
    bg = Image.new("RGB", (W, H), (34, 30, 26))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([W * 0.05, H * 0.05, W * 0.95, H * 0.95], fill=255)
    img = Image.composite(bg, img, glow.filter(ImageFilter.GaussianBlur(W * 0.12)))

    cx, top, sw, sh = W / 2, H * 0.08, W * 0.62, H * 0.68
    outer = shield_poly(cx, top, sw, sh)
    inset = 9 * SS
    inner = shield_poly(cx, top + inset, sw - 2 * inset, sh - 2.2 * inset)

    # drop shadow
    sh_m = mask_of((W, H), [(x + 10 * SS, y + 14 * SS) for x, y in outer]).filter(ImageFilter.GaussianBlur(14 * SS))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, sh_m.point(lambda v: v * 0.7))

    img.paste(RIM, mask=mask_of((W, H), outer))

    field = Image.new("RGB", (W, H), RED)
    d = ImageDraw.Draw(field)
    if heraldry:
        # quarterly gules and or, a cross between them in the other tincture
        d.rectangle([0, 0, cx, top + sh * 0.42], fill=RED)
        d.rectangle([cx, 0, W, top + sh * 0.42], fill=OR)
        d.rectangle([0, top + sh * 0.42, cx, H], fill=OR)
        d.rectangle([cx, top + sh * 0.42, W, H], fill=RED)
        cw = sw * 0.11
        d.rectangle([cx - cw / 2, 0, cx + cw / 2, H], fill=(24, 22, 24))
        d.rectangle([0, top + sh * 0.42 - cw / 2, W, top + sh * 0.42 + cw / 2], fill=(24, 22, 24))
    else:
        # what low spec shows: the realm's primary colour with the secondary on the lower half
        d.rectangle([0, top + sh * 0.55, W, H], fill=RED_DARK)
    # light from the upper left, like the map sun
    shade = Image.linear_gradient("L").rotate(35, expand=False).resize((W, H))
    field = Image.composite(field, Image.new("RGB", (W, H), (0, 0, 0)), shade.point(lambda v: 255 - v * 0.45))
    img.paste(field, mask=mask_of((W, H), inner))

    # gold boss line along the rim
    ImageDraw.Draw(img).line(inner + [inner[0]], fill=GOLD, width=3 * SS)
    return img.resize((col_w, col_h), Image.LANCZOS)


def fit(d, text, size, max_w):
    while size > 40:
        f = ImageFont.truetype(FB, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(FB, size)


def main():
    title, sub = "UNIT COATS OF ARMS", "ADVANCED SHADERS OFF"
    col_w, col_h = S // 2, S - BAND
    canvas = Image.new("RGB", (S, S), DARK)
    canvas.paste(draw_shield(col_w, col_h, False), (0, BAND))
    canvas.paste(draw_shield(col_w, col_h, True), (col_w, BAND))
    d = ImageDraw.Draw(canvas, "RGBA")
    f_title = fit(d, title, 92, S - 60)
    f_sub = fit(d, sub, 58, S - 60)
    f_tag = ImageFont.truetype(FB, 88)
    tw = d.textlength(title, font=f_title); d.text(((S - tw) / 2, 18), title, font=f_title, fill=CREAM)
    sw = d.textlength(sub, font=f_sub); d.text(((S - sw) / 2, 118), sub, font=f_sub, fill=GOLD)
    for i, text in enumerate(("BEFORE", "AFTER")):
        w = d.textlength(text, font=f_tag)
        x = i * col_w + (col_w - w) / 2
        y = S - f_tag.size - 50
        d.rectangle([x - 22, y - 8, x + w + 22, y + f_tag.size + 22], fill=(14, 12, 10, 215))
        d.text((x, y), text, font=f_tag, fill=CREAM)
    d.rectangle([0, BAND - 4, S, BAND], fill=GOLD)
    d.rectangle([col_w - 2, BAND, col_w + 2, S], fill=GOLD)

    # rebuilt from raw pixels: no text chunks, EXIF or ICC profile
    clean = Image.frombytes("RGB", canvas.size, canvas.tobytes())
    clean = clean.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    clean.save(OUT, "PNG", optimize=True)
    clean.convert("RGB").resize((200, 200), Image.LANCZOS).save(os.path.join(HERE, "thumbnail-200px.png"))
    print(OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
