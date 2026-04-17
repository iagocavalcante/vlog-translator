import datetime
import os
import sys
import whisper


def format_timestamp(seconds: float) -> str:
    td = datetime.timedelta(seconds=seconds)
    total_ms = int(td.total_seconds() * 1000)
    hours, rem = divmod(total_ms, 3600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def write_srt(segments, out) -> None:
    for index, segment in enumerate(segments, start=1):
        out.write(f"{index}\n")
        out.write(
            f"{format_timestamp(segment['start'])} --> "
            f"{format_timestamp(segment['end'])}\n"
        )
        out.write(segment["text"].strip() + "\n\n")
        out.flush()


if len(sys.argv) < 2 or not sys.argv[1]:
    print("ERROR: audio/video path argument is required", file=sys.stderr)
    sys.exit(1)

file_path = sys.argv[1]
subtitle_name = sys.argv[2] if len(sys.argv) > 2 else None

if not os.path.exists(file_path):
    print(f"ERROR: file not found at {file_path}", file=sys.stderr)
    sys.exit(1)

print("Loading whisper model...", file=sys.stderr, flush=True)
model = whisper.load_model("medium")

print(f"Transcribing {file_path}...", file=sys.stderr, flush=True)
result = model.transcribe(file_path, language="pt", fp16=False)

if subtitle_name:
    with open(subtitle_name, "w") as f:
        write_srt(result["segments"], f)
else:
    write_srt(result["segments"], sys.stdout)
