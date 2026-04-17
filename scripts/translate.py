import os
import sys
import pysrt
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

input_data = sys.stdin.read()
subs = pysrt.from_string(input_data)

SYSTEM_PROMPT = (
    "You are a professional subtitle translator. "
    "Translate the user's text into Brazilian Portuguese precisely and naturally, "
    "preserving the original meaning and tone. "
    "Return only the translated text, with no quotes, brackets, or commentary."
)


def translate_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    translated = (response.choices[0].message.content or "").strip()
    if translated.startswith("「"):
        translated = translated[1:]
    if translated.endswith("」"):
        translated = translated[:-1]
    return translated


for subtitle in subs:
    subtitle.text = translate_text(subtitle.text)
    sys.stdout.write(f"{subtitle.index}\n")
    sys.stdout.write(f"{subtitle.start} --> {subtitle.end}\n")
    sys.stdout.write(f"{subtitle.text}\n\n")
    sys.stdout.flush()
