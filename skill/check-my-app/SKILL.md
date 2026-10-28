---
name: check-my-app
description: Use when auditing, usability-testing, release-qualifying, improving, or checking and fixing a web, desktop, mobile, or agent product until it is ready to ship.
metadata:
  version: "1.4.0"
---

# Check My App

## Core principle

Test bounded user journeys as the target user experiences them. **No evidence, no pass.** Separate what is `confirmed`, what is an `inference`, and what remains `untested`. Delivery closure is convergence within a declared boundary, never a claim that no defect exists anywhere.

## Select the mode

Default to **Audit** unless the user explicitly requests another mode.

| Mode | Authority |
|---|---|
| `Audit` | Read-only inspection and interaction. Do not edit product files or cause external effects. |
| `Fix & Retest` | Modify only the explicitly authorized local scope, then rerun the failing journey. External mutations still require separate explicit authorization. |
| `Delivery Closure` | Inventory the declared delivery boundary, find and fix issues, run full regression, and repeat until the convergence gate passes. |
| `Release Gate` | Test the exact final artifact. Do not silently repair it. |

An audit request is not authorization to fix. A request to fix code is not authorization for production writes, messages, purchases, account changes, deletes, or other external effects.

Route requests in any language that mean "inspect and fix until delivery-ready," such as "check and fix until shippable," "fix everything needed for delivery," or "do not make me ask for another audit," to **Delivery Closure**. Read [references/delivery-closure.md](references/delivery-closure.md) before establishing the boundary. Do not reduce this request to `Fix & Retest` for one journey.

## Run the audit

For Delivery Closure, multi-finding repairs or resumed audits, first read [references/execution-control.md](references/execution-control.md). Complete executable discovery before batch repair; only a minimal unblock may interrupt discovery. Keep report corrections separate from product changes. A bounded single-fault fix does not require a full-product audit.

1. **Establish the boundary.** Record product type, artifact/environment, target persona, primary outcome, risk, permitted actions, prohibited effects, credentials/data boundary, and mode. Ask only when a missing answer materially changes safety or the result.
2. **Partition the work.** Name one bounded journey at a time with starting state, success state, required safety gates, and an action budget. In Delivery Closure, inventory the complete declared journey matrix before executing journeys one at a time. For a daily high-frequency journey, target three user decisions when this does not remove a necessary control.
3. **Route by surface.** Read [references/surface-routing.md](references/surface-routing.md) and load only the applicable adapter. A missing tool produces `untested`, never a substitute pass.
4. **Simulate the human.** Read [references/human-experience.md](references/human-experience.md). Start from the realistic state, interact as the persona, and record actions, time, dead ends, context switches, feedback, recovery, and rendered evidence.
5. **Test agent trust when applicable.** Read [references/agent-trust.md](references/agent-trust.md). Exercise evidence, authority, interruption, partial completion, stale state, unknown outcomes, and adversarial requests.
6. **Build an evidence ledger.** Give every material claim an ID and status. A `confirmed` claim needs a screenshot, interaction trace, log, authoritative read-back, deterministic test, or equally direct evidence. Code inspection alone usually supports an `inference` about runtime behavior.
7. **Write actionable findings.** Read [references/findings-and-report.md](references/findings-and-report.md) before the first finding, so report fields are captured once rather than reconstructed at the end. Every finding needs evidence, user impact, root cause, exact modification, recommended and alternative options, trade-offs, severity, effort, and a precise retest.
8. **Close the delivery loop when requested.** Follow [references/delivery-closure.md](references/delivery-closure.md). Keep one finding ledger across passes, rerun the full declared matrix after fixes, and stop only at its convergence gate or an explicit resource/authority boundary.
9. **Qualify the artifact when requested.** Read [references/release-gate.md](references/release-gate.md). Source tests do not prove the installer or hosted release. A blocking defect cannot be averaged away. Then run the five installed-reality gates in [references/installed-reality.md](references/installed-reality.md): locale completeness, representative real-data shapes, window size and scaling, information hierarchy, and desktop control fallback. Isolated fixture passes do not satisfy them. For an Apple App Store or external TestFlight submission, also run [references/app-store-review.md](references/app-store-review.md) on iPhone and iPad and recheck every past rejection.
10. **Validate the structured report.** Save a `check-my-app-report@1.1.0` JSON report and run:

   ```powershell
   python <check-my-app-skill-root>/scripts/validate_report.py <report.json>
   ```

   Resolve the validator path relative to this SKILL.md. Do not assume the product repository contains the Skill's `scripts` directory.

11. **Lead with the decision.** Present the verdict, blocking findings, and next actions first. Put full evidence, lower-priority detail, and technical notes after them.

## Required output contract

Produce both outputs for every completed audit:

1. **Machine report:** one complete `check-my-app-report@1.1.0` JSON document. Write it to the run-evidence directory when file output is available; otherwise include the complete JSON in a fenced block.
2. **Human summary:** verdict, tested boundary, blocking and must-fix findings, recommended implementation order, and untested areas. Link each summarized finding to its finding and evidence IDs.

Validate the JSON report before presenting the human-facing summary. If the validator cannot run, first diagnose and repair the local validation setup within scope. Continue independent product checks. If still unavailable, label report validation `untested`, report completed product checks separately, and do not call the audit or Delivery Closure complete. Do not replace the required finding fields with a prose checklist, a priority table, or one shared recommendation section. Each accepted finding must independently contain every field required by `references/findings-and-report.md`. A report-only correction does not invalidate unchanged product evidence; rerun report validation, not the product suite.

## Evidence and privacy rules

- Store run evidence outside the target repository by default, for example `<workspace>/check-my-app-runs/<product>/<timestamp>`.
- Capture the minimum necessary area. Redact secrets, tokens, cookies, personal records, account numbers, and unrelated content.
- Never reproduce sensitive values in findings, filenames, logs, or error messages.
- Record inability to test honestly. Do not infer a pass from code, copy, a disabled button, or an automated scan alone.
- Preserve the difference between demo, fixture, read-only live data, sandbox mutation, and production mutation.

## Fix & Retest rules

1. Reproduce and evidence the defect before editing.
2. Determine necessary files from the authorized goal and project evidence; do not request file-by-file approval. Preserve the external-effect boundary and ask only when the next action exceeds existing authority.
3. Add a regression test first when the behavior is deterministic.
4. Make the smallest root-cause change; do not hide truthful limitations or weaken safety to make a screen cleaner.
5. Rerun the original human journey, relevant automated checks, and the exact artifact in scope.
6. Mark the finding resolved only when its stated acceptance test passes; list remaining limitations separately.

`Fix & Retest` may stop after the authorized findings pass. It must not be reported as Delivery Closure unless the full declared matrix and convergence gate also pass.

## Verdicts

- `Not ready`: any required journey is blocked, materially misleading, unsafe, inaccessible to the target persona, or unable to recover safely.
- `Pilot ready`: critical journeys are safe and usable under explicit monitored conditions, with limitations and escalation named.
- `Delivery ready`: all required journeys and applicable lifecycle checks pass on the exact final artifact, no Blocking or Must fix finding remains, limitations are disclosed, and the Delivery Closure convergence gate has passed when that mode is active.

Read [references/examples.md](references/examples.md) when a recommendation needs before/after copy, a compact wireframe, state flow, or test example.
