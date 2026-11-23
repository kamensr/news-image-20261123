#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261123 grader.

Standard library only: copy the prebuilt entry.png sitting next to this
file into $MAKEFUN_OUTPUT_DIR/entry.png, then validate the output is a
1024x1024 PNG of at most 1 MiB and print its size, dimensions and SHA-256.

This script deliberately does NOT import generate.py (Pillow is not in the
grader image) and never writes into the current working directory (the
grader's filesystem is read-only outside $MAKEFUN_OUTPUT_DIR).
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1024 * 1024
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def png_dimensions(path):
    """Read width/height from a PNG header without any image library."""
    with open(path, "rb") as fh:
        header = fh.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    if header[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    if not os.path.isfile(source):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)

    size = os.path.getsize(dest)
    width, height = png_dimensions(dest)
    digest = sha256_of(dest)
    print("entry.png: %d bytes, %dx%d, sha256 %s"
          % (size, width, height, digest))
    if size > MAX_BYTES:
        print("error: entry.png exceeds 1 MiB (%d bytes)" % size,
              file=sys.stderr)
        return 1
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print("error: expected 1024x1024, got %dx%d" % (width, height),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
