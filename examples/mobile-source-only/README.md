# Source-only mobile audit: required device journeys are untested

This is a **synthetic documentation example**, not a report about a real app,
customer, device, or release. No app was installed or exercised to create it.
It contains no customer data, credentials, screenshots, or private run evidence.

## Scenario

An agent can inspect a repository and a responsive web preview, but cannot attach
to the mobile app on a device or emulator. The declared mobile scope requires
camera-permission recovery and draft restoration after restart. Source checks and
browser rendering cannot establish either result.

[report.json](report.json) therefore uses `Audit`, records both required journeys
as `untested`, and returns **Not ready** for this declared scope. It deliberately
does not invent a product bug or fabricate a successful device interaction.
The explanatory document is not runtime evidence.

## Validate from the repository root

```sh
python skill/check-my-app/scripts/validate_report.py examples/mobile-source-only/report.json
python -m pytest tests
```

A `VALID` response confirms the report structure and consistency. It does not
certify an app, establish device coverage, or authorize external actions.

## Close the evidence gap

With an authorized test account/device and the exact candidate installed, record
version/build, package, OS, device/emulator, locale, text size, and starting state.
Exercise the requested permission allow/deny/settings-return and restart journeys;
capture redacted traces and read back persisted state. Update each claim only for
what that exact run demonstrates. A physical-device claim remains untested if only
an emulator was exercised. No store upload, submission, or public release follows
from these local checks.
