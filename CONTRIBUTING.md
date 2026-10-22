# Contributing

Issues and pull requests are welcome — especially:

- Real audit stories where the skill missed something (with any sensitive data removed).
- New surface adapters in `references/surface-routing.md` (e.g. specific mobile or desktop tooling).
- Report-schema or validator improvements, with tests.

## Ground rules

1. Keep the skill tool-agnostic: it must work in any agent that reads `SKILL.md`.
2. Never weaken the core rules — *no evidence, no pass*; explicit authority per mode; `untested` is never a pass.
3. Every validator change needs a valid and an invalid fixture in `tests/fixtures/`.
4. Run `python -m pytest tests` before opening a pull request.
5. Do not commit real customer data, credentials, screenshots of private systems or run evidence.
