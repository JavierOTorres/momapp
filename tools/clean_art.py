#!/usr/bin/env python3
"""Clean and frame the prop and background art.

Characters go through normalize_sprites.py, which pins them to a shared baseline.
Props are different: each one is placed in the world by its ground contact, so what
matters is that the image *is* the art, with no transparent margin. Any transparent
row below the lowest pixel hangs the prop in the air by exactly that many pixels.

Three passes, in order:

  1. strip chroma-key residue -- the generators leave a faint magenta halo hugging
     the outline, low alpha but coloured enough to read as a pink fringe on screen
  2. despeckle, reusing the connected-island pass from normalize_sprites
  3. tight crop to the alpha bounding box, so the bottom row is the ground contact

The background is exempt from the crop: the empty space above its wall is load
bearing, since the wall has to sit at a fixed height in the world. It still gets
passes 1 and 2.

Usage:
    python3 tools/clean_art.py assets/props_src -o assets/props
    python3 tools/clean_art.py assets/background_src -o assets/background --no-crop
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install Pillow")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalize_sprites import despeckle, content_box


def strip_magenta(img, sat):
    """Erase pixels the key colour bled into. Magenta is never in this palette, so
       anything that reads as magenta at all is residue, whatever its alpha."""
    px = img.load()
    w, h = img.size
    n = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and r > 120 and b > 120 and g < min(r, b) * sat:
                px[x, y] = (0, 0, 0, 0)
                n += 1
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("Usage:")[0].strip(),
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="+", help="folder of PNGs, or individual files")
    ap.add_argument("-o", "--out", required=True, type=Path)
    ap.add_argument("--no-crop", action="store_true",
                    help="keep the canvas as-is; for the background, whose empty "
                         "space above the wall carries its position")
    ap.add_argument("--long-side", type=int, default=0, metavar="N",
                    help="resample so the longest side is N px (0 leaves it alone)")
    ap.add_argument("--alpha-threshold", type=int, default=8)
    ap.add_argument("--min-blob", type=int, default=48)
    ap.add_argument("--key-saturation", type=float, default=0.62, metavar="F",
                    help="how far green must sit below red and blue to count as key "
                         "residue (default 0.62)")
    args = ap.parse_args()

    files = []
    for raw in args.input:
        p = Path(raw)
        if p.is_dir():
            files += sorted(q for q in p.iterdir() if q.suffix.lower() == ".png")
        elif p.is_file():
            files.append(p)
        else:
            sys.exit("no such file or folder: %s" % p)
    if not files:
        sys.exit("no PNGs found")

    args.out.mkdir(parents=True, exist_ok=True)
    print("%-26s %-11s %-11s %7s %7s  %s" % ("file", "in", "out", "keyed", "specks", "note"))
    print("-" * 84)

    for f in files:
        img = Image.open(f).convert("RGBA")
        before = "%dx%d" % img.size
        keyed = strip_magenta(img, args.key_saturation)
        img, islands, lost = despeckle(img, args.alpha_threshold, args.min_blob)

        note = []
        if not args.no_crop:
            box = content_box(img, args.alpha_threshold)
            if box is None:
                print("%-26s fully transparent, skipped" % f.name)
                continue
            below = img.size[1] - box[3]
            if below:
                note.append("was floating %dpx" % below)
            img = img.crop(box)

        if args.long_side:
            w, h = img.size
            s = args.long_side / max(w, h)
            if s != 1:
                img = img.resize((max(1, round(w * s)), max(1, round(h * s))),
                                 Image.Resampling.LANCZOS)
                note.append("resampled %.2fx" % s)

        img.save(args.out / f.name)
        print("%-26s %-11s %-11s %7d %7s  %s" % (
            f.name, before, "%dx%d" % img.size, keyed,
            "%d (%dpx)" % (islands, lost) if islands else "-", ", ".join(note)))

    print("\n%d file(s) -> %s" % (len(files), args.out))


if __name__ == "__main__":
    main()
