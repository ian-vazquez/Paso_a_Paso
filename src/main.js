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
import { resolveInitialLang, setLang, getLang, SPANISH_PREVIEW } from './i18n.js';
import { toISODate, openNow, openingSoon } from './search.js';
import { renderOpenNow, renderOpeningSoon } from './render.js';
import scholarships from '../data/scholarships.json';

/**
 * The live site stays English only until Ian confirms the Spanish review is
 * done. While this is true the page always renders in English, whatever the
 * browser language or a previously saved choice, and the toggle keeps the
 * hidden attribute it has in index.html.
 *
 * PR preview builds (and `npm run dev`) set SPANISH_PREVIEW, which turns this
 * off and shows the toggle, so the Spanish can be reviewed on a real phone.
 *
 * To launch Spanish on the live site: set this to false and remove `hidden`
 * from the toggle in index.html.
 */
const ENGLISH_ONLY = !SPANISH_PREVIEW;

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
  if (!ENGLISH_ONLY) document.querySelector('.lang-toggle').hidden = false;
  initLangToggle();
  // persist: false so we never save a language the user did not choose.
  setLang(ENGLISH_ONLY ? 'en' : resolveInitialLang(), { persist: false });
}

init();
