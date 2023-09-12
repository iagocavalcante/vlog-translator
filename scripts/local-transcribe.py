import datetime
import sys
import whisper
import os

# get path from args or use default
file_path = sys.argv[1] if len(sys.argv) > 1 else 'audio.mp3'
subtitle_name = sys.argv[2] if len(sys.argv) > 2 else 'default.vtt'

audio_file_path = os.path.join(file_path)

model = whisper.load_model('medium')
option = whisper.DecodingOptions(language='pt-br', fp32=False)
result = model.transcribe(audio_file_path)

with open(subtitle_name, 'w') as file:
  for index, segment in enumerate(result['segments']):
    file.write(str(index + 1) + '\n')
    file.write(str(datetime.timedelta(seconds=segment['start'])) + ' --> ' + str(datetime.timedelta(seconds=segment['end'])) + '\n')
    file.write(segment['text'].strip() + '\n')
    file.write('\n')

