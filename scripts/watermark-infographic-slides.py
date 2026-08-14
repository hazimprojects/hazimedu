#!/usr/bin/env python3
"""Tampal watermark menegak kecil (sudut kanan bawah) pd slaid carousel
infografik (assets/infographics/<slug>/NN-*.webp) — BUKAN seo-thumbnail.webp
(fail tu dah ada watermark jalur footer sendiri, jangan sentuh).

Guna: python3 scripts/watermark-infographic-slides.py assets/infographics/bab-1-1
      python3 scripts/watermark-infographic-slides.py assets/infographics/bab-1-1 assets/infographics/bab-1-2

Rujuk docs/infographic-gallery.md ("Watermark menegak pd slaid carousel")
utk sejarah keputusan reka bentuk ni.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
TEXT = "zymnotes.com"
FONT_SIZE = 20
OPACITY = 140  # drpd 255 (~55%)
MARGIN = 18


def watermark_one(path: Path) -> None:
    base = Image.open(path).convert("RGBA")
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Ukur teks dulu pd kanvas sementara supaya tahu saiz label tepat.
    tmp = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tmp)
    bbox = tdraw.textbbox((0, 0), TEXT, font=font, stroke_width=2)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pad = 6

    label = Image.new("RGBA", (text_w + pad * 2, text_h + pad * 2), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(label)
    ldraw.text(
        (pad - bbox[0], pad - bbox[1]),
        TEXT,
        font=font,
        fill=(255, 255, 255, 255),
        stroke_width=2,
        stroke_fill=(0, 0, 0, 255),
    )

    # Susutkan opacity KESELURUHAN label (bukan hitam/putih penuh).
    alpha = label.split()[3].point(lambda a: int(a * OPACITY / 255))
    label.putalpha(alpha)

    # Menegak — rotate 90 (lawan jam), teks dibaca bawah-ke-atas.
    label = label.rotate(90, expand=True)

    x = base.width - MARGIN - label.width
    y = base.height - MARGIN - label.height
    base.alpha_composite(label, dest=(x, y))

    base.convert("RGB").save(path, "WEBP", quality=92, method=6)
    print(f"watermarked: {path}")


def main(argv):
    if not argv:
        print(__doc__)
        sys.exit(1)
    for arg in argv:
        d = Path(arg)
        for f in sorted(d.glob("*.webp")):
            if f.name == "seo-thumbnail.webp":
                continue
            watermark_one(f)


if __name__ == "__main__":
    main(sys.argv[1:])
