# Changelog

## 1.4.0 — 2026-10-28

- Add an App Store Review gate (`references/app-store-review.md`) built from real
  rejection rounds: purchases and restore without forced registration (5.1.1(v)),
  neutral pre-permission buttons (5.1.1(iv)), third-party AI consent naming the data and
  recipient (5.1.1(i)/5.1.2(i)), paywall disclosures and consistent territories/prices
  (3.1.2/3), Sign in with Apple (4.8), iPad completeness and review notes (2.1), metadata
  (2.3), plus a rejection log that is rechecked on every build.
- Link the gate from the release-qualification step for App Store/TestFlight targets.

No validator/schema changes or broader action permissions.

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
