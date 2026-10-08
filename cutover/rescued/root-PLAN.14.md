# PLAN — Phase 14: Facebook Page automation

> **QUEUED.** Run after Phase 13 lands. No Meta dashboard work is required — every permission this
> phase needs was added and verified on 2026-08-23.

**Branch:** `work/instagram-phase-5`

## Standing rules

- Do not modify/delete/re-seed `Account` or `Settings`. Do not touch `.env`.
- Do not restart ngrok or change `NEXT_PUBLIC_APP_URL`.
- Do not `git checkout` any PLAN / HANDOFF / SESSION / UI_AUDIT file.
- Scratch + screenshots go in `instagram-automation/scratch/` (gitignored).
- **Live sending stays OFF.** This phase ends with Facebook events logging `BLOCKED`, exactly as
  Instagram does today. Do not flip `liveSendingEnabled`.

## Why this is now cheap

The hard part — permissions and subscriptions — is already done:

- **Permissions on the app** (verified in a real token, 2026-08-23): `pages_messaging`,
  `pages_manage_engagement`, `pages_read_user_content`, `pages_manage_posts`,
  `pages_manage_metadata`, `pages_read_engagement`, `pages_show_list`, `business_management`.
- **The Page is already subscribed** to the app with `subscribed_fields: ["feed", "messages"]`
  (`POST /{page-id}/subscribed_apps`). **`feed` is the field that carries Page comments.**
- Page id `981814655020325`, permanent Page token already in the DB.

So Facebook comment events **should already be arriving** at `/api/webhooks/instagram` — they are
just not understood yet. **Step 1 is to prove that before building anything.**

## 14a — Prove the events arrive, and record their shape (commit 1)

1. Comment on a post on the **Gaznil AI & Marketing** Facebook Page from a second account.
2. Capture the raw webhook body. Confirm whether it arrives, and with what `object` value
   (expected `page`, not `instagram`).
3. **Write the captured payload into `HANDOFF.md`.** Do not guess the shape from documentation —
   record what actually arrived.

**If nothing arrives**, the app-level subscription needs a `page` object added:
`POST /{app-id}/subscriptions` with `object=page`, `fields=feed`, the same callback URL and
`META_WEBHOOK_VERIFY_TOKEN`, using an app access token (`APP_ID|APP_SECRET`). That is exactly how
the `instagram` subscription was created on 2026-08-23 — see `SESSION.md`.

**Commit 1:** `test(webhooks): capture and document the Facebook page comment payload [14a]`

## 14b — A `platform` dimension through the data model (commit 2)

Today everything silently assumes Instagram. Make the platform explicit.

- Add `platform` (`INSTAGRAM` | `FACEBOOK`) to `Automation` and `EventLog`. Default existing rows to
  `INSTAGRAM` in the migration — **no existing row may change behaviour.**
- The webhook router branches on the payload's `object` (`instagram` vs `page`) and stamps
  `platform` on the event.
- The matcher only considers automations whose `platform` matches the event.

**This is the riskiest commit in the phase** — it touches the live Instagram path. The full existing
suite must stay green, and an Instagram comment must still produce an identical result to today.

**Commit 2:** `feat(engine): add a platform dimension to automations and events [14b]`

## 14c — Facebook send adapters (commit 3)

Behind the **same** two-key safety gate. Different endpoints, same shape:

| Action | Instagram (today) | Facebook (new) |
|---|---|---|
| Public reply | `POST /{ig-comment-id}/replies` | `POST /{comment-id}/comments` |
| Private DM | Instagram messages API | `POST /{comment-id}/private_replies` |

- `private_replies` requires `pages_messaging` — **already granted.**
- Respect the **24-hour messaging window**; surface a clear status when a send falls outside it
  rather than failing opaquely.
- Every send path must honour `ALLOW_LIVE_SENDING` **and** `liveSendingEnabled`, and log `BLOCKED`
  when either is off. **No new code path may bypass the gate** — assert this in a test.

**Commit 3:** `feat(engine): Facebook public reply and private reply adapters [14c]`

## 14d — Separate Instagram and Facebook sections (commit 4)

**The user was explicit (2026-08-23): there must be SEPARATE SECTIONS for creating Facebook
automations and Instagram automations — not one wizard with a platform dropdown inside it.**
Do not implement this as a toggle on step 1.

**Entry points.** "New Automation" resolves to a **platform choice first**, as two clear cards —
**Instagram** and **Facebook**, each with its own icon and one line of plain description. Picking one
enters a wizard already committed to that platform. The platform is then **fixed for the life of
that automation** — it is not editable afterwards (changing it would invalidate the chosen post and
the whole compiled graph). Show the platform as a static badge in the wizard header instead.

**The Automations list is grouped by platform** — an Instagram section and a Facebook section, each
with its own heading, count and empty state. An empty Facebook section still shows with its own
invitation to create one; it must not be hidden just because it is empty.

**Everything else follows the platform already chosen:**
- The post picker loads Instagram media or Facebook Page posts accordingly — no mixed lists.
- Copy, placeholder text and the live preview reflect the right network (a Facebook preview must not
  render an Instagram frame).
- Activity rows carry a platform badge, and Activity can be filtered by platform.

Reuse the Phase 13 design system — no new visual vocabulary, no raw hex.

**Verify:** create one automation of each platform. Confirm by DB read that each is stored with the
right `platform`, that each compiles to a valid graph, and that the Automations list renders them in
their own sections. Screenshot the list and both wizard entry points at 1440x1100 and 390x844.

**Commit 4:** `feat(wizard): separate Instagram and Facebook automation sections [14d]`

## Verify (each commit)

- `npx tsc --noEmit` -> 0; `npm test` -> all green, **count must not drop**.
- The existing Instagram automation still matches and still logs `BLOCKED` — paste the event row.
- `liveSendingEnabled` still `false`; token still resolves to `gznl.ai`.
- For 14d, screenshots at 1440x1100 and 390x844 that you actually look at.

Report into `HANDOFF.md` under `## Phase 14 — worker report`, one section per commit.
