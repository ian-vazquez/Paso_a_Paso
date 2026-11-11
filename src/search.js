/**
 * search.js — deciding which scholarships appear, and in what order.
 *
 * Hard rule (CLAUDE.md section 3): NO DOM code in this file, ever. Everything
 * here must be a pure function of its arguments so that:
 *   1. it can be unit tested with plain `node --test`, and
 *   2. the Phase 6 Cloud Function can import the exact same logic to pre-filter
 *      candidates before calling the Claude API.
 *
 * v1 (Nov 2026 workshop) has no filters, only two sections: "Open now" and
 * "Opening soon". The filter and sort functions planned for January 2027
 * (filterScholarships, sortScholarships, URL query-string helpers) will be
 * added here alongside these.
 *
 * Dates are compared as ISO strings ("2026-12-15"). That works because the
 * format sorts the same way as the calendar, and it avoids any time-zone math:
 * `today` is the student's own local date, passed in by the caller.
 */

/** A Date's local calendar day as "YYYY-MM-DD". */
export function toISODate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

/** True once the deadline day is over. The deadline day itself still counts as open. */
export function deadlinePassed(entry, today) {
  return entry.deadline != null && entry.deadline < today;
}

/**
 * Is this entry open to apply to today?
 *
 * An `open` entry whose deadline has passed is treated as closed, even if
 * nobody has updated its cycle_status yet (CLAUDE.md section 4, the "open but
 * deadline in the past" rule). This is what takes Burger King off the page
 * after Dec 15 with no data change.
 */
export function isOpenNow(entry, today) {
  const status = entry.cycle_status;
  return (status === 'open' || status === 'rolling') && !deadlinePassed(entry, today);
}

/** Soonest deadline first. No deadline (e.g. rolling) goes last, then by name. */
function byDeadline(a, b) {
  if (a.deadline !== b.deadline) {
    if (a.deadline == null) return 1;
    if (b.deadline == null) return -1;
    return a.deadline < b.deadline ? -1 : 1;
  }
  return a.name.localeCompare(b.name);
}

/** The "Open now" section: open entries, soonest deadline first. */
export function openNow(entries, today) {
  return entries.filter((e) => isOpenNow(e, today)).sort(byDeadline);
}

/**
 * The "Opening soon" section, grouped by the month each entry is expected to
 * open (`opens_month`).
 *
 * Returns [{ month, year, entries }], in calendar order starting from the
 * current month. A month earlier in the year than today's means next year
 * (in November, "1" is January of next year). Entries with no opens_month
 * form one last group with month and year set to null, so nothing is guessed.
 */
export function openingSoon(entries, today) {
  const [thisYear, thisMonth] = today.split('-').map(Number);

  const upcoming = entries.filter(
    (e) => e.cycle_status === 'upcoming' && !deadlinePassed(e, today)
  );

  const groups = new Map(); // key: months from now (0-11), or "none"
  for (const entry of upcoming) {
    const month = entry.opens_month;
    const key = month == null ? 'none' : (month - thisMonth + 12) % 12;
    if (!groups.has(key)) {
      groups.set(key, {
        month: month ?? null,
        year: month == null ? null : thisYear + (month < thisMonth ? 1 : 0),
        entries: [],
      });
    }
    groups.get(key).entries.push(entry);
  }

  const keys = [...groups.keys()].sort((a, b) => {
    if (a === 'none') return 1;
    if (b === 'none') return -1;
    return a - b;
  });
  return keys.map((key) => {
    const group = groups.get(key);
    group.entries.sort(byDeadline);
    return group;
  });
}
