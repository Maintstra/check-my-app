# Execution control

Read for Delivery Closure, multi-finding Fix & Retest, or a resumed audit. This controls ordering and evidence reuse, not product scope or authority.

## One run record

Use the project's existing OpenSpec/tasks and one evidence ledger; do not create a second competing plan. Before expensive runs, record:

- declared required matrix and exclusions, artifact/environment/configuration identity;
- phase: discovery, minimal unblock, batch repair, focused regression, final pass, or handoff;
- coverage: checked, failed, blocked, untested, with evidence or reason;
- findings grouped by root cause (label unconfirmed causes as hypotheses), owners and allowed paths;
- checks/commands, prerequisites, expected duration and resource budget; fixture owner and cleanup verification;
- pass history, remaining work and the exact condition that allows a blocked step to resume.

Keep command output in evidence files, not repeated in conversation. Progress is required coverage and resolved findings, not test-assertion counts or invented percentages.

## Repair entry gate

Complete all executable discovery checks before ordinary repairs or repair dispatch. A finding is not a work order by itself.

If a defect prevents further checks, record the dependency, reproduce it, make only the minimum authorized unblocking change, then resume discovery. Do not bundle cosmetic or unrelated fixes into this exception. Independent checks can run before or alongside the unblock when resources and isolation permit.

Before batch repair, the owner/reviewer verifies coverage, remaining blocked checks and reasons, the consolidated finding list, root-cause batches and acceptance checks. This is an internal execution gate, not a new user-approval request. Single-fault Fix & Retest stays bounded to that fault and its impact.

After repairs, run the original failure, affected adjacent journeys and relevant automated checks. While discovering failures in a regression sweep, finish the remaining executable checks and consolidate new findings before the next repair batch. Final full passes start only after the candidate is stable.

## Evidence and rerun decision

| Change/event | Action |
|---|---|
| Report wording, metadata or ledger links only; tested artifact/configuration/matrix unchanged | Correct from evidence and rerun report validation and link/hash checks. No product rebuild or full test rerun. Missing evidence still needs the actual check. |
| Source, runtime config, migration, dependency, build input or tested artifact changed | Record impact, run focused regression; when stable identify the final artifact and execute both final full passes on it. |
| Test/harness logic changed but runtime artifact unchanged | Rerun affected checks. If the old test was invalid, invalidate its evidence and any qualifying full pass relying on it. |
| Completed check is reused during discovery or intermediate regression | Require the same relevant artifact, configuration, data preconditions and valid test implementation; record the original evidence and impact rationale. Uncertain impact means rerun. |
| A full pass is interrupted by environment/harness failure | Keep the failed log and all results; mark the pass interrupted, not clean. Recover within scope, resume discovery to collect remaining findings. After stabilization, restart that qualifying full pass; do not stitch failed attempts into a clean pass. |

Reuse builds when their inputs and artifact digest are unchanged. Freeze the actual tested artifact plus a separate manifest of relevant configuration, dependencies and test profile; a Git commit alone is insufficient in a dirty worktree. Exclude generated reports/logs from the product digest unless they are genuinely shipped product inputs. Never exclude behavior-affecting files just to keep a hash stable.

Two final full passes require independent execution evidence on the same final artifact; copying a prior pass is not evidence reuse. Report validation is a separate gate, not proof that screenshots, logs or external state are true.

## Failure handling and stopping

Classify failures using evidence: product, harness/environment, or external authority/dependency. Do not relabel an intermittent product defect as environmental merely to pass.

Preserve each failed attempt, exit code and relevant environment details. Retry after a concrete corrective action or evidence-backed transient recovery; do not loop unchanged until green. Use a resource-safe execution profile, not competing full builds/browser suites on a constrained host. Do not change timeout, skip assertions or reduce coverage just to get a pass.

Verify fixture cleanup with authoritative read-back in the intended isolated environment. Never reset a shared/user database to clear tests, bypass tool denial via another interface, or call an unavailable tool a lack of user approval.

When one step is blocked, continue independent authorized work. When only externally blocked work remains, provide one actionable handoff: completed scope/evidence, exact blocker, remaining checks and resume condition. Persist state and use the product's waiting mechanism if requested; unchanged state does not warrant repeated reminders.

## Scope and delegation

Put later paid/live/production activation in an explicit separate gate. If excluded at the outset, it does not block completion of an honestly labelled local-preparation milestone; it still prevents claims of hosted/live readiness. Do not downgrade a required test to optional after it fails.

When delegation is authorized, each work order contains phase, artifact/environment, matrix/ledger links, consolidated findings, blocked dependencies, owned paths, prohibited effects and required evidence. The reviewer checks the consolidated batch and high-risk evidence, not every file edit. Continue routine authorized local work without asking the user again. Do not create new agents or user-visible tasks solely because this reference has a delegation section.

At completion, stop the run and retire its monitoring when supported. New findings outside the agreed boundary go to a separately labelled follow-up, not an endless expansion of acceptance.
