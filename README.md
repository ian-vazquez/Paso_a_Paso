# Paso a Paso — El Paso Scholarship Finder

A free, bilingual (English/Spanish) scholarship search site for El Paso-area high
school students and their families.

**No accounts. No cookies. No analytics. No third-party scripts.** The only thing
the site stores is the visitor's language choice, in their own browser. That claim
is on the page, so it has to stay literally true — see `CLAUDE.md` for the rules
that protect it.

`CLAUDE.md` is the source of truth for this project. If this README ever
contradicts it, `CLAUDE.md` wins.

---

## Requirements

| Tool | Version | Why |
| :--- | :--- | :--- |
| Node.js | 24 or newer | Vite dev server and build; enforced by `engines` in package.json |
| Python | 3.10 or newer | `scripts/validate.py` (standard library only) |
| Firebase CLI | any recent | only needed for manual deploys; CI deploys on its own |

---

## Getting started

```bash
npm install        # first time only
npm run dev        # http://localhost:5173
```

Other commands:

```bash
npm run build      # production build into dist/
npm run preview    # serve the built site locally
npm run validate   # check data/scholarships.json
npm test           # runs tests/ — empty until Phase 2 adds search.js tests

python scripts/test_validate.py   # tests for the validator itself
python scripts/check_i18n.py      # en.json and es.json must stay in step
```

---

## Project layout

```
index.html                 the page shell; text comes from the i18n files
src/main.js                entry point: language toggle, and later the search UI
src/search.js              filtering + sorting. PURE FUNCTIONS ONLY, no DOM
src/render.js              all DOM building
src/i18n.js                the translation helper (no library)
src/i18n/en.json           English UI strings
src/i18n/es.json           Spanish UI strings
src/styles.css             all styles; system fonts, no web font request
data/scholarships.json     the scholarship list — the heart of the project
scripts/validate.py        schema + sanity checks; CI runs this
scripts/test_validate.py   tests for the validator
scripts/check_i18n.py      en/es key parity; CI runs this too
```

Two rules about this layout are worth repeating:

- **`search.js` must never touch the DOM.** The Phase 6 AI feature will import
  the same filtering logic server-side. DOM code in there would break that.
- **No user-facing string belongs in a `.js`, `.html` or `.css` file.** Every one
  comes from `src/i18n/en.json` and `src/i18n/es.json`.

---

## How to add a scholarship

This is the part that matters most. The site's promise is that every entry is
real, sourced, and dated. **Only add facts you read on the sponsor's own page.**

### 1. Verify it first

Open the sponsor's official page. Not a scholarship aggregator, not a blog, not
an AI answer. If a fact is not on that page, it is unknown.

### 2. Copy the template

Add an object to the array in `data/scholarships.json`:

```json
{
  "id": "sponsor-name-2026",
  "name": "Scholarship name as the sponsor writes it",
  "sponsor": "Who gives the money",
  "amount_min": null,
  "amount_max": null,
  "amount_display": { "en": "", "es": "" },
  "renewable": null,
  "deadline": null,
  "cycle_status": "unknown",
  "opens_month": null,
  "categories": [],
  "grade_levels": [],
  "residency": "national",
  "districts": [],
  "schools": [],
  "eligible_institutions": [],
  "degree_types": [],
  "gpa_min": null,
  "fields_of_study": [],
  "demographics": [],
  "requirements": {
    "essay_required": null,
    "recs_needed": null,
    "fafsa_required": null,
    "accepts_tasfa": null,
    "citizenship_required": null,
    "interview": null,
    "other": { "en": "", "es": "" }
  },
  "application_language": "en",
  "source_url": "https://",
  "apply_url": null,
  "summary": { "en": "", "es": "" },
  "notes": { "en": "", "es": "" },
  "translation_reviewed": false,
  "last_verified": "YYYY-MM-DD"
}
```

### 3. The one rule that matters most

> **Unknown is `null`. Never a guess.**

A `null` shows on the site as "Not listed — check source" / "No especificado —
consulta la fuente". That is honest and useful. A guessed deadline can cost a
student a scholarship. If the page is vague, leave the structured field `null`
and explain what it actually says in `notes`.

`""` (empty string) is the "unknown" value for the bilingual text blocks;
`null` is for everything else.

### 4. Field notes

| Field | What goes in it |
| :--- | :--- |
| `id` | lowercase, hyphens, no spaces; must be unique and stable — it may end up in a shared URL |
| `amount_min` / `amount_max` | numbers, for sorting. Set both to `null` if the award varies |
| `amount_display` | what a student reads, e.g. "Varies; up to $2,000". Free text |
| `cycle_status` | `open`, `upcoming`, `closed_reopens`, `rolling`, `unknown` |
| `opens_month` | month number 1–12 for when applications open; `null` if not stated |
| `categories` | at least one: `merit`, `need_based`, `first_gen`, `regional`, `demographic`, `field_specific` |
| `grade_levels` | `hs_junior`, `hs_senior`, `college`. Empty means it does not say |
| `residency` | one of `el_paso_county`, `specific_districts`, `specific_schools`, `texas`, `national` |
| `districts` / `schools` | fill these in when `residency` narrows to specific ones |
| `eligible_institutions` | empty means any school |
| `degree_types` | `associate`, `bachelor`, `trade_technical` |
| `gpa_min` | the number the sponsor states, e.g. `2.5`. `null` if no GPA rule |
| `fields_of_study` | empty means any field. Otherwise: `stem`, `cs`, `nursing`, `education`, `hospitality`, `business` |
| `demographics` | empty means no restriction. Otherwise: `hispanic`, `first_gen`, `female`, `african_american`, `aapi`, `native_american`, `military_connected` |
| `requirements.recs_needed` | how many letters, as a number |
| `application_language` | `en`, `es`, or `both` — the language of the **application form**, not the summary |
| `source_url` | the page you verified against. Shown on every card. Required, `https://` |
| `apply_url` | the form itself, if it is a different page. `null` otherwise |
| `summary.en` | 1–3 plain sentences. Required. Write for a 17-year-old, not a grant officer |
| `translation_reviewed` | `false` until a fluent speaker has read the Spanish. Only Ian sets this to `true` |
| `last_verified` | the date **you** opened the source page. Only Ian sets this |

Adding a tag that is not in the `fields_of_study` or `demographics` lists needs
approval first, because the filter UI and the Phase 6 pre-filter both read them.
The lists live in `scripts/validate.py`, so a new tag shows up in a diff. A new
tag also needs a label in **both** `en.json` and `es.json`, or `check_i18n.py`
fails the build — which is the point: an unlabelled tag would render as a raw
`snake_case` string on a card.

### 5. Validate before committing

```bash
npm run validate
```

Errors must be fixed — CI will refuse to deploy. Warnings are prompts for a
human, not blockers:

| Warning | What to do |
| :--- | :--- |
| `summary.es` is empty | Spanish visitors see the English summary with a note. Fine for now |
| `translation_reviewed is false` | a fluent speaker still needs to read the Spanish |
| `last_verified` older than 45 days | re-open the source page and re-date it |
| deadline within 14 days | confirm it is still accurate before the next deploy |
| 4+ requirement fields null | the entry could use more research, if the source supports it |
| `open` but the deadline has passed | change `cycle_status`; the site treats it as closed regardless |
| placeholder example entry | the two `example-` entries must be deleted before launch |

Useful flag when checking date-sensitive rules:

```bash
python scripts/validate.py --today 2026-10-15   # pretend it is workshop day
```

### 6. Spanish translations

Claude drafts Spanish text and always leaves `translation_reviewed: false`. A
fluent speaker reads it and flips that flag. Until then the site prefers the
English summary over unreviewed Spanish, with a note saying so — being clear
beats being wrong in two languages.

`src/i18n/es.json` carries a `_meta` block with the same caveat for the UI
strings. Keys starting with `_` are ignored by `src/i18n.js`.

---

## Re-verification

The site's trust rests on `last_verified`. Once a month:

```bash
npm run validate
```

Work the "older than 45 days" warnings: open each source page, correct anything
that changed, and re-date the entry. If a link is dead, fix or remove the entry —
never leave a card pointing at a 404.

---

## Deploying

Deploys are automatic. Nobody should need to run `firebase deploy` by hand.

| Event | What happens |
| :--- | :--- |
| push to any branch | `validate.yml` checks the data, runs the validator's tests, and checks en/es parity |
| open a pull request | data is validated, the site is built, and a temporary preview URL is posted to the PR |
| merge to `main` | data is validated, the site is built, and it deploys to production |

Validation runs *before* the build in both Firebase workflows, so malformed data
can never reach production. All three checks run in all three workflows:

```bash
python3 scripts/validate.py        # the data
python3 scripts/test_validate.py   # the validator's own tests
python3 scripts/check_i18n.py      # English and Spanish in step
```

`check_i18n.py` is there because "bilingual from the start" fails quietly: a key
added to `en.json` and forgotten in `es.json` does not crash anything — it just
puts an English word in the middle of a Spanish page, where nobody notices until
a student does.

**Merging to `main` is a production deploy, so only Ian merges.** Work happens on
branches named after their phase (`phase-0-setup`, `phase-2-search`, …).

Firebase project: `scholarship-site-fd70f`. The deploy credential lives in the
GitHub Actions secret `FIREBASE_SERVICE_ACCOUNT_SCHOLARSHIP_SITE_FD70F`. It is
never in this repo, and it never gets pasted into a chat.

`firebase.json` also sets a few response headers: long-lived caching for hashed
assets in `/assets/**`, no caching for `index.html` so a deploy is picked up
immediately, `X-Content-Type-Options: nosniff`, and `Referrer-Policy: no-referrer`
so that clicking through to a scholarship does not tell the sponsor where the
student came from.

---

## Accessibility and mobile

Most visitors arrive by QR code on a phone, so the baseline is:

- works at 360px wide, with tap targets at least 44px tall
- semantic HTML, a label on every input, visible focus rings, full keyboard use
- WCAG AA contrast in both the light and dark palettes
- no layout that breaks when Spanish runs 20–30% longer than English

Check the Spanish layout before merging anything. It is the easy thing to forget.
