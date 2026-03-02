---
name: youtube-transcripts
description: Pull transcripts from YouTube channels or individual videos using a headless browser. Use this when someone asks you to learn from, analyze, or build a knowledge base from a YouTube creator's content.
---

## How to use

Run the script at `skills/youtube-transcripts/scripts/pull.py`:

### Pull from a channel (latest N videos):
```bash
python3 skills/youtube-transcripts/scripts/pull.py \
  --channel "https://www.youtube.com/@channelname/videos" \
  --count 20 \
  --output ~/workspace/transcripts-channelname
```

### Pull a single video:
```bash
python3 skills/youtube-transcripts/scripts/pull.py \
  --video "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output ~/workspace/transcripts-channelname
```

### Arguments:
- `--channel` — YouTube channel URL (e.g. `https://www.youtube.com/@creator/videos`)
- `--video` — Single YouTube video URL
- `--count` — Number of videos to pull (default: 20, works with --channel)
- `--output` — Where to save transcript .md files (default: `./transcripts/`)

## After pulling transcripts

Once transcripts are saved, read the README.md in the output folder (if it exists) or list the files to understand what's available. Reference specific transcript files when answering questions about the creator's content.

## Dependencies

Already installed on this machine:
- Python 3
- Playwright
- Chromium at `/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome`
