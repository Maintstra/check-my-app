# Findings and report contract

Use `check-my-app-report@1.1.0` for new reports. Its machine-readable definition is `report-schema-v1.1.json`; validate with `scripts/validate_report.py`. The validator retains read compatibility with legacy `check-my-app-report@1.0.0` reports.

The JSON Schema is the structural contract. `scripts/validate_report.py` is the required semantic gate because JSON Schema cannot prove cross-reference targets, artifact hash equality across passes, or that final-pass evidence is independent. A schema-only pass is not report validation.

## Evidence ledger

For each material claim record:

- stable claim ID;
- `confirmed`, `inference`, or `untested`;
- one factual statement;
- evidence IDs supporting it.

Confirmed claims need direct evidence. Inferences must name their basis. Untested claims must say why and what would test them.

## Finding shape

Every finding must contain:

| Field | Required content |
|---|---|
| Evidence | Claim and evidence IDs with a stable artifact/source locator |
| User impact | The task, decision, safety, accessibility, or trust consequence |
| Root cause | The component, state, rule, data boundary, or feedback contract causing the issue |
| Recommended change | Exact location plus copy/layout/flow/state/rule/test change |
| Alternative | A reasonable second option |
| Trade-offs | Main usability, safety, effort, and maintenance difference |
| Severity | `Blocking`, `Must fix`, `Improve`, or `Polish` |
| Status | `open`, `resolved`, or `reopened` |
| Effort | `S`, `M`, or `L` |
| Retest | Starting state, action, observable result, and failure condition |

Reject advice such as “simplify the UI,” “make it clearer,” or “improve error handling.” Name what changes and how the user will perceive it.

## Severity

- `Blocking`: prevents a required journey, creates material deception or unsafe authority, or lacks safe recovery.
- `Must fix`: materially harms completion, trust, accessibility, or supportability but does not meet Blocking.
- `Improve`: measurable friction, density, inconsistency, or maintenance cost.
- `Polish`: low-risk fit-and-finish improvement.

Use effort only as a rough delivery size: `S` focused local change, `M` cross-component change, `L` architectural or multi-surface change.

## Human-facing order

1. verdict and tested boundary;
2. blocking and must-fix findings;
3. recommended next implementation sequence;
4. evidence and untested areas;
5. improve/polish findings and technical details.

Group repeated symptoms under one root cause while retaining screen-specific evidence and acceptance checks.

In Delivery Closure, also record capabilities, roles, surfaces, personas, configurations, lifecycle stages, and safety boundaries; each full pass; exact artifact identity and SHA-256; journey results; new or reopened finding IDs; independent pass evidence; and clean-pass count. A validated single-journey report is not closure evidence.
