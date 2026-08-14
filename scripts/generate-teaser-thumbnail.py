#!/usr/bin/env python3
"""Jana seo-thumbnail.webp — imej cover teaser SEO infografik (statik dlm
HTML, rujuk docs/infographic-gallery.md §"Teaser SEO Infografik") drpd
ilustrasi SUMBER (BELUM ada watermark) + jalur footer "zymnotes.com".

Guna:
  python3 scripts/generate-teaser-thumbnail.py <ilustrasi-sumber.png> \
      assets/infographics/<slug>/seo-thumbnail.webp

Jalur footer KEKAL KECIL (~72px, ~9% tinggi ilustrasi) — versi awal
(~150px, ~17%) dilaporkan pengguna "terlalu besar", rujuk docs/
infographic-gallery.md §"Watermark teaser terlalu besar" utk sejarah.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
LOGO_PATH = Path(__file__).resolve().parent.parent / "icons" / "icon-512.png"
TEXT = "zymnotes.com"
STRIP_H = 72
LOGO_SIZE = 36
FONT_SIZE = 30
STRIP_BG = (250, 247, 238)
TEXT_COLOR = (30, 32, 42)


def generate(src_path: Path, out_path: Path) -> None:
    illust = Image.open(src_path).convert("RGB")
    w, h = illust.size

    canvas = Image.new("RGB", (w, h + STRIP_H), STRIP_BG)
    canvas.paste(illust, (0, 0))

    logo = Image.open(LOGO_PATH).convert("RGBA").resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(canvas)

    bbox = draw.textbbox((0, 0), TEXT, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    gap = int(LOGO_SIZE * 0.28)

    total_w = LOGO_SIZE + gap + text_w
    start_x = (w - total_w) // 2
    strip_center_y = h + STRIP_H // 2

    logo_y = strip_center_y - LOGO_SIZE // 2
    canvas.paste(logo, (start_x, logo_y), logo)

    text_x = start_x + LOGO_SIZE + gap
    text_y = strip_center_y - text_h // 2 - bbox[1]
    draw.text((text_x, text_y), TEXT, font=font, fill=TEXT_COLOR)

    canvas.save(out_path, "WEBP", quality=92, method=6)
    print(f"saved: {out_path} ({canvas.width}x{canvas.height})")


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        sys.exit(1)
    generate(Path(argv[0]), Path(argv[1]))


if __name__ == "__main__":
    main(sys.argv[1:])
