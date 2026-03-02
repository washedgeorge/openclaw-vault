#!/usr/bin/env python3
"""Fetch YouTube transcript via residential proxy."""

import sys
import json
import os
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

PROXY_URL = os.environ.get("RESIDENTIAL_PROXY", "http://xThg9lo3:ExB66HGwUw02@gateway.aluvia.io:8080")
LANGUAGES = ["en", "fr", "de", "es", "it", "pt", "nl"]


def extract_video_id(url_or_id):
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$"
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id


def fetch_transcript(video_id, languages=None):
    if languages is None:
        languages = LANGUAGES

    session = requests.Session()
    session.proxies = {"http": PROXY_URL, "https": PROXY_URL}

    api = YouTubeTranscriptApi(http_client=session)
    transcript = api.fetch(video_id, languages=languages)

    return [{"text": entry.text, "start": entry.start, "duration": entry.duration} for entry in transcript]


def get_video_title(video_id):
    try:
        resp = requests.get(
            f"https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_id}",
            proxies={"http": PROXY_URL, "https": PROXY_URL},
            timeout=10
        )
        data = resp.json()
        return data.get("title", "Unknown"), data.get("author_name", "Unknown")
    except:
        return "Unknown", "Unknown"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: fetch_transcript.py <video_id_or_url> [languages]"}))
        sys.exit(1)

    video_input = sys.argv[1]
    languages = sys.argv[2].split(",") if len(sys.argv) > 2 else LANGUAGES

    video_id = extract_video_id(video_input)
    title, author = get_video_title(video_id)

    try:
        transcript = fetch_transcript(video_id, languages)
        full_text = " ".join([entry["text"] for entry in transcript])

        print(json.dumps({
            "video_id": video_id,
            "title": title,
            "author": author,
            "language": languages[0] if transcript else None,
            "entries": len(transcript),
            "full_text": full_text,
            "transcript": transcript
        }))
    except TranscriptsDisabled:
        print(json.dumps({"error": "Transcripts are disabled for this video", "video_id": video_id}))
        sys.exit(1)
    except NoTranscriptFound:
        print(json.dumps({"error": f"No transcript found in languages: {languages}", "video_id": video_id}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "video_id": video_id}))
        sys.exit(1)


if __name__ == "__main__":
    main()
