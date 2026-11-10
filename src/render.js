/**
 * render.js — all DOM building.
 *
 * Everything that touches the document lives here so search.js can stay pure.
 *
 * Rules this file has to honor (CLAUDE.md section 5, plus Ian's v1 decisions):
 *   - Every user-facing string comes from t(); no literals in here.
 *   - A null field is not shown at all (v1 decision): no "Not listed" rows,
 *     only facts we actually have.
 *   - No category badges in v1. Categories are partly placeholders until the
 *     January filters, so they must not reach students yet.
 *   - Every card shows its official link and "Last verified: [date]".
 *   - Scholarship text (summary, amount, notes, requirement details) is shown
 *     in English unless translation_reviewed is true, with the
 *     t('card.summary_english_only') note when the page is in Spanish.
 *   - Text goes in via textContent, not innerHTML — the data is Ian's, but this
 *     keeps a stray character in a scholarship name from ever becoming markup.
 */

import { t, getLang } from './i18n.js';

/* ------------------------------------------------------------------ *
 * Small helpers
 * ------------------------------------------------------------------ */

/** createElement with a class, attributes, text and children. */
function el(tag, { className, attrs, text } = {}, children = []) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (attrs) for (const [name, value] of Object.entries(attrs)) node.setAttribute(name, value);
  if (text != null) node.textContent = text;
  for (const child of children) if (child) node.append(child);
  return node;
}

function locale() {
  return getLang() === 'es' ? 'es-US' : 'en-US';
}

/**
 * "2026-12-15" -> "December 15, 2026" / "15 de diciembre de 2026".
 * Parsed and formatted in UTC so the day never shifts with the phone's time zone.
 */
function formatDate(iso) {
  return new Intl.DateTimeFormat(locale(), { dateStyle: 'long', timeZone: 'UTC' }).format(
    new Date(`${iso}T00:00:00Z`)
  );
}

/** (1, 2027) -> "January 2027" / "Enero de 2027". */
function formatMonth(month, year) {
  const label = new Intl.DateTimeFormat(locale(), {
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(Date.UTC(year, month - 1, 1)));
  return label.charAt(0).toUpperCase() + label.slice(1);
}

/** 2 -> "2.0", 2.75 -> "2.75". */
function formatGpa(gpa) {
  return Number.isInteger(gpa) ? gpa.toFixed(1) : String(gpa);
}

/**
 * The language for an entry's own text. Spanish is used only when Ian has
 * approved the translation; otherwise everything falls back to English.
 */
function entryLang(entry) {
  return getLang() === 'es' && entry.translation_reviewed ? 'es' : 'en';
}

function entryText(entry, field) {
  const lang = entryLang(entry);
  return (field?.[lang] || field?.en || '').trim();
}

/* ------------------------------------------------------------------ *
 * Card
 * ------------------------------------------------------------------ */

/** "Who it's for": only the structured facts that are known. */
function whoItsFor(entry) {
  const parts = [
    ...entry.grade_levels.map((g) => t(`grade_levels.${g}`)),
    ...entry.degree_types.map((d) => t(`degree_types.${d}`)),
  ];
  if (entry.eligible_institutions.length) {
    parts.push(t('card.institutions', { schools: entry.eligible_institutions.join(', ') }));
  }
  if (entry.gpa_min != null) parts.push(t('card.gpa_min', { gpa: formatGpa(entry.gpa_min) }));
  return parts.join(' · ');
}

/** Known requirement flags only. null means unknown, and unknown is not shown. */
function requirementItems(entry) {
  const r = entry.requirements;
  const items = [];
  const flag = (value, yesKey, noKey) => {
    if (value === true) items.push(t(yesKey));
    else if (value === false) items.push(t(noKey));
  };
  flag(r.essay_required, 'card.essay_required', 'card.no_essay_required');
  if (r.recs_needed != null) items.push(t('card.recs_needed', { count: r.recs_needed }));
  flag(r.fafsa_required, 'card.fafsa_required', 'card.no_fafsa_required');
  flag(r.accepts_tasfa, 'card.accepts_tasfa', 'card.no_tasfa');
  flag(r.citizenship_required, 'card.citizenship_required', 'card.no_citizenship_required');
  flag(r.interview, 'card.interview', 'card.no_interview');
  return items;
}

/** One <dt>/<dd> pair, or nothing when the value is empty. */
function fact(label, value, valueLang) {
  if (!value) return [];
  const dd = el('dd', { text: value });
  if (valueLang) dd.lang = valueLang;
  return [el('dt', { text: label }), dd];
}

export function renderCard(entry, headingLevel) {
  const pageLang = getLang();
  const textLang = entryLang(entry);
  // Mark English blocks on a Spanish page so screen readers switch voice.
  const tagLang = textLang !== pageLang ? textLang : undefined;

  const card = el('article', { className: 'card' });
  card.append(el(`h${headingLevel}`, { className: 'card__title', text: entry.name }));

  // Deadline line. Entries without a date point to the official page instead.
  const deadlineText = entry.deadline
    ? `${t('card.deadline')}: ${formatDate(entry.deadline)}`
    : t('card.check_dates');
  card.append(el('p', { className: 'card__deadline', text: deadlineText }));

  const renewable = entry.renewable == null ? '' : t(entry.renewable ? 'value.yes' : 'value.no');
  const facts = el('dl', { className: 'card__facts' }, [
    ...fact(t('card.amount'), entryText(entry, entry.amount_display), tagLang),
    ...fact(t('card.who'), whoItsFor(entry)),
    ...fact(t('card.renewable'), renewable),
  ]);
  if (facts.childElementCount) card.append(facts);

  // The entry's own prose, in English unless the translation is reviewed.
  const prose = el('div', { className: 'card__prose' });
  if (tagLang) prose.lang = tagLang;

  const summary = entryText(entry, entry.summary);
  if (summary) prose.append(el('p', { text: summary }));

  const reqs = requirementItems(entry);
  const otherReqs = entryText(entry, entry.requirements.other);
  if (reqs.length || otherReqs) {
    const list = el('ul', { className: 'card__reqs' });
    // Flag labels come from the i18n files, so they are in the page language.
    for (const item of reqs) list.append(el('li', { text: item, attrs: { lang: pageLang } }));
    if (otherReqs) list.append(el('li', { text: otherReqs }));
    prose.append(
      el('p', { className: 'card__label', text: t('card.requirements'), attrs: { lang: pageLang } }),
      list
    );
  }

  const notes = entryText(entry, entry.notes);
  if (notes) prose.append(el('p', { className: 'card__notes', text: notes }));

  if (prose.childElementCount) card.append(prose);

  if (pageLang === 'es' && textLang === 'en') {
    card.append(el('p', { className: 'card__note', text: t('card.summary_english_only') }));
  }
  if (pageLang === 'es' && entry.application_language === 'en') {
    card.append(el('p', { className: 'card__note', text: t('card.application_in_english') }));
  }

  // v1 shows only the official page. apply_url stays in the data, but an Apply
  // button on the one card that has a link looked odd (Ian, Nov 9); bring it
  // back in January once more entries have apply links.
  card.append(
    el('p', { className: 'card__links' }, [
      el('a', { attrs: { href: entry.source_url }, text: t('card.official_page') }),
    ])
  );

  card.append(
    el('p', {
      className: 'card__verified',
      text: `${t('card.last_verified')}: ${formatDate(entry.last_verified)}`,
    })
  );

  return card;
}

/* ------------------------------------------------------------------ *
 * Sections
 * ------------------------------------------------------------------ */

/** "Open now": a flat list of cards, or a short message pointing below. */
export function renderOpenNow(container, entries) {
  container.replaceChildren();
  if (!entries.length) {
    container.append(el('p', { className: 'empty', text: t('sections.open_now_empty') }));
    return;
  }
  for (const entry of entries) container.append(renderCard(entry, 3));
}

/**
 * "Opening soon": one sub-heading per expected month, then its cards.
 * With nothing to show, the whole section (heading included) is hidden.
 */
export function renderOpeningSoon(container, groups) {
  container.replaceChildren();
  container.closest('section').hidden = groups.length === 0;
  for (const group of groups) {
    const heading =
      group.month == null ? t('sections.dates_not_posted') : formatMonth(group.month, group.year);
    container.append(el('h3', { className: 'month-heading', text: heading }));
    for (const entry of group.entries) container.append(renderCard(entry, 4));
  }
}
