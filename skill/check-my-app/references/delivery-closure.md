# Delivery Closure

Use this mode when the user asks to inspect and fix the product until it is ready to deliver. It is a bounded convergence loop, not proof that the product contains no defects.

## Declare the delivery boundary

Before editing, record:

- exact source revision plus artifact identity and SHA-256;
- capabilities, target personas, roles, product surfaces, platforms, viewports, and supported configurations;
- every required journey and applicable lifecycle stage;
- safety, accessibility, privacy, data, credential, and external-effect boundaries;
- explicit exclusions, unavailable tools, and the action or time budget.

A request for Delivery Closure authorizes necessary local product changes within the declared scope. It does not authorize production writes, messages, purchases, deletes, account changes, or other external effects. Obtain separate authorization for those actions.

Build the full journey matrix before the first fix. A delivery-ready closure needs at least two distinct required journeys; a single passing journey is never full-product closure. Include happy paths, validation and failure states, recovery, permissions, interruption and stale state, accessibility basics, supported responsive states, and agent trust checks when applicable. Every coverage dimension needs at least one required item mapped only to required journeys. Mark unavailable required coverage `untested`; it cannot silently pass.

## Run the convergence loop

Apply [execution-control.md](execution-control.md) for the repair-entry checklist, interrupted runs, evidence invalidation and handoff. Keep one matrix and ledger; a new defect does not start a new audit.

1. Run every executable discovery check against a realistic starting state before ordinary repairs. If a blocker prevents downstream journeys, mark them `blocked`, apply only the minimum unblocking fix, and resume discovery. Record artifact changes; this mixed-artifact discovery is not a qualifying final pass.
2. Maintain one evidence and finding ledger across all passes. Keep stable IDs, merge repeated symptoms under their root cause, and mark findings `open`, `resolved`, or `reopened`.
3. Check coverage and the consolidated finding ledger before dispatching repairs. Fix in root-cause batches ordered by Blocking, Must fix, Improve, then Polish. Add a regression check first for deterministic defects.
4. After each batch, retest three rings: the original failing journey, adjacent journeys sharing the changed component or state, and relevant automated checks.
5. Build or deploy the exact current artifact, reset to realistic starting state, and rerun the entire required matrix. Source checks alone are insufficient when users receive an installer, package, or hosted release.
6. Run another full discovery pass over the same boundary. Vary only supported persona, viewport, state, and recovery conditions; do not silently expand the product scope.
7. A new or reopened Blocking or Must fix finding resets the clean-pass count to zero. Finish remaining executable discovery checks, consolidate findings, then repair and continue the loop. Do not immediately patch each newly discovered issue.

Do not stop merely because the originally reported failures pass.

## Convergence gate

Delivery Closure passes only when all are true:

- no Blocking or Must fix finding remains open;
- every required journey passes on the exact final artifact;
- every applicable lifecycle and safety gate passes, or a non-required limitation is explicitly accepted;
- two consecutive full passes over the declared matrix produce no new or reopened Blocking or Must fix finding, and each pass has independent run evidence;
- both clean passes name the same artifact identity and SHA-256 as the final product artifact;
- the final machine report validates and names every untested or excluded area.

Improve or Polish findings may remain only when they do not contradict a required journey or delivery claim and are disclosed with impact and follow-up criteria.

When authority, credentials, tooling, environment, or budget blocks a required check, pause that check, diagnose recoverable local problems, and continue independent authorized checks and fixes. If convergence remains blocked after that work, report `Not ready` or a conditionally justified `Pilot ready`. Preserve the ledger and exact remaining matrix so the next session continues the same run instead of starting a fresh audit. Never treat an unavailable check as passing.

## Completion language

Report the pass count and say: "No unresolved Blocking or Must fix finding was found within the declared boundary across two consecutive full passes."

Never say "all bugs are fixed." List the tested boundary, exclusions, untested areas, residual Improve/Polish findings, and exact artifact identity plus SHA-256.
