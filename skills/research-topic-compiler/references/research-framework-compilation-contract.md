---
name: research-framework-compilation-contract
description: Compile a research-specific explanation framework from the user goal, revise it with evidence, and project the latest version into Markdown or HTML
---

# Research Framework Compilation Contract

Use this contract for `Normal Research`, `Application`, `Learning Pack`, and business-facing research reports when the result must be logically complete, progressive, and useful to a defined reader. It governs how the research explanation is organized. It does not replace the evidence loop or provide one universal report outline.

## Core Model

```text
User Goal
  -> Research Job
  -> Explanation Framework V0
  -> Evidence acquisition and interpretation
  -> Structural change events
  -> Explanation Framework Vn
  -> Markdown / HTML projection
```

The first framework is a working hypothesis about how to explain the topic. The final framework is compiled from the latest evidence and the user's actual purpose. Do not freeze the user's first wording, a seed article's table of contents, or a familiar report template as the final structure.

## Two Linked Frameworks

Keep these layers distinct and linked:

| Layer | Question it answers | Typical objects | Quality test |
| --- | --- | --- | --- |
| `Evidence Framework` | What must be known, tested, or proven? | claims, hypotheses, evidence requirements, gaps, confidence | Can every important conclusion be traced to sufficient evidence? |
| `Explanation Framework` | In what logic should this reader understand the issue? | controlling question, conclusion spine, sections, relationships, progression | Does the structure answer the Research Job clearly, progressively, and without material overlap or omission? |

The Evidence Framework may contain more detail than the final report. The Explanation Framework selects and orders evidence-bearing conclusions for comprehension. Every material explanation node must map to one or more evidence claims, or be labeled as context, inference, assumption, or open question.

## Step 1: Identify the Research Job

Translate the user's goal into the job the research must perform. Do not infer the framework from the topic noun alone.

Common Research Jobs include, but are not limited to:

- build a first-principles understanding;
- explain an industry's current state and evolution;
- compare approaches, products, or operating models;
- diagnose a user or business problem;
- translate external practices into the user's domain;
- prepare product strategy, Roadmap, PRD, workflow, or evaluation input;
- discover candidates without making the final choice;
- teach an unfamiliar field;
- maintain an evolving research radar.

A research run can contain multiple jobs. Name one primary job and mark secondary jobs. If two jobs imply incompatible audiences or structures, split the deliverable rather than forcing them into one outline.

Minimum framing:

```yaml
research_job:
  primary: "After reading this, what can the user understand, judge, or do?"
  secondary: []
  audience: []
  decision_or_action_enabled: ""
  controlling_question: ""
  out_of_scope: []
```

## Step 2: Generate Explanation Framework V0

Build V0 after Research Goal Framing and before broad acquisition. V0 is a revisable logic map, not the report's locked table of contents.

```yaml
explanation_framework:
  version: "v0"
  research_job: ""
  audience: []
  controlling_question: ""
  conclusion_spine: "The shortest coherent path from the question to a usable answer"
  dominant_logic: "chronology | comparison | causal | hierarchy | workflow | decision | learning | hybrid"
  nodes:
    - id: "XF-01"
      purpose: "What this node helps the reader understand or judge"
      level: "context | dimension | mechanism | finding | implication | action"
      relation_to_parent: "explains | causes | compares | precedes | decomposes | supports | challenges | applies"
      question: ""
      provisional_answer: ""
      evidence_claim_ids: []
      children: []
      status: "open | supported | contested | reframed | removed"
  known_omissions: []
```

V0 should be just detailed enough to guide research:

- `L1`: one controlling question and a short answer path.
- `L2`: roughly 3-5 nodes, usually maintained inline.
- `L3`: a visible framework map with evidence links and open questions.
- `L4/L5`: explicit versioning, structural events, contradiction handling, and quality checks.

Do not force all studies through a fixed set of industry questions. For example, “行业位置、厂商做法、最佳实践、演变路线、业务迁移” can be useful for one applied industry study, but it is an eval fixture or candidate pattern, not the universal framework.

## Step 3: Link Evidence and Explanation

During research, maintain a two-way mapping:

```text
Explanation Node -> Evidence Claims needed to answer it
Evidence Claim -> Explanation Nodes whose meaning may change
```

Apply these rules:

- An evidence acquisition can update claim confidence without changing report structure.
- A material claim change can require a structural revision.
- A section with no evidence mapping must be labeled as framing, inference, assumption, or open question.
- Evidence that does not serve any current node may reveal a missing node, or may simply be irrelevant. Do not add it merely because it was collected.
- Report order follows explanation logic, not source discovery order.

## Step 4: Record Structural Change Events

After each material Evidence Framework update, ask whether the Explanation Framework should change. Record one event when it does, or `No structural change` when the acquisition is meaningful but the structure remains valid.

| Event | Use when |
| --- | --- |
| `Add` | Evidence reveals a material missing dimension, stage, actor, mechanism, or implication. |
| `Split` | One node contains concepts with different conditions, audiences, or evidence paths. |
| `Merge` | Multiple nodes are redundant or are better explained by one underlying mechanism. |
| `Reorder` | Reader comprehension or causal/temporal dependency requires a different sequence. |
| `Reframe` | The controlling question, dominant logic, or meaning of a major branch changes. |
| `Remove` | A node is unsupported, irrelevant to the Research Job, or only inherited from the seed. |
| `Challenge` | Evidence makes the structure contested but not yet replaceable. Preserve the competing frame. |
| `No structural change` | Evidence changes confidence or detail without changing the explanation logic. |

```yaml
structural_change_event:
  id: "SCE-01"
  from_version: "v0"
  to_version: "v1"
  type: "Add | Split | Merge | Reorder | Reframe | Remove | Challenge | No structural change"
  trigger_claim_ids: []
  affected_node_ids: []
  before: ""
  after: ""
  reader_impact: "How this improves or changes understanding"
  rationale: "Why the evidence or user goal requires this change"
```

Do not create a new version for cosmetic wording changes. Do create one when the controlling question, branch boundaries, logical relation, or reading sequence materially changes.

## Step 5: Run the Framework Quality Gate

Before synthesis, inspect the latest Explanation Framework against all checks below.

| Check | Pass condition | Repair action |
| --- | --- | --- |
| Goal fit | Every major branch helps answer the Research Job. | Remove or demote interesting but non-essential material. |
| Controlling question | The report has one primary question and a coherent conclusion spine. | Reframe or split incompatible jobs. |
| Abstraction level | Sibling nodes are comparable in level and type, unless the relation is explicit. | Split, merge, or relabel mixed-level nodes. |
| Logic relation | Each group states whether it is chronological, comparative, causal, hierarchical, workflow, decision, learning, or another named relation. | Choose and state the dominant relation. |
| Progression | A reader can move from context to understanding, judgment, implication, and action where applicable. | Reorder nodes around cognitive dependency. |
| Overlap | No two branches answer substantially the same question without an explicit comparison. | Merge or redefine boundaries. |
| Coverage | No material question required by the Research Job is silently missing. | Add a node or disclose a known omission. |
| Relative MECE | The framework is mutually distinct and collectively sufficient for the current scope and evidence budget. | Resolve overlap and disclose non-blocking omissions; do not claim universal completeness. |
| Evidence mapping | Material findings map to claims and sources; uncertainty remains visible. | Add mapping, downgrade the statement, or keep it open. |
| Audience fit | The structure matches the reader's decisions and knowledge level. | Reframe terminology, sequence, and implication layer without changing evidence strength. |

`Relative MECE` means fit-for-purpose within the declared scope, audience, evidence access, and budget. It does not mean the topic has been exhaustively partitioned for all possible users.

## Step 6: Freeze Framework Vn and Synthesize

Synthesize only after the evidence loop reaches its unique terminal state and the latest framework passes the quality gate at the required depth.

The synthesis sequence is:

1. Freeze the latest valid Explanation Framework as `Framework Vn` for this run.
2. Write the one-sentence conclusion and conclusion spine from Vn.
3. Populate each node with evidence-bearing findings, confidence, counterexamples, and implications.
4. Expose material structural changes when they help the reader understand why the final frame differs from the initial one.
5. Preserve residual gaps, contested branches, and known omissions.
6. Project Vn into the requested artifact mode.

Do not write the final report by filling V0 section headings in place. Recompile from Vn, even if that means changing the original order or removing an inherited section.

## Step 7: Project to Markdown or HTML

Markdown and HTML must share the same controlling question, conclusion spine, node boundaries, evidence mapping, confidence, and residual gaps. The visual form may change; the reasoning must not.

Choose visual forms from relationships in Vn:

| Relationship in Vn | Preferred visual form |
| --- | --- |
| Stages, maturity, or evolution | numbered progression, staircase, or timeline |
| Comparison across stable dimensions | matrix, compact table, or aligned columns |
| Causal mechanism or dependency | causal chain or directed flow |
| Workflow or handoff | process flow or swimlane |
| Hierarchy or taxonomy | tree or nested map |
| Feedback or iteration | loop diagram |
| State and transition | state map |
| Claim and evidence support | evidence map or claim-source matrix |
| Priority and uncertainty | quadrant or ordered portfolio |

Use a visual only when it makes a relationship materially easier to understand. Do not convert every section into cards or diagrams. Preserve information density with tables, annotations, drill-down sections, and visible source links.

## User-Provided Structure Boundary

When the user provides a clear report structure:

- treat it as an explicit output contract;
- map it to the Research Job and evidence claims;
- preserve it when it is coherent and sufficient;
- do not reorganize merely to demonstrate framework compilation;
- propose or apply a change only when evidence reveals a material overlap, omission, contradiction, or sequence problem;
- if the user explicitly forbids restructuring, keep the structure and disclose the limitation unless safety or factual integrity requires escalation.

## Failure Patterns

- Reusing the last successful report's questions as a universal framework.
- Treating a report template as the Evidence Framework.
- Keeping V0 unchanged after evidence invalidates its assumptions.
- Updating claims but not reconsidering explanation order or branch boundaries.
- Organizing the report by company, source, or browsing order when the user needs a cross-source synthesis.
- Claiming MECE without naming scope, audience, or known omissions.
- Creating a highly visual HTML artifact that hides weak evidence or drops report detail.
- Rewriting a sound user-provided outline without a material reason.

## Completion Evidence

For `L3+`, the final research result should make these inspectable:

- Research Job and controlling question;
- Explanation Framework V0 or its concise initial logic;
- latest Framework Vn;
- material structural change events, or a justified statement that none were needed;
- quality-gate outcome and known omissions;
- mapping between major explanation nodes and evidence claims;
- consistent Markdown/HTML projection from Vn.
