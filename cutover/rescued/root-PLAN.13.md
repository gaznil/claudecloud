# PLAN — Phase 13: design system and visual overhaul

> **QUEUED.** Run only after Phase 11 (wizard) and Phase 12 (IA restructure) have landed and been
> verified. Styling before those land means restyling screens that are about to move.
> Read `UI_AUDIT.md` first — it is the evidence this plan is built on.

**Branch:** `work/instagram-phase-5`

## Standing rules

- Do not modify/delete/re-seed `Account` or `Settings`. Do not touch `.env`.
- Do not restart ngrok or change `NEXT_PUBLIC_APP_URL`.
- Do not `git checkout` any PLAN / HANDOFF / SESSION / UI_AUDIT file.
- Scratch + screenshots go in `instagram-automation/scratch/` (gitignored).
- **No new dependencies.** No font packages, no UI kits, no CSS libraries.
- **No engine or behaviour changes.** This phase is presentation only. Test count must not drop.

## What is wrong today (measured — full detail in `UI_AUDIT.md`)

- **89% of all text is 12–14px.** 189 uses of `text-xs` against 2 of `text-3xl`. No hierarchy.
- **Nine colour families**, with `red` the second most used (77) — constant alarm in an app that
  is usually idle and healthy. `slate` and `zinc` are two grey families mixed together.
- **Seven radius values**, spacing dominated by `p-1`/`p-2` (161 uses) — nothing was chosen.
- **`aria-*` count across all 9 pages and 8 components: 0.** Neither modal closes on Escape.
- Home, Automations and Activity have **no error states**; Home has **no empty state**, which is
  exactly what the user sees today with 0 automations.
- `md:` breakpoints absent entirely from Home, Activity, Settings, test-mode and login.

## Design direction — warm editorial print

From the reference the user supplied (a Summer Margarita campaign site): cream paper, deep navy
ink, one burnt-orange accent, big scale contrast, generous air, small-caps numbered labels.

**Adapt it, do not copy it.** The reference is a landing page seen once; this is a utility used
daily. Specifically:

- The large serif appears **once per screen**, never as the norm.
- Botanical/decorative imagery only at page edges, **never behind text**, never on a working screen.
- **Never orange text on cream for body copy** — it fails contrast. Orange is for fills, rules and
  small accents; navy carries all text.
- **Red is demoted, not adopted.** In the reference red is decorative. Here `danger` means *error
  or destructive only*. Most of the current 77 red uses must go.
- The reference's `01 · 02 · 03` side labels **map onto the Phase 11 wizard stepper** — that is the
  single strongest idea to borrow.

## 13a — Foundations (commit 1). No page changes.

Build the token system **in three layers** — primitive, semantic, component. Never let a component
reference a raw value.

```
Primitive (raw)  →  Semantic (purpose)  →  Component (usage)
--paper-50: #FBF3E4  →  --color-bg: var(--paper-50)  →  --card-bg: var(--color-bg)
```

### Primitives — `globals.css`

```css
:root {
  /* paper / ink */
  --paper-50:  #FFFDF7;   --paper-100: #FBF3E4;   --paper-200: #E3D9C2;
  --ink-900:   #12233F;   --ink-500:   #5A6B82;
  /* accent */
  --orange-500: #E8892B;  --orange-600: #CE741C;  --orange-700: #A65A12;
  /* status */
  --green-700: #1F4A3A;   --red-600:   #C93A22;
}
```

### Semantic layer

```css
--color-bg: var(--paper-100);        /* page */
--color-surface: var(--paper-50);    /* cards */
--color-line: var(--paper-200);      /* borders, rules */
--color-fg: var(--ink-900);          /* all body text */
--color-fg-muted: var(--ink-500);    /* secondary — must pass 4.5:1 on --color-bg */
--color-primary: var(--orange-500);
--color-primary-hover: var(--orange-600);
--color-primary-active: var(--orange-700);
--color-success: var(--green-700);
--color-danger: var(--red-600);
```

Expose these through `tailwind.config` `theme.extend.colors` so classes read
`bg-surface`, `text-fg-muted`, `border-line` — **not** `bg-[#FBF3E4]`.

### Type scale — six steps, nothing between

| Token | Size / line | Face | Use |
|---|---|---|---|
| `display` | 40 / 1.1 | serif | once per screen, max |
| `title` | 28 / 1.2 | serif | section headings |
| `head` | 20 / 1.3 | sans 600 | card and group headings |
| `body` | **16 / 1.5** | sans 400 | **the default** |
| `label` | 14 / 1.4 | sans 500 | form labels, meta |
| `micro` | 12 / 1.3 | sans 600, uppercase, tracked | labels only — **never sentences** |

**The single highest-impact rule in this phase: body text is 16px.** Today it is 12px nearly
everywhere. Serif is a system stack (`ui-serif, Georgia, serif`) — no font downloads.

### Spacing — 4pt scale, six steps

`4 · 8 · 16 · 24 · 40 · 64`. Card padding defaults to `24`. Retire the `p-1`/`p-2` habit.

### Radius — two, plus pills

`8px` buttons and inputs · `16px` cards · `full` pills and avatars. Delete the other four.

### Component specs — every state defined, no exceptions

**Button**

| Variant | Default | Hover | Active | Focus-visible | Disabled |
|---|---|---|---|---|---|
| primary | `primary` fill, paper text | `primary-hover` | `primary-active` | 2px `primary` ring, 2px offset | `line` fill, `fg-muted` text |
| secondary | transparent, `fg` text, `line` border | `surface` fill | `line` fill | same ring | 40% opacity |
| quiet | text only, `fg-muted` | `fg` text | `fg` text | same ring | 40% opacity |
| danger | `danger` fill, paper text | darken 8% | darken 14% | `danger` ring | as primary |

**No drop shadows anywhere.** Depth comes from paper-vs-surface contrast, as in the reference.

**Input** — `surface` fill, 1px `line`, 8px radius, 16px text, label above in `label`, help below
in `micro`. On error: `danger` border, and the error message **replaces** the help text.
Focus-visible: 2px `primary` ring.

**Card** — `surface`, 1px `line`, 16px radius, 24px padding, no shadow.

Put these in `src/components/ui/` as `Button.tsx`, `Input.tsx`, `Card.tsx`. **No page is changed in
this commit** — this is the foundation everything else builds on.

**Commit 1:** `feat(ui): add three-layer design tokens and base component primitives [13a]`

## 13b — Home and Automations list (commit 2)

The most-seen screens and the worst-measured. Rebuild both on the primitives.

- **Home's empty state is the main deliverable** — the user has 0 automations, so this is what they
  actually see. It should be a warm, confident invitation with one obvious action, not an empty
  dashboard with zeroes.
- Add the **missing error states** to both (currently zero).
- One `display` heading per screen. Numbers in `title`, their labels in `micro`.

**Commit 2:** `refactor(ui): rebuild home and automations list on the design system [13b]`

## 13c — The wizard (commit 3)

Restyle what Phase 11 shipped. Highest craft value — it is the thing the user actually does.
Apply the **`01 · 02 · 03` editorial stepper** from the reference. One question per screen, one
`display` heading, generous air, large tap targets.

**Commit 3:** `refactor(ui): apply the editorial design system to the wizard [13c]`

## 13d — Activity, Settings, Login (commit 4)

- **Activity:** plain-language rows ("replied to @someone on your Reel · 2m ago"), not raw event
  vocabulary. Add the missing empty and error states. Must not scroll sideways on a phone.
- **Settings:** the Apple-style grouped list from Phase 12, now on the type and spacing scale.
- **Login:** currently has *zero* responsive classes and is seen every session. Cheap, and it is
  the first impression.

**Commit 4:** `refactor(ui): restyle activity, settings and login [13d]`

## 13e — Modals and the accessibility sweep (commit 5)

**Do not defer this again — accessibility is currently zero across the entire app.**

- `PostPickerModal` and `LogDetailModal`: close on **Escape**, **trap focus**, restore focus to the
  trigger on close, `role="dialog"` + `aria-modal="true"` + `aria-labelledby`, labelled close button.
- `focus-visible` styling on every interactive element app-wide (Home and Settings have none today).
- Label every icon-only button. Alt text on every image, with a **designed fallback for Instagram
  thumbnails** — `scontent.cdninstagram.com` genuinely fails for this user, so a broken image is a
  normal case, not an edge case.
- Check contrast: `fg-muted` on `bg` must pass 4.5:1.

**Commit 5:** `fix(a11y): focus management, modal semantics and contrast pass [13e]`

## Not in scope

`test-mode` — developer surface, hidden behind the Phase 12 Developer toggle. Leave it functional
and plain. Do not spend styling effort there.

## Verify (each commit)

- `npx tsc --noEmit` -> exit 0; `npm test` -> all pass, count not reduced.
- **No raw hex or arbitrary values in components.** Run and paste the output:
  `grep -rnE '#[0-9a-fA-F]{6}|\[#' src/app src/components | grep -v globals.css`
  It must be empty. Every colour goes through a token.
- **No `text-xs` used for sentences** — only for `micro` labels.
- Screenshot **1440x1100 and 390x844** against the **tunnel URL**, and look at both.
- Keyboard-only pass on 13e: tab through Home, open a modal, press Escape, confirm focus returns.

Report into `HANDOFF.md` under `## Phase 13 — worker report`, one section per commit.
