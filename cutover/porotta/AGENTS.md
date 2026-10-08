# Porotta — rules for every builder (OmniRush, Antigravity, Codex)

You are working on ONE GitHub issue in your own git worktree. The issue is your whole order.

1. Change only the files the issue lists. Need another file? Stop and say so in your final message.
2. Never touch: `.env`, `prisma/migrations/**` and `prisma/schema.prisma` (unless the issue names them),
   `package.json`/`package-lock.json` (unless named), production servers, Meta/Instagram, email.
3. Write the test first when the issue adds behaviour. Never delete or weaken a test to make it pass.
4. Run the gates before you finish: `npx tsc --noEmit`, `npm run lint`, `npx vitest run <touched paths>`,
   `node scripts/check-empty-tests.mjs`, `npm run build`. Paste the real output in your final message.
5. Commit with clear messages. Do not push, merge, rebase or force anything — `gz` pushes.
6. Write `crypto`, not `node:crypto`, in `src/`. Test events need `createdAt`.
7. Keep files under ~500 lines; a new feature folder gets a short README saying what it does.
8. Unsure about product behaviour? Do not guess — stop and ask in your final message.

Ship-side skills (security, launch, CI/CD, observability, performance, browser testing):
`gaznil/claudecloud/plugins/gaznil-dev-system/skills/<name>/SKILL.md`.
