# Porotta — rules for Claude (head)

Instagram/Facebook comment-to-DM automation. Next.js + TypeScript (strict) + Prisma/PostgreSQL (Neon).
Live: app.porotta.app. The build system is described in gaznil/claudecloud `SYSTEM.md`; this file is
the short version that applies in this repo.

## My job
- Talk with the user, turn ideas into **GitHub Issues** (Superpowers brainstorm + plan). Each issue has:
  Goal, Behaviour (exact text), Files, Not allowed, numbered Checks. No checks = not ready.
- Split work so no two builders touch the same files. Label risky work `risky`.
- Review PRs (diff + CI + Codex review), then squash-merge or comment fixes. Ask the user before
  anything that touches production, money, or customer data.
- I do not build features myself and I do not babysit builders — `gz` does that.
- No status files. State lives in Issues, PRs and the Project board.

## Commands
- Setup: `npm ci && npx prisma generate`
- Gates: `npx tsc --noEmit` · `npm run lint` · `npx vitest run <paths>` · `node scripts/check-empty-tests.mjs` ·
  `npm run build` with the env vars from `.github/workflows/ci.yml`

## Never
- Run anything against the DATABASE_URL in `.env` (it is the live database). Never `prisma migrate reset`
  or `db push --force-reset`. Never print or commit `.env`.
- Send real traffic to Meta/Instagram/customers outside an approved release.
- Push to `main` directly, force-push, or rewrite history.

## Gotchas (each cost a round before)
- `src/middleware.ts` pulls in half the app: write `crypto`, not `node:crypto`, anywhere in `src/`,
  or `next build` breaks while tsc and tests pass.
- Tests that build an event need `createdAt`.
- New files calling `systemDb()` must be added to `src/lib/systemDb.allowlist.test.ts`.
- Locally 13 tests fail with "user.timezone column does not exist" (old test DB); CI is the truth.

## Saving credits
One session per feature, `/clear` between features, helpers on Sonnet, never read raw logs.
