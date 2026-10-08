# Gaznil build system — Claude heads, GitHub runs, a script dispatches

Goal: idea → shipped in a day, with every change proven before it reaches users, while spending
the cheapest tokens first and keeping the PC's disk free.

## The one idea

The manager's routine job — start builders, watch logs, run checks, retry, open the review — is
done by a **script** (free, never forgets, never runs out of credits). The AIs only do the thinking.
**GitHub holds all shared state**, so there are no TASK / REPORT / SESSION / HEAD / NEXT / PROGRESS
files to keep in sync.

| Old (Oct 2026) | New |
|---|---|
| TASK.md / CODEX-TASK.md / NEXT.md / tasks/*.md | **GitHub Issue** (spec + file list + checks) |
| REPORT.md / CODEX-REPORT.md / PROGRESS.md | **Pull request** (diff + gate output pasted by the script) |
| HEAD.md loop, watchers, .cmd launchers, "builder go" | **`gz` script** in WSL |
| Head re-runs tsc/lint/build after cherry-pick | **Same gates in the script and in GitHub CI** |
| SESSION.md credit board / status card | **GitHub Project board** (open on the phone) |
| `USER YES: <date>` lines, deploy.ps1 by hand | **Merge to main → deploy job**; risky migrations wait for your tap in a GitHub "production" environment |
| Clones with `origin` removed, work only on C: | **Worktrees of one WSL clone, every branch pushed** |
| ROADMAP NEXT UP lanes | Issues labelled `ready`, ordered on the board |

## Roles and which tokens they burn

| Who | Does | Model rule |
|---|---|---|
| **Claude (head)** | Talks with you, writes specs as Issues (Superpowers brainstorm + plan), splits work into independent issues with file lists, makes product decisions, final PR verdict + merge | Opus for specs and decisions only. Subagents on Sonnet/Haiku. One session per feature, then `/clear`. Never reads raw logs |
| **`gz` script** | Queue, worktrees, starting builders, gates, retries, escalation, push, PR, labels, cleanup | Free |
| **OmniRush Sol** | Default builder for every issue; fixes its own gate failures | `--model gpt-6.1-sol --thinking low` |
| **OmniRush Astra** | Escalation after 2 failed tries, or issues labelled `risky` (auth, webhooks, money, migrations) | `--thinking medium`, never unset, never max |
| **Codex** | Automatic first review of every PR (comment on the PR). This month also: one-time infrastructure jobs (below) | Luna low for reviews; Sol low for `risky` PRs. Never Astra, never xhigh |
| **Antigravity CLI** | A second builder pool with its own Google quota, started by `gz` headless (`agy -p "…" --effort low --dangerously-skip-permissions --print-timeout 60m`, run inside the worktree). Best for screens/UI issues; OmniRush keeps engine issues. The Antigravity IDE stays the window where you watch the app | `--effort low` default, `medium` on retry |
| **GitHub Actions** | CI on every PR, deploy on merge, production smoke test after deploy | Free tier |

## The flow of one feature

```
You + Claude: "I want X"  →  Superpowers brainstorm (questions)  →  plan
Claude: gh issue create … (one issue per independent slice, label "ready")
gz loop  (in WSL; up to 4 builders at once — 3 OmniRush + 1 Antigravity — never two on the same files)
  ├─ worktree ~/work/<repo>/wt/<issue> from origin/main, branch issue-<n>
  ├─ omnirush -p "<issue body + AGENTS.md rules>" --model gpt-6.1-sol --thinking low
  ├─ gates: typecheck · lint · tests for touched paths · empty-test guard · CI-env build
  │     fail → feed the errors back (2 tries) → Astra medium (1 try) → label "needs-human", move on
  ├─ git push; gh pr create (body = issue link + gate output + model used + token cost)
  └─ remove the worktree (saves disk)
GitHub CI runs the same gates  ·  Codex posts its review on the PR
Claude: reads PR + CI + Codex review → approve and squash-merge, or comment the fixes
  (a comment with label "fix" sends the PR back through gz on the same branch)
Merge to main → deploy workflow → health check + Playwright smoke on production → Sentry watching
```

## Spec format (every issue)

```
## Goal            2-4 plain lines
## Behaviour       exact screen text / API result, word for word
## Files           paths the builder may change (gz refuses a diff outside them)
## Not allowed     schema/migrations/package.json unless named; secrets; production
## Checks          numbered, each a command + the result that must come back
```
If Claude cannot write the checks, the issue is not ready.

## Gates (identical in `gz` and in CI)

1. `npx tsc --noEmit` → 0 errors
2. `npm run lint` → 0
3. `npx vitest run <touched paths>` → pass (full suite in CI)
4. `node scripts/check-empty-tests.mjs` → 0
5. `npm run build` with the CI env vars → success (catches the `node:` import trap)
6. Diff stays inside the issue's file list
7. Line endings: solved once by `.gitattributes` (`* text=auto eol=lf`), no per-task check

## Safety (replaces the NEVER BREAK card)

- Builders never get secrets; worktrees have no `.env`. Secrets live only in GitHub Actions secrets.
- `main` is protected: no direct push, CI must be green, squash merge only.
- Deploy job runs only from `main`. A migration that is not purely additive pauses the job in the
  `production` environment until you approve it in GitHub (phone notification).
- Tests never touch the live database (CI uses its own Postgres service).
- Nothing is sent to Meta, Instagram or customers from a builder run.

## Disk and storage

- One clone per product inside WSL (`~/work/<repo>`), not on `/mnt/c` — faster builds, no CRLF,
  no path mangling. Builders use `git worktree` (shared history), removed after each PR.
- Max 4 live worktrees. `npm ci` reuses the shared npm cache.
- With only C:, free space once and keep it free: push and then delete the old `C:\Gaznil.astra*`
  clones and their node_modules; delete `.next/` build folders; `npm cache verify`; clear old Claude
  transcripts (`%USERPROFILE%\.claude\projects`, ~600 MB); then shrink the WSL disk
  (`wsl --shutdown`, then `Optimize-VHD` or diskpart `compact vdisk` on its `ext4.vhdx`) —
  WSL's disk never gives space back to C: on its own.
- Keep screenshots, videos, zips and evidence out of git (`.gitignore`); attach them to the PR instead.

## Saving Claude credits

- CLAUDE.md under 60 lines: commands, gates, gotchas. History goes in git, not in rules.
- One session per feature; `/clear` between features; specs carry the context, not the chat.
- Claude never polls builders — `gz` and GitHub do. Claude is woken by "review" or a PR link.
- `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` so helper agents never run on Opus.

## A day, start to ship

| Time | Who | What |
|---|---|---|
| 1 h | You + Claude | Brainstorm, plan, 3-6 independent issues labelled `ready` |
| 4-6 h | gz + OmniRush | Builds in parallel; PRs appear with green gates |
| rolling | Codex + Claude | Review each PR as it lands; merge; auto-deploy |
| 30 min | Claude + Playwright | End-to-end smoke on production; fix-issues for anything found |

## Setting it up (order matters)

0. Free disk on C:; push every local-only builder commit to a GitHub branch.
1. **Codex, this month (luna/sol low):** `.gitattributes`; branch protection; PR template; deploy
   workflow on merge with the `production` environment; Playwright smoke suite for the main user
   flows; the `gz` script (+ its tests); the Codex PR-review step.
2. **Claude:** review those PRs; write the lean CLAUDE.md and one AGENTS.md read by every agent;
   archive the old relay files; turn the open roadmap items into Issues.
3. Run one small real feature through the whole flow before trusting it with a day of work.

Recommended: give each product its own repository (`git subtree split` keeps its history), so its
Issues, PRs, Actions and clone size belong to that product alone.
