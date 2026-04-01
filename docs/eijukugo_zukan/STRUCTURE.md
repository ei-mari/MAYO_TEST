# eijukugo_zukan Structure

## Main folders

- `MAYO/audio/eijukugo_zukan/`
  - `U01`, `U02`: sentence audio by unit
- `MAYO/images/eijukugo_zukan/`
  - `U01`, `U02`, `U03`: quiz images by unit
- `MAYO/data/eijukugo_zukan/`
  - `units/U01/dataset.csv`
  - `units/U02/dataset.csv`
  - `units/U03/README.md` (`U03` は画像のみ先行追加)
- `MAYO/apps/eijukugo_zukan/quiz_preview/`
  - local preview app
- `MAYO/apps/eijukugo_zukan/cloudflare_quiz/`
  - Cloudflare Workers deployment app
  - `public/audio`, `public/images`, `public/data`: deployment copies for public hosting
- `MAYO/scripts/eijukugo_zukan/`
  - dataset/image helper scripts
- `MAYO/docs/eijukugo_zukan/`
  - notes and structure docs
- `MAYO/archive/eijukugo_zukan/`
  - raw source files and older generated materials kept for reference

## Naming rule

- images: `Q01.png` to `Q12.png`
- audio: `S01.mp3` to `S12.mp3`
- datasets point to `/images/eijukugo_zukan/...` and `/audio/eijukugo_zukan/...`

## Current active paths

- local preview datasets:
  - `MAYO/data/eijukugo_zukan/units/U01/dataset.csv`
  - `MAYO/data/eijukugo_zukan/units/U02/dataset.csv`
- local preview assets:
  - `MAYO/images/eijukugo_zukan/U01`, `MAYO/images/eijukugo_zukan/U02`, `MAYO/images/eijukugo_zukan/U03`
  - `MAYO/audio/eijukugo_zukan/U01`, `MAYO/audio/eijukugo_zukan/U02`

## Archived paths

- `MAYO/archive/eijukugo_zukan/raw/`: original csv/json/cover/question images
- `MAYO/apps/eijukugo_zukan/cloudflare_quiz/archive/legacy_public/`: previous public folder layout kept as backup
