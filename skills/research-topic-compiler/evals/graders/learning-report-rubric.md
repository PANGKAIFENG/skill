# Learning Report HTML Rubric

Use this rubric for `learning-report-html`. Grade the generated HTML, companion summary, and trace. Run the static validator first; do not infer visual or semantic quality from marker compliance.

## Automatic Failures

- HTML or required companion summary is missing or empty.
- The route uses the Dashboard root or makes evidence/status administration the dominant reading surface.
- The report changes the named research object, hides a material counterexample, or presents inference as runtime fact.
- Static validation fails, the page has whole-document horizontal overflow, or core content requires a backend/CDN.
- The reading layer exposes research-control vocabulary, evidence filters, or status administration as part of the learning path.

## Weighted Review

| Dimension | Weight | Pass condition |
| --- | ---: | --- |
| Research Job and thesis | 15 | One primary reader, explicit learning outcome, controlling question, and a precise contestable thesis. |
| Mechanism depth | 20 | At least three core claims explain causal/operational mechanisms, not only definitions or feature lists. |
| Evidence and boundaries | 15 | Claims remain traceable; counterexamples, limitations, and overturn conditions bound the argument without dominating it. |
| Narrative coherence | 15 | Continuous logical progression; sections are not organized by source, research stage, or disconnected cards. |
| Comparison and user translation | 15 | Exact comparisons explain why differences matter and connect them to the reader's current state. |
| Action quality | 10 | Bounded changes or experiments include deliverable, acceptance/stop criteria, and user value. |
| Editorial UI | 10 | Restrained hierarchy, readable type scale, purposeful visuals, secondary evidence appendix, and usable desktop/mobile layout. |

Release threshold: 85/100, no automatic failure, and no dimension below half credit. Compare old/new blind when the release claim is that the new Skill materially improves quality.

## Blind Comparison Protocol

When evaluating an existing-Skill improvement, remove filenames and version labels, randomize the old/new order, and have the reviewer score both artifacts with the same weighted review before revealing identity. Record:

- total and per-dimension score;
- which artifact better supports each Learning-Effect Question;
- any regression in factuality, boundary language, or mobile usability;
- the minimum meaningful delta required for release.

Release the candidate only when it clears 85/100 and beats the baseline by at least 8 points without losing factual/boundary accuracy. Run one historical regression, one transfer case, one near-boundary negative case, and one independent holdout that was not used to tune the contract.

## Learning-Effect Questions

After reading the main narrative without opening the evidence appendix, the reviewer should be able to answer:

1. What is the central model and why does it matter?
2. How do at least two mechanisms work?
3. What is one meaningful comparison and its consequence?
4. Where does the conclusion stop applying or remain uncertain?
5. What should the target reader change or test next?

Failure on two or more questions means the artifact is still concept introduction, not a deep learning report.
