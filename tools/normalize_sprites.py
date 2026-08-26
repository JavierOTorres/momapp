#!/usr/bin/env python3
"""Normalize hand-generated sprites so a figure never jumps or resizes between poses.

Sprites come out of image generation and background removal framed inconsistently:
the content sits at a different height and a different scale in every file. In game
that reads as the character changing size and hopping vertically every time it
changes pose, on top of the idle bob the renderer already applies.

For each image this script:

  1. finds the alpha bounding box of the actual content
  2. scales that content so its HEIGHT matches a target figure height
  3. places it on a fresh transparent canvas of the output size
  4. centres it horizontally
  5. positions it so the BOTTOM of the content sits on a fixed baseline

Scaling is by height alone, never by bounding box. Widths stay free, or a wide
sitting pose gets squashed relative to a narrow standing one.

Poses that are legitimately lower and squatter -- sitting, resting -- can be run
with --no-scale, which aligns the baseline without rescaling. Feet on the same
line is what matters; a sitting figure is meant to be shorter overall.

Usage:
    python3 tools/normalize_sprites.py assets/sprites_src -o assets/sprites
    python3 tools/normalize_sprites.py assets/sprites_src/frog_sit.png \
        assets/sprites_src/frog_rest.png -o assets/sprites --no-scale
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install Pillow")


RESAMPLE = {
    "LANCZOS": Image.Resampling.LANCZOS,
    "BICUBIC": Image.Resampling.BICUBIC,
    "BILINEAR": Image.Resampling.BILINEAR,
    "NEAREST": Image.Resampling.NEAREST,
}


def content_box(img, threshold):
    """Alpha bounding box, ignoring the near-transparent halo background removal leaves."""
    alpha = img.getchannel("A")
    if threshold > 0:
        alpha = alpha.point(lambda v: 255 if v >= threshold else 0)
    return alpha.getbbox()


def despeckle(img, threshold, min_blob):
    """Erase alpha islands smaller than min_blob pixels.

    Background removal leaves specks, and a speck is not a harmless cosmetic
    problem here: a stray dot below the feet extends the bounding box, so the
    figure gets scaled down to fit and then hung in the air with the speck
    sitting on the baseline. Measuring has to happen on cleaned alpha.

    Returns (cleaned image, islands removed, pixels removed).
    """
    if min_blob <= 0:
        return img, 0, 0

    w, h = img.size
    solid = img.getchannel("A").point(lambda v: 255 if v >= threshold else 0).load()
    seen = bytearray(w * h)
    doomed = []

    for sy in range(h):
        for sx in range(w):
            if seen[sy * w + sx] or not solid[sx, sy]:
                continue
            stack, blob = [(sx, sy)], []
            seen[sy * w + sx] = 1
            while stack:                                   # iterative: 256x256 overflows recursion
                x, y = stack.pop()
                blob.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and solid[nx, ny]:
                        seen[ny * w + nx] = 1
                        stack.append((nx, ny))
            if len(blob) < min_blob:
                doomed.append(blob)

    if not doomed:
        return img, 0, 0

    out = img.copy()
    px = out.load()
    n = 0
    for blob in doomed:
        for x, y in blob:
            px[x, y] = (0, 0, 0, 0)
            n += 1
    return out, len(doomed), n


def collect(inputs):
    files = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            files += sorted(q for q in p.iterdir() if q.suffix.lower() == ".png")
        elif p.is_file():
            files.append(p)
        else:
            sys.exit("no such file or folder: %s" % p)
    if not files:
        sys.exit("no PNGs found in: %s" % ", ".join(inputs))
    return files


def normalize(path, args):
    """Returns (before, after) as (x0, y0, x1, y1, w, h) tuples, plus warnings."""
    img = Image.open(path).convert("RGBA")
    warn = []

    img, islands, lost = despeckle(img, args.alpha_threshold, args.min_blob)
    if islands:
        warn.append("%s: dropped %d speck%s (%d px) before measuring"
                    % (path.name, islands, "" if islands == 1 else "s", lost))

    box = content_box(img, args.alpha_threshold)
    if box is None:
        return None, None, warn + ["%s is fully transparent, skipped" % path.name]

    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    content = img.crop(box)

    if args.no_scale:
        new_w, new_h = w, h
    else:
        new_h = args.height
        new_w = max(1, round(w * new_h / h))
        content = content.resize((new_w, new_h), RESAMPLE[args.resample])

    canvas = Image.new("RGBA", (args.canvas, args.canvas), (0, 0, 0, 0))
    px = round((args.canvas - new_w) / 2)
    py = args.baseline - new_h

    if new_w > args.canvas:
        warn.append("%s is %dpx wider than the canvas and will be clipped"
                    % (path.name, new_w - args.canvas))
    if py < 0:
        warn.append("%s overflows the top of the canvas by %dpx" % (path.name, -py))
    if args.baseline > args.canvas:
        warn.append("baseline %d is below the canvas bottom %d" % (args.baseline, args.canvas))

    canvas.alpha_composite(content, (px, py))

    out = args.out / path.name
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)

    after = content_box(canvas, args.alpha_threshold)
    return (x0, y0, x1, y1, w, h), after + (after[2] - after[0], after[3] - after[1]), warn


def main():
    ap = argparse.ArgumentParser(
        description="Normalize transparent sprite PNGs to a shared baseline and scale.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:")[1].strip(),
    )
    ap.add_argument("input", nargs="+", help="folder of PNGs, or individual PNG files")
    ap.add_argument("-o", "--out", required=True, type=Path, help="output folder")
    ap.add_argument("--canvas", type=int, default=256, help="output canvas size, square (default 256)")
    ap.add_argument("--baseline", type=int, default=236,
                    help="y of the content bottom in the output (default 236)")
    ap.add_argument("--height", type=int, default=185,
                    help="target figure height in px (default 185)")
    ap.add_argument("--resample", default="LANCZOS", choices=sorted(RESAMPLE),
                    help="resampling filter (default LANCZOS)")
    ap.add_argument("--no-scale", action="store_true",
                    help="align the baseline without rescaling; for poses that are "
                         "legitimately shorter, like sit and rest")
    ap.add_argument("--alpha-threshold", type=int, default=8, metavar="N",
                    help="alpha below N counts as empty when measuring content (default 8)")
    ap.add_argument("--min-blob", type=int, default=48, metavar="N",
                    help="erase disconnected islands smaller than N px before measuring; "
                         "background removal leaves specks that otherwise drag the bounding "
                         "box out and hang the figure in the air (default 48, 0 disables)")
    args = ap.parse_args()

    files = collect(args.input)
    if any(f.resolve() == (args.out / f.name).resolve() for f in files):
        sys.exit("refusing to overwrite the source in place: pick a different --out")

    print("canvas %d  baseline %d  height %s  resample %s"
          % (args.canvas, args.baseline,
             "unchanged (--no-scale)" if args.no_scale else args.height, args.resample))
    print()
    head = "%-18s  %-28s  %-28s" % ("file", "before  (x0,y0,x1,y1  w x h)", "after   (x0,y0,x1,y1  w x h)")
    print(head)
    print("-" * len(head))

    warnings, afters = [], []
    for f in files:
        before, after, warn = normalize(f, args)
        warnings += warn
        if before is None:
            print("%-18s  %s" % (f.name, "(empty)"))
            continue
        afters.append(after)
        print("%-18s  %-28s  %-28s" % (
            f.name,
            "%3d,%3d,%3d,%3d  %3d x %3d" % before,
            "%3d,%3d,%3d,%3d  %3d x %3d" % after,
        ))

    if afters:
        bottoms = [a[3] for a in afters]
        heights = [a[5] for a in afters]
        centres = [(a[0] + a[2]) / 2 for a in afters]
        print()
        print("baseline spread : %dpx  (bottoms %d..%d)" % (max(bottoms) - min(bottoms), min(bottoms), max(bottoms)))
        print("height spread   : %dpx  (heights %d..%d)" % (max(heights) - min(heights), min(heights), max(heights)))
        print("centre spread   : %.1fpx" % (max(centres) - min(centres)))

    for w in warnings:
        print("warning: %s" % w, file=sys.stderr)
    print("\n%d file(s) -> %s" % (len(afters), args.out))


if __name__ == "__main__":
    main()
