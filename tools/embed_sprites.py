#!/usr/bin/env python3
"""Bake the normalized sprites into index.html as data URIs.

The game has to stay one double-clickable file. A page opened over file:// cannot
load its own assets/ folder in Safari, and in browsers where it can, the images come
back cross-origin and taint the canvas, which breaks the hollow treatment. Data URIs
are same-origin everywhere, so embedding fixes both at once.

assets/sprites/ stays the source of truth. This rewrites the block between the
sprite-data markers in index.html and touches nothing else, so it is safe to re-run
after every art change. Anything not embedded still falls back to the folder path.

Usage:
    python3 tools/embed_sprites.py
    python3 tools/embed_sprites.py --check      # non-zero exit if out of date
"""

import argparse
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SPRITES = ROOT / "assets" / "sprites"

START = "/* sprite-data:start */"
END = "/* sprite-data:end */"

POSES = ["stand", "walk_a", "walk_b", "sit", "rest", "weary"]


def wired_species(html):
    """Only embed what the game actually asks for, so unused art costs nothing."""
    m = re.search(r"const SPRITE_SPECIES\s*=\s*\[([^\]]*)\]", html)
    if not m:
        sys.exit("could not find SPRITE_SPECIES in index.html")
    return re.findall(r'"([^"]+)"', m.group(1))


def build(species):
    entries, total, missing = [], 0, []
    for key in species:
        for pose in POSES:
            f = SPRITES / ("%s_%s.png" % (key, pose))
            if not f.is_file():
                missing.append(f.relative_to(ROOT).as_posix())
                continue
            raw = f.read_bytes()
            total += len(raw)
            b64 = base64.b64encode(raw).decode("ascii")
            entries.append('  "%s_%s": "data:image/png;base64,%s"' % (key, pose, b64))
    body = "const SPRITE_DATA = {\n" + ",\n".join(entries) + "\n};" if entries \
        else "const SPRITE_DATA = {};"
    return body, total, missing


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("Usage:")[0].strip(),
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify index.html is up to date; do not write")
    args = ap.parse_args()

    html = INDEX.read_text()
    if START not in html or END not in html:
        sys.exit("index.html is missing the %s / %s markers" % (START, END))

    species = wired_species(html)
    body, total, missing = build(species)
    for m in missing:
        print("warning: %s not found, falling back to the folder path" % m, file=sys.stderr)

    before = html.index(START) + len(START)
    after = html.index(END)
    updated = html[:before] + "\n" + body + "\n" + html[after:]

    if args.check:
        stale = updated != html
        print("index.html is %s" % ("OUT OF DATE — run tools/embed_sprites.py" if stale else "up to date"))
        return 1 if stale else 0

    INDEX.write_text(updated)
    n = len(species) * len(POSES) - len(missing)
    print("embedded %d sprite%s for %s" % (n, "" if n == 1 else "s", ", ".join(species) or "nothing"))
    print("  art      %8d bytes" % total)
    print("  encoded  %8d bytes" % (len(body) - 30))
    print("  index    %8d -> %d bytes" % (len(html), len(updated)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
