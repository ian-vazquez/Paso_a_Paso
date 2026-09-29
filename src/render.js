/**
 * render.js — all DOM building. Built in Phase 2.
 *
 * Everything that touches the document lives here so search.js can stay pure.
 *
 * Planned exports, for reference while reviewing Phase 2:
 *
 *   renderResults(container, scholarships) -> void
 *   renderCard(scholarship) -> HTMLElement
 *   renderEmptyState(container) -> void
 *
 * Rules this file has to honor (CLAUDE.md section 5):
 *   - Every user-facing string comes from t(); no literals in here.
 *   - A null field renders as t('value.not_listed'), never as a guess, never blank.
 *   - Every card shows its source link and "Last verified: [date]".
 *   - Unreviewed Spanish summaries fall back to the English summary with the
 *     t('card.summary_english_only') note (Ian's answer to Open Decision 3).
 *   - Text goes in via textContent, not innerHTML — the data is Ian's, but this
 *     keeps a stray character in a scholarship name from ever becoming markup.
 */

export {};
