# Editorial Projection Gate

Use this gate after research synthesis and before writing any `learning-report-html` artifact. Its purpose is to convert research state into a coherent reader experience without weakening traceability.

## Two-Layer Model

Keep two distinct layers:

1. **Reading layer**: the thesis, explanatory model, mechanisms, comparisons, boundaries, user-context translation, and actions.
2. **Audit layer**: source lineage, evidence grades, detailed citations, research limitations, change events, and unresolved evidence gaps.

The reading layer is the default surface. The audit layer remains reachable through footnotes, endnotes, a compact source table, or a collapsed appendix. Only uncertainty, counterevidence, or a limitation that can change the conclusion belongs in the main narrative.

Do not expose research-control vocabulary such as `terminal status`, `NBE`, `Framework Vn`, `confidence ledger`, or `evidence map` in the default reading flow unless the term itself matters to the subject. Translate it into natural reader language such as “what is established”, “where this stops applying”, or “what would change this judgment”.

## Reader Contract

Before outlining the report, write an internal Reader Contract:

- Primary reader and their current level.
- What they should understand after reading.
- What judgment they should be able to make.
- What comparison to their current situation matters.
- What they should change, test, or stop doing next.
- What is intentionally out of scope.

For learning work, the report is incomplete if the reader can repeat terminology but cannot explain the mechanism, distinguish alternatives, or act differently.

## Conclusion Spine

Compile three to five contestable core claims. A core claim is not a topic label or generic principle. It must state a position that could be wrong and explain why it matters.

For every core claim, verify the following authoring fields internally:

| Field | Required question |
| --- | --- |
| Claim | What exactly are we asserting? |
| Mechanism | Through what causal or operational chain does it happen? |
| Evidence basis | Which fact, code path, case, or observation supports it? |
| Boundary / counterexample | Where does it stop applying or what contradicts it? |
| User implication | What changes for this reader's product, system, or workflow? |
| Overturn condition | What new evidence would materially change the judgment? |

Do not render these six labels mechanically for every paragraph. Use them as a depth test, then write natural prose. Keep compact citations beside the relevant claim and put detailed evidence in the audit layer.

## Narrative Compilation

Choose the dominant logic from the latest explanation framework. Common sequences include:

- premise -> mechanism -> system model -> comparison -> application;
- historical pressure -> operating model -> current inflection -> future boundary -> action;
- user problem -> competing mechanisms -> evidence-led diagnosis -> intervention;
- architecture path -> responsibility boundaries -> failure modes -> design implications.

Use only the sequence that fits the Research Job. Do not create one section per source, company, evidence type, or research stage. Merge related material into a single argument and remove repeated summaries.

## Fragmentation Check

Before rendering:

- Each major section advances one part of the conclusion spine.
- Adjacent sections have a visible logical transition.
- Tables are used for exact comparison, not to avoid writing synthesis.
- Cards are reserved for repeated peer items; the main argument stays in paragraphs, figures, or unframed bands.
- No major claim appears only as a slogan, badge, metric tile, or isolated card.
- No evidence section interrupts the narrative merely to prove that research happened.

If the outline feels like a collection of modules, recompile it around the controlling question before styling it.

## Evidence Placement Rules

- Put citation numbers or short source labels next to claims that need support.
- Put full source identity, locator, role, and limitations in endnotes or the collapsed appendix.
- Keep counterevidence in the main flow when it changes the claim's scope.
- Keep a material unknown in the main flow when acting without it would be unsafe.
- Do not repeat the same evidence in a dedicated chapter and again in every claim card.

## Projection Decision

Return one internal decision before HTML authoring:

- `ready`: Reader Contract, conclusion spine, depth fields, narrative sequence, and audit mapping are complete.
- `recompile`: Research is sufficient but the reader flow is fragmented or generic; revise the explanation framework.
- `research-gap`: A core claim lacks enough evidence or a boundary could reverse the conclusion; return to research.
- `wrong-artifact`: The user needs multi-role scanning or evidence audit, so use `research-dashboard-html`; or they need only UI implementation, so hand off to `frontend-design`.

Only `ready` proceeds to the learning-report template.
