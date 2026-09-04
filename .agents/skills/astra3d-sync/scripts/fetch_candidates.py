#!/usr/bin/env python3
"""Fetch and rank candidate posts for the GPT-6 Astra 3D gallery.

Single-run replacement for ad-hoc curl loops: multi-query advanced search via
twitterapi.io with pagination and rate-limit backoff, dedup, original-post and
3D-keyword filtering, existing-entry exclusion, engagement ranking.

Time window defaults to "last sync -> now": meta.lastSyncAt from
data/creations.json, falling back to the newest entry's postedAt, then to
--hours before now. After a successful deploy, run with --mark-synced to
record the window end as the next run's start (prevents both gaps and
re-scans).

Usage:
    python3 fetch_candidates.py                       # auto window
    python3 fetch_candidates.py --hours 6             # force a window
    python3 fetch_candidates.py --since 2026-09-04T22:49:00Z
    python3 fetch_candidates.py --mark-synced         # after deploy

Key comes from $TWITTERAPI_KEY or <repo>/.env.local. Writes ranked candidates
to --out and prints a compact table. Exit code 0 even with zero candidates
(empty windows are normal); non-zero only on auth/network failure.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.twitterapi.io/twitter/tweet/advanced_search"

QUERIES = [
    '"GPT-6 Astra" 3D',
    '"GPT-6 Astra" three.js',
    '"GPT-6 Astra" Blender',
    '"GPT-6 Astra" Unreal',
    '"GPT-6 Astra" WebGL',
    '"GPT-6 Astra" Minecraft',
    '"GPT-6 Astra" game',
    '"GPT-6 Astra" world',
    '"GPT-6 Astra" model',
]

KEYWORDS = [
    "3d", "three.js", "threejs", "blender", "unreal", "webgl", "minecraft",
    "voxel", "mesh", "polygon", "low-poly", "low poly", "godot", "engine",
    "model", "３d", "3-d",
]

TIME_FMT = "%a %b %d %H:%M:%S %z %Y"


def load_key(repo):
    key = os.environ.get("TWITTERAPI_KEY", "").strip()
    if key:
        return key
    env_path = os.path.join(repo, ".env.local")
    if os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            line = line.strip()
            if line.startswith("TWITTERAPI_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("ERROR: TWITTERAPI_KEY not set and .env.local has no TWITTERAPI_KEY")


def load_data(repo):
    path = os.path.join(repo, "data", "creations.json")
    if not os.path.exists(path):
        sys.exit(f"ERROR: {path} not found — run from the gpt6-astra-3d repo")
    return path, json.load(open(path, encoding="utf-8"))


def parse_iso(s):
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        try:
            return dt.datetime.fromtimestamp(int(s), dt.timezone.utc)
        except (TypeError, ValueError):
            return None


def api_search(key, query, cursor="", retries=3):
    params = {"query": query, "queryType": "Latest"}
    if cursor:
        params["cursor"] = cursor
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, headers={"X-API-Key": key})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries:
                time.sleep(5 * attempt)
                continue
            if e.code == 401:
                sys.exit("ERROR: twitterapi.io returned 401 — key expired/revoked")
            raise
    return {}


def parse_time(s):
    try:
        return dt.datetime.strptime(s, TIME_FMT).astimezone(dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def resolve_start(args, data, end):
    """Window start priority: --since > meta.lastSyncAt > newest postedAt > now-hours."""
    if args.since:
        t = parse_iso(args.since)
        if not t:
            sys.exit(f"ERROR: bad --since value {args.since!r}")
        return t, "--since"
    meta = data.get("meta", {})
    t = parse_iso(meta.get("lastSyncAt"))
    if t:
        return t, "meta.lastSyncAt"
    posts = [parse_iso(c.get("postedAt")) for c in data.get("creations", [])]
    posts = [p for p in posts if p]
    if posts:
        return max(posts), "newest postedAt (set meta.lastSyncAt via --mark-synced)"
    return end - dt.timedelta(hours=args.hours), f"--hours fallback ({args.hours}h)"


def mark_synced(args, repo, data_path, data):
    """Set meta.lastSyncAt to the recorded window end (or an explicit ISO)."""
    val = None
    if args.mark_synced and args.mark_synced != "auto":
        if not parse_iso(args.mark_synced):
            sys.exit(f"ERROR: bad --mark-synced value {args.mark_synced!r}")
        val = args.mark_synced
    elif os.path.exists(args.out):
        val = json.load(open(args.out, encoding="utf-8")).get("windowEnd")
    if not val:
        sys.exit("ERROR: no window end on record — pass an ISO value to --mark-synced")
    data.setdefault("meta", {})["lastSyncAt"] = val
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"meta.lastSyncAt = {val}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=25,
                    help="fallback window length when no sync marker exists")
    ap.add_argument("--since", default=None,
                    help="explicit window start: ISO 8601 or unix epoch")
    ap.add_argument("--min-likes", type=int, default=15)
    ap.add_argument("--max-pages", type=int, default=4)
    ap.add_argument("--repo", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
    ap.add_argument("--out", default="/tmp/astra3d-candidates.json")
    ap.add_argument("--mark-synced", nargs="?", const="auto", default=None,
                    metavar="ISO",
                    help="set meta.lastSyncAt (from --out or the given ISO) and exit")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    data_path, data = load_data(repo)

    if args.mark_synced is not None:
        mark_synced(args, repo, data_path, data)
        return

    key = load_key(repo)
    end = dt.datetime.now(dt.timezone.utc)
    start, src = resolve_start(args, data, end)
    if start >= end:
        sys.exit(f"ERROR: window start {start} is not before now — bad lastSyncAt?")
    print(f"window: {start:%Y-%m-%d %H:%M} .. {end:%Y-%m-%d %H:%M} UTC "
          f"(from {src}), min likes {args.min_likes}")

    existing = {c.get("url", "").rstrip("/").split("/")[-1]
                for c in data.get("creations", [])}

    tweets, fetched = {}, 0
    qbase = "since_time:{0} until_time:{1} -is_retweet".format(
        int(start.timestamp()), int(end.timestamp()))
    for q in QUERIES:
        qfull = f"{q} {qbase}"
        cursor, pages = "", 0
        while pages < args.max_pages:
            d = api_search(key, qfull, cursor)
            got = d.get("tweets") or []
            fetched += len(got)
            for t in got:
                tweets[t["id"]] = t
            cursor = d.get("next_cursor") or ""
            pages += 1
            if not d.get("has_next_page") or not cursor:
                break
            time.sleep(1.0)  # stay under the per-minute rate limit
        time.sleep(1.0)

    rows = []
    for t in tweets.values():
        if t.get("isRetweet") or t.get("isReply"):
            continue
        if t["id"] in existing:
            continue
        ct = parse_time(t.get("createdAt"))
        if not ct or not (start <= ct <= end + dt.timedelta(minutes=5)):
            continue
        likes = t.get("likeCount") or 0
        if likes < args.min_likes:
            continue
        text = re.sub(r"\s+", " ", t.get("text", ""))
        if not any(k in text.lower() for k in KEYWORDS):
            continue
        rows.append({
            "id": t["id"],
            "url": f"https://x.com/{t['author']['userName']}/status/{t['id']}",
            "author": t["author"]["userName"],
            "likes": likes,
            "views": t.get("viewCount") or 0,
            "retweets": t.get("retweetCount") or 0,
            "createdAt": ct.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "text": text,
        })
    rows.sort(key=lambda r: (-r["likes"], -r["views"]))

    window_end = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump({"windowStart": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
               "windowEnd": window_end,
               "count": len(rows),
               "candidates": rows},
              open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"fetched {fetched}, unique {len(tweets)}, "
          f"candidates after filter {len(rows)} -> {args.out}")
    print(f"after deploying, run with --mark-synced to record "
          f"lastSyncAt={window_end}\n")
    for r in rows[:40]:
        print(f"\u2764{r['likes']:>6} \U0001f441{r['views']:>9} "
              f"@{r['author']:<16} {r['createdAt'][:16].replace('T', ' ')}")
        print(f"  {r['url']}")
        print(f"  {r['text'][:200]}")


if __name__ == "__main__":
    main()
