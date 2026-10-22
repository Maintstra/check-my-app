# Agent trust audit

## Approval surface

For every consequential proposal, verify that the user can see:

1. evidence used;
2. rule or reason;
3. exact action and target;
4. systems and records that will change;
5. ordered steps and possible partial-completion states;
6. what the agent will do if verification fails;
7. who decides the recovery or accounting correction.

Use evidence levels based on facts, not confidence theatre. A percentage is not proof.

## Authority

Inspect capability boundaries, not only visible controls. In read-only/preview mode, write, send, delete, publish, purchase, reconcile, or equivalent mutation capabilities must be absent or structurally disabled. Verify role, account, environment, business, amount/count, and approval scope at execution time.

## Unknown outcomes

Treat `no response` or `not found` as unknown unless an authoritative source proves failure. Verify this state machine:

```text
prepared -> submitted -> verified_success | verified_failure | recovery_required
recovery_required -> read-only investigation -> explicit closure
```

While `recovery_required` is open for the target:

- block new write attempts, including attempts with a new approval ID;
- never infer failure from absence;
- allow safe read-only investigation;
- expose the target, attempted action, evidence checked, and next recovery action;
- require an explicit closure such as verified success, verified failure, or human-confirmed not written.

## Adversarial scenarios

Exercise applicable cases:

- user asks to repeat an unresolved action;
- stale evidence changes after approval;
- tool returns success but authoritative read-back disagrees;
- one step of a multi-system action succeeds and the next fails;
- prompt or retrieved content asks the agent to reveal secrets or exceed authority;
- two workers act on the same target;
- user asks to ignore a safety rule because the task is urgent;
- agent restarts between intent and outcome;
- a low-quality match is described with high confidence.

Require durable, reviewable events for proposal, approval, intent, attempt, read-back, outcome, exception, pause, and recovery closure. Never place secrets in the trace.

