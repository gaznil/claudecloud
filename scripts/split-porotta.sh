#!/usr/bin/env bash
# Copies instagram-automation out of Gaznil-workspace (branch work/instagram-phase-5) into its
# own repo with full history, minus the committed Chrome profiles (scratch/chrome-profile*,
# which hold cookies and saved-login files). Never changes Gaznil-workspace.
# Re-running later produces the same commits plus any new ones, so the push is a plain
# fast-forward; it refuses to force-push.
#
# Usage: scripts/split-porotta.sh <path-to-Gaznil-workspace-clone> <work-dir> [push-url]
# Needs: git, git-filter-repo (pip install git-filter-repo)
set -euo pipefail
SRC=${1:?path to Gaznil-workspace clone}; WORK=${2:?empty work dir}; PUSH=${3:-}
BRANCH=work/instagram-phase-5

git -C "$SRC" fetch origin "$BRANCH"
[ "$(git -C "$SRC" rev-parse --is-shallow-repository)" = false ] || { echo "clone is shallow; fetch full history first"; exit 1; }
SPLIT=$(git -C "$SRC" subtree split --prefix=instagram-automation FETCH_HEAD 2>/dev/null)

# The split commit is not reachable from any ref yet, so a plain clone would not carry it:
# pin it under a temporary ref for the clone, then remove the ref again.
git -C "$SRC" update-ref refs/heads/porotta-split-tmp "$SPLIT"
rm -rf "$WORK"; git clone -q --no-local --no-checkout --single-branch --branch porotta-split-tmp "$SRC" "$WORK"
git -C "$SRC" update-ref -d refs/heads/porotta-split-tmp
git -C "$WORK" checkout -q -B main "$SPLIT"
(cd "$WORK" && git filter-repo --force --refs main --path-glob 'scratch/chrome-profile*' --invert-paths)

# Proof nothing else changed: every file except the removed profiles is byte-identical.
A=$(git -C "$SRC" ls-tree -r "$SPLIT" | grep -v 'scratch/chrome-profile')
B=$(git -C "$WORK" ls-tree -r main)
[ -n "$A" ] && [ "$A" = "$B" ] || { echo "unexpected differences:"; diff <(echo "$A") <(echo "$B") | head; exit 1; }
echo "split ok: $(git -C "$WORK" rev-list --count main) commits, head $(git -C "$WORK" log -1 --format='%h %s' main)"

if [ -n "$PUSH" ]; then
  git -C "$WORK" push "$PUSH" main:main   # no --force: a non-fast-forward is refused
fi
