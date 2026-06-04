#!/usr/bin/env python3
"""Render og-image.svg to og-image.png (1200x630).

On first run, downloads Sora and Space Mono from Google Fonts into .fonts/.
Subsequent runs reuse the cached fonts. Re-run after editing og-image.svg.
"""
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
FONT_DIR = ROOT / ".fonts"
SVG = ROOT / "og-image.svg"
PNG = ROOT / "og-image.png"

FONTS = {
    "Sora-Variable.ttf":    "https://github.com/google/fonts/raw/main/ofl/sora/Sora%5Bwght%5D.ttf",
    "SpaceMono-Bold.ttf":   "https://github.com/google/fonts/raw/main/ofl/spacemono/SpaceMono-Bold.ttf",
    "SpaceMono-Regular.ttf":"https://github.com/google/fonts/raw/main/ofl/spacemono/SpaceMono-Regular.ttf",
}


def ensure_fonts() -> dict[str, Path]:
    FONT_DIR.mkdir(exist_ok=True)
    paths: dict[str, Path] = {}
    for name, url in FONTS.items():
        p = FONT_DIR / name
        if not p.exists():
            print(f"  fetching {name}...")
            urllib.request.urlretrieve(url, p)
        paths[name] = p.resolve()
    return paths


def inject_font_paths(svg_text: str, paths: dict[str, Path]) -> str:
    for name, p in paths.items():
        svg_text = svg_text.replace(f"{{{{FONT:{name}}}}}", f"file://{p}")
    return svg_text


def main() -> int:
    try:
        import cairosvg
    except ImportError:
        print("error: cairosvg not installed.\n  run: pip install -r requirements.txt", file=sys.stderr)
        return 1

    if not SVG.exists():
        print(f"error: {SVG} not found", file=sys.stderr)
        return 1

    print("ensuring fonts...")
    paths = ensure_fonts()

    print(f"rendering {SVG.name} -> {PNG.name}...")
    svg_text = SVG.read_text(encoding="utf-8")
    svg_text = inject_font_paths(svg_text, paths)

    cairosvg.svg2png(
        bytestring=svg_text.encode("utf-8"),
        write_to=str(PNG),
        output_width=1200,
        output_height=630,
    )

    size_kb = PNG.stat().st_size / 1024
    print(f"wrote {PNG.name} ({size_kb:.1f} KB, 1200x630)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
