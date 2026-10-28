# App Store Review Gate (iOS / iPadOS)

Load this when the release target is the Apple App Store or TestFlight external review. Rejections cost days per round, so check the following before every submission. Each row needs evidence from the exact build: screenshots or traces from an iPhone **and** an iPad running the submitted binary. A source reading only supports an `inference`.

Reviewers commonly test on the newest large iPhone and an 11-inch iPad, both signed out, with the review account supplied in App Store Connect.

## 1. Registration and purchases (Guideline 5.1.1(v)) — most common repeat rejection

| Check | Pass condition |
|---|---|
| Purchase without an account | A signed-out user can open the paywall, buy any In-App Purchase or subscription, and use what was bought, with no sign-in, registration, email or "create workspace" step before StoreKit. |
| Sign-in is optional | After purchase, sign-in may be *offered* ("Sign in to use your purchase on other devices"), with a working "Not now". |
| Restore without an account | "Restore Purchases" is visible on the paywall and works while signed out. |
| Later account linking | Signing in later carries the purchase over (e.g. RevenueCat `logIn` alias/transfer, server webhook for TRANSFER). |
| No interception | No modal, interstitial or "explain then Sign in" step between "choose plan" and the StoreKit sheet. A Cancel/Sign-in choice still counts as forced registration. |

**Lesson:** arguing that "the subscription is account-based cloud data" in Resolution Center was rejected three times. Unless the *entire* app requires an account at launch for the core service, App Review treats purchases as not account-based. Fix the flow; don't argue.

Also check:
- **Account deletion** is available inside the app (5.1.1(v)).
- Registration collects only the fields the feature needs.

## 2. Permission requests (5.1.1(iv))

- A pre-permission explainer screen may explain why the permission is needed, but its button must be neutral: "Continue" or "Next". Never "Allow camera" or "Enable".
- Request each permission only when the user starts the feature that needs it, never at launch.
- Every `NS…UsageDescription` names the concrete feature and purpose.
- When permission is denied, the app explains the impact and offers a link to Settings. It does not loop the prompt.

## 3. Third-party AI and data sharing (5.1.1(i), 5.1.2(i), 2.1 information requests)

Before any personal data, photos, text or files go to an external AI or API, show an in-app consent screen. It must:
1. state **what data** is sent;
2. **name the recipient**, e.g. "OpenRouter → OpenAI";
3. obtain explicit permission before sending.

Also:
- Declining keeps the feature usable manually, without errors or a retry loop.
- The privacy policy states the same collection, use and third parties. A privacy policy or ToS alone is **not** enough.
- Put a short "AI service: X, data sent: Y, consent shown at: Z" note in the App Review Information so the reviewer doesn't have to ask (2.1).

## 4. Subscriptions and pricing (3.1.1, 3.1.2, 3)

- The paywall shows: price and billing period, auto-renewal statement, free-trial terms if any, and links to Terms of Use (EULA) and Privacy Policy that open.
- There are no links, buttons or copy that steer users to buy outside the App Store.
- Prices in the app come from StoreKit for the user's storefront. Never hard-code prices.
- **Prices and territories in App Store Connect match everything you told App Review.** An earlier reply saying "AU/NZ only" while ASC has all regions configured is a credibility problem.
- Be ready to confirm unusually high prices (3: Business). Keep a table of product IDs, prices and territories in the review notes.

## 5. Sign in with Apple (4.8)

If any third-party or social login exists, Sign in with Apple is offered with equal prominence and supports Hide My Email.

## 6. Completeness and the review account (2.1)

- The review account works, has representative data, and is not expired or MFA-locked.
- The app has no crashes, blank screens, placeholder or "TODO" text, or dead buttons on iPhone **and** iPad. Check iPad layout even for iPhone-first apps.
- Offline and slow-network states show a message, not a spinner forever.
- Review notes give numbered steps for every gated or non-obvious feature. Put the purchase-without-account path first, and the language switch if the app has one.

## 7. Metadata (2.3)

- Screenshots for every required device size show real features of this build.
- The description has no features that are missing or "coming soon", no other-platform names (e.g. "Android"), and no prices that may differ by region.
- Support URL, privacy policy URL and marketing URL load. Contact details are current (1.5).
- App Privacy nutrition labels match actual collection, including analytics SDKs, crash reporting and AI uploads.

## 8. Other frequent blockers

- 4.2 minimum functionality: the app does more than wrap a website.
- 2.5.2: no downloading or executing code.
- 5.1.1: no private APIs and no tracking without App Tracking Transparency.
- 2.3.1: no hidden or undocumented features.

## Report

Add one finding per failed row, using guideline numbers as the finding category. Mark the submission `Not ready` while any row in sections 1–3 fails: those are repeat-rejection causes. Keep a rejection log (date, build, device, guideline, issue, fix, retest evidence) and recheck **every past rejection** on each new build, so a fixed issue doesn't regress.
