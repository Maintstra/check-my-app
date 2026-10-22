# Installed-reality gates

Isolated fixture runs prove the build behaves on data its authors imagined. These gates catch what real users see on the installed artifact. Apply them to every `Release Gate` and `Delivery Closure`, and to any `Audit` of a desktop or localized product. A gate that cannot be run is `untested`, never `confirmed`.

## 1. Locale completeness

For every supported interface language, switch the installed app to that language and visit every screen in the declared journey matrix, including empty, loading, error, and expired-session states.

- Capture each screen and scan the rendered text for strings in another language. In a Chinese interface, a run of Latin words that is not a proper noun, product name, amount, identifier, or provider term is a defect.
- Include native and operating-system surfaces the web layer does not render: exit/confirm dialogs, file pickers' titles, notifications, tray menus, and window titles.
- A passing translation-key test does not prove the rendered screen is translated. Record the screen, string, and locale for each residue.

## 2. Representative real-data shapes

For every parser or classifier on the journey (email bodies, bank lines, invoices, imports), run at least one redacted sample whose structure came from real production data, not only authored fixtures.

- Preserve the structural traits that break parsers: missing line breaks, forwarded history, signatures, odd encodings, split payments, overpayments, merchant settlements, and transfers.
- Store the redacted sample with the run evidence. Never store raw personal or financial values.
- A journey that passes only on synthetic data is `Pilot ready` at best, with the real-data gap named as a limitation.

## 3. Window size and scaling matrix

Test the installed app at:

- the minimum window size the app allows (drag until it stops), plus 1366×768;
- operating-system scaling at 100%, 125%, and 150%;
- the primary list/detail journeys at each size, including returning from detail to list.

Simulated `deviceScaleFactor` or a browser viewport is supporting evidence only. When real OS scaling cannot be changed under the current authority, mark it `untested` and name who must run it.

## 4. Information hierarchy

For each daily, high-frequency journey, at 1366×768 with no scrolling:

- today's actionable items and the primary action must be visible;
- historical, recovery, and diagnostic content must sit below or be collapsed;
- each row must offer the decision that fits its type. A merchant settlement, a transfer, or a refund must not offer only customer-facing actions such as "email customer."

Compare against the product's design specification or approved mockup when one exists, and cite the difference.

## 5. Desktop control fallback

If the testing agent cannot focus or click the installed desktop window:

1. Try launching the installed executable through Playwright's Electron support (`_electron.launch` with the installed path) or an equivalent automation route that drives the packaged binary.
2. If no route works, hand the exact click path to a named human or coordinator, and record who performed each step.
3. Never substitute a development server, web preview, or source inspection for the installed-window evidence. Mark the affected claims `untested` until one of the routes above produces direct evidence.
