import os
import openai
import sys
openai.api_key = ''
# video_id = sys.argv[1]
audio_file_path = os.path.join(os.getcwd(), 'tmp', 'the-epic-stack.mp4')

audio_file = open(audio_file_path, "rb")
transcript = openai.Audio.transcribe(
  file=audio_file,
  model="whisper-1",
  response_format='srt',
  prompt=(
      'This is a talk about epic stack using remix. '
      'In this presentation Kent C. Dodds will talk about the epic stack. '
      'This a talk for DevsNorth Community. '
  )
)
print(transcript)
