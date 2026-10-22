# Surface routing

Choose tools from the observable surface, not from the repository language. Use available specialized Skills and tools rather than recreating them.

| Surface | Preferred evidence | Typical route | Required honesty |
|---|---|---|---|
| Desktop/Electron | Window screenshots, keyboard trace, process logs, persisted state, packaged binary identity | Use desktop/computer control for the installed app; if it cannot focus the window, drive the installed binary with Playwright Electron or hand off to a named human (see [installed-reality.md](installed-reality.md)); inspect source only to explain confirmed behavior | A web preview does not prove Electron packaging, native dialogs, restart, tray, permissions, or installed paths |
| Web | Browser screenshots, DOM/accessibility tree, network/console trace, task timing | Use Playwright/webapp testing or browser DevTools; run accessibility scanning plus manual keyboard/zoom checks | A DOM assertion does not prove visual comfort; a screenshot does not prove interaction |
| Mobile | Device screenshots/video, tap trace, rotation, text scaling, lifecycle, permission prompts | Use available device automation or a real device/emulator | If no device surface is available, mark mobile interaction untested; do not treat responsive desktop emulation as full mobile qualification |
| Conversational agent | Multi-turn transcript, tool-call trace, permission state, durable audit events, authoritative read-back | Use scenario harnesses, fixture tools, and adversarial prompts | Model confidence and plausible prose are not evidence of tool outcome |
| Source/code | Deterministic tests, static analysis, dependency/config inspection | Use code review, security review, focused test commands, and repository guidance | Code inspection supports implementation facts and runtime inferences, not a runtime pass |
| Release artifact | Hash/version/signature state, clean install, launch, restart, update, uninstall, critical journey | Exercise the exact installer/package/hosted version | A different build or developer machine is not equivalent evidence |

## Routing sequence

1. Inventory the surfaces necessary to complete the named journey.
2. Inspect the currently available tools and their authority.
3. Pick the smallest combination that can produce direct evidence.
4. State any unavailable surface before testing.
5. Preserve evidence identifiers across tools so one finding can link screenshot, trace, log, and read-back.

## Tool failure

If a tool cannot attach, authenticate, or observe the required surface:

- record the failure category without secret values;
- preserve any safe evidence already captured;
- mark only the affected claim `untested`;
- do not substitute a source-code inference for runtime confirmation;
- continue independent safe checks where they still add value.

