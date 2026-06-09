# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project

**ReviewBriefs** - a fake-door / concierge MVP static site that validates demand before a future Laravel SaaS build.

**Vertical:** Hospitality agencies and independent hotels.

**Core promise:** Turn guest reviews into client-ready intelligence reports - what guests love, what hurts perception, what to improve next.

**Current phase:** Static GitHub Pages site. No backend, no framework. Structured so it migrates cleanly to Laravel later.

---

## Site structure

```
reviewbriefs-site/
  index.html
  sample-report.html
  request-baseline.html
  order-report.html
  request-report.html     ← legacy redirect to request-baseline.html
  pricing.html
  thank-you.html
  404.html

  assets/
    css/styles.css
    js/main.js
    images/

  data/
    sample-report.json

  reports/
    sample-boutique-hotel/
      index.html

  prompts/
    weekly-review-brief.md   ← Codex prompt used to generate reports manually

  make_logo.py               ← one-off script that generated assets/images/logo.*
  make_og.py                 ← one-off script that generated assets/images/og-image.png
  CNAME                      ← custom domain for GitHub Pages (reviewbriefs.com)
```

## Pages and their purpose

| File | Purpose |
|---|---|
| `index.html` | Homepage - explain offer, push to sample report or request form |
| `sample-report.html` | Teaser page - abbreviated report, CTA to full report |
| `reports/sample-boutique-hotel/index.html` | Full sample report - the most important asset |
| `request-baseline.html` | Free baseline snapshot lead capture form |
| `order-report.html` | Paid full ReviewBrief order form |
| `request-report.html` | Legacy redirect to `request-baseline.html` |
| `pricing.html` | Private beta pricing ($0 sample / $99 one-time / $499/mo agency) |
| `thank-you.html` | Post-form confirmation |

---

## Development

No build step. Open HTML files directly in a browser, or serve locally:

```bash
# Python (built-in)
python3 -m http.server 8080

# or npx serve
npx serve .
```

Deploy: push to `main` branch → GitHub Pages serves from root.

---

## CSS architecture

All styles live in `assets/css/styles.css` using CSS custom properties.

### Design tokens

```css
:root {
  --rb-ink: #18201C;
  --rb-ink-soft: #3D4943;
  --rb-muted: #6F7A73;
  --rb-cream: #F7F3EA;
  --rb-paper: #FFFDF8;
  --rb-stone: #E7E0D3;
  --rb-moss: #4F6F52;
  --rb-moss-dark: #304734;
  --rb-sage: #A8B8A0;
  --rb-clay: #B86B4B;
  --rb-clay-soft: #E7BFAE;
  --rb-gold: #C6A15B;
  --rb-line: rgba(24, 32, 28, 0.12);
  --font-body: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
  --font-display: Georgia, "Times New Roman", serif; /* headlines only if needed */
}
```

### Key layout utilities

```css
.container { width: min(1120px, calc(100% - 40px)); margin-inline: auto; }
```

Breakpoints: `max-width: 900px` and `max-width: 640px`.

### Card style

```css
.card {
  background: var(--rb-paper);
  border: 1px solid var(--rb-line);
  border-radius: 18px;
  box-shadow: 0 20px 60px rgba(24, 32, 28, 0.06);
}
```

---

## JavaScript

`assets/js/main.js` only - keep minimal:
- Mobile nav toggle
- Print button helper (`window.print()`)
- Current year in footer

No analytics until explicitly confirmed. No tracking scripts, chat widgets, or heavy third-party libraries.

---

## HTML conventions

Mark reusable sections with component comments so they become Blade partials in Laravel:

```html
<!-- component: site-header -->
<!-- component: hero-section -->
<!-- component: report-preview-card -->
<!-- component: site-footer -->
```

Use semantic HTML: `<header>`, `<main>`, `<section>`, `<footer>`. One `<h1>` per page.

---

## Brand and copy rules

**Feel:** Professional, editorial, boutique B2B. Calm analytics + hospitality consultancy.

**Avoid in copy:** "revolutionary", "10x", "AI-driven", "game-changing", "effortlessly", "transform overnight", robot/sparkle/brain motifs, AI-purple gradients.

**Preferred vocabulary:** review intelligence · guest feedback patterns · client-ready briefs · reputation signals · marketing opportunities · operational friction · direct booking copy · guest experience themes.

---

## The sample report is the product

`/reports/sample-boutique-hotel/index.html` is the most important page. It must feel like a real deliverable - a polished paper document, not a webpage with fake data.

Report sections (in order):
1. Executive Summary
2. Top Praise Themes
3. Reputation Risks
4. Guest Language Worth Reusing
5. Marketing Opportunities
6. Suggested Website Copy
7. Suggested Review Responses
8. Priority Action List (table: Priority / Action / Owner / Expected Impact)

Report print styles hide header, footer, CTAs and remove shadows. The print button uses `window.print()`.

---

## Form workflow

No backend. Use **Tally** or **Fillout** embeds on `request-baseline.html` and `order-report.html`.

Form fields map to future DB columns: `name`, `email`, `company`, `property_name`, `property_website`, `city_country`, `property_type`, `main_goal`, `review_links`, `pasted_reviews`.

On submit → redirect to `/thank-you.html`. Notification email subject: `New ReviewBriefs request: {Property Name}`.

---

## SEO / metadata

Every page needs:

```html
<title>ReviewBriefs | Client-ready review intelligence</title>
<meta name="description" content="...">
<meta property="og:title" content="ReviewBriefs">
<meta property="og:description" content="Turn guest reviews into client-ready insights.">
<meta property="og:type" content="website">
<meta property="og:image" content="/assets/images/og-image.png">
```

`robots.txt` at root allows all. Future real client report pages get `<meta name="robots" content="noindex,nofollow">`.

---

## Build priority order

1. Global styles and layout
2. Homepage
3. Full sample report (`/reports/sample-boutique-hotel/`)
4. Sample report teaser (`sample-report.html`)
5. Request form page
6. Thank-you page
7. Pricing page
8. Mobile polish
9. Print styles
10. Metadata / OG image

---

## Laravel migration path

URL structure is intentionally close to future Laravel routes:

| Static file | Future Laravel route |
|---|---|
| `index.html` | `Route::view('/', 'marketing.home')` |
| `sample-report.html` | `Route::view('/sample-report', ...)` |
| `request-baseline.html` | `Route::view('/request-baseline', ...)` |
| `order-report.html` | `Route::view('/order-report', ...)` |
| `request-report.html` | legacy redirect to `/request-baseline` |
| `pricing.html` | `Route::view('/pricing', ...)` |
| `reports/sample-boutique-hotel/` | `Route::get('/reports/{report:slug}', ...)` |
| _(future)_ `/app` | Authenticated dashboard |

HTML component comments → `resources/views/components/*.blade.php`

Key future models: `Organization`, `Property`, `ReviewBatch`, `Review`, `Report`, `ReportRequest`.

Keep `data/sample-report.json` aligned with the future `reports` DB table shape so seeding is straightforward.

---

## Brief generation workflow

Real client deliverables live in `/briefs/`. See `briefs/README.md` for the full workflow.

### Architecture (3 layers)

```
evidence packet (markdown) → Layer 2 JSON → internal brief HTML + client brief HTML
```

**Layer 1 - Evidence packet:** Semi-structured markdown from the scraper. Verbose, ugly, machine-oriented.

**Layer 2 - Analysis object:** Structured JSON output (`data/brief-schema.json` defines the shape). Generated by `prompts/packet-to-analysis.md`. Feeds both briefs. Do not let brief prompts re-analyze the packet - the JSON is the controlled middle layer.

The analysis object covers: guest praise themes, complaint themes, operational friction, luxury expectation failures, website alignment gaps, SEO/AI readiness, public response quality, hospitality trends, quick wins, strategic recommendations, reputation risks, guest language, confidence notes, and analysis limitations.

**Layer 3 - Presentation:** Two HTML files per job, rendered from the analysis object.

### Prompts (run in Codex session)

| Prompt | Input → Output |
|---|---|
| `prompts/packet-to-analysis.md` | Evidence packet → `analysis.json` |
| `prompts/internal-brief.md` | `analysis.json` → internal HTML sections |
| `prompts/client-brief.md` | `analysis.json` → client HTML sections |
| `prompts/qa-brief.md` | Final QA pass - 15 checks before publishing either brief |

### Output structure

```
briefs/
  internal/{job-id}/index.html   ← no password, not for client
  client/{job-id}/index.html     ← JS password gate (per-brief SHA-256 hash)
```

Job ID convention: `{property-slug}-{YYYY-MM}` (e.g., `casa-mariposa-2025-05`).

### Client brief access gate

The client template includes a lightweight JS access gate (SHA-256 password hash via Web Crypto API). **This is casual privacy only - brief content is inside the HTML file and visible to anyone who views source.** Do not use for confidential data.

For real protection later: server-side auth, signed expiring links, or basic auth at the hosting layer.

To generate a hash for the gate:
```js
crypto.subtle.digest('SHA-256', new TextEncoder().encode('yourpassword'))
  .then(b => console.log([...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')))
```
Replace `{{PASSWORD_HASH}}` in the client template with the 64-char hex output.

### Brief CSS classes

Brief-specific classes are scoped inside each template's `<style>` block (not in `styles.css`). Key classes: `.brief-section`, `.brief-section__title`, `.brief-badge`, `.brief-badge--risk-{level}`, `.brief-evidence`, `.brief-flag` (internal only), `.brief-theme`, `.brief-gap`, `.brief-table`.
