---
name: youtube-transcript
description: Fetch YouTube video transcripts via residential proxy. Use when asked to pull transcripts, learn from YouTube videos, or build knowledge bases from channels.
---

## Usage

```bash
python3 ~/workspace/skills/youtube-transcript/scripts/fetch_transcript.py <video_url_or_id> [languages]
```

Returns JSON with: video_id, title, author, full_text, transcript (timestamped entries).

## Bulk channel pull

To pull all videos from a channel:
1. Get the channel page HTML and extract video IDs (grep for `/watch?v=`)
2. Loop through each ID and run the script
3. Save each transcript as a markdown file to the workspace

## Environment

- Proxy is configured in the script (RESIDENTIAL_PROXY env var can override)
- Requires: `youtube-transcript-api`, `requests` (both installed)

## Output format

The script prints JSON to stdout:
```json
{
  "video_id": "abc123",
  "title": "Video Title",
  "author": "Channel Name",
  "full_text": "entire transcript as one string",
  "entries": 1497,
  "transcript": [{"text": "...", "start": 0.0, "duration": 3.5}, ...]
}
```

Save `full_text` as markdown files for knowledge base use.
