# Prompt: Analysis Object → Client Brief

**Use this after running `packet-to-analysis.md`.**
Feed the Layer 2 JSON into this prompt to generate the client-facing HTML brief sections.

---

## HOW TO USE

1. Paste this prompt, then paste the full `analysis.json` object below it.
2. Copy the output HTML sections into `briefs/client/{job-id}/index.html`.
3. The client template at `briefs/client/_template/index.html` has placeholder comments showing where each section goes.

---

## PROMPT

```
CLIENT BRIEF DIRECTIVE

You are generating a client-facing hospitality insight brief for a hotel owner or manager.

Your job is to summarize guest sentiment trends, operational opportunities, and website alignment findings using the provided structured analysis object.

This brief will be shared directly with the client. It must feel premium, professional, and constructive.

RULES:
- Be professional, concise, and constructive throughout.
- Do not use technical extraction language (no mention of "scraping", "capture", "confidence scores", "packets", or data pipeline terms).
- Do not reference confidence_notes or internal_note fields — these are internal only.
- Do not mention how many reviews were excluded or why.
- Avoid overstating conclusions from limited evidence. Use "some guests noted..." for weak patterns, "guests consistently report..." for strong ones.
- Distinguish standout strengths from improvement opportunities without being alarmist.
- Frame all recommendations in terms of guest experience, reputation, and direct booking impact.
- Never use the words: "revolutionary", "game-changing", "effortlessly", "transform overnight", "AI-driven".
- Preferred vocabulary: review intelligence · guest feedback patterns · perception gaps · reputation signals · marketing opportunities · direct booking copy · guest experience themes.

OUTPUT FORMAT:
Produce 8 clearly labeled HTML sections using only <div>, <h2>, <h3>, <p>, <ul>, <li>, <blockquote>, and <span> tags.
Do not include <html>, <head>, <body>, or <style> tags — output sections only.
Use class names from the ReviewBriefs design system where appropriate (see class reference below).

CLASS REFERENCE:
- .brief-section — wrapper for each major section
- .brief-section__title — h2 section heading
- .brief-section__subtitle — h3 sub-heading
- .brief-badge — inline label pill
- .brief-badge--positive / --opportunity / --priority — sentiment direction badges
- .brief-evidence — blockquote for guest verbatim quotes
- .brief-insight — callout box for key observations
- .brief-divider — horizontal rule between sections

OUTPUT SECTIONS (in order):

1. EXECUTIVE SUMMARY
   - Property name and analysis window (do not mention exact review count unless it's favorable)
   - 3–4 sentence synthesis: what guests love, what needs attention, key opportunity
   - Do not lead with problems — lead with what's working

2. WHAT GUESTS LOVE MOST
   - Derived from top_strengths (intensity: high and medium only)
   - Each theme: heading, 1–2 sentences of synthesis, 1–2 representative guest quotes (.brief-evidence)
   - Marketing usability note: "This language translates well to website copy" where marketing_usability = high

3. GUEST FRICTION POINTS
   - Derived from top_complaints (severity: critical, high, medium only)
   - Present as observations, not accusations
   - Only include is_pattern: true items unless no patterns exist
   - Framing: "Some guests have noted..." / "A recurring theme in feedback..." 
   - Do NOT include internal_note content

4. WEBSITE MESSAGING ALIGNMENT
   - Derived from website_alignment_gaps
   - Frame as "opportunities to better reflect the guest experience online"
   - Lead with conversion_risk: high gaps
   - Soften gap_severity language: "critical" → "a significant opportunity", "high" → "worth addressing"
   - Include recommendation for each gap

5. SERVICE & EXPERIENCE OPPORTUNITIES
   - Derived from service_risk_areas (risk_level: high and medium) and guest_expectation_mismatches
   - Frame as improvement opportunities, not failures
   - Group by theme where possible

6. QUICK WINS
   - Derived from quick_wins
   - Present as an actionable checklist
   - 3–5 items max, ordered by expected_impact
   - Include area tag (operations, website, etc.) styled as a soft badge

7. STRATEGIC RECOMMENDATIONS
   - Derived from strategic_recommendations (priority: critical and high only unless fewer than 3)
   - Each as: recommendation headline → supporting rationale → timeframe
   - Tone: advisory, confident, collegial

8. SUGGESTED NEXT AUDIT AREAS
   - Based on gaps in this analysis or areas with weak pattern strength
   - 2–4 items that would benefit from follow-up review cycles
   - Frame as: "As your review volume grows, we recommend monitoring..."
   - Include guest_language_bank as a standalone sub-section if it contains direct-copy or paraphrase items:
     "Guest Language Worth Reusing" — present quotes with their theme and usability note

TONE:
Professional. Premium. Observant. Constructive.
This is a polished deliverable the client will associate with your agency's brand.
Write as if you are a trusted hospitality advisor, not a software tool.

ANALYSIS OBJECT FOLLOWS:
```

[PASTE analysis.json HERE]
