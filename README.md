# GPT-6 Astra three.js Creations

**[English](README.md)** | [简体中文](README.zh-CN.md)

> Collected: 2026-09-05 (covering the first two days after the GPT-6 Astra release: Sep 3 – Sep 5, 2026)
> Source: original X (Twitter) posts, each verified via the fxtwitter API (author, date, full text, external links); all hosted demo URLs confirmed live.

GPT-6 Astra was released by OpenAI on September 3, 2026 ([announcement](https://x.com/OpenAI/status/2095595757072191802)). Within 48 hours, numerous three.js demos appeared on X. This repo is a verified roundup of the key posts.

## Creations

| # | Author | Post | Title | Description | Demo |
|---|--------|------|-------|-------------|------|
| 1 | **Ethan Mollick** (@emollick, Wharton professor)<br>Sep 4, 00:42 UTC | [x.com/emollick/status/2095673885605630429](https://x.com/emollick/status/2095673885605630429) | Abyssal Living Deep — procedural ocean world | Started from an open-source single-file ocean storm generator and asked GPT-6 Astra to build out the rest of the ocean, including procedural simulations of deep-sea animal behavior; supports switching biomes (reef etc.), lighting, and seeds. 676 likes / 71.6K views | [abyssal-living-deep.netlify.app](https://abyssal-living-deep.netlify.app/?site=reef&seed=713&light=day&surface=1)<br>Source: [github.com/emollick/abyssal-living-deep](https://github.com/emollick/abyssal-living-deep) |
| 2 | **Peter Gostev** (@petergostev, AI Capability Lead at Arena.ai)<br>Sep 4, 07:31 UTC | [x.com/petergostev/status/2095776685807346105](https://x.com/petergostev/status/2095776685807346105) | Van Gogh Town | GPT-6-Astra (Max) blended 6 Van Gogh paintings (The Starry Night, Bedroom in Arles, Café Terrace at Night, etc.) into a single walkable first-person three.js town with ~3,295 editable objects; hosted by the author for everyone to try. 1,474 likes / 108.5K views | [van-goghs-town.surge.sh](https://van-goghs-town.surge.sh/) |
| 3 | **leo 🐾** (@synthwavedd)<br>Sep 4, 11:44 UTC | [x.com/synthwavedd/status/2095840435319001278](https://x.com/synthwavedd/status/2095840435319001278) | Naval war scene in a single turn | GPT-6 Astra (max) generated a Three.js war scene in a single turn (no examples, basic prompt only): detailed ship models and objects interacting with the water; ~50K tokens, done in about 12 minutes. 741 likes / 39.1K views | No public URL (video demo only in the post) |

## Related Roundup Posts (index)

| Author | Link | Notes |
|--------|------|-------|
| TechHalla (@techhalla) · Sep 4 | [x.com/techhalla/status/2095778682648334421](https://x.com/techhalla/status/2095778682648334421) | "12 hours since GPT-6 Astra dropped — 8 wild examples" thread, includes the Van Gogh three.js town (3,295 editable objects) among others |

## Excluded Borderline Cases (to avoid confusion)

| Case | Reason for exclusion |
|------|----------------------|
| [Tom Krcha's house 3D reconstruction](https://x.com/tomkrcha/status/2095598645190291775) (Sep 3), [steam train with 3,295 objects](https://x.com/tomkrcha/status/2095756085890310311) (Sep 4) | High engagement, but built in **Blender** (runs locally at 60fps) — not three.js; often conflated with Gostev's Van Gogh town in roundup articles |
| [Matthew Berman's Fall Guys clone](https://x.com/MatthewBerman/status/2095595895584907501) (Sep 3) | Video demo; three.js not stated, no playable link |
| [TimJayas' 3D spaceship](https://x.com/TimJayas/status/2093702026601566272) | Posted Aug 29 (pre-release leak) — outside the two-day window |
| CtrlAltDwayne's GTA 6 bayou airboat game | Posted Aug 28 and not Astra-related |
| Mikko Ohtamaa's racecar / 3D reconstruction demos | Built with the previous-gen GPT-5.6 Sol, not Astra |

## Methodology

- X search requires login (login wall), so candidates were discovered via multiple web searches and each post was then verified against its original text through the fxtwitter API.
- Authors, dates, content, and engagement stats are taken from the posts themselves (fxtwitter API responses), not second-hand retellings.
- `van-goghs-town.surge.sh`, `abyssal-living-deep.netlify.app`, and the GitHub source repo were all confirmed to return HTTP 200 on 2026-09-05.
