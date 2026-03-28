#!/usr/bin/env python3
"""Generate macOS app icon from source artwork.

Reads assets/icon.png and outputs assets/icon.icns.

Usage: python3 scripts/generate-icon.py
"""

import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "assets", "icon.png")
OUTPUT = os.path.join(ROOT, "assets", "icon.icns")


def main():
    if not os.path.exists(SOURCE):
        print(f"Error: source icon not found at {SOURCE}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {SOURCE}")

    iconset = tempfile.mkdtemp(suffix=".iconset")
    sizes = [16, 32, 64, 128, 256, 512]
    retina_bases = [16, 32, 128, 256, 512]

    for size in sizes:
        out = os.path.join(iconset, f"icon_{size}x{size}.png")
        subprocess.run(
            ["sips", "-z", str(size), str(size), SOURCE, "--out", out],
            capture_output=True,
        )

    for base in retina_bases:
        double = base * 2
        out = os.path.join(iconset, f"icon_{base}x{base}@2x.png")
        subprocess.run(
            ["sips", "-z", str(double), str(double), SOURCE, "--out", out],
            capture_output=True,
        )

    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", OUTPUT], check=True)

    for f in os.listdir(iconset):
        os.remove(os.path.join(iconset, f))
    os.rmdir(iconset)

    print(f"  Wrote {OUTPUT}")
    print("Done.")


if __name__ == "__main__":
    main()
