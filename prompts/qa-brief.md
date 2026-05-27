# Prompt: QA Pass — Brief Integrity Check

**Run this last**, after generating both internal and client brief sections.

Feed it the analysis JSON plus both sets of generated HTML sections.
It will flag violations before you publish.

---

## HOW TO USE

1. Open a Claude Code session
2. Paste this prompt
3. Paste the `analysis.json` object
4. Paste the full internal brief HTML sections
5. Paste the full client brief HTML sections
6. Review all flags before publishing either brief

---

## PROMPT

```
QA BRIEF INTEGRITY CHECK

You are performing a quality assurance review of two generated hospitality intelligence briefs.

You will be given:
1. The Layer 2 analysis JSON object (the controlled evidence source)
2. The internal brief HTML sections
3. The client brief HTML sections

Your job is to check both briefs against the analysis object and flag any violations.

OUTPUT FORMAT:
Produce a structured QA report with PASS or FAIL for each check.
For each FAIL, quote the specific offending text and state what rule it breaks.
Conclude with an overall verdict: PUBLISH READY or REQUIRES REVISION.

CHECKS TO RUN:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVIDENCE INTEGRITY (both briefs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] EVIDENCE-1: Excluded reviews not used
    No claims reference reviews that were excluded (low-confidence, duplicate, flagged).
    Check: does the analysis JSON show excluded_low_confidence or excluded_duplicate > 0?
    If so, do either briefs draw conclusions that could only come from excluded captures?

[ ] EVIDENCE-2: No unsupported trend claims
    Every trend or pattern claim in both briefs must trace to top_strengths, top_complaints,
    service_risk_areas, or guest_expectation_mismatches in the analysis JSON.
    Flag any claim that appears to be invented or extrapolated beyond the evidence.

[ ] EVIDENCE-3: Isolated incidents not presented as patterns
    Any complaint where is_pattern: false must not be written as a recurring theme.
    Acceptable: "One guest noted..." or "An isolated report..."
    Not acceptable: "Guests consistently report..." or "A recurring issue..."

[ ] EVIDENCE-4: Owner responses not treated as guest sentiment
    Neither brief should draw sentiment conclusions from hotel management responses.
    Check: does any claim appear to be based on owner tone rather than guest experience?

[ ] EVIDENCE-5: Frequency language matches data
    Check that intensity qualifiers in the briefs roughly match mention counts in the JSON.
    "Consistently" / "repeatedly" / "overwhelmingly" → should have 5+ mentions.
    "Some guests" / "a few reviewers" → appropriate for 1–3 mentions.
    Flag any mismatch between language intensity and evidence volume.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEPARATION OF INTERNAL / CLIENT (critical)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] SEPARATION-1: Internal notes not in client brief
    The client brief must not contain any content from internal_note fields in top_complaints.
    Check each top_complaint's internal_note against the client brief text.

[ ] SEPARATION-2: Confidence notes not in client brief
    The client brief must not reference confidence_notes content, extraction warnings,
    data quality flags, or language like "low confidence", "capture", "excluded", or "flagged".

[ ] SEPARATION-3: Technical language absent from client brief
    The client brief must not contain: "scraping", "packet", "capture", "confidence score",
    "extraction", "low-confidence", "analysis object", "Layer 2", "pipeline".

[ ] SEPARATION-4: Risk severity language softened in client brief
    "critical" severity items should not appear as "critical" in the client brief.
    They should be reframed as "significant opportunity" or "worth prioritizing".

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDATION TRACEABILITY (both briefs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] RECS-1: Quick wins map to analysis data
    Each quick win must correspond to a complaint, service risk area, or alignment gap
    in the analysis JSON. Flag any quick win without a traceable source.

[ ] RECS-2: Strategic recommendations have rationale grounded in evidence
    Each strategic recommendation must reference at least one specific finding
    (complaint theme, alignment gap, expectation mismatch). Generic advice is a flag.

[ ] RECS-3: Website alignment recommendations match gaps in JSON
    Each website alignment recommendation in both briefs must correspond to a
    website_alignment_gaps entry. No gaps should be invented.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TONE AND FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] TONE-1: Prohibited words absent
    Neither brief uses: "revolutionary", "game-changing", "effortlessly",
    "transform overnight", "AI-driven", "AI-powered".

[ ] TONE-2: Client brief tone is constructive, not alarming
    The client brief does not use alarmist language about risks.
    Findings are framed as opportunities or observations, not verdicts.

[ ] TONE-3: Internal brief is appropriately skeptical
    The internal brief does not over-soften serious findings.
    Critical risks should be named clearly, not buried in diplomatic language.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For each check above, output:
  ✓ PASS — [check ID]: [one-line confirmation]
  ✗ FAIL — [check ID]: [offending text quoted] → [rule broken]
  ⚠ WARN — [check ID]: [borderline case, judgment call noted]

Then output:

SUMMARY
  Passed: X / 15
  Failed: X
  Warnings: X

VERDICT: PUBLISH READY
or
VERDICT: REQUIRES REVISION — [list of FAIL check IDs to address]

Be specific. Quote the actual text that fails. Do not give vague feedback.

ANALYSIS JSON:
[PASTE analysis.json HERE]

INTERNAL BRIEF SECTIONS:
[PASTE internal brief HTML sections HERE]

CLIENT BRIEF SECTIONS:
[PASTE client brief HTML sections HERE]
```
