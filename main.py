#!/usr/bin/env python3
"""VELDARA -- a travel poster for a place that isn't there.

Writes the stored poster to $MAKEFUN_OUTPUT_DIR (or this script's own
directory when the variable is unset) and verifies the copy byte-for-byte
with sha256. Standard library only; no network, no image processing.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or str(here)
    destination = Path(output_dir) / SOURCE_NAME
    destination.parent.mkdir(parents=True, exist_ok=True)

    # The output directory may be this repository's own directory, in which
    # case source and destination are the same file: verify in place and
    # skip the copy instead of failing on SameFileError.
    if destination.resolve() == source.resolve():
        print(f"{destination} is already the stored poster; skipping copy")
    else:
        shutil.copyfile(source, destination)

    source_hash = sha256_of(source)
    destination_hash = sha256_of(destination)
    if source_hash != destination_hash:
        print(
            f"error: sha256 mismatch after copy "
            f"(source {source_hash}, dest {destination_hash})",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {destination} ({destination.stat().st_size} bytes)")
    print(f"sha256: {destination_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
