# Porotta cutover — move from Gaznil-workspace to gaznil/porotta

Trigger: the user says **"do the Porotta cutover"**. Claude runs every step itself, on the user's PC,
checks each result, and stops and reports if a check fails. Nothing here touches production.

## 1. Stop and save (old system)
1. Let running OmniRush/Codex tasks finish; confirm no builder runs (`wsl.exe -e pgrep -af omnirush` empty).
2. In every builder clone (`C:\Gaznil.astra`, `astra2`, `astra3`): commit finished work and get it
   reviewed/merged into `work/instagram-phase-5` the usual way, or push it as branch `cutover/<clone>`
   to Gaznil-workspace. Check: `git status --short` clean in each clone.
3. Push `work/instagram-phase-5`. Check: `git status` says up to date with origin.

## 2. Collect project files that live outside the project folder or only on this PC
Copy into a new folder `instagram-automation/archive/old-system/` in Gaznil-workspace, commit, push:
- From the workspace root: `agents/codex.md`, `agents/project-instagram.md`, `agents/workflow.md`,
  `AGENTS.md`, `WORKFLOW-SETUP.md`, `CODEX-REPORT.md`, `DEPLOY-REPORT-d23.md`, `hooks/`.
- From each builder clone root (untracked on purpose): `NEXT.md`, `PROGRESS.md`, `REPORT.md`, `tasks/`
  → `archive/old-system/<clone>/`.
- `C:\Users\newuser\.claude\context\own\instagram-automation.md`.
- Everything in `cutover/rescued/` of gaznil/claudecloud (old top-level SESSION.md, PLAN.13.md, PLAN.14.md
  and the Superpowers workspace spec, recovered from git history) → `archive/old-system/rescued/`.
- Any untracked discussion/notes files in `C:\Gaznil.instagram` that belong to Porotta (list them with
  `git status --short --untracked-files=all instagram-automation` and show the user before copying).
- Never copy: `.env*`, SSH keys, `deploy/state/`, browser profiles, `node_modules`, `.next`.
Check: `git ls-files instagram-automation/archive/old-system | wc -l` > 0 and no file name contains `.env`.

## 3. Final sync into the new repo
`scripts/split-porotta.sh <Gaznil-workspace clone> <empty dir> https://github.com/gaznil/porotta`
Check: script prints `split ok`, push is a fast-forward (it refuses anything else).

## 4. New home on the PC (inside WSL, not /mnt/c)
`git clone https://github.com/gaznil/porotta ~/work/porotta`; copy `.env` from
`C:\Gaznil.instagram\instagram-automation\.env` (never commit it); `npm ci && npx prisma generate`;
run the gates. Check: tsc 0 errors, build succeeds.

## 5. Make the new system the default
On a branch `setup/rules` in the new repo, via PR:
- Add `CLAUDE.md` and `AGENTS.md` from `cutover/porotta/` in gaznil/claudecloud.
- Move `.github/workflows/ci.yml` from the old repo, with `working-directory` and the
  `instagram-automation/` path prefixes removed.
- Add `.gitattributes` (`* text=auto eol=lf`) and `scratch/` to `.gitignore`.
Merge after CI is green. From now on any Claude session opened in `~/work/porotta` loads these rules.

## 6. Close the old home
In Gaznil-workspace: replace `instagram-automation/` contents' entry point with a `MOVED.md`
("Porotta now lives in gaznil/porotta") and update `agents/project-instagram.md` + workspace
`CLAUDE.md` to say the same, so no agent builds there again. Keep the old history; delete nothing.
Remove the `C:\Gaznil.astra*` clones only after step 1 is verified (frees disk).

## 7. First jobs in the new system (as Issues)
1. Protect `main` (CI required, squash only). 2. Deploy-on-merge workflow with a `production`
environment approval. 3. `gz` script. 4. Codex PR review. 5. Cleanup PR: move AI notes, videos,
logos, screenshots out of the code. 6. README + ARCHITECTURE for a human developer.
Then: Meta App Review submission and Razorpay.
