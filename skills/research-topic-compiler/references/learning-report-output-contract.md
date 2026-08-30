# Learning Report HTML Output Contract

Use this contract when the user's primary job is to deeply understand a topic, build a durable mental model, compare it with their current situation, and decide what to change. This is the default HTML route for `Learning Pack`, and it can also serve `Normal Research` or `Application` when there is one primary reader and continuous learning matters more than cross-functional scanning.

The internal design name is **Deep Editorial Learning Report**. Do not display that label unless the user asks about the format.

## Artifact Boundary

Choose `learning-report-html` when the reader should move through an argument from beginning to end. Choose `research-dashboard-html` when several roles need to scan evidence, status, confidence, and actions independently. Choose `frontend-design` when the content is fixed and the request is only to redesign or implement a UI.

An HTML request alone does not imply a Dashboard. When the prompt says “让我系统学会”, “逐步理解”, “深入解释”, “对比我的现状”, or “最后落到怎么改”, prefer this route.

## Required Inputs

Do not render until all of these exist:

- A resolved primary reader and Reader Contract.
- A latest Explanation Framework and a three-to-five-claim conclusion spine.
- Claim-to-evidence mapping and a clear audit-layer destination.
- Mechanism and boundary analysis for each core claim.
- A user-context comparison or application path when the user's current system/workflow is in scope.
- `ready` from `editorial-projection-gate.md`.

## File Layout

Honor the user's filename and output directory when specified. Otherwise create:

```text
./learning-report-outputs/<topic-slug>/
  report.html
  summary.md
```

The report must be self-contained: inline content, CSS, and JavaScript; no backend, build step, runtime API, analytics, remote font dependency, or required CDN. Optional links in the source appendix may point to public sources.

## Content Contract

The exact section names come from the Explanation Framework. The report as a whole must let the reader answer:

1. What is the subject really about, and what problem does it solve?
2. What is the report's central judgment?
3. Through what mechanism or execution chain does that judgment hold?
4. What alternatives, stages, or systems differ, and why?
5. Where does the judgment fail, remain uncertain, or need qualification?
6. How does this compare with the reader's current state?
7. What should the reader change, test, or learn next?

Every core claim must pass the Claim / Mechanism / Evidence / Boundary / User implication / Overturn condition depth test from `editorial-projection-gate.md`. The visible prose should feel authored, not templated around those labels.

## Information Architecture

Use this as a flexible editorial rhythm, not a fixed table of contents:

1. **Opening thesis**: literal subject title, a precise standfirst, and a short map of the argument. Do not show research status or evidence administration in the hero.
2. **Mental model**: define the object and the central model before listing details.
3. **Mechanism**: trace the causal, operational, or code path that makes the model work.
4. **Comparison**: use one exact table or aligned visual for meaningful differences; explain why the differences matter.
5. **Evolution or boundary**: show stages, tradeoffs, counterexamples, or what comes next only when they advance the thesis.
6. **Reader translation**: compare the findings with the reader's current workflow, architecture, or decisions.
7. **Action**: propose bounded changes, experiments, acceptance criteria, and stop conditions.
8. **Audit appendix**: compact source notes, evidence identity, limitations, and methods at the end or inside collapsed disclosure.

Do not create a standalone evidence chapter in the main narrative unless evidence interpretation is itself the subject.

## Visual System

Start from `assets/semantic-editorial-template.html`, then adapt the layout to the report's relationships.

- Use a centered reading column for prose and a wider measure only for tables or diagrams.
- Use one restrained display type scale: desktop H1 about 56-68px, H2 about 32-40px; mobile H1 about 36-40px, H2 about 26-30px.
- Keep the opening section normally within 60-65vh on desktop and leave the next section visible.
- Do not scale font size with viewport width; use fixed breakpoints.
- Use a compact top navigation or in-flow contents list; no persistent reading sidebar by default.
- Use cards only for repeated peer items. Do not put sections in floating cards or nest cards.
- Use one exact comparison table where comparison matters and one to three purposeful visuals that encode a relationship. Avoid decorative diagrams.
- Use color for hierarchy and semantic distinction, not as a one-hue theme. Avoid purple/blue gradients, decorative blobs, glassmorphism, and oversized marketing composition.
- Keep evidence citations visually quiet but keyboard reachable. Put full evidence in endnotes or a collapsed appendix.
- Keep long paths and identifiers wrap-safe with `overflow-wrap:anywhere`.

## Required Markers

Place these attributes on real elements inside exactly one `data-learning-report` root:

```html
data-learning-report
data-report-thesis
data-report-nav
data-reading-path
data-core-claim
data-mechanism
data-report-comparison
data-application
data-action
data-report-boundary
data-evidence-appendix
data-sources
```

Use three to five `data-core-claim` elements, at least two `data-action` elements, and one to three `data-visual-memory` elements. Put `data-evidence-appendix` on a `<details>` element or set `data-evidence-placement="endnotes|footnotes|collapsed"` on that element. A `<details>` audit appendix must be collapsed by default.

## Summary Contract

`summary.md` is a delivery companion, not a duplicate report. Include the reader, Research Job, central thesis, three-to-five core claims, intended action, important boundary, artifact path, source/audit location, and validation result.

## Verification

Run:

```bash
python3 scripts/validate_html_artifact.py <report.html> <summary.md>
```

Static validation rejects required remote assets, unresolved internal links, an expanded-by-default evidence appendix, missing comparison/boundary/action semantics, and research-control vocabulary leaking into the reading layer. It complements but does not replace browser and editorial review.

Then check at desktop, tablet, and `390x844` mobile:

- no whole-document horizontal overflow, clipped text, overlap, or blank content;
- title and opening section do not consume the whole first viewport;
- navigation anchors work and keyboard focus is visible;
- tables remain readable through wrapping or local scrolling;
- evidence appendix opens and every referenced footnote resolves;
- console has zero errors;
- the report still reads coherently with JavaScript disabled.

Finally apply the learning-effect rubric: a reviewer should be able to restate the central model, explain at least two mechanisms, name a meaningful boundary, compare the topic with the user's current state, and identify the next bounded action without opening the evidence appendix.

## Definition of Done

The route is complete only when the HTML and summary exist, static validation passes, browser checks pass or limitations are explicit, the audit layer remains accessible, and semantic review confirms depth, viewpoint, transfer, and action. A visually polished file that merely introduces concepts is not complete.
