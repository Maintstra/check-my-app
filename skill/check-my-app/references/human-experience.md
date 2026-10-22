# Human experience audit

## 1. First-use clarity

From a fresh or representative state, answer within five seconds:

- What is this product for?
- What state is it in?
- What is the single next action?
- What will that action change?

Record what the persona would actually click, not what the designer intended.

## 2. Journey efficiency

Exercise the journey end to end. Record:

- user decisions and clicks;
- elapsed time and waits;
- repeated data entry;
- screen and application context switches;
- dead ends, backtracking, and external guidance;
- recovery from an injected or naturally occurring failure.

Use three decisions as a target for safe, high-frequency daily work. Count an approval or evidence review as a necessary decision when risk requires it. Do not remove a safety gate to hit the target.

## 3. Progressive disclosure

The current screen should expose the current decision. Check whether:

- one-time setup disappears or collapses after verification;
- completed steps collapse to a labelled checkmark and remain editable;
- advanced rules stay discoverable under business/settings context;
- technical IDs and logs default to a details region;
- daily work does not resemble a system configuration page.

## 4. Visual comfort

Capture representative standard and large-text views. Inspect:

- body text readability and line length;
- hierarchy between page title, task, evidence, status, and secondary detail;
- vertical rhythm and whitespace;
- excessive cards, borders, badges, columns, and equal visual weight;
- overlap, clipping, horizontal scroll, nested scroll, sticky controls, and unreachable content;
- primary and dangerous action separation;
- contrast and interactive target size.

Prefer fewer meaningful groups over many equally weighted cards. Density is acceptable when it improves expert scanning and remains readable; it is not acceptable when it hides the next action.

## 5. Language and feedback

Verify every save, connect, test, import, run, approve, and continue action exposes:

- in-progress state when delay is meaningful;
- specific success or failure;
- what was saved, read, or changed;
- whether live, demo, fixture, or cached data was used;
- the next action and recovery route.

Replace internal implementation terms with task language. Keep provider IDs and diagnostics in technical details.

## 6. Accessibility

Combine automated scanning with manual checks:

- keyboard reachability, order, focus visibility, modal containment, and escape;
- semantic names, roles, groups, headings, errors, and status announcements;
- text resize and operating-system scaling;
- contrast, color-independent meaning, and target size;
- reduced-motion and timeout behavior where relevant.

An automated zero-violation result is evidence for the rules scanned, not proof of full accessibility.

