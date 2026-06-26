"""Stitch translated cue text back onto the original SRT timestamps.

Reads the authoritative English SRT (for indices + timestamps) and all
batch_*.pt.json translation maps. Validates that every cue has a translation
before writing. Timestamps come only from the original SRT, so they cannot
drift during translation.
"""

import glob
import json
import os
import sys

import pysrt

if len(sys.argv) < 4:
    print("usage: stitch_subs.py <original.srt> <batch_dir> <output.srt>", file=sys.stderr)
    sys.exit(1)

original_srt = sys.argv[1]
batch_dir = sys.argv[2]
output_srt = sys.argv[3]

subs = pysrt.open(original_srt)

translations: dict[str, str] = {}
for path in sorted(glob.glob(os.path.join(batch_dir, "batch_*.pt.json"))):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for k, v in data.items():
        translations[str(k)] = v

missing = [s.index for s in subs if str(s.index) not in translations]
if missing:
    print(f"ERROR: {len(missing)} cues missing translation: {missing[:20]}...", file=sys.stderr)
    sys.exit(2)

empty = [s.index for s in subs if not translations[str(s.index)].strip()]
if empty:
    print(f"WARNING: {len(empty)} translated cues are empty: {empty[:20]}", file=sys.stderr)

for s in subs:
    s.text = translations[str(s.index)]

subs.save(output_srt, encoding="utf-8")
print(f"OK: wrote {len(subs)} cues to {output_srt}")
