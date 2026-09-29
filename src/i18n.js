/**
 * i18n.js — the whole translation layer. No library, no dependencies.
 *
 * Design notes (see CLAUDE.md sections 1 and 5):
 *  - The two JSON files are imported, not fetched, so they are bundled into the
 *    page. That means one less network request and no loading flash.
 *  - The ONLY thing written to localStorage anywhere in this project is the
 *    language code, under the key below. Nothing else is stored, ever.
 *  - If a Spanish key is missing, t() falls back to the English string rather
 *    than showing a raw key to a student.
 */

import en from './i18n/en.json';
import es from './i18n/es.json';

const DICTIONARIES = { en, es };
export const SUPPORTED_LANGS = ['en', 'es'];
export const DEFAULT_LANG = 'en';

/** The one and only storage key used by this site. */
const STORAGE_KEY = 'pasoapaso.lang';

let currentLang = DEFAULT_LANG;

/* ------------------------------------------------------------------ *
 * Reading and writing the saved preference
 * ------------------------------------------------------------------ */

/**
 * localStorage throws in some privacy modes, so every access is guarded and
 * the site works fine when it fails — it just forgets the choice on reload.
 */
function readStoredLang() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return SUPPORTED_LANGS.includes(stored) ? stored : null;
  } catch {
    return null;
  }
}

function writeStoredLang(lang) {
  try {
    localStorage.setItem(STORAGE_KEY, lang);
  } catch {
    /* Preference is not persisted. Not worth telling the user about. */
  }
}

/**
 * Browser language, narrowed to one we support. "es-MX", "es_419" and "es"
 * all resolve to "es"; anything else falls back to English.
 */
function detectBrowserLang() {
  const candidates = navigator.languages?.length
    ? navigator.languages
    : [navigator.language];

  for (const tag of candidates) {
    if (!tag) continue;
    const base = String(tag).toLowerCase().split(/[-_]/)[0];
    if (SUPPORTED_LANGS.includes(base)) return base;
  }
  return DEFAULT_LANG;
}

/** Saved choice wins over the browser's language. */
export function resolveInitialLang() {
  return readStoredLang() ?? detectBrowserLang();
}

/* ------------------------------------------------------------------ *
 * Lookup
 * ------------------------------------------------------------------ */

/** Walks a dotted path like "card.last_verified" through a nested object. */
function lookup(dictionary, key) {
  let node = dictionary;
  for (const part of key.split('.')) {
    if (node == null || typeof node !== 'object') return undefined;
    node = node[part];
  }
  return typeof node === 'string' ? node : undefined;
}

/** Replaces {name} placeholders with values from `vars`. */
function interpolate(template, vars) {
  if (!vars) return template;
  return template.replace(/\{(\w+)\}/g, (match, name) =>
    Object.hasOwn(vars, name) ? String(vars[name]) : match
  );
}

/**
 * Translate a key in the current language.
 *
 * @param {string} key   dotted path, e.g. "filters.no_essay"
 * @param {object} [vars] values for {placeholders}
 * @returns {string} the translated string, the English string if the current
 *   language lacks the key, or the key itself if neither has it (which is a
 *   bug worth seeing rather than hiding).
 */
export function t(key, vars) {
  const template =
    lookup(DICTIONARIES[currentLang], key) ??
    lookup(DICTIONARIES[DEFAULT_LANG], key) ??
    key;
  return interpolate(template, vars);
}

export function getLang() {
  return currentLang;
}

/**
 * True when the current language has its own translation for this key.
 * render.js uses this to decide whether it is showing a real translation or
 * an English fallback.
 */
export function hasTranslation(key, lang = currentLang) {
  return lookup(DICTIONARIES[lang], key) !== undefined;
}

/* ------------------------------------------------------------------ *
 * Applying a language to the page
 * ------------------------------------------------------------------ */

/**
 * Fills every element carrying data-i18n with its translation. Also handles
 * data-i18n-attr="placeholder:search.placeholder,title:search.label" for
 * strings that belong in an attribute instead of the text content.
 */
export function applyTranslations(root = document) {
  for (const el of root.querySelectorAll('[data-i18n]')) {
    el.textContent = t(el.dataset.i18n);
  }

  for (const el of root.querySelectorAll('[data-i18n-attr]')) {
    for (const pair of el.dataset.i18nAttr.split(',')) {
      const [attr, key] = pair.split(':').map((s) => s.trim());
      if (attr && key) el.setAttribute(attr, t(key));
    }
  }
}

/**
 * Switch language: updates <html lang>, the document title and description,
 * every translated node, and the saved preference. Fires a
 * "languagechange" event on document so other modules can re-render.
 */
export function setLang(lang, { persist = true } = {}) {
  currentLang = SUPPORTED_LANGS.includes(lang) ? lang : DEFAULT_LANG;

  document.documentElement.lang = currentLang;
  document.title = `Paso a Paso — ${t('site.title')}`;

  const description = document.querySelector('meta[name="description"]');
  if (description) description.setAttribute('content', t('site.meta_description'));

  applyTranslations();
  if (persist) writeStoredLang(currentLang);

  document.dispatchEvent(
    new CustomEvent('languagechange', { detail: { lang: currentLang } })
  );
}
