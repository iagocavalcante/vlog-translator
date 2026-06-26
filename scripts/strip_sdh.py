"""Strip SDH annotations from an SRT, producing clean dialogue-only subtitles.

Removes bracketed annotations ([sound cues] and [speaker labels]), drops cues
that become empty, and normalizes multi-speaker dashes. Song lyrics (lines with
the ♪ marker) are kept — they are sung content, not sound effects. Remaining
cues are renumbered sequentially; timestamps are never modified.
"""

import re
import sys

import pysrt

if len(sys.argv) < 3:
    print("usage: strip_sdh.py <input.srt> <output.srt>", file=sys.stderr)
    sys.exit(1)

src, dst = sys.argv[1], sys.argv[2]

# Character classes match newlines, so this also catches bracket cues that span
# two lines, e.g. ["Que Sera, Sera (O Que Será,\nSerá)" toca].
BRACKET = re.compile(r"\[[^\]]*\]")

subs = pysrt.open(src)
kept = []
removed = 0

for cue in subs:
    text = BRACKET.sub("", cue.text)

    clean_lines = []
    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line in ("", "-"):  # blank, or a dash left behind by a removed cue
            continue
        clean_lines.append(line)

    if not clean_lines:
        removed += 1
        continue

    if len(clean_lines) == 1:
        # Single remaining speaker -> drop the leading dialogue dash.
        clean_lines[0] = re.sub(r"^-\s*", "", clean_lines[0]).strip()
    else:
        # Multiple speakers -> keep dashes, normalized to source style "-text".
        clean_lines = [re.sub(r"^-\s*", "-", ln) for ln in clean_lines]

    cue.text = "\n".join(clean_lines)
    kept.append(cue)

out = pysrt.SubRipFile()
for i, cue in enumerate(kept, start=1):
    cue.index = i
    out.append(cue)
out.save(dst, encoding="utf-8")

print(f"kept={len(kept)} removed={removed} total={len(subs)}")
