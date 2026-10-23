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

## Mobile evidence boundary

Record the app version/build, package identity, OS version, device or emulator,
locale, text size, and whether the app starts with fresh or retained state.
Keep source tests, a responsive web preview, emulator interaction, physical-device
behavior, and store review as separate claims. A passing source test or a build
number in a config file does not prove the installed binary was exercised.

For the named journey, choose only the applicable checks:

- Exercise permission allow, deny, and return-from-settings paths without
  entering credentials or accepting an unapproved permission on the user's behalf.
- Check background/foreground and restart behavior, including whether a draft,
  unsent action, or previous user/workspace state is restored safely.
- Check the required locale and large-text layout on the actual mobile surface;
  responsive desktop emulation is useful web evidence, not a native-device pass.
- Keep store upload, submission, approval, and public release outside local
  qualification unless each external action is explicitly authorized.

If only source or browser tools are available, complete those safe checks and
mark the required mobile interactions `untested`. Explain exactly which device
check would close the gap; do not invent a runtime failure or an observed pass.
See the [source-only mobile example](../../../examples/mobile-source-only/README.md).

## Tool failure

If a tool cannot attach, authenticate, or observe the required surface:

- record the failure category without secret values;
- preserve any safe evidence already captured;
- mark only the affected claim `untested`;
- do not substitute a source-code inference for runtime confirmation;
- continue independent safe checks where they still add value.

