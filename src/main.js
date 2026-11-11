/**
 * main.js — entry point. Wires up the language toggle and renders the two v1
 * sections ("Open now" and "Opening soon").
 *
 * The scholarship data is imported, not fetched, so Vite bundles it into the
 * page: no extra request, no loading state, and nothing to fail on a weak
 * phone connection.
 */

// styles.css is loaded by the <link> in index.html, not imported here, so the
// page is styled before this module runs (no flash of unstyled content).
import { resolveInitialLang, setLang, getLang } from './i18n.js';
import { toISODate, openNow, openingSoon } from './search.js';
import { renderOpenNow, renderOpeningSoon } from './render.js';
import scholarships from '../data/scholarships.json';

/**
 * v1 (Nov 2026 workshop) ships in English only, because there was no time to
 * review the Spanish before launch. While this is true the page always renders
 * in English, whatever the browser language or a previously saved choice, and
 * the toggle in index.html carries the hidden attribute. es.json and i18n.js
 * are untouched. To bring Spanish back: set this to false and remove `hidden`
 * from the toggle.
 */
const ENGLISH_ONLY = true;

/** Reflects the active language on the two toggle buttons. */
function syncLangToggle() {
  const active = getLang();
  for (const button of document.querySelectorAll('[data-set-lang]')) {
    const isActive = button.dataset.setLang === active;
    button.setAttribute('aria-pressed', String(isActive));
  }
}

/**
 * "Today" is the student's own calendar day, read on every render, so an
 * entry whose deadline has ended drops off on the next load with no data change.
 */
function renderLists() {
  const today = toISODate(new Date());
  renderOpenNow(document.getElementById('open-now-list'), openNow(scholarships, today));
  renderOpeningSoon(document.getElementById('opening-soon-list'), openingSoon(scholarships, today));
}

function initLangToggle() {
  for (const button of document.querySelectorAll('[data-set-lang]')) {
    button.addEventListener('click', () => setLang(button.dataset.setLang));
  }
  // setLang fires this, so the buttons and cards stay in sync no matter who switched.
  document.addEventListener('languagechange', () => {
    syncLangToggle();
    renderLists();
  });
}

function init() {
  initLangToggle();
  // persist: false so we never save a language the user did not choose.
  setLang(ENGLISH_ONLY ? 'en' : resolveInitialLang(), { persist: false });
}

init();
