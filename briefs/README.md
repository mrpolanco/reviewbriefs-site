# Brief Generation Workflow

This directory holds all generated briefs.

```
briefs/
  internal/
    _template/    ← copy this to create a new internal brief
    {job-id}/
      index.html
  client/
    _template/    ← copy this to create a new client brief
    {job-id}/
      index.html
  README.md       ← this file
```

---

## Three-step workflow

### Step 1 — Packet → Analysis JSON (Layer 2)

1. Open `prompts/packet-to-analysis.md`
2. Paste the prompt into a Claude Code session, then paste your evidence packet below it
3. Save the JSON output as `briefs/{job-id}/analysis.json`

This is the canonical structured analysis object. It feeds both briefs.

---

### Step 2 — Analysis JSON → Internal Brief

1. Open `prompts/internal-brief.md`
2. Paste the prompt, then paste `analysis.json` below it
3. Copy the HTML output sections
4. Duplicate `briefs/internal/_template/` → `briefs/internal/{job-id}/`
5. Open the new `index.html` and fill in:
   - The `{{PLACEHOLDER}}` values in the header (property name, dates, etc.)
   - Paste each AI-generated section into the corresponding `<!-- INSERT -->` comment

The internal brief is not password-protected. Share via direct URL or internal link.

---

### Step 3 — Analysis JSON → Client Brief

1. Open `prompts/client-brief.md`
2. Paste the prompt, then paste `analysis.json` below it
3. Copy the HTML output sections
4. Duplicate `briefs/client/_template/` → `briefs/client/{job-id}/`
5. **Set the password hash:**
   - Open browser console and run:
     ```js
     crypto.subtle.digest('SHA-256', new TextEncoder().encode('yourpassword'))
       .then(b => console.log([...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')))
     ```
   - Copy the 64-character hex string
   - Replace `{{PASSWORD_HASH}}` in the client `index.html` with it
6. Fill in the `{{PLACEHOLDER}}` header values
7. Paste each AI-generated section into the corresponding `<!-- INSERT -->` comment

---

## URL structure

Once pushed to GitHub Pages:

| Brief type | URL |
|---|---|
| Internal | `https://reviewbriefs.com/briefs/internal/{job-id}/` |
| Client | `https://reviewbriefs.com/briefs/client/{job-id}/` |

All brief pages carry `<meta name="robots" content="noindex, nofollow">`.

---

## Naming convention for job IDs

`{property-slug}-{YYYY-MM}`

Examples:
- `casa-mariposa-2025-05`
- `hotel-central-2025-06`
- `parasol-resort-2025-06`

Use the same job ID across the analysis JSON, internal brief folder, and client brief folder.

---

## Files in the chain

| File | Role |
|---|---|
| `data/brief-schema.json` | Canonical Layer 2 analysis object shape |
| `prompts/packet-to-analysis.md` | Prompt: evidence packet → analysis JSON |
| `prompts/internal-brief.md` | Prompt: analysis JSON → internal HTML sections |
| `prompts/client-brief.md` | Prompt: analysis JSON → client HTML sections |
| `briefs/internal/_template/index.html` | Internal brief template |
| `briefs/client/_template/index.html` | Client brief template + JS password gate |
