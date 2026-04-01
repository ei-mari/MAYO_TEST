# Cloudflare Quiz Deployment

This app deploys the quiz to Cloudflare Workers, stores compose-mode submissions in D1, and optionally posts each submission to Slack.

## Files

- `public/`: static quiz app and assets
- `src/worker.js`: Worker routes for static assets and `/api/submissions`
- `schema.sql`: D1 schema
- `wrangler.jsonc`: Worker config

## Setup

1. Install dependencies

```bash
npm install
```

2. Log in to Cloudflare

```bash
npx wrangler login
```

3. Create a D1 database

```bash
npx wrangler d1 create eijukugo-zukan-db
```

4. Copy the returned `database_id` into `wrangler.jsonc`

5. Apply the schema

```bash
npx wrangler d1 execute eijukugo-zukan-db --remote --file=schema.sql
```

6. Add the Slack webhook secret

```bash
npx wrangler secret put SLACK_WEBHOOK_URL
```

7. Run locally

```bash
npm run dev
```

8. Deploy

```bash
npm run deploy
```

## Submission payload

Compose-mode submissions send:

- learner ID
- unit
- question number
- mode
- Japanese prompt
- correct English answer
- learner answer
- IPA
- image/audio source path
- client timestamp

## Notes

- `提出する` is shown only in compose mode.
- `回答` shows the answer without storing anything.
- `提出する` stores the entry in D1 and posts a Slack notification if `SLACK_WEBHOOK_URL` is configured.
- The current local Python preview is unchanged. This Cloudflare app is a separate deployment target.
