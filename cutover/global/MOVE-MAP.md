# Global CLAUDE.md slim-down — where every removed line goes

Draft only. Nothing on the PC changes until the user says yes. Old file kept as
`CLAUDE.md.bak-<date>` beside it. Every moved section goes **word for word** into its new home,
including the dated quotes, so nothing is lost.

| Old section | Words | New home |
|---|---|---|
| WHO I AM | 186 | stays (tightened, same facts) |
| RULE ZERO | 251 | stays (same rules) |
| REPLY STYLE | 102 | stays |
| NEVER GUESS | 134 | stays; the "local connectors / claude_desktop_config.json" line → `machine.md` |
| SKILLS | 232 | stays (shorter); the `ui-ux-pro-max` broken-skill note → `machine.md` (tool quirk) |
| CODEX MODEL CHOICE | 577 | → new `context\builders.md`, verbatim (Luna-first ladder, never Astra, pricing check, plugin version fix, Astra exception). Routed by "Codex / builder / model" |
| WHAT COUNTS AS A PROJECT | 278 | stays (shorter, same rules) |
| HANDOFF | 637 | stays as the 4 steps + two-alert rule. The `HANDOFF.md` worker-file name collision → removed (that file is archived; old text kept in `builders.md` history). The discuss-session exception → `own\instagram-automation.md` RULES (it only applies there) |
| PROJECT INDEX | 357 | stays; Porotta row points at the new repo; new rows for `builders.md` and `clients\README.md`; the "moved 13 Sep" note → `machine.md` |
| CLIENT SYSTEM | 250 | → new `context\clients\README.md`, verbatim. Routed by client stage words |
| SERVER ACTIONS NEED YES | 363 | stays as SAFETY (every rule kept; the dated history quotes → `machine.md` "rule history") |

Result: about 3,270 words → about 1,250 words loaded in every chat (≈60% less), with nothing
deleted — Codex, client and history details load only when their trigger words appear.

Also fixed in the same pass: the Porotta rules that are duplicated in the global file, the
workspace `CLAUDE.md` and the context file are kept in exactly one place each
(personal → global, Porotta product → context file, how-to-build → repo `CLAUDE.md`).
