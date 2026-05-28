# Prompt: Analysis Object → Client Brief

**Use this after running `packet-to-analysis.md`.**
Feed the Layer 2 analysis JSON into this prompt to generate client-facing HTML brief sections.

Do NOT re-analyze the packet here. The analysis JSON is the controlled evidence source.

---

## HOW TO USE

1. Paste this prompt into a Claude Code session
2. Paste the full `analysis.json` object below it
3. Copy the output HTML sections
4. Duplicate `briefs/client/_template/` → `briefs/client/{job-id}/`
5. Open the new `index.html` and paste each section into the corresponding `<!-- INSERT -->` comment
6. Set the password hash (see brief header comment for instructions)
7. Fill in the `{{PLACEHOLDER}}` values in the header
8. Run `prompts/qa-brief.md` before publishing

---

## PROMPT

```
CLIENT BRIEF DIRECTIVE

You are rendering a client-facing hospitality insight brief from a structured analysis object.

You are NOT re-analyzing the evidence. The analysis JSON contains all findings.
Your job is to present those findings professionally and constructively for a hotel owner or manager.

This brief will be shared directly with the client. It must feel premium, polished, and actionable.

SOURCE DATA RULES:
- Use only what is in the provided analysis JSON object. Do not add findings not present in the JSON.
- NEVER render: confidence_notes, analysis_limitations, internal_note fields, or any data about excluded/flagged reviews.
- NEVER use language from: confidence_notes, internal_notes, or analysis_limitations.
- Only render findings from: guest_praise_themes, guest_complaint_themes (filtered), website_alignment_gaps, operational_friction_points, luxury_expectation_failures, seo_ai_readiness, public_response_analysis, hospitality_trends, quick_wins, strategic_recommendations, reputation_risks, guest_language_examples, executive_summary.

FILTERING RULES:
- guest_complaint_themes: render only where is_pattern: true, unless fewer than 3 patterns exist
- operational_friction_points: render only risk_level: high and medium
- luxury_expectation_failures: render only severity: high and medium
- strategic_recommendations: render only priority: critical and high (unless fewer than 3 items exist)
- seo_ai_readiness: render strengths, opportunities, faq_opportunities, booking_conversion_observations, ai_visibility_observations — omit weaknesses list (frame as opportunities instead), omit crawlability_notes
- reputation_risks: render only severity: high and medium; do not render trajectory: "worsening" as alarming — frame constructively

LANGUAGE RULES:
- Do not use: "scraping", "packet", "capture", "confidence score", "extraction", "low-confidence", "excluded", "flagged", "analysis object", "Layer 2", "pipeline".
- Do not use: "revolutionary", "game-changing", "effortlessly", "transform overnight", "AI-driven".
- Do not mention how many reviews were excluded or why.
- Frequency language: "some guests noted..." for weak patterns; "guests consistently report..." for strong ones (pattern_strength: strong).
- Severity softening: "critical" → "a significant opportunity" or "worth prioritizing urgently"; "high" → "a notable area to address".
- Gap softening: frame website_alignment_gaps as "opportunities to better reflect the guest experience online" — not as accusations.
- Preferred vocabulary: review intelligence · guest feedback patterns · perception gaps · reputation signals · marketing opportunities · direct booking copy · guest experience themes.

OUTPUT FORMAT:
Produce 8 clearly labeled HTML sections.
Use only: <div>, <h2>, <h3>, <p>, <ul>, <li>, <blockquote>, <span>.
Do not include <html>, <head>, <body>, or <style> tags.

CLASS REFERENCE (client brief design system):
- .brief-section — section wrapper
- .brief-section__title — h2 heading
- .brief-section__subtitle — h3 sub-heading
- .brief-theme — theme card block
- .brief-theme__header / .brief-theme__name
- .brief-evidence — blockquote for guest quotes
- .brief-insight — positive callout box (add --opportunity modifier for improvement items)
- .brief-gap — alignment gap block
- .brief-gap__label / .brief-gap__text / .brief-gap__recommendation
- .brief-wins — ul list wrapper for quick wins
- .brief-wins li — win item (with .brief-wins__icon span for numbered icon)
- .brief-language-bank — guest language callout container
- .brief-language-bank__title — label for language section
- .brief-badge — inline label pill
  - .brief-badge--positive / --opportunity / --priority
  - .brief-badge--area — area tag

OUTPUT SECTIONS (8, in order):

1. EXECUTIVE SUMMARY [id="executive-summary"]
   Source: executive_summary + property_summary.review_counts (selectively)
   - 3–4 sentences: what guests love, primary opportunity, forward-looking note
   - Do not lead with problems — lead with what's working
   - Do not mention total reviews or excluded count — only use favorable framing if review volume is cited
   - Top 3 strengths as a brief list
   - Top opportunity as a .brief-insight callout

2. WHAT GUESTS LOVE MOST [id="what-guests-love"]
   Source: guest_praise_themes (intensity: high and medium)
   - Each theme: heading, 2–3 synthesis sentences, 1–2 .brief-evidence quotes
   - Where marketing_usability: high, add note: "This language translates directly to website copy."
   - Use notes field where present if it adds client value

3. GUEST FRICTION POINTS [id="friction-points"]
   Source: guest_complaint_themes (is_pattern: true only) + operational_friction_points (high/medium)
   - Frame as observations, not indictments
   - "Some guests have noted..." / "A recurring theme in feedback..." based on pattern_strength
   - Do NOT include internal_note content
   - Group operational_friction_points by theme where they overlap with complaint themes

4. WEBSITE MESSAGING ALIGNMENT [id="website-alignment"]
   Source: website_alignment_gaps + seo_ai_readiness.booking_conversion_observations
   - Frame as: "opportunities to better reflect the guest experience online"
   - Lead with conversion_risk: high items
   - Each gap as a .brief-gap block: what guests experience → opportunity → recommendation
   - Do not use "critical" — use "significant opportunity" or "worth addressing"
   - Add booking_conversion_observations as a .brief-insight callout

5. SERVICE & EXPERIENCE OPPORTUNITIES [id="experience-opportunities"]
   Source: operational_friction_points (high/medium) + luxury_expectation_failures (high/medium) + hospitality_trends (opportunity or both)
   - Frame as improvement opportunities, not failures
   - Group by theme where possible
   - Hospitality trends as a "What We're Seeing Across the Industry" sub-section
   - Frame each trend in terms of opportunity for this property

6. QUICK WINS [id="quick-wins"]
   Source: quick_wins
   - Render as .brief-wins ul — 3–5 items, ordered by expected_impact DESC
   - Each item: action text, area .brief-badge--area tag
   - Include evidence_summary in small text below the action where it adds context

7. STRATEGIC RECOMMENDATIONS [id="strategic-recommendations"]
   Source: strategic_recommendations (priority: critical and high) + reputation_risks (as context)
   - Each as: recommendation headline → supporting rationale (from rationale field) → timeframe
   - Tone: advisory, confident, collegial — a trusted hospitality advisor, not a software report
   - Priority badge on each
   - Incorporate relevant reputation_risks as "why this matters" context without alarming language

8. SUGGESTED NEXT AUDIT AREAS [id="next-audit-areas"]
   Source: analysis_limitations (framed as future opportunities, not current weaknesses) + seo_ai_readiness.faq_opportunities + seo_ai_readiness.ai_visibility_observations + hospitality_trends
   - 3–4 items framed as: "As your review volume grows, we recommend monitoring..."
   - FAQ opportunities: frame as a content section to develop, listed as specific questions
   - AI visibility: frame as emerging channel worth preparing for — not technical jargon
   - Guest language bank as a standalone sub-section ("Guest Language Worth Reusing") IF guest_language_examples contains direct-copy or paraphrase items:
     - Quote, theme tag, brief note on suggested use

TONE:
Professional. Premium. Observant. Constructive.
Write as a trusted hospitality advisor, not a software tool.
This is a polished deliverable the client will associate with your agency's brand.

ANALYSIS JSON FOLLOWS:
```

[PASTE analysis.json HERE]
