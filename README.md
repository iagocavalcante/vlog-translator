# Vlog Transcription & Brazilian Portuguese Translation Tool

A personal tool for transcribing vlogs and translating them into Brazilian Portuguese.

![screenshot](./docs/screenshot.png)

## Tutorial video

[![frame_02](./docs/frame_02.jpg)](https://youtu.be/UNGi144eVbI)

## Ingredients

- Python and [pip](https://pypi.org/project/pip/)
  - [pysrt](https://github.com/byroot/pysrt) - Python parser for SubRip (srt) files
  - [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features and fixes
  - [openai](https://github.com/openai/openai-python) (SDK v1+) - Official OpenAI Python library
  - [openai-whisper](https://github.com/openai/whisper) - Optional, for fully local transcription
- Next.js 16 (pages router)
- [Radix UI](https://www.radix-ui.com/) - Unstyled, accessible components
- [Stitches](https://github.com/stitchesjs/stitches) - CSS-in-JS library

## How to use

1. Get your OpenAI API Key [here](https://platform.openai.com/account/api-keys)
2. Export the key: `export OPENAI_API_KEY=sk-...`
3. Install and run:

```bash
pip install -r requirements.txt
npm install
npm run dev
```

### Local (offline) transcription

If you prefer to transcribe locally with Whisper instead of the OpenAI API:

```bash
python3 scripts/local-transcribe.py path/to/audio.mp3 output.vtt
```

This uses the `whisper` model directly on your machine (configured for `pt-br`).

## Project Structure

```
PROJECT_ROOT
├── components    # React components
├── pages         # Pages
│   └── api       # API routes
├── public
├── scripts       # Python scripts (transcribe, translate, download)
├── tmp           # Temporary files (downloaded audio)
└── utils         # Utility modules
```

## License

MIT License.

---

Looking for a Markdown note-taking app? Check out Inkdrop:

[![Inkdrop](https://github.com/craftzdog/dotfiles-public/raw/master/images/inkdrop.png)](https://www.inkdrop.app/)
