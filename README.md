# CCA-F Study Prompts

Personal study notes and prompts for the Claude Certified Architect – Foundations (CCAR-F) exam, published with GitHub Pages.

Live site: https://jtirado5933.github.io/cca-f-study-prompts/

Not affiliated with or endorsed by Anthropic or Trace3.

## Structure

- `index.html`: the study post. Each exam domain is a `<section id="section-0N">`, linked from the table of contents.
- `assets/css/site.css`: Trace3 Full Throttle styling (see `brand.md`).
- `assets/skills/claude-cert-assessment/SKILL.md`: agent-agnostic CCAR-F readiness assessor skill (linked from the site).
- `brand.md`: palette, typography, motifs, and GTM copy rules for this page.
- `.nojekyll`: serves the files as-is, without a Jekyll build.

Content lives in `index.html`: intro, eight copy/paste prompts, and per-domain study notes with abbreviated instructor prompts (full task-by-task course text: see Resources link). Commit and push to `main`; Pages redeploys automatically.

The local working folder is `cc_cca_f_prompts_page`; the GitHub repo is `cca-f-study-prompts`.

## Preview locally

```powershell
python -m http.server 8000
```

Then open http://localhost:8000.

If you still see **orange** accents or `[PLACEHOLDER]` text, the browser is serving an old cached copy. Hard-refresh (Ctrl+Shift+R) or open the site in a private window. The stylesheet URL includes `?v=` so a fresh load pulls current Trace3 Full Throttle colors (`#0D1329` background, `#24B1E6` / `#1680B6` blues).
