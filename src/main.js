/**
 * main.js — entry point. Wires up the language toggle and (from Phase 2 on)
 * the search UI.
 *
 * Phase 0 scope: the placeholder page plus a fully working language toggle,
 * so the bilingual plumbing is proven before any data or filters exist.
 */

// styles.css is loaded by the <link> in index.html, not imported here, so the
// page is styled before this module runs (no flash of unstyled content).
import { resolveInitialLang, setLang, getLang } from './i18n.js';

/** Reflects the active language on the two toggle buttons. */
function syncLangToggle() {
  const active = getLang();
  for (const button of document.querySelectorAll('[data-set-lang]')) {
    const isActive = button.dataset.setLang === active;
    button.setAttribute('aria-pressed', String(isActive));
  }
}

function initLangToggle() {
  for (const button of document.querySelectorAll('[data-set-lang]')) {
    button.addEventListener('click', () => setLang(button.dataset.setLang));
  }
  // setLang fires this, so the buttons stay in sync no matter who switched.
  document.addEventListener('languagechange', syncLangToggle);
}

function init() {
  initLangToggle();
  setLang(resolveInitialLang(), { persist: false }); // don't save a language the user never chose
  syncLangToggle();
}

init();
