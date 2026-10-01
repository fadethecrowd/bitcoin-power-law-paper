#!/usr/bin/env python3
"""Verify whether a local file is the exact frozen v0.8 CSV.

This checks bytes only. A different lawfully obtained provider file can reproduce
similar statistical results without matching this hash.
"""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
EXPECTED = "ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f"

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('csv', type=Path)
    args=ap.parse_args()
    got=sha256(args.csv)
    print(f"sha256 = {got}")
    if got == EXPECTED:
        print("MATCH: exact frozen v0.8 CSV")
        return 0
    print("NO MATCH: this is not byte-for-byte the frozen v0.8 CSV")
    print("That does not by itself imply the data are unsuitable for statistical reproduction.")
    return 1
if __name__=='__main__': raise SystemExit(main())
