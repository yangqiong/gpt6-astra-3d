---
name: astra3d-sync
description: >-
  Collect, curate and publish new GPT-6 Astra 3D creations for the gpt6-astra-3d
  gallery site. Use whenever the user asks to 采集/抓取/更新/发布 the Astra 3D 画廊
  (collect recent posts from X, update creations.json, redeploy the site), or asks
  for a scheduled sync run — even short phrases like "采集一下" "更新画廊" "同步最近作品"
  or "astra sync" in the gpt6-astra-3d repo. Covers the full pipeline: twitterapi.io
  search → filter original 3D posts → bilingual entries → README sync → git push deploy.
---

# Astra 3D Gallery Sync

Pipeline: **fetch → curate → write → sync → push-deploy**. Repo root is the
gpt6-astra-3d checkout (skill lives at `<repo>/.agents/skills/astra3d-sync/`).
Site deploys automatically on `git push` to `main` via GitHub Actions — never
deploy with wrangler manually unless Actions is broken.

## Preconditions (verify, then stop reporting them)

1. `data/creations.json` loads and `npm run sync:readme` exists (repo intact).
2. `.env.local` contains `TWITTERAPI_KEY`. If missing, ask the user — do not
   search the disk for keys. Never print the key value or commit `.env.local`.

## Step 1 — Fetch candidates (one command, ~1 min)

```bash
python3 .agents/skills/astra3d-sync/scripts/fetch_candidates.py
```

Time window is **last sync → now** automatically: it reads `meta.lastSyncAt`
from `data/creations.json`, falls back to the newest entry's `postedAt`, then
to `--hours N` (default 25) if neither exists. Overrides: `--since <ISO|epoch>`
to force a start, `--hours N` as fallback length only.

Output: `/tmp/astra3d-candidates.json` (contains `windowStart`/`windowEnd` +
ranked candidates, already deduped, original-only, 3D-keyword-filtered,
existing entries excluded, sorted by likes) plus a ranked list on stdout.
Other options: `--min-likes K` (default 15; lower to 0 when hunting niche
works with playable demos).

The script handles pagination, rate-limit backoff and the timestamp-based
`since_time`/`until_time` operators (twitterapi.io rejects `since:` date
strings). Do not re-implement this with curl loops.

## Step 2 — Curate (judgment step, this is the skill's value)

Read the ranked candidates and keep posts that are ALL of:

- An **original creation** made with GPT-6 Astra by the poster: 3D scene,
  model (Blender etc.), browser 3D (three.js/WebGL), game/world, or 3D video.
- 3D-related (the script's keyword filter is a net — discard 2D-only apps,
  pure text tools, agent demos with no 3D output).
- Not already covered: different status id than existing entries. Multiple
  entries per author are fine when the works are distinct.

Reject, even at high engagement:

- **News/repost accounts** restating someone else's work (many languages:
  FR/ES/JA/AR/FA accounts reposting the Manhattan or survival-world tweets).
- **Vendor/official announcements** (OpenAI, Databricks, Abacus, Higgsfield,
  benchmark indexes, "now available" posts).
- **Pure commentary**: price/performance threads, "is it AGI" takes, model
  comparisons with no build of the author's own.
- Author's own A/B comparison **builds** are fine (e.g. "Max vs Medium, both
  are my builds").

Default bar ❤ ≥ 15; keep sub-bar posts only when they ship a playable link.
Non-English posts are fine — write the bilingual entry from their content.

## Step 3 — Write entries (bilingual, exact schema)

Append to `data/creations.json` with `id` = max existing id + 1. Snapshot
engagement at fetch time; never update stats of existing entries (the table
is a "collected at" snapshot, and sorting derives from it).

Category must be one of `categoryOrder`: `world` (games / explorable worlds),
`web3d` (three.js / WebGL browser demos), `modeling` (Blender / 3D assets),
`video` (3D-generated video). Tech label uses "(not stated)"/"（未注明）"
when the post doesn't name a tool. Literal example of one entry:

```json
{
  "id": 23,
  "author": "yasei_no_otoko",
  "url": "https://x.com/yasei_no_otoko/status/2095975195312029889",
  "likes": 468,
  "views": 51771,
  "postedAt": "2026-09-04T20:40:00Z",
  "category": "web3d",
  "tech": { "en": "WebGL", "zh": "WebGL" },
  "demos": [],
  "title": { "en": "Panzer Dragoon Episode 1 in 24 minutes", "zh": "24 分钟做出《铁甲飞龙》第一关" },
  "description": {
    "en": "Half-jokingly asked Astra Pro to build Episode 1 of Panzer Dragoon in WebGL — 24 minutes later the on-rails dragon shooter came out",
    "zh": "半开玩笑地让 Astra Pro 用 WebGL 做一道《铁甲飞龙》第一关——24 分钟后就输出了这个轨道射击游戏"
  }
}
```

Style: title = concrete artifact + the wow fact; description = 1–2 sentences,
keep the poster's numbers (minutes, object counts, quota %) — they are the
interesting part. `demos` entries: `{"kind": "play"|"source", "url": ...}`
only when the post/thread links one.

Update `meta.collectedAt` to today only when the README header prose also
still makes sense; leave `coverage` prose alone unless the window grew a lot.

## Step 4 — Sync and verify locally

```bash
npm run sync:readme && npm run build
```

Sanity-check the regenerated README tables contain the new rows (both
languages) and the build prints no errors.

## Step 5 — Commit, push, confirm deployment

```bash
git add data/creations.json README.md README.zh-CN.md
git commit -m "docs: add N creations via twitterapi.io search"
python3 .agents/skills/astra3d-sync/scripts/fetch_candidates.py --mark-synced
git add data/creations.json && git commit -m "chore: mark lastSyncAt"
git push
gh run watch $(gh run list --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status
curl -s -o /dev/null -w "%{http_code}\n" https://gpt6-astra-3d.pages.dev/
```

`--mark-synced` writes this run's `windowEnd` into `meta.lastSyncAt` — run it
only after the curated entries are committed, so a crashed run never skips
its window (its output file `/tmp/astra3d-candidates.json` holds `windowEnd`;
pass an explicit ISO if that file is gone). The Action takes ~40 s. If it
fails, read `gh run view --log-failed` before retrying; a 401 in the deploy
step means the `CLOUDFLARE_API_TOKEN` secret rotated — tell the user, don't
guess tokens.

Report at the end: how many candidates the script found, how many you kept,
one-line reasons for the notable rejections, and the deployed URL.

## Failure modes

- **HTTP 401 from twitterapi.io**: key expired/revoked → ask user for a new
  `TWITTERAPI_KEY` (also update `.env.local`).
- **Zero results for every query**: almost always a bad time window (script
  prints it) or rate-limit exhaustion; retry after 60 s before concluding.
- **`isReply` filtering**: the script drops replies; a great work posted as a
  reply-in-thread is rare — if the user points one out, fetch it by id via
  the twitterapi.io tweet detail endpoint.

## Scheduled runs

When invoked by a scheduler or with no explicit window, the script already
scopes to "since last sync" — run the whole pipeline autonomously with
defaults (min-likes 15), including commit + push + --mark-synced. If nothing
qualifies, still run `--mark-synced` and push the marker (cheap, keeps the
next window tight) — or report "no new qualifying posts" and skip pushing if
you prefer zero-noise history; both are acceptable, state which you did.
