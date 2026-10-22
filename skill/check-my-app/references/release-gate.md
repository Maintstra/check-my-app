# Release Gate

Test the artifact users will receive, not only source code or a development server.

## Identity

Record all available identity fields:

- product version and build configuration;
- commit or source revision;
- installer/package/hosted-release identity and SHA-256 where available;
- signing state without assuming signing is required for every distribution model;
- target operating system and architecture.

First establish the distribution model. An unsigned internal, in-person deployment can be a declared limitation when the user accepts the warning path; do not silently convert it into public-store readiness.

## Lifecycle matrix

Mark each applicable row `confirmed`, `failed`, or `untested`:

| Stage | Evidence |
|---|---|
| Install | Exact artifact installs under intended privilege and path conditions |
| First launch | No developer tools, repository files, or cached runtime required |
| Critical journey | Target persona completes the required outcome in packaged build |
| Restart/reboot | Required state persists and no duplicate process/startup behavior appears |
| Update | Supported prior version updates without loss or broken recovery |
| Failure/rollback | Interrupted or rejected update has a documented safe outcome |
| Uninstall | Binaries/integrations and user data follow declared policy |
| Clean environment | Representative clean machine/VM has the required dependencies only |

## Verdict gate

`Delivery ready` requires the exact final artifact, all required journeys, applicable lifecycle checks, no open Blocking or Must fix finding, and declared limitations. In Delivery Closure it also requires two consecutive qualifying full passes. Source tests and local build success remain valuable evidence but cannot substitute for packaged behavior.

Use `Pilot ready` only when conditions are explicit: named users/businesses, supported environment, monitoring, manual fallback, limits, and escalation owner.
