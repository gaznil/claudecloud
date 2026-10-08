# Multi-project workspace without branch collisions

**Date:** 5 Sep 2026
**Problem:** `c:\Gaznil.code.workspace` is a single checkout, so it can only be on one
branch at a time. A session working phloem blocks a session working the iron site.

## Decision

Keep **one repo** (as `context\machine.md` already requires). Add **git worktrees**:
one permanent folder per project, all backed by the same repo and history.

- `C:\Gaznil.code.workspace` — **home**. Holds `main` permanently. No project work here.
- `C:\Gaznil.<project>` — one per project, permanently on `work/<project>`.

Rejected: a separate repo per project. It would multiply backups, scripts and drift
checks for a solo operator, and `machine.md` already rules it out.

## Measured facts (verified 5 Sep 2026)

- Tracked files: 408 MB per worktree. Free disk: 15 GB. ~35 worktrees fit.
- Project folders are disjoint at the top level (`iron/`, `phloemlearning.com/`,
  `instagram-automation/`, `ainaura-seo/`, `vortexen/`, `3d/`), so cross-project
  merge conflicts are structurally impossible.
- Per-project `PLAN.md` / `HANDOFF.md` already exist for iron, instagram, ainaura, 3d.
  Only the root `PLAN.md` is shared and stale.
- `done.ps1` and `task.ps1` both run `git checkout main`. Git refuses this when `main`
  is checked out in another worktree, so **both break** the moment worktrees exist.
  They must be rewritten as part of this change, not after.
- `backup.ps1` pushes `git rev-parse --abbrev-ref HEAD`, which is per-worktree. Correct as-is.

## Residual collision risks and their mitigations

| Risk | Mitigation |
|---|---|
| `git stash` is repo-global, not per-worktree — a stash made in one folder is visible in all | Rule: never stash, always commit. Scripts commit rather than stash. |
| Two folders both edit root files (`CLAUDE.md`, `AGENTS.md`, `*.ps1`) | Rule: root files are edited only from home. |
| Two sessions run `done.ps1` at once → `index.lock` in home | Git fails safely; `done.ps1` reports it in plain language and changes nothing. |
| A branch cannot be deleted while checked out in a worktree | `done.ps1` re-points the folder onto a fresh branch off `main` after merging, instead of deleting. |
| Session asked for a project that is not its folder | `branch-check.ps1` names the folder's project; rule says stop and say so. |
| Stale root `PLAN.md` picked up by the wrong project | Retire it; per-project `PLAN.md` becomes mandatory. |

## Commands after this change

- `open.ps1 <project>` — **new.** Create or reopen a folder for any project, existing or future.
- `task.ps1 <name>` — starts a task inside the current project folder; never switches branch.
- `done.ps1` — merges into `main` without moving anything, then resets the folder onto a
  fresh branch so it is ready for the next job.
- `backup.ps1` — unchanged.

## Safety constraint

Work in progress must not break. Phase 1 is **additive only**: new folders, new/rewritten
scripts. Nothing existing is moved, deleted or switched, and the uncommitted
`iron/site/src/components/Peephole.tsx` edit in home is left exactly as it is.
Phloem moves out of home last, only on explicit approval.
