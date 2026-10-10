# Porotta cutover — from Gaznil-workspace to gaznil/porotta

Trigger: **"do the Porotta cutover"**. Claude runs every step itself on the user's PC, checks each
result, and stops and reports in one line if a check fails. The live app is never touched.
Phase A switches the home (one session). Phase B builds the self-running parts as tasks.

## PHASE A — move house (today)

**A1. Save everything that is only on this PC.**
1. Nothing else is working: no OmniRush (`wsl.exe -e pgrep -af omnirush` empty), no codex exec job,
   and the Codex "head" chat in VS Code is told to stop (mark `HEAD.md` "ENDED <date>: replaced by the
   new system"). Ask the user to close every other Claude/Codex/Antigravity chat until Phase A is done.
2. In `C:\Gaznil.instagram`: commit the modified/untracked project files (CODEX-REPORT.md, CODEX-TASK.md,
   REPORT.md, ROADMAP.md, evidence/*, archive/reports/REPORT-H15.md, the staged FQ-127 audit doc).
3. Astra clones: review or keep their unfinished work — in `C:\Gaznil.astra2` the untracked docs
   (FQ-127 x2, FQ-132, FQ-139) and the three QuickAutomation test files; in `C:\Gaznil.astra3`
   docs/FQ-140-RESEARCH.md; in `C:\Gaznil.astra` `.b1-checks/`. Commit them on each clone's branch,
   then fetch each clone's branch into `C:\Gaznil.instagram` as `cutover/astra`, `cutover/astra2`,
   `cutover/astra3` (so they reach GitHub). Accepted work merges the usual way first.
4. Push every local-only commit: the 57 workspace commits (`git log --branches --not --remotes`) and
   the three `cutover/astra*` branches. Check: `git log --branches --not --remotes` is empty.

**A1b. Nothing pending gets lost — make a list of every unfinished piece of work** and show it to
the user before moving on:
- uncommitted Codex changes (Codex cannot commit; check `git status` in `C:\Gaznil.instagram` AND
  `C:\Gaznil.instagram-codex`) — commit them on their branch as-is, labelled "unreviewed";
- builder work written but not yet reviewed (each astra clone's `REPORT.md` sections and commits not
  yet marked ACCEPTED in the project log, e.g. H16 in Clone 1, H18 not started);
- accepted but not deployed (everything after the last live tag, d32);
- the queue: unstruck items in `ROADMAP.md` NEXT UP, `HEAD.md` QUEUE, PARKED FOR CLAUDE, and the
  REMIND THE USER box in the context file.
In A5 each item on this list becomes a task on the new board (unreviewed work = a PR or task
"review <id>"), so the new system starts exactly where the old one stopped.

**A2. Collect project files that live outside the project folder** into
`C:\Gaznil.instagram\instagram-automation\archive\old-system\`, commit, push:
- workspace root: `agents\codex.md`, `agents\project-instagram.md`, `agents\workflow.md`, `AGENTS.md`,
  `WORKFLOW-SETUP.md`, `CODEX-REPORT.md`, `DEPLOY-REPORT-d23.md`, `hooks\`
- each astra clone root: `NEXT.md`, `PROGRESS.md`, `REPORT.md`, `tasks\` → `old-system\<clone>\`
- `C:\Users\newuser\.claude\context\own\instagram-automation.md`, `instagram-automation-history.md`,
  `porotta-prompts.md` (copies; originals stay) — remove the HetrixTools key line from the copies
- everything in `cutover/rescued/` of gaznil/claudecloud → `old-system\rescued\`
- never: `.env*`, `.neon`, keys, `deploy\state\`, browser profiles, node_modules, .next
Check: no `.env` in `git ls-files instagram-automation/archive/old-system`.

**A3. Final copy into the new repo.**
`scripts/split-porotta.sh <Gaznil-workspace clone> <empty dir> https://github.com/gaznil/porotta`
(from Git Bash or WSL; needs `pip install git-filter-repo`). Check: prints `split ok`, push is a
fast-forward (it refuses anything else).

**A4. New home on the PC.** `git clone https://github.com/gaznil/porotta C:\Gaznil.porotta`; copy
`.env`, the four `.env.*.local` files and `.neon` from `C:\Gaznil.instagram\instagram-automation\`
(never commit them); `npm ci && npx prisma generate`; run the gates. Check: tsc 0 errors, build ok,
`scripts\deploy.ps1 -DryRun` passes from the new folder.
(Stays on C: for now because deploys run Windows tar/scp; it moves into WSL once Phase B's deploy
workflow replaces deploy.ps1.)

**A5. Install the new rules (PR `setup/rules`, merge when CI is green):**
- `CLAUDE.md` and `AGENTS.md` from `cutover/porotta/` in gaznil/claudecloud
- `.github/workflows/ci.yml` from the old repo with `working-directory` and the
  `instagram-automation/` path prefixes removed
- `.gitattributes` (`* text=auto eol=lf`); `scratch/` in `.gitignore`
- labels Task, Bug, Feature, risky, needs-human, ready; a Project board To do → Building → Review → Live

**A6. Point everything at the new home.**
- `~\.claude\context\own\instagram-automation.md`: project folder = `C:\Gaznil.porotta`, repo
  gaznil/porotta, workflow = this system; move old STATUS to the history file (30 KB cap); remove
  the HetrixTools key line (user is rotating it).
- In that same file, rewrite the RULES so every chat type follows the new system:
  discuss chats save ideas to `DISCUSSION.md` as before, but a **confirmed** item becomes a **task**
  (GitHub issue with checks, labelled Task/Bug/Feature) — not a ROADMAP NEXT UP line; "builder go" =
  board + `gz`; no TASK/HEAD/NEXT/SESSION writes; status = the board. Move the old lane / NEXT UP /
  HEAD / credit-board rules into the history file. `ROADMAP.md` becomes read-only history with a
  first line pointing to the board.
- `~\.claude\CLAUDE.md` project index row: same trigger words, same file.
- `~\.claude\context\machine.md`: Porotta now has its own repo (user decided 10 Oct 2026); the
  one-repo rule stays for the other projects.
- `~\.claude\settings.json`: remove the duplicate obsidian SessionStart hook (it is listed twice)
  and the old one-off `scp ... d19` permission. Ask the user before editing settings (their rule).
- `~\.codex\config.toml`: add `C:\Gaznil.porotta` to the projects / writable roots.
- `sonnet-worker*.md`: replace PLAN.md / WORK.md / QUESTION.md with "the issue is your order;
  report in your final message".
- Old repo: `instagram-automation\MOVED.md` ("Porotta now lives in gaznil/porotta") and the same
  line in `agents\project-instagram.md` and workspace `CLAUDE.md`. Delete nothing.

**A7. Free disk (only after A1–A4 checks passed).** Delete `C:\Gaznil.astra`, `astra2`, `astra3`,
`C:\Gaznil.instagram-codex`; in `deploy\state\` keep only the live tag and the one before; clear
`.next` folders. Report free space before and after. `C:\Gaznil.instagram` itself stays until
Phase B is done.

**A8. Report to the user:** what moved, commit hashes, free disk, anything skipped — and the
first tasks created for Phase B.

## PHASE B — build the self-running parts (Codex luna/sol low, one task each)
1. Protect `main`: PR required, CI green required, squash merge.
2. Deploy-on-merge workflow (GitHub Actions + server SSH secret): build, upload, swap, health + smoke
   test, automatic rollback; migrations that delete/rewrite data wait for the user's yes in a
   `production` environment. Then retire deploy.ps1.
3. `gz` script: picks `ready` tasks, worktree per task, starts OmniRush (Sol low; Astra after two
   failures), runs the gates, pushes, opens the PR, cleans up; phone notification when stuck.
4. Codex review on every PR (luna low; sol low for `risky`); auto-merge safe PRs when green.
5. Playwright smoke test of the main user flows (used after every deploy).
6. Cleanup PR: AI notes, videos, logos and screenshots out of the code; README + ARCHITECTURE for a human.
Then move the home into WSL, delete `C:\Gaznil.instagram`, and back to the product:
Meta App Review submission and Razorpay.
