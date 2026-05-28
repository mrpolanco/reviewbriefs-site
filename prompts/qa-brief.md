# Prompt: QA Pass — Brief Integrity Check

**Run this last**, after generating both internal and client brief sections.

Feed it the analysis JSON plus both sets of generated HTML sections.
It will flag violations before you publish.

---

## HOW TO USE

1. Open a Claude Code session
2. Paste this prompt
3. Paste the `analysis.json` object
4. Paste the internal brief HTML sections
5. Paste the client brief HTML sections
6. Review all flags — do not publish with any FAIL result

---

## PROMPT

```
QA BRIEF INTEGRITY CHECK

You are performing a quality assurance review of two generated hospitality intelligence briefs.

You will be given:
1. The Layer 2 analysis JSON object (the controlled evidence source)
2. The internal brief HTML sections
3. The client brief HTML sections

Your job is to check both briefs against the analysis object and flag all violations.

Do not re-analyze the evidence. Only check what the briefs say against what the JSON contains.

OUTPUT FORMAT:
For each check: ✓ PASS, ✗ FAIL, or ⚠ WARN.
For each FAIL: quote the specific offending text and state which rule it breaks.
For each WARN: describe the borderline case and your judgment call.
Conclude with a summary and overall verdict.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVIDENCE INTEGRITY (both briefs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] EVIDENCE-1: No claims from excluded reviews
    Check review_counts in property_summary. If excluded_low_confidence or excluded_duplicate > 0,
    verify that no brief claim could only originate from excluded captures.

[ ] EVIDENCE-2: No invented findings
    Every trend, pattern, risk, or recommendation in both briefs must trace to a field
    in the analysis JSON. Flag any claim that is not present in the JSON.

[ ] EVIDENCE-3: Isolated incidents not presented as patterns
    For each guest_complaint_themes entry where is_pattern: false —
    verify neither brief presents it as a recurring or confirmed pattern.
    Acceptable: "One guest noted..." or "An isolated report..."
    Not acceptable: "Guests consistently report..." or "A recurring issue..."

[ ] EVIDENCE-4: Owner responses not treated as guest sentiment
    Neither brief should attribute sentiment conclusions to management responses.
    public_response_analysis is its own section — findings there must not bleed into
    guest_praise_themes or guest_complaint_themes sections of either brief.

[ ] EVIDENCE-5: Frequency language matches mention data
    Match intensity qualifiers in brief text against mentions counts in the JSON:
    - "consistently" / "repeatedly" / "overwhelmingly" → requires pattern_strength: strong (5+ mentions)
    - "some guests" / "a few reviewers" → appropriate for pattern_strength: weak (1–3 mentions)
    Flag any mismatch.

[ ] EVIDENCE-6: SEO/AI findings not overstated
    seo_ai_readiness findings must be framed as: strengths, opportunities, hypotheses, or
    likely impacts — never as confirmed rankings, indexing states, traffic, or search performance.
    Flag any claim that states or implies a confirmed SEO outcome not present in the JSON.

[ ] EVIDENCE-7: Hospitality trends tied to evidence
    Each hospitality trend in both briefs must reference the evidence_basis from the JSON.
    Generic hospitality advice with no connection to property evidence is a FAIL.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEPARATION OF INTERNAL / CLIENT (critical)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] SEPARATION-1: Internal notes absent from client brief
    Check each guest_complaint_themes[].internal_note against client brief text.
    No internal_note content may appear in the client brief.

[ ] SEPARATION-2: Confidence notes absent from client brief
    confidence_notes content, data_quality_summary, and all flags must not appear in client brief.
    Verify: no mention of confidence levels, data exclusions, or extraction quality.

[ ] SEPARATION-3: Technical language absent from client brief
    Client brief must not contain: "scraping", "packet", "capture", "confidence score",
    "extraction", "low-confidence", "excluded", "flagged", "analysis object", "Layer 2", "pipeline",
    "brief-schema", "analysis JSON".

[ ] SEPARATION-4: Severity language softened in client brief
    "critical" severity items must not appear as "critical" in client brief.
    Required reframing: "significant opportunity", "worth prioritizing urgently".

[ ] SEPARATION-5: is_pattern filtering respected in client brief
    Client brief must not render guest_complaint_themes entries where is_pattern: false
    as a named complaint section (unless no pattern entries exist).

[ ] SEPARATION-6: analysis_limitations not exposed in client brief
    analysis_limitations content must not appear verbatim in client brief.
    May be rephrased as future audit opportunities (Next Audit Areas section only).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDATION TRACEABILITY (both briefs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] RECS-1: Quick wins trace to JSON fields
    Each quick win in both briefs must correspond to an entry in quick_wins[].
    The evidence_summary or action should match. Flag any win not in the JSON.

[ ] RECS-2: Strategic recommendations trace to JSON fields
    Each strategic recommendation must correspond to strategic_recommendations[] entry.
    The rationale must reference specific findings — not generic advice.

[ ] RECS-3: Website alignment recommendations match JSON gaps
    Each website alignment recommendation must correspond to a website_alignment_gaps[] entry.
    No gaps should be invented.

[ ] RECS-4: SEO opportunities match JSON
    Any SEO recommendation in either brief must trace to seo_ai_readiness.opportunities[]
    or seo_ai_readiness.faq_opportunities[]. No SEO advice outside the JSON.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TONE AND FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] TONE-1: Prohibited words absent from both briefs
    Neither brief uses: "revolutionary", "game-changing", "effortlessly",
    "transform overnight", "AI-driven", "AI-powered".

[ ] TONE-2: Client brief tone is constructive throughout
    The client brief does not use alarmist language about risks.
    Reputation risks and complaint themes are framed as observations and opportunities.

[ ] TONE-3: Internal brief is appropriately direct
    The internal brief does not over-soften findings.
    Critical and high severity items must be named clearly.
    Confidence flags and internal notes must be present and labeled.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

List every check with result. Then:

SUMMARY
  Passed: X / 18
  Failed: X
  Warnings: X

VERDICT: PUBLISH READY
or
VERDICT: REQUIRES REVISION
  — List of FAIL check IDs
  — For each: the specific text to fix and the corrected direction

Be specific. Quote actual text that fails. Do not give vague feedback.

ANALYSIS JSON:
[PASTE analysis.json HERE]

INTERNAL BRIEF SECTIONS:
[PASTE internal brief HTML sections HERE]

CLIENT BRIEF SECTIONS:
[PASTE client brief HTML sections HERE]
```
