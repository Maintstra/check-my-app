# Changelog

## 1.3.1 — 2026-10-24

- Clarify mobile evidence boundaries: source, responsive web, emulator, physical
  device, and store review are separate claims.
- Add a synthetic source-only mobile example that validates against report
  schema 1.1.0 and leaves required device journeys untested with a Not ready verdict.
- Exercise the public example through the existing report validator in tests.

No validator/schema changes, new dependencies, or broader action permissions.

## 1.3.0 — 2026-10-23

First public release.

- Delivery Closure mode: inventory a declared boundary, fix, run full regression and repeat until a convergence gate passes.
- Execution control for multi-finding repairs and resumed audits.
- Installed-reality gates: locale completeness, real-data shapes, window size and scaling, information hierarchy, desktop control fallback.
- Report schema `check-my-app-report@1.1.0` with delivery-closure fields; validator still accepts 1.0.0 reports.

## 1.0.0 — 2026-08-08

- Audit, Fix & Retest and Release Gate modes.
- Human-experience and agent-trust evaluation references.
- `check-my-app-report@1.0.0` schema and dependency-free validator.
