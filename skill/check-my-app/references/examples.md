# Examples

## Precise interface finding

**Weak:** “Simplify the setup page.”

**Actionable:**

- Evidence: `E12` screenshot and `T4` interaction trace show three verified connection panels expanded above the only incomplete step.
- Impact: a first-time bookkeeper must scan 18 controls before finding the required Xero account choice.
- Root cause: completed steps and the active step use the same expanded card treatment.
- Recommended change (`AddBusinessWizard/ConnectionStep`): collapse each verified provider to one row containing provider name, verified account, last-check time, green check, and `Change`; auto-expand only the first incomplete step.
- Alternative: move verified connections to a final review page.
- Trade-off: collapsing preserves edit-in-place and reduces density; a review page is cleaner but adds navigation.
- Effort: `M`; severity: `Must fix`.
- Retest: start with two verified providers and one incomplete provider at 150% text size; confirm only the incomplete step is expanded, every provider is editable, and Continue stays visible without overlap.

## Before and after copy

```text
Before: Credential saved — not tested
After:  Key saved on this computer. Not yet connected.  [Test connection]

Success: Connected to RetailExpress organisation “Example Store” at 10:42 AM. [Change]
Failure: We could not connect with the saved key. No records were changed. [Try again] [Setup help]
```

## Safe unknown-outcome state

```text
Payment submission sent
  -> authoritative read-back confirms it: Verified
  -> authoritative read-back proves no write: Closed as not written
  -> neither can be proven: Recovery required; block retry; continue read-only investigation
```

## Regression test shape

```text
Given a saved but untested connection
When the user selects Test connection
Then the control shows progress
And the result names the provider and verified account
And failure states that no external record changed
And a successful step collapses to a checked summary
```
