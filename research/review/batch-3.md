# Batch 3 — evidence for review

Drafted under the Evidence Rule (CLAUDE.md §4). Every non-null field below has a
verbatim quote from a page that was actually fetched, plus that page's URL. No
quote → the field is `null`. No inference, no memory, no aggregators.

`last_verified` is `null` on every entry. The validator therefore fails until Ian
verifies each one — that is intentional.

**Status of this batch: incomplete.** Candidates 1–14 are covered below.
Candidates 15–50 have not been fetched yet. See "Not yet attempted" at the end.

## ⚠ Time-critical, found while fetching

| Entry | Deadline on the page | Note |
|---|---|---|
| coca-cola-scholars | **September 30, 2026, 5 pm Eastern** | **Closes today.** Quote: "Wednesday, September 30, 2026, at 5 pm Eastern" |
| questbridge-national-college-match | **October 1, 2026** | **Closes tomorrow**, before the Oct 15 workshop |
| jack-kent-cooke-college | November 11, 2026 | 42 days out |
| chick-fil-a-community-scholars | November 3, 2026 | 34 days out |

## APPLIED — corrections to unverified entries

These entries had `last_verified: null`, so they were rewritten in place from
fetched evidence. They were drafted from `candidates.json` prose before, and the
sponsor pages contradicted them:

| Entry | Field | Was | Now | Quote |
|---|---|---|---|---|
| utep-terry-scholars | `residency` | `national` | `texas` | "be a Texas resident AND graduate from a Texas high school or home-school program in Texas" |
| utep-terry-scholars | `amount_display` | "Full cost of attendance" | *(empty)* | No amount stated anywhere on the page |
| utep-terry-scholars | `sponsor` | inferred | The Terry Foundation | "The Terry Foundation" |
| dell-scholars | `residency` | `national` | `texas` | "Be a high school senior graduating from a Texas high school" |
| jack-kent-cooke-college | `renewable` | `true` | `null` | "renewable for up to 4 years" is not on either fetched page; the three-year figure belongs to the separate Transfer scholarship |
| jack-kent-cooke-college | `essay_required` / `recs_needed` | `true` / `2` | `null` / `null` | Neither is stated on the fetched pages |
| jack-kent-cooke-college | `deadline` | `null` | `2026-11-11` | "will close on November 11, 2026" |

## NOT APPLIED — proposed changes to entries Ian has already verified

These five carry `last_verified: 2026-09-30`. **Nothing was changed on them.**
Rewriting a fact under a verified entry would make that date attest to values Ian
never saw, so the disagreements are listed here for him to apply or reject.

### sisd-foundation — the sponsor page has been updated since the research
| Field | In the file | Page says | Quote |
|---|---|---|---|
| `deadline` | `null` | **2027-02-14** | "**February 14, 2027:** Completed application with all supporting documentation is due" |
| `cycle_status` | `unknown` | `upcoming` | The page now shows the Class-of-2027 cycle. **The stale-deadline flag is resolved** — no need to call (915) 937-1618. |
| `amount_min` / `amount_max` | `null` / `null` | 3500 / 3500 | "$3,500 Foundation scholarships" |
| `degree_types` | `[]` | `["associate","bachelor","trade_technical"]` | "Recipients may attend a community college, a 4-year university, or a trade/technical school" |
| `essay_required` | `null` | `true` | "Write a personal essay" |

### braden-aboud-b-strong-utep
| Field | In the file | Page says | Quote |
|---|---|---|---|
| `deadline` | `null` | **2026-04-03 (already past)** | "April 3rd, 2026" |
| `cycle_status` | `upcoming` | `unknown` | The page still shows the 2026 cycle and never says it reopens. As `upcoming` with no deadline, students are told to come back with no date. |

### el-paso-community-foundation
| Field | In the file | Page says | Quote |
|---|---|---|---|
| `amount_min` / `amount_max` | 500 / 5000 | **no amount stated** | The portal page states no amount at all. The "typically $500-$5,000" figure came from `candidates.json`, not the page. |
| `opens_month` | `null` | 1 | "Applications open January 1" |
| `cycle_status` | `upcoming` | `unknown` | No quote states the current status |

### paso-del-norte-community-foundation
| Field | In the file | Page says | Quote |
|---|---|---|---|
| `grade_levels` | `["hs_senior"]` | per-fund only | "high school seniors" appears for individual funds, not for the portal as a whole; other funds are for college and graduate students |

### episd-education-foundation
No comparison possible — the page could not be fetched. Ian verified this one
himself, so his values stand.

---

## el-paso-community-foundation
Pages fetched: https://epcf.org/grants-and-scholarships/apply-for-a-scholarship

| Field | Value | Quote | Page |
|---|---|---|---|
| opens_month | 1 | "Applications open January 1" | https://epcf.org/grants-and-scholarships/apply-for-a-scholarship |
| grade_levels | ["hs_senior"] | "High school seniors may be eligible" | https://epcf.org/grants-and-scholarships/apply-for-a-scholarship |
| apply_url | https://www.grantinterface.com/Home/Logon?urlkey=epcfscholarship | "https://www.grantinterface.com/Home/Logon?urlkey=epcfscholarship" | https://epcf.org/grants-and-scholarships/apply-for-a-scholarship |

Left null (no quote found): amount_min, amount_max, amount_display, renewable, deadline, gpa_min, districts, schools, eligible_institutions, degree_types, fields_of_study, demographics, essay_required, recs_needed, fafsa_required, accepts_tasfa, citizenship_required, interview

**deadline stays null on purpose.** The page says "Applications open January 1 and are due May 1" — **no year**, so it cannot become an ISO date.

**Judgment calls for Ian to approve or reject:**
- `residency: el_paso_county` — the page says "students in the El Paso region", not "county". `residency` cannot be null, so a value had to be chosen.
- `cycle_status: unknown` — no quote states whether it is currently open.
- This is an **umbrella portal**. The page lists ~19 named funds (Texas Education Scholarship, Makios Technology Fund, Chris Powers Scholarship Fund, …) each with its own rules. Per-fund facts are NOT recorded on this umbrella entry.

Couldn't fetch: (none)

---

## paso-del-norte-community-foundation
Pages fetched: https://pdnfoundation.org/grants-and-scholarships/scholarships

| Field | Value | Quote | Page |
|---|---|---|---|
| — | — | No fact on this page applies to the umbrella entry itself | — |

Left null (no quote found): amount_min, amount_max, amount_display, renewable, deadline, opens_month, gpa_min, grade_levels, districts, schools, eligible_institutions, degree_types, fields_of_study, demographics, essay_required, recs_needed, fafsa_required, accepts_tasfa, citizenship_required, interview

**deadline stays null on purpose.** "Select scholarship application deadlines have been extended on our new platform, Scholarship360 until April 17th" — **no year**.

**Judgment calls for Ian to approve or reject:**
- `residency: el_paso_county` — supported by "El Paso County, Texas" appearing for multiple funds, but that is per-fund, not umbrella-wide. Some funds are Doña Ana County (New Mexico) or Arizona.
- `cycle_status: unknown` — no quote.
- **This entry covers 31 separate named funds** with GPA minimums ranging from 2.5 to 3.2, different districts, and restrictions including "female high school seniors", "young mothers in El Paso County", "first-generation students" and "military veterans". None of that is recorded here, because it belongs to individual funds. **Recommendation: split the productive ones into their own entries** — several are strong `first_gen` and `demographic` candidates, which the list currently has none of.

Couldn't fetch: (none)

---

## sisd-foundation
Pages fetched: https://sisdfoundation.org/apply-now/

| Field | Value | Quote | Page |
|---|---|---|---|
| deadline | 2027-02-14 | "**February 14, 2027:** Completed application with all supporting documentation is due" | https://sisdfoundation.org/apply-now/ |
| amount_min / amount_max | 3500 / 3500 | "$3,500 Foundation scholarships" | https://sisdfoundation.org/apply-now/ |
| residency | specific_districts | "Must have attended an SISD high school for a minimum of 2 full school years" | https://sisdfoundation.org/apply-now/ |
| districts | ["Socorro ISD"] | "Must have attended an SISD high school for a minimum of 2 full school years" | https://sisdfoundation.org/apply-now/ |
| degree_types | ["associate","bachelor","trade_technical"] | "Recipients may attend a community college, a 4-year university, or a trade/technical school" | https://sisdfoundation.org/apply-now/ |
| essay_required | true | "Write a personal essay" | https://sisdfoundation.org/apply-now/ |

Left null (no quote found): renewable, opens_month, gpa_min, schools, eligible_institutions, fields_of_study, demographics, recs_needed, fafsa_required, accepts_tasfa, citizenship_required, interview

**Judgment calls for Ian to approve or reject:**
- `grade_levels: []` — the page says "Must be graduating in 2026-2027 school year" but never the words "senior". Strict reading of the rule leaves this empty. **Promote to `["hs_senior"]`?**
- `districts: ["Socorro ISD"]` — the page says "SISD"; I expanded the abbreviation.
- `recs_needed: null` — "You may submit up to 2 letters of recommendation" is optional and a range, so it is not a required count.
- `cycle_status: upcoming` — supported by a future deadline, but no quote states the status.
- The page also lists 7 other distinct awards ($1,000–$2,500, one at $1,051) with their own GPA rules (3.5 for Fine Arts, 2.75 for Fifty-One). Not recorded here.

Couldn't fetch: (none)

---

## episd-education-foundation
Pages fetched: (none — attempt failed)

| Field | Value | Quote | Page |
|---|---|---|---|
| — | — | — | — |

**Couldn't fetch: https://www.episd.org/educationfoundation** — the page content truncates before any scholarship text is reachable, on two separate attempts with different prompts. Nothing could be verified.

Per Evidence Rule item 3, **this entry's fields are left for Ian.** Note that the version currently in `data/scholarships.json` (amount_max 5000, essay_required true, districts ["El Paso ISD"]) came from `candidates.json` prose and has **no evidence behind it**.

---

## braden-aboud-b-strong-utep
Pages fetched: https://bstrongelpaso.org/grants-scholarships

| Field | Value | Quote | Page |
|---|---|---|---|
| amount_min / amount_max | 2000 / 2000 | "One year, non-renewable award of **$2,000.**" | https://bstrongelpaso.org/grants-scholarships |
| renewable | false | "One year, non-renewable award" | https://bstrongelpaso.org/grants-scholarships |
| deadline | 2026-04-03 | "April 3rd, 2026" | https://bstrongelpaso.org/grants-scholarships |
| grade_levels | ["hs_senior"] | "high school seniors" | https://bstrongelpaso.org/grants-scholarships |
| eligible_institutions | ["UTEP"] | "accepted to and plan to attend the University of Texas at El Paso" | https://bstrongelpaso.org/grants-scholarships |
| recs_needed | 2 | "two letters of recommendation" | https://bstrongelpaso.org/grants-scholarships |
| apply_url | https://scholarships360.org/scholarships/search/braden-aboud-memorial-foundation-scholarship/ | "https://scholarships360.org/scholarships/search/braden-aboud-memorial-foundation-scholarship/" | https://bstrongelpaso.org/grants-scholarships |

Left null (no quote found): opens_month, gpa_min, districts, schools, degree_types, fields_of_study, demographics, essay_required, fafsa_required, accepts_tasfa, citizenship_required, interview

**Judgment calls for Ian to approve or reject:**
- `deadline: 2026-04-03` is **in the past** — the sponsor page still shows the 2026 cycle. `cycle_status` is therefore `unknown`, not `upcoming`, since no quote says it reopens.
- `residency: el_paso_county` — page says "graduating seniors from the El Paso area".
- `sponsor: "B STRONG El Paso"` — inferred from the domain; the page does not state a legal entity name.

Couldn't fetch: (none)

---

## utep-terry-scholars
Pages fetched: https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/

| Field | Value | Quote | Page |
|---|---|---|---|
| deadline | 2027-01-11 | "January 11th, 2027 at 11:59 pm MST" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| residency | texas | "be a Texas resident AND graduate from a Texas high school or home-school program in Texas" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| grade_levels | ["hs_senior"] | "CURRENT high school senior" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| gpa_min | 3.0 | "hold a minimum GPA of 3.0" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| citizenship_required | true | "be a U.S. citizen or permanent resident" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| fafsa_required | true | "REQUIRED to be eligible for the Terry Foundation Scholarship" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| essay_required | true | "Essay Questions (500 WORD max)" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| recs_needed | 1 | "1 letter must be uploaded" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| interview | true | "interview with the Terry Foundation on the UTEP campus sometime in mid-March" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| sponsor | The Terry Foundation | "The Terry Foundation" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |
| apply_url | https://www.utep.edu/scholarmine | "utep.edu/scholarmine" | https://www.utep.edu/student-affairs/terryscholars/become-a-scholar/ |

Left null (no quote found): amount_min, amount_max, amount_display, renewable, opens_month, districts, schools, degree_types, fields_of_study, demographics, accepts_tasfa

**`amount_display` is now empty.** The previous draft said "Full cost of attendance", taken from `candidates.json` prose. The page states no amount, so under the rule it goes blank and the card will show "Not listed — check source".

**Judgment calls for Ian to approve or reject:**
- `eligible_institutions: ["UTEP"]` — the page is UTEP's own Terry Scholars page and requires UTEP admission, but no single sentence states "UTEP only".
- `categories: ["merit","need_based"]` — supported by the GPA minimum and the FAFSA requirement, but the page does not use the words merit or need-based.

Couldn't fetch: (none)

---

## dell-scholars
Pages fetched: https://www.dellscholars.org/ , https://www.dellscholars.org/students/

| Field | Value | Quote | Page |
|---|---|---|---|
| amount_min / amount_max | 20000 / 20000 | "A $20,000 flexible scholarship covers tuition and housing—plus a laptop, book credits, and emergency funds" | https://www.dellscholars.org/students/ |
| residency | texas | "Be a high school senior graduating from a Texas high school" | https://www.dellscholars.org/students/ |
| grade_levels | ["hs_senior"] | "Be a high school senior graduating from a Texas high school" | https://www.dellscholars.org/students/ |
| gpa_min | 2.4 | "Have at least a 2.4 GPA" | https://www.dellscholars.org/students/ |
| sponsor | Michael & Susan Dell Foundation | "Michael & Susan Dell Foundation" | https://www.dellscholars.org/ |
| apply_url | https://apply.dellscholars.org/Account/Login | "https://apply.dellscholars.org/Account/Login" | https://www.dellscholars.org/students/ |

Left null (no quote found): renewable, deadline, opens_month, districts, schools, eligible_institutions, fields_of_study, demographics, essay_required, recs_needed, accepts_tasfa, citizenship_required, interview

**deadline stays null on purpose.** The Important Dates block shows "JAN 12" with **no year on the page**. Needs confirming.

**Judgment calls for Ian to approve or reject:**
- `eligible_institutions: []` — the page restricts to "an accredited four-year public college or university in Texas" but names no institutions, so the list stays empty and the restriction is recorded in `requirements.other`.
- `degree_types: []` — "four-year public college" implies a bachelor's but the page never says "bachelor". **Promote to `["bachelor"]`?**
- `fafsa_required: null` — "FAFSA Submission Summary (FSS)" is required **for finalists**, not to apply.
- `categories: ["need_based"]` — "Be Pell Grant eligible" supports need; the page does **not** state a first-generation requirement, so `first_gen` is NOT applied despite your `need_based_first_gen` bucket.

Couldn't fetch: (none)

---

## horatio-alger-national-texas
Pages fetched: (none — attempt failed)

**Couldn't fetch: https://scholars.horatioalger.org/** — HTTP 403 Forbidden.

Per Evidence Rule item 3, **this entry's fields are left for Ian.** The values currently in `data/scholarships.json` (amount 10000–25000, essay_required true, residency national) came from `candidates.json` prose and have **no evidence behind them**.

---

## jack-kent-cooke-college
Pages fetched: https://www.jkcf.org/our-scholarships/ , https://www.jkcf.org/our-scholarships/college-scholarship-program/

| Field | Value | Quote | Page |
|---|---|---|---|
| amount_max | 55000 | "as much as $55,000 per year to pursue a bachelor's degree at any accredited undergraduate institution" | https://www.jkcf.org/our-scholarships/college-scholarship-program/ |
| deadline | 2026-11-11 | "will close on November 11, 2026" | https://www.jkcf.org/our-scholarships/college-scholarship-program/ |
| grade_levels | ["hs_senior"] | "high school seniors" | https://www.jkcf.org/our-scholarships/college-scholarship-program/ |
| degree_types | ["bachelor"] | "bachelor's degree" | https://www.jkcf.org/our-scholarships/college-scholarship-program/ |
| apply_url | https://apply.commonapp.org/login | "https://apply.commonapp.org/login" | https://www.jkcf.org/our-scholarships/college-scholarship-program/ |

Left null (no quote found): amount_min, renewable, opens_month, gpa_min, districts, schools, eligible_institutions, fields_of_study, demographics, essay_required, recs_needed, fafsa_required, accepts_tasfa, citizenship_required, interview

**`renewable` went back to null.** The previous draft said `true`; the quote "renewable for up to 4 years" came from `candidates.json`, not from either fetched page. The transfer scholarship says "up to three years", which is a different program.

**`essay_required` and `recs_needed` went back to null** for the same reason — the previous `true` / `2` came from prose.

**Still unresolved schema problem:** `amount_max: 55000` is **per year** ("$55,000 per year"), while dell-scholars' 20000 is a one-time total. Sorting by "largest amount" will compare them directly and mislead.

**Judgment calls for Ian to approve or reject:**
- `residency: national` — supported only by "any accredited undergraduate institution"; no residency sentence exists.
- `fields_of_study: []` — "Ability to pursue any area of study".

Couldn't fetch: (none)

---

## questbridge-national-college-match
Pages fetched: https://www.questbridge.org/apply-to-college/programs/national-college-match/apply/dates-and-deadlines

| Field | Value | Quote | Page |
|---|---|---|---|
| deadline | 2026-10-01 | "October 1" with "10 01 2026" shown in the page header | https://www.questbridge.org/apply-to-college/programs/national-college-match/apply/dates-and-deadlines |
| grade_levels | ["hs_senior"] | "Eligible high school seniors" | https://www.questbridge.org/apply-to-college/programs/national-college-match/apply/dates-and-deadlines |
| apply_url | https://apply.questbridge.org/portal/apply | "https://apply.questbridge.org/portal/apply" | https://www.questbridge.org/apply-to-college/programs/national-college-match/apply/dates-and-deadlines |

Left null (no quote found): amount_min, amount_max, renewable, opens_month, gpa_min, residency-specific fields, districts, schools, eligible_institutions, degree_types, fields_of_study, demographics, essay_required, recs_needed, fafsa_required, accepts_tasfa, citizenship_required, interview

**⚠ Deadline is 2026-10-01 — the day after this was drafted, and before the Oct 15 workshop.** Verify before the site shows it.

**Judgment calls for Ian to approve or reject:**
- `amount_display: "full four-year scholarship"` — quoted from the page, but it is a phrase, not an amount.
- `residency: national` — no residency sentence on the page.

Couldn't fetch: (none)

---

## chick-fil-a-community-scholars
Pages fetched: https://www.chick-fil-a.com/community-scholars/application-tips

| Field | Value | Quote | Page |
|---|---|---|---|
| deadline | 2026-11-03 | "Applications close November 3, 2026" | https://www.chick-fil-a.com/community-scholars/application-tips |
| gpa_min | 3.0 | "minimum cumulative grade point average (GPA) of 3.0 on a 4.0 scale" | https://www.chick-fil-a.com/community-scholars/application-tips |
| grade_levels | ["college"] | "postsecondary undergraduate or graduate student or planning to enroll" | https://www.chick-fil-a.com/community-scholars/application-tips |
| degree_types | ["associate","bachelor","trade_technical"] | "accredited two- or four-year college, university or vocational-technical school" | https://www.chick-fil-a.com/community-scholars/application-tips |
| apply_url | https://scholarshipamerica.org/scholarship/cfacommunityscholars/ | "https://scholarshipamerica.org/scholarship/cfacommunityscholars/" | https://www.chick-fil-a.com/community-scholars/application-tips |

Left null (no quote found): amount_min, amount_max, amount_display, renewable, opens_month, districts, schools, eligible_institutions, fields_of_study, demographics, essay_required, recs_needed, fafsa_required, accepts_tasfa, citizenship_required, interview

**Judgment calls for Ian to approve or reject:**
- `residency: national` — the page says "Be a resident in the United States, Puerto Rico or Canada". **Canada is outside every enum value**, so `national` slightly overstates and slightly understates at once.
- `grade_levels` — "or planning to enroll" may cover high school seniors; I only recorded `college`. **Add `hs_senior`?**
- **Disqualifier recorded in `requirements.other`:** "Not be employed at a Chick-fil-A® restaurant or Chick-fil-A, Inc." — worth surfacing on the card, since a student working there would waste the application.

Couldn't fetch: (none)

---

## hacu-dennys-hungry-for-education
Pages fetched: (none — attempt failed)

**Couldn't fetch: https://dennys.com/hfe-scholarships** — HTTP 403 Forbidden.

Per Evidence Rule item 3, this entry's fields are left for Ian. No entry was drafted.

---

## coca-cola-scholars
Pages fetched: https://www.coca-colascholarsfoundation.org/apply/

| Field | Value | Quote | Page |
|---|---|---|---|
| amount_min / amount_max | 20000 / 20000 | "150 Coca-Cola Scholars are selected each year to receive this $20,000 scholarship." | https://www.coca-colascholarsfoundation.org/apply/ |
| deadline | 2026-09-30 | "Wednesday, September 30, 2026, at 5 pm Eastern" | https://www.coca-colascholarsfoundation.org/apply/ |
| gpa_min | 3.0 | "Able to verify a minimum overall B/3.0 GPA in high school coursework" | https://www.coca-colascholarsfoundation.org/apply/ |
| grade_levels | ["hs_senior"] | "will graduate high school during the 2026-2027 academic school year" | https://www.coca-colascholarsfoundation.org/apply/ |
| citizenship_required | true | "U.S. Citizens, U.S. Nationals, U.S. Permanent Residents, Refugees, Asylees, Cuban-Haitian Entrants, or Humanitarian Parolees" | https://www.coca-colascholarsfoundation.org/apply/ |
| interview | true | "250 will advance as Regional Finalists and will participate in a final interview" | https://www.coca-colascholarsfoundation.org/apply/ |
| apply_url | https://webportalapp.com/sp/login/cokescholar | "https://webportalapp.com/sp/login/cokescholar" | https://www.coca-colascholarsfoundation.org/apply/ |

Left null (no quote found): renewable, opens_month, districts, schools, eligible_institutions, degree_types, fields_of_study, demographics, recs_needed, fafsa_required, accepts_tasfa

**⚠ Deadline is today, 2026-09-30, 5 pm Eastern.**

**Judgment calls for Ian to approve or reject:**
- `citizenship_required: true` **needs care on the card.** The page admits "Refugees, Asylees, Cuban-Haitian Entrants, or Humanitarian Parolees", so a blunt "U.S. citizenship required" badge would wrongly turn away students who qualify. The full quote is in `requirements.other`.
- `essay_required: null` — "Phase 1 application…requires no essays" applies only to Phase 1; Phase 2 requirements are not fully stated.
- `categories: ["merit"]` — supported by "The Coca-Cola Scholars Program scholarship is an achievement-based scholarship", which also rules out `need_based`.
- `residency: national` — "one of the 50 U.S. states, the District of Columbia, Puerto Rico, or select DoD schools".

Couldn't fetch: (none)

---

# Summary

## Couldn't fetch (fields left for Ian)
| Entry | URL | Reason |
|---|---|---|
| episd-education-foundation | https://www.episd.org/educationfoundation | Content truncates before any scholarship text; two attempts |
| horatio-alger-national-texas | https://scholars.horatioalger.org/ | HTTP 403 Forbidden |
| hacu-dennys-hungry-for-education | https://dennys.com/hfe-scholarships | HTTP 403 Forbidden |

## Excluded
| Entry | Reason |
|---|---|
| GECU Robert A. Cunningham Memorial (candidate 7) | In `research/rejected.md`: "different credit union (gecreditunion.org), not El Paso's GECU. Cut 2026-09-29." Ian had already removed it from `data/scholarships.json`; no action was needed. Note candidate 32, GECU Financial Literacy, is on `gecu.com` and is **not** excluded. |

## Not yet attempted (candidates 15–50)
Elks MVS · National Honor Society · Texas PTA · GE-Reagan · Regions Riding Forward ·
HSF · McDonald's HACER · Jackie Robinson · NAACP LDF Herbert Lehman · UNCF STEM ·
APIA Scholars · EPHCC Foundation · El Paso Electric · FirstLight Community Foundation ·
MountainStar All-Star · EPCC Foundation · Makios Technology Fund · GECU Financial
Literacy · Sallie Mae Bridging the Dream · Amazon Future Engineer · Terry Foundation
UT Austin track · Greater Texas Foundation · UT System Promise+ · NACME · Foot Locker ·
VFW Voice of Democracy · American Legion Texas Oratorical · Davidson Fellows ·
Ayn Rand Institute · Optimist International · TheDream.US · Point Foundation · AISES ·
SWE · Anne Ford & Allegra Ford Thomas · Hispanic Scholarship Consortium

Note: **El Paso Electric (27) and Makios Technology Fund (31) share candidate 1's
source URL** (the EPCF portal). Makios appears there — "El Paso County students",
"careers in Information Technology" — but **El Paso Electric is not named on that
page at all**, so it may need a different source.
