# Check My App

**An evidence-first Agent Skill that audits, fixes and release-qualifies web, desktop, mobile and AI-agent products — the way a real user experiences them.**

[中文说明](README.zh-CN.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · MIT licensed

Coding agents are good at writing code and bad at telling you whether the product actually works. "All tests pass" while the installer is broken, the setup wizard dead-ends, or the agent silently claims a payment went through. Check My App gives your agent (Codex, Claude Code, or any agent that reads `SKILL.md`) a strict, repeatable method for answering one question honestly:

> **Is this product ready for the person who will use it — and what exactly must change if not?**

## Core rule: no evidence, no pass

Every claim in a Check My App report is labelled:

| Status | Meaning |
|---|---|
| `confirmed` | Backed by a screenshot, interaction trace, log, authoritative read-back or deterministic test |
| `inference` | Reasoned from code or copy, not observed at runtime |
| `untested` | Could not be exercised — never silently converted into a pass |

A blocking defect cannot be averaged away by a high score elsewhere.

## Four modes, explicit authority

| Mode | What the agent may do |
|---|---|
| **Audit** (default) | Read-only inspection and interaction. No edits, no external effects. |
| **Fix & Retest** | Edit only the authorized local scope, then rerun the failing journey. |
| **Delivery Closure** | Inventory the declared boundary, fix, run full regression, repeat until a convergence gate passes. |
| **Release Gate** | Test the exact final artifact (installer, hosted build). Never silently repair it. |

An audit request is not permission to fix. A fix request is not permission to send messages, write production data, make purchases or delete anything.

## What it checks

- **Human experience** — bounded journeys from a realistic starting state: action count, time, dead ends, context switches, feedback and recovery, for a named persona.
- **Agent trust** — evidence, authority, interruption, partial completion, stale state, unknown outcomes and adversarial requests for AI-agent features.
- **Installed reality** — five gates that fixture tests miss: locale completeness, real-data shapes, window size and scaling, information hierarchy, desktop control fallback.
- **Actionable findings** — each finding carries evidence IDs, user impact, root cause, the exact change, a recommended option and an alternative, trade-offs, severity, effort and a precise retest.

## Output

1. A machine report in the `check-my-app-report@1.1.0` JSON schema, checked by a dependency-free validator (`scripts/validate_report.py`, Python 3.10+ standard library only).
2. A human summary that leads with the verdict: **Not ready**, **Pilot ready** or **Delivery ready**.

## Install

The skill is a single folder, `skill/check-my-app`.

**Codex**

```bash
git clone https://github.com/Maintstra/check-my-app.git
cp -r check-my-app/skill/check-my-app ~/.codex/skills/
```

**Claude Code**

```bash
cp -r check-my-app/skill/check-my-app ~/.claude/skills/
```

On Windows, copy the folder to `%USERPROFILE%\.codex\skills\` or `%USERPROFILE%\.claude\skills\`.

## Use

```text
Use check-my-app to audit the sign-up and first-invoice journey of this web app for a first-time bookkeeper.
```

```text
Use check-my-app in Delivery Closure mode: check and fix this desktop app until it is shippable. Do not send emails or write to production.
```

```text
Use check-my-app as a Release Gate on dist/MyApp-Setup-1.4.0.exe.
```

Validate a report yourself:

```bash
python skill/check-my-app/scripts/validate_report.py path/to/check-my-app-report.json
```

## Real-world use

Check My App was built while shipping real products — a property-maintenance app published on Google Play, a desktop bookkeeping agent, and an AI phone receptionist. It is the gate those releases pass through: it caught installers that differed from tested source, setup screens that claimed readiness they did not have, and agent flows that reported success on unknown outcomes.

## Development

```bash
python -m pytest tests
```

`tests/` covers the skill contract (required sections, references and routing) and the report validator (valid and invalid fixtures). `tests/forward/` holds small synthetic fixtures used for forward-testing the skill end to end.

## License

[MIT](LICENSE)
