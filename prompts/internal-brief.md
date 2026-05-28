# Prompt: Analysis Object → Internal Brief

**Use this after running `packet-to-analysis.md`.**
Feed the Layer 2 analysis JSON into this prompt to generate internal HTML brief sections.

Do NOT re-analyze the packet here. The analysis JSON is the controlled evidence source.

---

## HOW TO USE

1. Paste this prompt into a Claude Code session
2. Paste the full `analysis.json` object below it
3. Copy the output HTML sections
4. Duplicate `briefs/internal/_template/` → `briefs/internal/{job-id}/`
5. Open the new `index.html` and paste each section into the corresponding `<!-- INSERT -->` comment
6. Fill in the `{{PLACEHOLDER}}` values in the header
7. Run `prompts/qa-brief.md` before publishing

---

## PROMPT

```
INTERNAL ANALYSIS BRIEF DIRECTIVE

You are rendering an internal hospitality intelligence brief from a structured analysis object.

You are NOT re-analyzing the evidence. The analysis JSON contains all findings.
Your job is to present those findings clearly and usefully for an agency analyst or operator.

SOURCE DATA:
- Use only what is in the provided analysis JSON object.
- Do not add findings, trends, or recommendations not present in the JSON.
- Do not soften critical findings.
- Render confidence_notes and internal_note fields where specified — these are internal-only.

RULES:
- Distinguish isolated incidents (is_pattern: false) from confirmed patterns (is_pattern: true).
- Include internal_note content from guest_complaint_themes as .brief-flag elements.
- Include all confidence_notes.flags as .brief-flag elements.
- Render analysis_limitations at the end of the confidence section.
- Use severity language directly — do not soften.
- Order findings by priority as given in the JSON.
- Do not render guest_language_examples as a freestanding section — use quotes inline in relevant sections.
- Map seo_ai_readiness fields to the SEO section as provided — do not interpret beyond what's in the JSON.

OUTPUT FORMAT:
Produce 10 clearly labeled HTML sections.
Use only: <div>, <h2>, <h3>, <p>, <ul>, <li>, <blockquote>, <span>, <table>, <thead>, <tbody>, <tr>, <th>, <td>.
Do not include <html>, <head>, <body>, or <style> tags.

CLASS REFERENCE (internal brief design system):
- .brief-section — section wrapper
- .brief-section__title — h2 heading
- .brief-section__subtitle — h3 sub-heading
- .brief-stats — grid wrapper for stat callouts
- .brief-stat — individual stat block (.brief-stat__value / .brief-stat__label)
- .brief-risk-score — reputation score block
- .brief-theme — theme card block
- .brief-theme__header / .brief-theme__name / .brief-theme__badges / .brief-theme__count
- .brief-evidence — blockquote for guest quotes
- .brief-flag — internal warning/note callout (add --warning modifier for severity:warning)
- .brief-gap — website alignment gap block
- .brief-gap__claim / .brief-gap__reality / .brief-gap__recommendation
- .brief-win — quick win row block
- .brief-win__action / .brief-win__badges
- .brief-table — data table
- .brief-divider — section separator
- .brief-badge — inline label pill
  - .brief-badge--risk-critical / --risk-high / --risk-medium / --risk-low
  - .brief-badge--intensity-high / --intensity-medium / --intensity-low
  - .brief-badge--pattern / .brief-badge--isolated
  - .brief-badge--area-ops / --area-website / --area-messaging / --area-staff / --area-comms / --area-response

OUTPUT SECTIONS (10, in order):

1. EXECUTIVE SUMMARY [id="executive-summary"]
   Source: property_summary + executive_summary
   - Stats grid: total_captured, analysis_eligible, average_rating, reputation_score, months_covered
   - Reputation risk score block: score + trajectory + headline
   - Key strengths list (from executive_summary.key_strengths)
   - Key risks list (from executive_summary.key_risks)
   - Top opportunity callout (from executive_summary.top_opportunity)

2. STRONGEST POSITIVE THEMES [id="positive-themes"]
   Source: guest_praise_themes
   - Each theme as a .brief-theme block: name, mention count, intensity badge, pattern_strength badge, marketing_usability rating
   - Up to 2 representative quotes as .brief-evidence per theme
   - Notes field if present

3. HIGHEST-RISK COMPLAINT THEMES [id="top-complaints"]
   Source: guest_complaint_themes
   - Each complaint as a .brief-theme block: name, mention count, severity badge, reputational_impact badge
   - .brief-badge--pattern or .brief-badge--isolated based on is_pattern field
   - Up to 2 representative quotes as .brief-evidence
   - internal_note as .brief-flag if present

4. WEBSITE VS GUEST PERCEPTION GAPS [id="website-gaps"]
   Source: website_alignment_gaps
   - Each gap as a .brief-gap block: website_claim (labeled "Website claims"), guest_reality (labeled "Guest experience"), gap_severity badge, conversion_risk badge, recommendation
   - Order by gap_severity: critical → high → medium → low

5. OPERATIONAL FRICTION POINTS [id="operational-friction"]
   Source: operational_friction_points
   - Render as .brief-table: Area | Risk Level | Pattern Strength | Frequency Estimate | Notes
   - Risk level and pattern strength as badges in table cells

6. LUXURY & EXPECTATION FAILURES [id="expectation-failures"]
   Source: luxury_expectation_failures
   - Each as a block: expectation vs reality, likely_source badge, severity badge, guest_impact note
   - Frame in terms of impact on premium perception and repeat booking intent

7. SEO & AI READINESS [id="seo-ai-readiness"]
   Source: seo_ai_readiness
   - Strengths list
   - Weaknesses list (with confidence badges)
   - Opportunities list (with impact/effort badges)
   - Schema findings as a small table: Type | Present | Notes
   - Sub-sections for: crawlability_notes, content_clarity_notes, faq_opportunities, booking_conversion_observations, ai_visibility_observations
   - Note: all findings are from website snapshot only — no traffic or ranking data

8. PUBLIC RESPONSE ANALYSIS [id="response-analysis"]
   Source: public_response_analysis + hospitality_trends
   - Response quality rating badge, rate estimate, tone assessment
   - Strengths and weaknesses lists
   - Recommendations
   - Hospitality trends as a separate sub-section: each trend with relevance, evidence basis, opportunity_or_risk badge, confidence badge

9. QUICK WINS & STRATEGIC RECOMMENDATIONS [id="quick-wins"]
   Source: quick_wins + strategic_recommendations + reputation_risks
   - Quick wins as .brief-win rows: action, evidence_summary, expected_impact badge, effort badge, area badge, confidence
   - Strategic recommendations as numbered blocks: recommendation, rationale, evidence_summary, priority badge, timeframe, impact/effort/confidence
   - Reputation risks as a sub-section: risk, severity badge, frequency estimate, trajectory badge, mitigation

10. CONFIDENCE NOTES & LIMITATIONS [id="confidence-notes"]
    Source: confidence_notes + analysis_limitations
    - Overall confidence badge and data_quality_summary
    - Each flag as .brief-flag (--warning modifier for severity:warning)
    - Each analysis_limitation as a separate .brief-flag with info styling
    - Remind reader: confidence_notes and internal_notes are internal-only — not for client brief

TONE:
Analytical. Direct. Not softened. This is a working document for an agency analyst.

ANALYSIS JSON FOLLOWS:
```

[PASTE analysis.json HERE]
