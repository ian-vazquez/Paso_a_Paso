/**
 * search.js — filtering and sorting. Built in Phase 2.
 *
 * Hard rule (CLAUDE.md section 3): NO DOM code in this file, ever. Everything
 * here must be a pure function of (scholarships, criteria) so that:
 *   1. it can be unit tested with plain `node --test`, and
 *   2. the Phase 6 Cloud Function can import the exact same logic to pre-filter
 *      candidates before calling the Claude API.
 *
 * Planned exports, for reference while reviewing Phase 2:
 *
 *   filterScholarships(scholarships, criteria) -> Scholarship[]
 *     criteria: { query, categories[], gpa, residency[], degreeTypes[],
 *                 noEssay, noCitizenship, acceptsTasfa, includeClosed, lang }
 *
 *   sortScholarships(scholarships, sortKey) -> Scholarship[]
 *     sortKey: 'deadline' (default) | 'amount'
 *
 *   criteriaFromQueryString(search) -> criteria
 *   criteriaToQueryString(criteria) -> string
 *     Filter state lives in the URL only, so a link can be shared. It is never
 *     written to storage.
 */

export {};
