#!/usr/bin/env python3
"""
YouTube Channel Transcript Puller
Uses Playwright with stealth settings to extract transcripts via YouTube's UI.

Usage:
  python3 pull.py --channel <channel_url> [--count 20] [--output <dir>]
  python3 pull.py --video <video_url> [--output <dir>]
  python3 pull.py --help
"""

import argparse, html, json, os, re, sys, time
from pathlib import Path

CHROME_PATH = "/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"

def get_browser():
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = pw.chromium.launch(
        executable_path=CHROME_PATH,
        headless=False,
        args=[
            "--headless=new",
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-gpu",
            "--window-size=1920,1080",
        ]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
    )
    ctx.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
    """)
    return pw, browser, ctx

def get_video_ids(ctx, channel_url, count=20):
    page = ctx.new_page()
    page.goto(channel_url, wait_until="networkidle", timeout=30000)
    time.sleep(3)
    for _ in range(count // 5 + 3):
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        time.sleep(2)

    links = page.eval_on_selector_all(
        "a[href*='/watch?v=']",
        "els => els.map(e => e.href)"
    )
    page.close()

    seen = set()
    ids = []
    for link in links:
        m = re.search(r'v=([a-zA-Z0-9_-]{11})', link)
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            ids.append(m.group(1))
    return ids[:count]

def get_transcript_via_ui(ctx, video_id):
    page = ctx.new_page()
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        title = page.title().replace(" - YouTube", "").strip()

        # Dismiss consent if present
        try:
            page.click('button[aria-label="Accept all"]', timeout=3000)
            time.sleep(2)
        except:
            pass

        # Click "...more" to expand description
        try:
            page.click('#expand', timeout=3000)
            time.sleep(1)
        except:
            pass

        # Click "Show transcript"
        try:
            page.click('button[aria-label="Show transcript"]', timeout=5000)
            time.sleep(3)
        except:
            # Try via more actions menu
            try:
                page.click('#button-shape button[aria-label="More actions"]', timeout=3000)
                time.sleep(1)
                page.click('text=Show transcript', timeout=3000)
                time.sleep(3)
            except:
                pass

        # Extract transcript segments
        segments = page.eval_on_selector_all(
            'ytd-transcript-segment-renderer .segment-text, '
            'ytd-transcript-segment-renderer yt-formatted-string',
            'els => els.map(e => e.textContent.trim())'
        )

        if segments:
            transcript = " ".join(s for s in segments if s)
            page.close()
            return title, transcript

        # Fallback: try extracting caption URL from page JS and fetching directly
        cap_url = page.evaluate("""() => {
            try {
                const s = document.querySelector('script:not([src])');
                const all = document.querySelectorAll('script');
                for (const el of all) {
                    const t = el.textContent || '';
                    const idx = t.indexOf('"captions"');
                    if (idx > -1) {
                        const m = t.match(/"baseUrl":"(https:\\/\\/www\\.youtube\\.com\\/api\\/timedtext[^"]+)"/);
                        if (m) return m[1].replace(/\\\\u0026/g, '&');
                    }
                }
            } catch(e) {}
            return null;
        }""")

        if cap_url:
            cap_page = ctx.new_page()
            cap_page.goto(cap_url, timeout=15000)
            time.sleep(2)
            xml = cap_page.content()
            cap_page.close()
            texts = re.findall(r'<text[^>]*>(.*?)</text>', xml, re.DOTALL)
            if texts:
                transcript = " ".join(html.unescape(t).replace("\n", " ") for t in texts)
                page.close()
                return title, transcript

        page.close()
        return title, None

    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        try:
            page.close()
        except:
            pass
        return None, None

def main():
    parser = argparse.ArgumentParser(description="Pull YouTube transcripts")
    parser.add_argument("--channel", help="YouTube channel URL")
    parser.add_argument("--video", help="Single YouTube video URL")
    parser.add_argument("--count", type=int, default=20, help="Number of videos (default: 20)")
    parser.add_argument("--output", default=None, help="Output directory")
    args = parser.parse_args()

    if not args.channel and not args.video:
        parser.print_help()
        sys.exit(1)

    output_dir = Path(args.output) if args.output else Path.cwd() / "transcripts"
    output_dir.mkdir(parents=True, exist_ok=True)

    pw, browser, ctx = get_browser()

    try:
        if args.video:
            m = re.search(r'v=([a-zA-Z0-9_-]{11})', args.video)
            video_ids = [m.group(1)] if m else []
        else:
            print(f"Fetching video list from {args.channel}...")
            video_ids = get_video_ids(ctx, args.channel, args.count)
            print(f"Found {len(video_ids)} videos")

        success = 0
        failed = []

        for i, vid in enumerate(video_ids):
            print(f"[{i+1}/{len(video_ids)}] {vid}...", end=" ", flush=True)
            title, transcript = get_transcript_via_ui(ctx, vid)

            if transcript and len(transcript) > 100:
                fname = f"{vid}.md"
                with open(output_dir / fname, "w") as f:
                    f.write(f"# {title or vid}\n\n")
                    f.write(f"Video: https://www.youtube.com/watch?v={vid}\n\n")
                    f.write(f"## Transcript\n\n{transcript}\n")
                print(f"OK ({len(transcript)} chars)")
                success += 1
            else:
                print("FAILED (no transcript)")
                failed.append(vid)

        # Generate index
        readme = output_dir / "README.md"
        with open(readme, "w") as f:
            f.write("# Transcripts\n\n")
            for md in sorted(output_dir.glob("*.md")):
                if md.name == "README.md":
                    continue
                first_line = md.read_text().split("\n")[0]
                f.write(f"- **{md.name}**: {first_line}\n")

        print(f"\nDone: {success}/{len(video_ids)} saved to {output_dir}")
        if failed:
            print(f"Failed: {', '.join(failed)}")

    finally:
        ctx.close()
        browser.close()
        pw.stop()

if __name__ == "__main__":
    main()
