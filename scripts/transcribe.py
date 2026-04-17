import os
import sys
from openai import OpenAI

if len(sys.argv) < 2 or not sys.argv[1]:
    print("ERROR: video_id argument is required", file=sys.stderr)
    sys.exit(1)

video_id = sys.argv[1]
audio_file_path = os.path.join(os.getcwd(), "tmp", f"{video_id}.m4a")

if not os.path.exists(audio_file_path):
    print(f"ERROR: audio file not found at {audio_file_path}", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

with open(audio_file_path, "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="srt",
    )

print(transcript)
