# 23 November 2026 — 49 Stories, One Day

One image summing up the world news of Monday 23 November 2026: 4 illustrated
feature stories, 12 mini-stories, 33 one-liners, a UTC timeline, a 12-pin world
map, a DATE CHECK box and a sources footer — 49 stories across 7 regions, every
one from 23 November 2026.

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/kamensr/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/kamensr/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

Built for the [make.fun news-image-20261123 bounty](https://make.fun/bounty/news-image-20261123).

## Files

- `entry.png` — the rendered poster (1024×1024 PNG).
- `generate.py` — the Pillow script that draws the poster from the research brief.
- `main.py` — the grader entrypoint: standard-library-only, copies the prebuilt
  `entry.png` into `$MAKEFUN_OUTPUT_DIR` and validates it (1024×1024, ≤1 MiB).

## Reproduce

```sh
python3 generate.py   # renders entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # copies + validates entry.png
```
