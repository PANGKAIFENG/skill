# Research Topic Compiler Evals

This suite separates routing compatibility from research-behavior quality.

## Running Comparisons

- Snapshot the old Skill before editing it.
- Run old and new versions with the same model, prompt, fixture files, and grader.
- Treat the fixture summaries as frozen eval evidence, not as current public documentation.
- Do not use network access for deterministic old/new comparison.
- Run live source retrieval only as a separate smoke test.
- Capture the final output and tool/read trace. A final answer alone cannot prove that a boundary case avoided unnecessary acquisition.

## Holdout Boundary

The independent holdout is intentionally absent from this directory. Reveal it only after the candidate Skill version is frozen.

## Grading

Use `graders/iterative-research-rubric.md`. Objective assertions may be checked against fixture IDs and paths. Gap quality, source independence, framework change, and stopping sufficiency require model or human review.

Use `graders/research-framework-compilation-rubric.md` for framework-compilation cases. It grades Research Job fit, separate Evidence/Explanation Frameworks, structural adaptation, logical progression, relative MECE, user-provided structure boundaries, and consistent Markdown/HTML projection.

Use `graders/dashboard-artifact-rubric.md` for `research-dashboard-html` runs. Grade both files plus the trace, run the validator, and keep browser-only claims unverified until desktop/mobile evidence exists.

Use `graders/learning-report-rubric.md` for `learning-report-html` runs. Grade the continuous reading flow, thesis and mechanism depth, comparison, boundaries, user translation, action quality, audit-layer evidence placement, and desktop/mobile UI. Marker compliance alone is not a semantic pass.

The learning-report release gate includes a frozen activation transfer fixture and a synthetic non-AI feature-flag holdout. Generate both HTML + summary pairs in an external eval workspace, run the validator, and record a rubric score. The holdout is frozen after the candidate contract is authored; do not tune the contract against its prose or expected answer.

## Deterministic Checks

Run from the repository root:

```bash
python3 -m unittest discover -s skills/research-topic-compiler/tests -v
python3 -m py_compile skills/research-topic-compiler/scripts/validate_html_artifact.py
python3 skills/research-topic-compiler/scripts/validate_html_artifact.py \
  skills/research-topic-compiler/evals/fixtures/research-dashboard/dashboard.html
jq empty skills/research-topic-compiler/evals/evals.json
```

The unit suite covers both dashboard roots plus the learning-report root, required real-element attributes, evidence-secondary placement, core-claim count, missing markers, dual roots, comment/script fake markers, backend calls, unresolved placeholders, local source paths, and the persisted general Dashboard fixture.

## Behavior Run Layout

Save each old/new comparison under the external evaluation workspace, not inside the Skill package:

```text
research-topic-compiler-workspace/dashboard-reintegration/iteration-N/<eval-id>/
  eval_metadata.json
  old_skill/outputs/
  with_skill/outputs/
  old_skill/grading.json
  with_skill/grading.json
```

Use the snapshot SHA in run metadata. Do not rewrite the existing `iteration-1-new` benchmark schema; record Dashboard results as a separate release-gate suite.

To create a static review artifact with the shared viewer:

```bash
python3 /path/to/skill-creator/eval-viewer/generate_review.py \
  /absolute/path/to/dashboard-reintegration/iteration-N \
  --skill-name research-topic-compiler \
  --static /absolute/path/to/dashboard-reintegration/iteration-N/review.html
```

Open the static file directly. Its feedback button downloads `feedback.json`; a plain `python3 -m http.server` does not implement the viewer's feedback API.
