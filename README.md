# Gaznil dev system

How the whole build system works (roles, flow, setup): see [SYSTEM.md](SYSTEM.md).

The standard setup for every new project. One workflow, no overlap.

| Layer | What | Install (in Claude Code) |
|---|---|---|
| Build workflow | Superpowers: brainstorm -> plan -> fresh subagent per task -> review -> finish | `/plugin install superpowers@claude-plugins-official` |
| Ship side | **gaznil-dev-system** (this repo): launch, security, CI/CD, observability, browser testing, performance | see below |
| Final check | Anthropic official code review | `/plugin install code-review@claude-plugins-official` |

```
/plugin marketplace add gaznil/claudecloud
/plugin install gaznil-dev-system@gaznil
```

Do not also install the full `addyosmani/agent-skills` plugin: its spec, plan, build, TDD and
review skills duplicate Superpowers and the two fight over the same requests.

Moving an existing project in: see [cutover/CUTOVER.md](cutover/CUTOVER.md).

Other agents (Codex, OmniRush, Antigravity) can use the same skills by reading
`plugins/gaznil-dev-system/skills/<name>/SKILL.md` from a clone of this repo; point to it from the
project's `AGENTS.md`.

## Where the skills come from

The six skills and their checklists are copied unchanged from
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) at commit `1401c8b`
(MIT, see `plugins/gaznil-dev-system/LICENSE-agent-skills`). To update, copy the same folders
from a newer commit and bump the version in `plugin.json`.
