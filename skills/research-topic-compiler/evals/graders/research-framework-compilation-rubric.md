# Research Framework Compilation Grader

Use this grader for cases whose main risk is a generic, fixed, source-ordered, or example-overfit report structure. Grade the final artifact together with the research trace and any Framework/Change Event state. Do not reward extra sections, visual decoration, or repeated technical terminology.

## Evidence To Inspect

1. User goal, audience, requested action, and any explicit structure constraint.
2. Research Goal Framing and named Research Job.
3. Explanation Framework V0 and latest Framework Vn.
4. Evidence Framework claims and their mapping to explanation nodes.
5. Structural Change Events and evidence triggers.
6. Final Markdown/HTML artifact and its relationship to Framework Vn.

If a run only presents a polished final outline without showing the requested V0/Vn or change evidence, do not infer that framework compilation occurred.

## Critical Gates

A case cannot pass if any applicable gate fails:

- The framework is copied from a prior example, seed table of contents, source order, or generic template without fitting it to the current Research Job.
- Evidence Framework and Explanation Framework are treated as the same object.
- Material evidence invalidates the explanation logic but the report keeps V0 and merely appends caveats.
- The final report is not synthesized from Framework Vn.
- A coherent user-provided structure is changed without a material evidence, logic, safety, or factual-integrity reason.
- A Markdown/HTML projection changes conclusion boundaries, evidence strength, material uncertainty, or residual gaps.
- The run claims absolute MECE completeness without bounding scope, audience, evidence access, and budget.

## Semantic Rubric

Score each dimension from 1 to 5.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Research Job fit | Starts from the topic noun | Mentions audience or goal | Names primary job, audience, enabled action, controlling question, and out-of-scope; structure directly serves them |
| V0 quality | Generic headings or source list | Relevant sections but unclear logic | Revisable conclusion spine, dominant logic, comparable nodes, relationships, evidence needs, and known omissions |
| Two-framework mapping | Evidence and explanation are conflated | Some claim links exist | Every material explanation node maps to evidence claims or is explicitly labeled context, inference, assumption, or open question |
| Structural adaptation | Evidence is appended to a frozen outline | Changes are mentioned | Material Add/Split/Merge/Reorder/Reframe/Remove/Challenge events preserve before, after, trigger, rationale, and reader impact |
| Logical progression | Sections are piled up | Mostly readable | One coherent path uses explicit chronological, comparative, causal, hierarchical, workflow, decision, learning, or justified hybrid relations |
| Relative MECE | Overlap and gaps are hidden | Some boundaries stated | Sibling levels are comparable, overlap is resolved, material omissions are disclosed, and sufficiency is bounded to the current job |
| User structure boundary | Rewrites user structure by default | Mostly preserves it | Treats a sound supplied outline as a contract and changes it only for a disclosed material reason |
| Artifact projection | Markdown and HTML become different stories or lose detail | Core conclusion is similar | Framework Vn, evidence strength, uncertainty, gaps, and conclusion boundaries remain consistent; visuals follow actual relationships without lowering information density |

## Case-Specific Expectations

- `framework-compilation-skill-evaluation-industry-regression`: the industry-oriented concerns belong to this job, but the run must not claim they are the universal framework.
- `framework-compilation-transfer-user-activation-diagnosis`: a causal or behavioral diagnosis frame should replace industry-status and vendor-practice sections.
- `framework-compilation-preserves-user-provided-structure`: preserving the three chapters is critical.
- `framework-compilation-reframes-after-evidence`: appending caveats to the six-stage model is insufficient; a material reframe or challenge is required.

## Scoring

- Convert the eight semantic dimensions to an 80-point score: `sum(scores) / 40 * 80`.
- Give up to 20 points for the case's explicit assertions, weighted equally unless marked critical.
- Cap the total at 79 if any critical gate fails.
- Historical regression, negative boundary, and structural-reframe cases require all critical assertions to pass.
- Transfer requires at least 80/100.

## Required Grading Output

```json
{
  "expectations": [
    {"text": "<assertion>", "passed": true, "evidence": "<specific artifact or trace evidence>"}
  ],
  "rubric_scores": {
    "research_job_fit": {"score": 1, "evidence": "..."},
    "v0_quality": {"score": 1, "evidence": "..."},
    "two_framework_mapping": {"score": 1, "evidence": "..."},
    "structural_adaptation": {"score": 1, "evidence": "..."},
    "logical_progression": {"score": 1, "evidence": "..."},
    "relative_mece": {"score": 1, "evidence": "..."},
    "user_structure_boundary": {"score": 1, "evidence": "..."},
    "artifact_projection": {"score": 1, "evidence": "..."}
  },
  "total_score": 0,
  "critical_gate_failed": false,
  "verdict": "pass | fail | needs-human-review",
  "uncertainties": []
}
```
