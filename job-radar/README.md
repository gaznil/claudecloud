# Job Radar

Your own AI job hunter, built for Kerala, the rest of India, the Gulf and overseas jobs.

Tell Claude once what job you want. Every morning it:

1. Searches job sources that fit your role: Kerala IT parks, company hiring pages, Indian job
   boards, Gulf boards, and government recruiters like NORKA Roots and ODEPC.
2. Throws out scams (fee demands, fake visa agents, Telegram "task" jobs).
3. Scores every job against your profile.
4. Rewrites your CV for each good match so it passes company screening software (ATS), without
   adding anything that isn't true.
5. Applies for you where it can, and gives you a one-click list for the rest.
6. Sends you a short report and keeps a tracker so nothing is applied to twice.

## What it can and can't apply to

| Job type | Who submits |
|---|---|
| "Send your CV to hr@…" | Claude, through your Gmail |
| Simple company forms (Darwinbox, Keka, Zoho Recruit, Lever, Greenhouse, Google Forms) | Claude, in your Chrome (Claude in Chrome extension) |
| Sites with login OTP or CAPTCHA | Claude fills it, you finish |
| LinkedIn, Naukri | You click; Claude prepares the CV and answers. Automating these breaks their rules and can get your account blocked. |

You choose **Review first** (you approve each batch with one reply) or **Full auto** (Claude
submits matches above your score and reports after). Start with Review first.

## Set it up (pick one)

**A. Claude Code** (easiest if you have it)
Clone this repo, open it in Claude Code, and say **"set up job radar"**.

**B. claude.ai Skill**
1. Build the zip with `scripts/build-skill-zip.sh` (it lands in `dist/job-radar.zip`).
2. In claude.ai, open Settings, find Skills (under Capabilities), upload the zip and turn it on.
3. Create a Project called "Job Radar", start a chat in it, and say **"set up job radar"**.

**C. No skill upload**
Create a Project, paste the contents of `skills/job-radar/SKILL.md` into the Project
instructions and add the `references/` and `templates/` files to the Project files. Then say
**"set up job radar"**.

## For the most automation

- A paid Claude plan (for scheduled daily runs)
- Gmail connected (email applications)
- Claude in Chrome extension (form applications)
- Google Drive connected (optional: stores your CVs and tracker)

Without any of these it still works: say **"run my job hunt"** each morning and click apply
on the list it gives you.

## Your data

Your profile, CVs and tracker stay in your own Claude Project, Google Drive or the `my-data/`
folder, which is never committed. Claude never asks for or shares passport, Aadhaar, PAN or bank
details, and never pays any fee.
