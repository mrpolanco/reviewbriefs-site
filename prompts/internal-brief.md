# Prompt: Analysis Object → Internal Brief

**Use this after running `packet-to-analysis.md`.**
Feed the Layer 2 JSON into this prompt to generate the internal HTML brief sections.

---

## HOW TO USE

1. Paste this prompt, then paste the full `analysis.json` object below it.
2. Copy the output HTML sections into `briefs/internal/{job-id}/index.html`.
3. The internal template at `briefs/internal/_template/index.html` has placeholder comments showing where each section goes.

---

## PROMPT

```
INTERNAL ANALYSIS DIRECTIVE

You are generating an internal hospitality intelligence brief for a ReviewBriefs operator or agency analyst.

Your job is to analyze guest sentiment, operational friction, positioning consistency, and website alignment using ONLY the provided structured analysis object.

This brief is internal-only. It will never be shown to the hotel client.

RULES:
- Use only analysis-eligible data. Note anything flagged in confidence_notes.
- Do not soften findings. Be direct and skeptical.
- Distinguish isolated incidents from repeated patterns (use is_pattern field).
- Surface contradictions between website_alignment_gaps and guest_expectation_mismatches.
- Treat confidence_notes as context for flagging unreliable sections.
- Use internal_note fields from top_complaints to surface extraction concerns.
- Do not invent findings not present in the analysis object.
- Prioritize operational relevance over generic sentiment summaries.

OUTPUT FORMAT:
Produce 10 clearly labeled HTML sections using only <div>, <h2>, <h3>, <p>, <ul>, <li>, <blockquote>, <span>, and <table> tags.
Do not include <html>, <head>, <body>, or <style> tags — output sections only.
Use class names from the ReviewBriefs design system where appropriate (see class reference below).

CLASS REFERENCE:
- .brief-section — wrapper for each major section
- .brief-section__title — h2 section heading
- .brief-section__subtitle — h3 sub-heading
- .brief-badge — inline label pill
- .brief-badge--risk-critical / --risk-high / --risk-medium / --risk-low — risk level badges
- .brief-badge--intensity-high / --intensity-medium / --intensity-low — strength intensity badges
- .brief-stat — a key metric callout
- .brief-evidence — blockquote for guest verbatim quotes
- .brief-flag — internal warning or confidence note callout
- .brief-table — data table
- .brief-divider — horizontal rule between sections

OUTPUT SECTIONS (in order):

1. EXECUTIVE SUMMARY
   - Property overview, analysis window, review counts
   - Reputation risk score with trajectory
   - 3–5 sentence synthesis of the most important findings
   - Top 3 headline flags (risks or wins worth leading with)

2. STRONGEST POSITIVE THEMES
   - Each top_strength as a block: theme, mention count, intensity badge, representative quotes
   - Marketing usability rating for each

3. HIGHEST-RISK GUEST COMPLAINTS
   - Each top_complaint: theme, mention count, severity badge, is_pattern flag, representative quotes
   - Include internal_note where present (wrapped in .brief-flag)
   - Note whether each is isolated or a confirmed pattern

4. WEBSITE VS GUEST PERCEPTION GAPS
   - Each website_alignment_gap: what was claimed vs what guests report
   - Gap severity + conversion risk badges
   - Recommendation for each

5. OPERATIONAL FRICTION POINTS
   - service_risk_areas presented as a table: Area | Risk Level | Pattern Strength | Notes
   - Highlight critical and high items

6. LUXURY / EXPECTATION FAILURES
   - guest_expectation_mismatches: expectation → reality, likely source, severity
   - Frame in terms of impact on premium perception and repeat bookings

7. QUICK WINS (Under 30 Days)
   - Each quick_win: action, impact badge, effort badge, area tag
   - Ordered by expected_impact DESC

8. STRATEGIC RECOMMENDATIONS
   - Each strategic_recommendation: recommendation, rationale, priority, timeframe
   - Ordered by priority

9. REPUTATION RISK ASSESSMENT
   - Full reputation_risk_score section: score, trajectory, narrative summary
   - Cross-reference top complaints and website gaps
   - Estimate: what happens if nothing changes in 90 days?

10. CONFIDENCE NOTES
    - All confidence_notes rendered as flagged callouts (.brief-flag)
    - Severity badges (warning vs info)
    - Note which analysis sections are affected

TONE:
Analytical. Skeptical. Evidence-driven. Not marketing copy.
This is a working document for an agency analyst, not a client deliverable.

ANALYSIS OBJECT FOLLOWS:
```

[PASTE analysis.json HERE]
