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
 * Design comparison (temporary, Nov 2026): ?design=a|b|c picks one of three
 * stylesheets, loaded on top of styles.css. Default is c, the warm design Ian
 * picked for the Nov 17 workshop. The chosen letter is also set as
 * <html data-design> so a stylesheet can scope rules if it wants.
 * Only the URL is read; nothing is stored. Delete this block once Ian picks one.
 */
const DESIGNS = {
  a: () => import('./design-a.css'),
  b: () => import('./design-b.css'),
  c: () => import('./design-c.css'),
};
const DEFAULT_DESIGN = 'c';

function loadDesign() {
  const requested = new URLSearchParams(location.search).get('design');
  const design = Object.hasOwn(DESIGNS, requested) ? requested : DEFAULT_DESIGN;
  document.documentElement.dataset.design = design;
  DESIGNS[design]();
}

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
  loadDesign();
  initLangToggle();
  setLang(resolveInitialLang(), { persist: false }); // don't save a language the user never chose
}

init();
