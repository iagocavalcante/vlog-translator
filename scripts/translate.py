import os
import sys
import openai
import pysrt

openai.api_key = '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'
input_data = sys.stdin.read()
subs = pysrt.from_string(input_data)

prompt_base = (
    "You are going to be a good translator. "
    "Here is a part of the transcript of presentation. "
    "Hello DevsNorte, I'm so excited to talk with you remotely about the epic stack. I've got a bit of a content warning here for you"
    "Translate the following text precisely into Brazilian Portuguese"
    "You will be a good talk translator. "
    "Translate from [START] to [END]:\n[START]\n"
)


def translate_text(text):
    prompt = prompt_base
    prompt += text + "\n[END]"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        temperature=0,
    )
    translated = response.choices[0].text.strip()
    if translated.startswith('「'):
        translated = translated[1:]
    if translated.endswith('」'):
        translated = translated[:-1]
    return translated

def write_to_file(text):
    with open('translated.srt', 'w') as f:
        f.write(text + '\n')

save_target = 'the-epic-stack.vtt'
with open(save_target, 'w') as file:
    for index, subtitle in enumerate(subs):
        subtitle.text = translate_text(subtitle.text)
        file.write(str(subtitle.index) + '\n')
        file.write(str(subtitle.start) + ' --> ' + str(subtitle.end) + '\n')
        file.write(subtitle.text + '\n')
        print(subtitle, flush=True)
