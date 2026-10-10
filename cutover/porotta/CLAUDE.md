# Porotta — rules for Claude (head)

Instagram/Facebook comment-to-DM automation. Next.js + TypeScript (strict) + Prisma/PostgreSQL (Neon).
Live: app.porotta.app. Repo: gaznil/porotta. System design: gaznil/claudecloud `SYSTEM.md`.
The user's global rules (Rule Zero, reply style, never guess, credits) still apply on top of this file.

## The user's words
- **"discuss" / "discuss automation"** — unchanged: talk it through; ideas go to `DISCUSSION.md` inbox;
  a real decision becomes a **task** (GitHub issue, label Task/Bug/Feature) with Goal, Behaviour,
  Files, Not allowed, numbered Checks — and a line in `DISCUSSION.md` LATEST. Commit as you go.
- **"builder go"** — look at the board, make sure `gz` is running and builders are busy, start it if
  not, report a 4-line card (Done / Live / Waiting / Working). Never babysit or poll.
- **"review"** — look only at PRs labelled `risky` or `needs-human`; approve or comment fixes.
- **"handoff"** — the board and issues hold the state: commit any open notes, print one resume line.

## How work flows
Task (issue) → `gz` gives it to a builder (OmniRush Sol default) → automatic checks → Codex review →
PR. **Safe PRs auto-merge and auto-deploy** when checks are green. `risky` PRs (auth, payments,
webhooks, migrations) wait for my look; a migration that deletes or rewrites data waits for the
user's yes. After every deploy the live smoke test runs; failure rolls back by itself.

## Commands
- Setup: `npm ci && npx prisma generate`
- Gates: `npx tsc --noEmit` · `npm run lint` · `npx vitest run <paths>` · `node scripts/check-empty-tests.mjs` ·
  `npm run build` with the env vars from `.github/workflows/ci.yml`

## Never
- Run anything against the DATABASE_URL in `.env` (live database). Never `prisma migrate reset`
  or `db push --force-reset`. Never print or commit `.env`.
- Send real traffic to Meta/Instagram/customers outside an approved release.
- Push to `main` directly, force-push, or rewrite history. Write feature code myself (builders do it).

## Gotchas
- Write `crypto`, not `node:crypto`, in `src/` (middleware pulls in half the app; `next build` breaks).
- Test events need `createdAt`. New `systemDb()` callers go in `src/lib/systemDb.allowlist.test.ts`.
- Locally 13 tests fail with "user.timezone column does not exist" (old test DB); CI is the truth.
- Until the deploy workflow exists, deploys still run `scripts/deploy.ps1` from `C:\Gaznil.porotta`;
  it reads `CODEX-TASK.md` and appends to `CODEX-REPORT.md` — do not move those two files yet.

## Credits
No polling. Short chats. Discuss on Sonnet. Helpers on Sonnet low. Never read raw logs.
