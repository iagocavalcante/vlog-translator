"""Split an English SRT into text-only batches for translation.

Timestamps are intentionally NOT included in the batches: subagents translate
only the text, keyed by cue index, so timestamps can never drift. Stitching
happens later in stitch_subs.py against the original SRT.
"""

import json
import os
import sys

import pysrt

if len(sys.argv) < 3:
    print("usage: prep_batches.py <input.srt> <batch_dir> [batch_size]", file=sys.stderr)
    sys.exit(1)

input_srt = sys.argv[1]
batch_dir = sys.argv[2]
batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 75

subs = pysrt.open(input_srt)
os.makedirs(batch_dir, exist_ok=True)

cues = [{"i": s.index, "text": s.text} for s in subs]

batches = [cues[i : i + batch_size] for i in range(0, len(cues), batch_size)]

for n, batch in enumerate(batches):
    path = os.path.join(batch_dir, f"batch_{n:02d}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)

print(f"total_cues={len(cues)}")
print(f"num_batches={len(batches)}")
print(f"batch_size={batch_size}")
