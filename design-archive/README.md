# Design archive

Designs A ("over the top") and B ("official and trustworthy") from the
November 2026 comparison. Design C (warm) is the live site. These files are
kept so Ian can revisit them in January 2027.

Nothing in this folder is built or deployed: Vite only bundles what
`index.html` and `src/` reference, and only `public/` is copied as-is.

The files are as they were on the day they were archived, so they do not
have later changes made to `src/design-c.css`.

## To try one again

1. Move the stylesheet back into `src/` (for A, also move `fonts/a/` back to
   `public/fonts/a/`, because `design-a.css` loads `/fonts/a/archivo-black-latin.woff2`).
2. In `index.html`, change `data-design="c"` on `<html>` to `a` or `b`, and
   point the second stylesheet `<link>` at that file.
