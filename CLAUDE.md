# CLAUDE.md — El Paso Scholarship Finder

This file is the source of truth for this project. Read it fully at the start of every session. If anything I ask for in chat conflicts with this file, stop and ask which one wins. Don't pick one yourself.

---

## 1\. What we're building

A public, free, bilingual (English/Spanish) scholarship search site for El Paso-area high school students and their families.

- **Audience:** El Paso-area students. Region decides who is searching, not which scholarships qualify. The list includes local/regional scholarships AND nationwide ones relevant to these students.  
- **Coverage:** merit, need-based, first-gen, regional, and demographic-specific scholarships. This is not a CS/merit tool. Need-based and first-gen entries matter as much as merit ones.  
- **v1 deadline:** a school scholarship workshop before the end of October 2026 (exact date: `WORKSHOP_DATE_TBD` — Ian fills this in).  
- **Later versions:** an AI chat feature (Phase 6+). v1 must be built so it can be added without a rebuild.

### Core principles (these override convenience)

1. **Stateless and private.** No accounts, no login, no cookies, no analytics, no tracking, and no third-party scripts. The only thing stored is the language preference, in the user's own browser (localStorage). The site's trust line is "no account, no personal info stored," and it has to be literally true.  
2. **Trust over volume.** Every scholarship shows its source link and its last-verified date. The site never shows guessed or invented data.  
3. **Bilingual from the start.** Spanish is a core feature from Phase 0, not something translated at the end.  
4. **Mobile-first.** Most students will open the site on a phone from a QR code.  
5. **Simple over clever.** No frameworks or dependencies we don't need. Ian must be able to maintain this alone.

---

## 2\. Division of labor

### Claude does

- Scaffold and build the site, the validation script, and the deploy pipeline  
- Build the search/filter UI, result cards, and language toggle  
- Draft Spanish translations of UI strings and scholarship summaries. **These are drafts, always marked unreviewed.**  
- Write and maintain the validation script and GitHub Actions workflows  
- Explain code clearly enough for Ian to review it and maintain it later  
- (Phase 6+) Build the Cloud Function, the pre-filter logic, and the AI prompt

### Ian does. Claude never does these.

- **All scholarship data sourcing and verification.** Claude never adds, removes, or edits a scholarship's facts (amount, deadline, eligibility, URLs) unless Ian supplies them. Claude never sets or updates `last_verified`.  
- **All credentials and accounts:** creating the Firebase project, the GitHub repo, and the service-account secret for deploys; the Blaze plan and billing; API keys. Claude never asks Ian to paste a secret into chat, and never writes one into any file.  
- **Final approval of Spanish translations** (Ian or a fluent reviewer he picks)  
- **Merging to `main`,** since merging to `main` deploys to production  
- Real-user testing, the workshop itself, and feedback collection

### Claude never

- Invents scholarship data, fills unknowns with plausible guesses, or "fixes" data it thinks is wrong. It flags it instead.  
- Changes the schema without approval  
- Adds a dependency, library, font service, CDN, or third-party script without approval  
- Adds analytics, cookies, tracking, or any storage of user input  
- Pushes or merges to `main`  
- Deletes files or rewrites git history  
- Moves on to the next phase without passing the checkpoint

---

## 3\. Tech stack

| Layer | Choice | Notes |
| :---- | :---- | :---- |
| Frontend | **Vite \+ vanilla JavaScript** (ES modules), plain CSS | No React/Vue/etc. No CSS frameworks. |
| Data | `data/scholarships.json` in the repo | Git history is the audit trail. |
| i18n | `src/i18n/en.json`, `src/i18n/es.json` \+ a small custom helper | No i18n library. |
| Validation | Python 3 script `scripts/validate.py` | Standard library only if possible. |
| CI/CD | GitHub Actions | Validate on every push/PR; deploy on merge to `main` only if validation passes. |
| Hosting | **Firebase Hosting** | Chosen now so Cloud Functions can be added later on the same domain. |
| Fonts | Self-hosted or system font stack | No Google Fonts link (it calls out to a third party). |
| Later (Phase 6+) | Firebase Cloud Functions (**Python**), Claude API, Secret Manager, App Check, per-IP rate limiting, budget alerts | Not built in v1. |

### Repo structure (target)

/

├── CLAUDE.md

├── README.md                 \# setup \+ how to add/verify a scholarship (for Ian or a successor)

├── index.html

├── src/

│   ├── main.js

│   ├── search.js             \# filtering/sorting logic, pure functions, no DOM

│   ├── render.js             \# DOM rendering

│   ├── i18n.js

│   ├── i18n/en.json

│   ├── i18n/es.json

│   └── styles.css

├── data/

│   └── scholarships.json

├── scripts/

│   ├── validate.py

│   ├── test\_validate.py       \# tests for the validator

│   └── check\_i18n.py          \# en.json / es.json parity check

├── .github/workflows/

│   ├── validate.yml           \# data \+ i18n checks on every push and PR

│   ├── firebase-hosting-pull-request.yml   \# checks, build, preview URL on a PR

│   └── firebase-hosting-merge.yml          \# checks, build, deploy on merge to main

├── firebase.json

├── .gitattributes

└── .firebaserc

The two `firebase-hosting-*.yml` names are the ones the Firebase CLI generated. They keep those names on purpose (renaming them would break nothing but gains nothing either). The deploy workflow is `firebase-hosting-merge.yml`, not `deploy.yml`.

Keep `search.js` free of DOM code. The Phase 6 AI pre-filter will reuse the same filtering logic.

---

## 4\. Data schema (locked after Checkpoint 1\)

Every entry in `data/scholarships.json` follows this shape. **Unknown \= `null`. Never guess.** The UI shows null values as "Not listed — check source" / "No especificado — consulta la fuente".

{

  "id": "mcdonalds-el-paso-2026",

  "name": "McDonald's El Paso Scholarships",

  "sponsor": "McDonald's El Paso",

  "amount\_min": null,

  "amount\_max": null,

  "amount\_display": { "en": "Varies; up to \$100,000 total across 18 students", "es": "..." },

  "renewable": null,

  "deadline": "2026-03-13",

  "cycle\_status": "closed\_reopens",

  "opens\_month": null,

  "categories": \["need\_based", "regional"\],

  "grade\_levels": \["hs\_senior"\],

  "residency": "el\_paso\_county",

  "districts": \[\],

  "schools": \[\],

  "eligible\_institutions": \["UTEP", "EPCC"\],

  "degree\_types": \["associate", "bachelor"\],

  "gpa\_min": 2.7,

  "fields\_of\_study": \[\],

  "demographics": \[\],

  "requirements": {

    "essay\_required": null,

    "recs\_needed": null,

    "fafsa\_required": null,

    "accepts\_tasfa": null,

    "citizenship\_required": null,

    "interview": null,

    "other": { "en": "", "es": "" }

  },

  "application\_language": "en",

  "source\_url": "https://...",

  "apply\_url": "https://...",

  "summary": { "en": "...", "es": "..." },

  "notes": { "en": "", "es": "" },

  "translation\_reviewed": false,

  "last\_verified": "2026-10-02"

}

### Allowed values (enums)

- `cycle_status`: `open` | `upcoming` | `closed_reopens` | `rolling` | `unknown`  
- `categories` (1+ required): `merit` | `need_based` | `first_gen` | `regional` | `demographic` | `field_specific`  
- `grade_levels`: `hs_junior` | `hs_senior` | `college`  
- `residency`: `el_paso_county` | `specific_districts` | `specific_schools` | `texas` | `national`  
- `degree_types`: `associate` | `bachelor` | `trade_technical`  
- `fields_of_study`: empty \= any field. Otherwise tags such as `stem`, `cs`, `nursing`, `education`, `hospitality`, `business` (new tags need Ian's approval)  
- `demographics`: empty \= no restriction. Otherwise tags such as `hispanic`, `first_gen`, `female`, `african_american`, `aapi`, `native_american` (new tags need approval)  
- `eligible_institutions`: empty \= any institution  
- `application_language`: `en` | `es` | `both`

### Why the schema is strict

Filters in v1, and the AI pre-filter in Phase 6, both read these structured fields. Free text is only for display. If a fact matters for matching, it goes in a structured field, not in `summary` or `notes`.

### Validation rules (`scripts/validate.py`)

**Errors (fail CI, block deploy):**

- Missing required field, wrong type, or value outside its enum  
- Duplicate `id`  
- Bad date format (must be ISO `YYYY-MM-DD`)  
- URL not starting with `https://`  
- `summary.en` empty  
- `amount_min` greater than `amount_max` (when both are set)

**Warnings (print, don't fail):**

- `summary.es` empty, or `translation_reviewed: false`  
- `last_verified` older than 45 days  
- Deadline within 14 days (so Ian re-checks it)  
- Many null requirement fields (entry may need more research)  
- `cycle_status: "open"` but `deadline` is in the past. A warning, not an error, so one entry nobody got around to updating cannot block an unrelated deploy (say, an urgent bug fix during workshop week). Phase 2 owns the other half of this: the UI must treat an `open` entry whose deadline has passed as closed, so an expired entry is never shown as open.  
- `cycle_status: "open"` but `deadline` is null  
- `cycle_status: "upcoming"` but `opens_month` is null

Output should be human-readable, listing each problem with its entry `id`.

---

## 5\. Frontend requirements

### Search and filters

- Text search over name, sponsor, and summary (in the current language)  
- Filters:  
  - category (multi-select)  
  - "my GPA" (shows entries where `gpa_min` is null or at or below the entered GPA)  
  - residency/district  
  - degree type  
  - "no essay required"  
  - "citizenship not required"  
  - "accepts TASFA"  
- Sort: deadline soonest (default), amount highest  
- Default view shows `open`, `rolling`, and `upcoming`. A toggle also shows `closed_reopens`.  
- Filter state may go in the URL query string (so links can be shared). It is never stored anywhere else.

### Result card must show

Name, sponsor, amount display, deadline or cycle-status badge, category badges, key requirement indicators (essay, recs, FAFSA/TASFA, citizenship), summary, an "Application in English" note when `application_language` is `en` and the UI is in Spanish, **source link**, **"Last verified: \[date\]"**, and an apply button.

### Bilingual rules

- No hardcoded user-facing strings. Every string comes from the i18n files.  
- EN/ES toggle is visible in the header. Default is the browser language, falling back to English. The choice is saved to localStorage (language only).  
- `<html lang>` updates when the language changes.  
- If `translation_reviewed` is false, **fall back to the English summary** and show a small note saying so ("Este resumen aún no está traducido, así que se muestra en inglés."). Decided at Checkpoint 1, Open Decision 3: clear English beats unreviewed Spanish that might be wrong. This applies to the per-entry `summary` and `notes` text, not to the UI strings in `es.json`.  
- Test layouts with Spanish, which runs about 20–30% longer. Nothing may overflow or truncate badly.

### Quality bar

- Works well at 360px wide  
- Accessible: semantic HTML, labels on every input, keyboard navigable, visible focus, WCAG AA contrast  
- Fast: the whole site loads quickly on mobile data, with no heavy assets  
- Empty state (no results) suggests loosening filters. It never shows a blank screen.  
- Trust line visible on the page: "No account. No personal info stored." / "Sin cuenta. No guardamos tu información personal."

---

## 6\. Working rules

1. **Branches:** do all work on feature branches (`phase-0-setup`, `phase-2-search`, etc.). Never push to `main`. When a chunk is done, tell Ian it's ready to review and merge.  
2. **Small commits** with clear messages.  
3. **State assumptions out loud.** If you had to assume something, list it in your summary. Don't bury it.  
4. **Ask instead of guess** when:  
   - the ambiguity affects user-facing text, data, or privacy  
   - you're unsure which of two reasonable approaches Ian wants  
5. **Explain for review.** When you finish a chunk, briefly explain how it works and why, so Ian can review the code, not just approve it.  
6. **Don't expand scope.** If you notice a good idea outside the current phase, add it to a "Parking lot" section in your summary. Don't build it.  
7. **Flag, don't fix, data problems.** If a scholarship entry looks wrong (dead link, odd date), report it to Ian. Don't edit it.

---

## 7\. STOP conditions (outside the scheduled checkpoints)

Stop, explain, and wait for Ian's answer before continuing if any of these come up:

- A schema change of any kind  
- Adding any dependency, service, or external request  
- Anything involving credentials, secrets, billing, or Firebase/GitHub settings  
- Deleting or renaming existing files  
- Something in this file seems wrong, contradictory, or impossible  
- A task is turning out much bigger than expected  
- You're about to deviate from this file for any reason

---

## 8\. Phases and checkpoints

At every checkpoint, post a summary in this format, then **stop and wait:**

\#\# Checkpoint N summary

Done: ...

How to test it: (exact commands / what to click)

Assumptions I made: ...

Decisions I need from you: ...

Your action items: ...

Parking lot: ...

### Phase 0 — Setup and schema (target: Sep 28 – Oct 3\)

**Ian first:** create the GitHub repo and Firebase project, install the Firebase CLI, and add the deploy service-account key as a GitHub Actions secret. Tell Claude the Firebase project ID. Do not paste the key. **Claude:**

Done: the project is `scholarship-site-fd70f` and the secret the Firebase CLI created is **`FIREBASE_SERVICE_ACCOUNT_SCHOLARSHIP_SITE_FD70F`**. That is the name the workflows use.

- Scaffold the repo per section 3, with `firebase.json` configured for Hosting  
- Set up the i18n helper plus starter `en.json`/`es.json`  
- Write `validate.py` per section 4, plus the `validate.yml` workflow and the validation gate in the two `firebase-hosting-*.yml` workflows  
- Create `data/scholarships.json` with **2 clearly fake example entries** (ids starting `example-`) that exercise every field, and a README section on how to add an entry  
- Deploy a placeholder page through the pipeline to prove it works

**🛑 CHECKPOINT 1 — Schema lock.** Ian reviews the schema, enums, and validation rules, and answers the Open Decisions. After this, schema changes require a STOP.

### Phase 1 — Data collection (target: Oct 1 – Oct 16\) — mostly Ian

**Ian:** sources and verifies 40–60 entries, then adds them to the JSON himself (or pastes verified facts to Claude to format). **Claude:** only formats data Ian provides, drafts Spanish summaries (marked unreviewed), and runs validation. Reports category counts on request.

**🛑 CHECKPOINT 2 (\~Oct 9\) — Balance check.** Claude reports the count per category and per residency. If need\_based and first\_gen are thin compared to merit, Ian fixes that before continuing data entry.

### Phase 2 — Search UI (target: Oct 5 – Oct 18, parallel to Phase 1\)

**Claude:** build everything in section 5 against the current data. Keep the filter logic in `search.js` as pure functions, with simple tests for it.

**🛑 CHECKPOINT 3 — Working build.** Ian tests on his phone in both languages. Claude supplies a short test checklist: filters, sorting, toggle, empty state, overflow in Spanish.

### Phase 3 — Polish and trust (target: Oct 19 – Oct 25\)

**Claude:** accessibility pass, empty states, cycle-status handling, trust copy, performance check, README finalized. **Ian:** soft launch with 2–3 students outside his usual circle (ideally need-based seekers) and at least one Spanish-reading tester, ideally a parent. He watches them use the site without explaining it.

**🛑 CHECKPOINT 4 — Launch readiness.** Claude fixes only what the testers hit. Ian merges to `main`.

### Phase 4 — Workshop launch (last week of October)

**Code freeze:** bug fixes only, no new features. Ian handles the QR code, poster, and a separate Google Form for feedback (the site itself stays stateless).

### Phase 5 — Maintenance (Nov – Dec)

**Ian:** monthly re-verification, 2027 cycle updates, new entries from feedback. **Claude:** a helper that lists stale entries (the validation warnings), plus small improvements Ian approves from the parking lot.

**🛑 CHECKPOINT 5 — Go/no-go on the AI layer.**

### Phase 6 — AI layer groundwork (winter) — do not start without Checkpoint 5

**Ian:** upgrade to the Blaze plan, set a hard budget alert, put the Claude API key in Secret Manager himself, and write \~20 test questions with expected answers, including Spanish and mixed-language ones. **Claude:**

- Python Cloud Function: receive the query, pre-filter to \~15 candidates using the same logic as `search.js`, then call Claude with only those candidates  
- The prompt requires the model to recommend only from the candidates, cite `source_url`, answer in the user's language, and say plainly when nothing fits  
- App Check plus per-IP rate limiting  
- **No logging of query text**

**🛑 CHECKPOINT 6 — Must pass Ian's test set before any student sees it.**

### Phase 7 — AI beta then public (spring)

### Phase 8 — Optional later

Auto-discovery feeding a **review queue that Ian approves** (never auto-publish), embedding search if the list grows past a few hundred entries, and expanding to more El Paso schools.

---

## 9\. Out of scope for v1

AI chat · live scraping or auto-discovery · accounts or saved lists · essay help · application tracking (that's Ian's separate personal tracker, a different codebase) · analytics of any kind

---

## 10\. Open decisions (Ian answers at Checkpoint 1\)

### Answered at Checkpoint 1

1. **Exact workshop date:** October 15th (2026 — see the open item below).  
2. **Custom domain, or the default Firebase URL for v1?** Default Firebase URL for now.  
3. **Unreviewed Spanish summaries:** fall back to English, with a note saying the summary is only available in English. Reflected in section 5\.  
4. **Who is the Spanish reviewer?** Ian.  
5. **Approve the starter tags for `fields_of_study` and `demographics`** — still open, see below.  
6. **Site name:** Paso a Paso.

### Still open

7. **Approve the starter tags** for `fields_of_study` (`stem`, `cs`, `nursing`, `education`, `hospitality`, `business`) and `demographics` (`hispanic`, `first_gen`, `female`, `african_american`, `aapi`, `native_american`). They are enforced as enums in `scripts/validate.py` today, so nothing breaks either way, but the filter UI in Phase 2 is built from this list.  
8. **Custom domain or a second Hosting site — decide by Oct 19.** The default Firebase URL covers the workshop; this is about what goes on the poster and QR code longer term.  
9. **Spanish register: `tú` or `usted`?** The current drafts mix registers and no strings have been changed pending this decision. It matters because the audience is both students (`tú` reads natural) and parents (`usted` reads respectful). Whatever is chosen applies to every string in `es.json` and to every scholarship summary.  
10. **Confirm the workshop year is 2026** and replace `WORKSHOP_DATE_TBD` in section 1 with the full date.