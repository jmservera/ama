---
title: Zava Forward API and web workbench
description: Staff features, configuration, local run, honest limits and container checks for the api project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-31
ms.topic: reference
---

## Complete local gate baseline repair (2026-10-31, Refs #572)

The strict case-journey browser check binds iteration-specific route callback
state without copying its pending-request lists or changing journey behavior.
The gate's exact chat-panel skip regression captures its intentional synthetic
transcripts internally, so outer unittest discovery does not mistake them for
real integration skips. Production skip detection and the existing dedicated
Chromium selector remain unchanged; no workflow or application code changes.

The unchanged chat-panel Chromium case executes locally with
`ZF_BROWSER_TESTS=1`. This is synthetic local engineering evidence, not hosted,
live-site or human acceptance, and does not establish all of #572's criteria.
Use the complete clean exact-head gate documented in the
[source guide](../README.md#local-rpi-gate) before publication.

## AI consumption report (#432)

Manager-only `GET /api/ai/report` preserves evaluation/live/registry fields and
adds `consumption`. Optional `start`, `end`, `as_of` are timezone-aware ISO
timestamps with exclusive `[start,end)` call-time bounds. Defaults are today's
UTC start through now. Invalid, empty, repeated or unknown parameters return an
explicit error. The JSON report adds no UI or deployment changes.
Timestamp, range and as-of validation also apply when the JSON store or
unavailable assistant schema prevents durable consumption reporting.
Backend meter-capacity/evidence holds return HTTP 200 with the ordinary
evaluation/live/registry sections and unavailable consumption, Unknown costs
and a safe hold reason. Invalid reporting parameters still return HTTP 400.

See the [core ledger contract](../core/README.md#ai-consumption-ledger-432) for
price/spend/billing evidence inputs, monetary limits, quality and accepted-output
semantics. Real core `Ai` calls without financial admission now stop before the
network and keep the template/manual route. No spend authority, deployment
configuration or release is created here. Existing activation, continuity,
role, human approval, resident consent and statutory controls remain unchanged.
Unknown image liability prevents AI reading but not document storage.

The report exposes Unknown prices/costs, incomplete joins, retry/failure counts,
owned alert references and tokens-per-proposal minimum/maximum/mean. Those
observations are not an owner-authorised held-out batch. The separate resident
advisor's existing SQL currency reservations remain unchanged and unjoined;
whole #432 coverage and actual Azure financial reconciliation are not claimed.
No raw case, prompt or output text is returned in `consumption`.
`unjoined_reviews` exposes interrupted legacy financial review links and keeps
money ratios Unknown until a matching authoritative disposition is recovered.
Missing legacy output links do not prevent human rejection; their original
root association keeps output/review gaps visible until linkage is repaired.
Meter-capacity-held assistant withdrawal persists as financially unresolved
and invalidates stale accepted economics, including after reads recover.
Post-call financial publication holds return persistent workflow-only
legacy/priority/chat fallbacks with unresolved attribution rather than failing
the request or calling the model again. Returned-model mismatches instead
quarantine assistant tasks without retry and suspend the released record;
bounded model evidence and financial settlement survive worker serialization.
Append-only review revisions preserve withdrawal and historical as-of state;
replaying a pending link never reapplies domain/content edits.

## Employee acceptance identity check (#570)

For Entra staff, `/api/me.user.tid` and `oid` identify the person. The assigned
app role controls access; roster binding is optional business metadata.
`account.email`, `display_email` and names are display-only, and an unbound
`user.email` is a derived `@entra.invalid` key, not the sign-in UPN.
`account.email` may be empty when email-like claims are absent or multiple.
Do not provision a roster row or change application mapping to fix an
acceptance runner's display-email comparison.

Future authorized acceptance runners should import `BINDING` from
`checks.employee_identity_check` (run from this project directory) and use
`page.evaluate(BINDING, expected)`. `expected` must contain independently
verified tenant `tid` and account object `oid` GUIDs, supplied by the
owner/identity administrator before attempting sign-in, never copied from
the observed response. Optional `email` supplies a diagnostic comparison only.
The predicate requires the expected IDs, trusted-proxy provider, Entra schema,
ProgrammeManager app/effective role and strict `view_only=false`. It returns
only booleans, including explicit transport/JSON failure flags.
`displayEmailMatches` and `rosterBound` never grant or deny admission.
Fetch failures, redirects, non-JSON/status failures and malformed expectations
fail closed. It has no sign-in entry point and consumes no attempt itself.

The recorded 2026-10-30 failure proves a failed display-email comparison,
not whether the requested account actually signed in or which display claim
was missing/different. Case was already normalized and roster binding was not
an admission gate. The offline regression demonstrates the faulty runner
expectation; it does not demonstrate an application mapping defect or
retrospectively establish the historical identity.

Next live attempt: obtain explicit owner authorization and a fresh finite
attempt budget, independently verify expected tenant/object IDs, and integrate
this predicate into a fresh guarded runner/manifest with capture-free boolean
evidence. The previous two employee slots remain consumed; do not replay their
immutable runners or reuse historical sessions. Only after strict identity
admission should the runner exercise employee chat/skill switching, map
filters and the case view. These live criteria remain unverified here.

Maintained authenticated-session integration now lives in
`checks.employee_acceptance_check.verify_employee`. For a caller-owned,
already authenticated Playwright `Page`, invoke
`verify_employee(page, {"tid": independently_verified_tid, "oid": independently_verified_oid})`.
It validates the exact boolean predicate projection, checks the authorized
origin and rechecks identity before and after each chat, map and case stage,
after hash/link navigation and before subsequent offered-control actions
(including chat draft/send). Observer callbacks take `(page, admit)` and must
invoke the supplied fresh-admission function at navigation/action boundaries.
Admission loss leaves the current and later stages blocked without executing
the next action. Probes are not an atomic guarantee against concurrent session
changes; the application still enforces authorization on every request.
Only strict `authenticated=true` admits observations; email/roster diagnostics
cannot substitute for it. Each stage returns `passed`, `failed` or `blocked`,
and the overall `passed` flag is true only when every stage passes.
Output contains fixed status and boolean fields, never response bodies,
exception text, identity values or case text. The adapter has no sign-in or
credential entry point, saves no sessions and consumes zero sign-in attempts.
The authorized caller still owns independent ID attestation, credential/debug/
capture safety, finite attempt accounting and browser lifecycle/watchdog.

Map acceptance excludes requests initiated before filter activation, matches
the selected flag/area and observes fit/viewport follow-ups until request/render
settlement. It validates points/clusters/empty payloads and compares the latest
response's actual list links/labels, marker labels/count and status. Malformed
data, map alerts, page errors and mismatched rendering fail; HTTP 200, selected
state or a cleared busy indicator alone cannot pass. Temporary listeners are
removed on success, failure and admission loss. Payloads remain in memory only.
Cluster containment permits 1e-9 degrees of absolute centroid roundoff against
the original-coordinate bounds. Point containment, finite coordinates and
geographic limits remain exact.

From `src/api`, run the changed local Chromium check with the existing test
paths (installed Chromium required; no live identity or credential access):

```bash
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
  python3 -m checks.employee_acceptance_check
```

This executes three real loopback Chromium regressions with constructed
trusted-proxy `/api/me` HTTP responses: a rosterless expected account with
no display email is admitted, and a different immutable account is denied
before any downstream callback; the third covers valid and malformed map
rendering, pre-activation stale responses and fit/viewport replacements.
The positive test also runs the actual local
chat/map/case observers against the synthetic server, with explicitly synthetic
privacy references, workflow-only chat and no external network. This does not
prove deployed behavior or operational privacy approval. On 2026-10-31 the authorized
demo health check returned 200, but independent directory resolution was
denied. No sign-in occurred; all live employee criteria remain blocked pending
independently verified expected tenant/object IDs.

Fresh non-integration discovery records the existing approved
`Chromium is installed by the later browser-check step` skip only when the
browser executable is absent; other launch failures propagate. That skip is
not executed acceptance. The maintained CLI requires exactly three successful
tests and zero skips, so missing Chromium exits nonzero. Complete-gate browser
setup and source CI invoke this CLI after installing Chromium with the test
import paths above. The discovery qualification remains unchanged; all three
reviewed integration extras must actually execute; no
missing-browser fallback or passing skipped integration is permitted.

## Compact case journey (#552)

The six workflow steps retain text labels and status words alongside the exact
icons from slide 4 of `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`.
The local `web/journey-icons/` PNGs are byte-exact extracts: survey image11,
assessment image6, funding image12, resident image13, contractor image14 and
quality image15. A regression checks those bytes against the tracked deck.
The API package data explicitly includes `web/journey-icons/*.png` so these
assets also ship in the wheel installed by the container.

Blocked steps and the case summary show a single-line reason with a native
Details button. Click, tap, Enter or Space opens the complete reasons, owners
and next actions; Escape, Close details or tapping outside dismisses them.
Long content wraps and scrolls inside a viewport-bounded, keyboard-focusable
popover. Status words and existing approval, safety and manual paths remain.
Native popovers require a current browser; the local check covers Chromium,
not full cross-browser or assistive-technology acceptance.

Tabs wrap on the same bordered surface as their panel, outside its vertical
scrolling area. Arrow keys, Home and End move tab focus; Enter or Space selects.
The selected tab stays in the URL. Sections remain mounted so tab changes
retain inputs. If enhancement is unavailable or fails, all sections are listed
without inner scrolling bounds.

From `src/api`, using the existing installed source dependencies:

```bash
PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests \
  /tmp/mv/bin/python -m unittest test_case_journey test_workspace_scripts \
  test_design_system test_accessibility_baseline test_content_standard -q
PYTHONPATH=src:../core/src:../agents/src:tests:../core/tests:../agents/tests \
  /tmp/mv/bin/python -m checks.case_view_ux_browser_check --out /new/external/case-results \
  --axe /path/to/axe-4.10.3.min.js
node --check src/zava_forward/api/web/case-workspace.js
node --check src/zava_forward/api/web/app.js
```

Normal verification requires the repository-hash-verified axe-core 4.10.3 asset
before starting the app.
The browser check starts and stops its own constructed-data loopback app,
blocks external requests and records 1280/390/320px geometry and screenshots,
keyboard/touch disclosure, enlarged text, retained fields, panel scrolling and
both enhancement-fallback paths. Attached-tab geometry and actual keyboard
panel scrolling are checked at all three widths. Axe scans the overview, open
blocker and scrolled Resident panel at each width, rejects every violation,
and retains full findings and incomplete checks in `results.json`, including
on a failed run. Incomplete axe checks still need human assessment.
`--baseline` captures geometry without requiring axe and is not acceptance
verification. The UI was already delivered by PR #554; a later verification
run is not a new before/after redesign.
These are focused local engineering checks, not publication or WCAG acceptance.

## Shared resident and employee chat widget (#550)

### Release-safe assets (Refs #568)

Employee welcome/workspace/law pages and both resident entry points render
packaged asset URLs with a deterministic SHA-256 release version. The version
includes file names and bytes, including shared chat and vendored Leaflet.
Each handler snapshots the release once: restart the process after changing
packaged files. A normal new page load selects the new release without repeated
hard refreshes. An already open page is not hot-reloaded.

HTML, API responses and access denials remain `Cache-Control: no-store`.
Static files carrying exactly one `v` query value matching the current release
use `Cache-Control: public, max-age=31536000, immutable`. All static files retain
byte-derived ETags and conditional GET/HEAD support, with the same cache policy
on 200 and 304 responses. Bare, blank, duplicate and previous-version URLs use
`Cache-Control: no-cache, must-revalidate` and return current snapshot bytes;
they are not immutable historical artifacts. HTML remains no-store even with a
matching version query. Employee dependency retries reuse the exact versioned URL from the
initial script element, including shared chat and libraries. No service worker
or browser-storage asset cache is introduced.

Both sites already used the same widget and the employee focus fix in this
source baseline. Ordinary-launcher browser regressions now also submit Enter
and mouse Send through real local employee endpoints, without resetting or
reinstalling the widget. This does not identify which assets a historical
deployment served or establish live-site acceptance.

From `src/api`, with the existing pip environment on PATH:

```bash
export PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m unittest \
  test_static_assets test_workspace_scripts test_chat_widget_focus -q
flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m checks.asset_cache_browser_check \
  --out /new/external/asset-cache-results
flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m checks.chat_submit_browser_check \
  --out /new/external/chat-submit-results
```

The cache browser check keeps the origin and browser context unchanged, proves
reuse of fresh legacy unversioned script/style cache entries, then selects a
new handler snapshot. Executed JavaScript, computed CSS, shared chat, Leaflet,
versioned recovery, fresh immutable reuse without another origin asset request,
exact cache headers and explicit ETag revalidation are observed with browser cache enabled.
It uses constructed local data, no live sign-in, model or external requests.

Browser asset instrumentation uses `checks.asset_urls.asset_url` to match the
complete canonical asset suffix independently of release queries or leading
version directories. Routes, waits, DOM script observation and CDP coverage
use that same pattern; page routes and coverage are bound to the owned origin.
Bare HTTP requests and warm-cache priming still deliberately exercise bare URLs.
The application currently emits query versions; directory-version tests prove
matcher compatibility, not an additional HTTP serving contract.

The synthetic design-system CI step runs these checks from `src/api`, with
pip-installed src projects and the existing Playwright/Chromium prerequisite:

```bash
export PYTHONPATH=tests:../core/tests:../agents/tests
flock -w 600 /tmp/ama-rpi-heavy.lock bash -c '
  set -e
  python -m checks.design_system_browser_check
  curl --fail --silent --show-error --location --retry 2 \
    --connect-timeout 10 --max-time 30 \
    https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js \
    --output "$RUNNER_TEMP/axe-4.10.3.min.js"
  python -m checks.regulatory_ux_check --axe "$RUNNER_TEMP/axe-4.10.3.min.js" \
    --out "$RUNNER_TEMP/regulatory-ux-results.json"
  python -m checks.case_journey_browser_check --axe "$RUNNER_TEMP/axe-4.10.3.min.js" \
    --out "$RUNNER_TEMP/case-journey-results"
'
flock -w 600 /tmp/ama-rpi-heavy.lock python -m unittest \
  test_browser_asset_urls test_static_assets test_workspace_scripts -q
```

Set `RUNNER_TEMP` to a fresh external output directory for local use. The same
matcher also covers workspace recovery, loading/briefing, employee workspace,
chat widget, focused case-view UX and asset-cache checks. These constructed
loopback checks do not establish hosted CI, live-site or WCAG acceptance.

### Shared interaction contract

Both applications serve the same `web/chat-widget.js` and `web/chat-widget.css`.
A bottom-right icon opens a nonmodal popup: the thread scrolls independently,
the composer stays below it, Enter sends and Shift+Enter inserts a newline.
Resident chat also offers **Chat size**, with native width/height sliders
(pointer or arrow keys, Home and End), and **Dock to right edge**. Docking fills
the right vertical edge from top to bottom; the height slider is disabled while
docked. The same button returns to the floating window. Sizes fit the viewport,
including small screens, and no resize animation runs. Size changes preserve
the first visible message and relative reading position, or keep readers at the
end if they were following replies. Escape restores the launcher; reopening
retains the existing scroll-to-end behavior. Drafts and replies remain in this
page session only. No chat text or size is saved in browser storage.
The employee input-area selector uses the general option and five bounded
skills from `/api/chat/skills`; residents use the resident assistant only.
The case panel's Open chat action opens this same popup, not another composer.
Employee input stays disabled until the existing API privacy warning loads;
drafts retain the workspace's unsaved-change and unload protection.
Attach and Voice are disabled with a visible unsupported-capability reason.
Labels distinguish AI suggestions from workflow-only/rules output, with native
collapsed Sources details. AI output is advisory and may be incorrect.

Closing and reopening retains history, draft, skill and pending reads in the
current page session/context. Moving focus into the page hides chat without
redirecting focus or cancelling pending work; the visible launcher remains
available. Setup and incoming replies never refocus the composer, even while
chat is visible. Replies, status and inline errors use polite live updates.
New messages follow the end only when the conversation was already at the
bottom and focus is outside its history; reading older messages or focusing
Sources preserves the scroll position. Loading, status and error size changes
preserve that same current bottom-follow intent, including the 200 ms loading
row; scrolling upward or focusing history during a pending reply stops following.
Employee chat sits above embedded map
panes, controls and home summaries, below the account menu. Close chat has a
readable explicit hover state on both sites. Same-context filter refreshes
retain the conversation and the launcher's open/close toggle. Background
workspace rendering leaves chat-owned focus in place, so Enter and Send keep
the dialog and answer visible during a same-context route refresh. After
Escape, Close chat or moving focus outside, a delayed same-context render also
leaves the selected connected launcher or page control focused and keeps chat
closed. Destination or authenticated-session changes, and removal of the focused
control, still move focus to the workspace. A successful
session re-check with identical authenticated user and account details also
retains pending answers; changed identity or capabilities clear the conversation.
Employee case navigation, session/access loss and resident consent withdrawal
clear the relevant conversation and invalidate late results. Reloading does
not restore a conversation; no resident text is saved in browser storage.
Resident record-use consent remains explicit before requests and is not works
consent. For consented, in-scope typed questions, an enabled advisor receives the
question and a limited own-case answer/progress, not the full case or identity.
Repair concerns, including the dead-rat example, now reach grounded generation
instead of the unrelated home summary. AI can explain how to ask for help,
not diagnose the cause, assess safety or claim a repair was reported.
Every generated route matches the complete message against recognised questions
or observations: status, documents, forms, home and household repairs. A keyword
or recognised prefix alone is not enough. Legal and consent intents take
precedence over document and other record admission and keep protected rules
replies, without calling the advisor or reserving model usage.
Combined requests, instruction-style and report/contact
actions remain deterministic refusals, including when they mention a home.
Recognised questions about how residents can report a repair or whom they should
contact may receive informational guidance. This conservative finite grammar is
not general language understanding; unrecognised descriptions or wording keep
the host-owned refusal and human-help route.
Complete polite requests such as "Can you tell me about my case?", "What is
happening with my retrofit?", "What documents do I need to upload?" and
"There is a smell of dead rat in my house" now reach their bounded generated
route when AI is configured. This is not arbitrary free-text admission:
mixed actions, unrelated suffixes and protected intents still use rules.
Safety, legal, consent, appointments, action requests and out-of-scope messages
keep their host-owned rules/human routes. No model conversation is retained.
Disabled AI and inference failures show an explicit rules fallback and human help.
Inference fallback labels distinguish exercise expiry, usage limits, request/
response limits and invalid or incomplete replies. Logs record only a fixed
reason code, never exception details, questions, case identifiers or credentials.
Unknown service/parsing errors show an unverified-reply reason. Local synthetic
checks do not determine the live site's configuration or establish model quality.

Generated typed replies use a thin "AI-generated" metadata label, with visible
"Not approved" and "AI-generated content may be incorrect" wording. Sources
remain native collapsed details, keyboard-operable. This resident-specific
label follows the [Teams AI content-label pattern](https://learn.microsoft.com/en-us/microsoftteams/platform/agents-in-teams/integrate-ai/ai-content-labels);
staff and legacy fixed-topic labels are unchanged.

Resident callback answers leave chat open and offer an explicit action to use
the manual callback form. Booking/cancellation still requires the separate
specific confirmation; chat has not alerted staff or booked works.
Missing shared employee script recovery is bounded and does not block ordinary
authorized work. Resident script failure shows a visible manual-help route.

From `src/api`, using the source distributions and existing `/tmp/mv` tools:

```bash
export PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
/tmp/mv/bin/python -m unittest test_resident_chat_api test_chat_panel test_chat_isolation -q
/tmp/mv/bin/python -m checks.chat_submit_browser_check \
  --out /new/external/chat-submit-results
/tmp/mv/bin/python -m checks.chat_widget_browser_check \
  --axe /path/to/axe-4.10.3.min.js --out /new/external/chat-widget-results
```

The shared browser check starts actual local applications with constructed data,
checks identical asset bytes, multi-turn layout, 199/200ms loading, Enter/IME/
Shift+Enter, unobscured external keyboard focus (including 320px sign-in and
short-window launcher), controlled setup/reply focus preservation, delayed
long-reply following from the pre-send bottom without repositioning after loading, errors,
reduced motion, collapsed
sources, consent, stale results and dependency recovery. Existing employee and
resident browser checks retain their session/access/manual-callback assertions.
These are engineering checks, not human screen-reader, voice-control, live-model,
live-site, full Fluent adoption or WCAG-conformance acceptance.

The focused submit check exercises real Enter and mouse Send with and without
a case, delayed replies during actual route/session refreshes, exact focus,
delayed deliberate dismissal without reopening, ordinary navigation focus,
auth snapshot changes and stale re-checks. It also checks actual resident rules
answers with both send methods. No live model or deployment is needed.

## Loading feedback and Today's briefing (#531)

The employee shell contains startup text before workspace scripts load. An
independent watchdog shows a slow-start hint and retry at four seconds, then
support guidance at fifteen seconds. It cannot display before the host returns
the HTML document. API startup failures show an explicit error and retry.
Main workspace login, ready and error paths remove startup independently, so
a failed watchdog download cannot leave the startup message over a working or
failed workspace. The law viewer reuses the same watchdog for a failed law
entry-script download; its own success and service-error paths independently
settle startup, retaining All sources/search retry without clearing prior text.
Before sign-in or account action listeners are registered, bootstrap checks the
shared async-action helper and recovers a failed download through the existing
bounded script loader. Only this helper is required before authentication;
role-specific dependencies are selected after sign-in. Exhausted retries or
a loaded script without helper readiness show an explicit error and native
"Reload workspace" action. Other workspace-script and Leaflet retry bounds
and session/route guards remain unchanged.
Recovery controls also retain their native listeners when the helper exists
but its handler is not callable, so an incomplete helper cannot prevent reload.

The shared native async-action helper wraps click, submit and change handlers.
It shows text immediately, adds a decorative spinner beside that text after 200ms,
disables the pending control, suppresses duplicate activation and announces
progress politely. Existing handler-owned disabled states and inline errors win
over cleanup. CSV, account, filters, appointment forms and the standalone law
viewer use the same helper; non-control reads and map refreshes show progress
without disabling navigation. Reduced motion keeps a static icon plus text.
The standalone law viewer checks its required helper methods before binding
actions or reading sources. If the helper is missing or incomplete, it shows
an explicit error and native "Reload law viewer" button; search is disabled
until reload restores the helper. Workspace startup requires all three helper
methods (handler, run and feedback), not just an exported object or handler.
Controls whose handlers already set `aria-disabled="true"` retain that
focus-preserving state without an additional native disable; pending duplicate
activation is still suppressed.
Editable queue search uses non-control progress: it stays enabled and focused
while overlapping reads use the existing latest-response sequence guard.
Busy cleanup restores the attribute captured before the handler runs,
including handlers that manage their own temporary busy state.
Each fresh attempt removes only that control's previous helper-owned feedback,
including after a synchronous failure. Pending duplicate attempts keep the
same promise and notice; distinct controls and non-control reads stay independent.
Failed writes are never automatically retried.
Form progress is a sibling of the busy form; briefing progress is outside its
busy content. Action-specific live text is not deferred inside those regions.

Today's briefing distinguishes "AI suggestion, not approved" from "Summary by
rules", shows the actual preparation timestamp and statement references, and
links declared case sources. Missing/unresolved references are explicit;
references and explanations are not proof of truth. The mode selector says
"Use rules and templates, without AI" and applies to subsequent briefing and
draft requests for the page session. Ordinary case work remains available.
"Use this draft" records a draft review only. "Edit this draft" reveals a large
editor and required reason; "Do not use this draft" reveals only the reason.
Cancel retains local text and returns focus to the choice that opened review,
including rejection when stale or unverified evidence disables editing.
Trailing sentence citations remain associated with their separate statements,
including line breaks before or between references. Common titles and medial
abbreviations do not fragment statements; genuine sentence and line boundaries
remain separate. Ambiguous capitalized street suffixes such as "High St." are
conservatively treated as sentence boundaries, not general language inference.
Complete sentence-ending punctuation runs (including ellipses and ?!) followed
by closing quotes or brackets retain
the same statement/reference boundaries. Terminal name suffixes such as
"Contact John Smith Jr. Repairs are due." do not borrow the next claim's
references; lowercase medial continuations and titles remain intact.
Hide/Show briefing is local reversible dismissal,
not reversal of an immutable recorded review. Server source/review checks and
all human approval, resident consent and manual boundaries remain unchanged.
Rules text and statement references use the same immutable case snapshot.
Refreshing or changing mode requires explicit discard of unsubmitted review
edits; a failed refresh retains them. Neither action can replace a pending
review or clear a committed/uncertain outcome's history-check barrier.
An initial load failure offers "Try loading briefing again". A failed refresh
or mode change retains the previous briefing and its "Refresh briefing"
control; retry uses the currently selected mode.

HAX design mapping (pattern references, not usability acceptance):

| Guideline | Applied pattern |
| --- | --- |
| [G1/G2](https://www.microsoft.com/en-us/haxtoolkit/library/) | Source-type label, explicit limits, confidence not inferred |
| G7 | Explicit assistance-mode choice and refresh action |
| [G8](https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-dismissal/) | Hide/Show briefing, no case mutation |
| [G9](https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/) | Outcome selection, conditional editor/reason, cancel before recording |
| [G11](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/) | Ranking/scope rationale, actual timestamp and declared statement references, trust caveat |
| G15 | Explicit draft feedback and immutable review result; a visible paragraph says how to correct, give feedback and refresh |

[Fluent UI React Storybook](https://storybooks.fluentui.dev/react/) and its
Spinner guidance inform native loading/button/field patterns only. No React
dependency or framework adoption is added. This bounded mapping uses the cited
guidelines and owner feedback; it is not staff user research.

The 2026-10-31 UX-specialist invocation returned discovery questions rather
than a design note. The mapping above remains maintainer-authored source/design
evidence, not a specialist contribution, approval or usability result.

From `src/api`, with installed source distributions and dev dependencies:

```bash
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python -m unittest \
  test_loading_feedback test_workspace_scripts test_ai_tasks -q
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python -m checks.loading_briefing_browser_check \
  --axe /path/to/axe-4.10.3.min.js --out /new/external/loading-results
```

Run heavy checks under `flock -w 600 /tmp/ama-rpi-heavy.lock <command>`. A
lock timeout blocks that check; do not run it concurrently without the lock.
The browser check also disables page JavaScript to verify the static startup
message at 320 and 1280 CSS px, without script requests.
This is separate from the held-script slow-start and retry scenarios and the
script-enabled axe scans.
The same runner also submits each of the three draft-review outcomes through
the real local UI and API. It compares the successful response with the
same-ID retained record read through the existing evidence export by a
separately authenticated synthetic Programme Manager. Exact reasons, edited
text and draft-only disclaimers are checked; a repeated review is refused and
the retained record and permitted case detail projections stay unchanged.
`review-roundtrip-results.json` records these outcomes separately from axe
results. This is not a complete export/continuity acceptance test.
Constructed loopback data only; no Azure or live model is needed.
Live employee-site cold-start verification, screen-reader, voice-control and
staff usability acceptance remain separate owner checks, not local passes.

The 2026-10-31 correction executed this runner on constructed loopback data:
all three successful review outcomes and retained-record checks passed.
Four axe-core 4.10.3 scans reported zero violations; the three viewport scans
each retained one incomplete colour-contrast check for human assessment.
The static no-JavaScript shell, cold-start/retry, failure recovery, pending
review barriers and reduced-motion scenarios passed. Full API discovery ran
1,430 tests with 320 opt-in/nonapplicable skips; configured Ruff lint and
format checks passed. These results do not satisfy live employee verification,
the undelivered specialist note, assistive-technology or full WCAG acceptance.


## Progress dashboard and closed case archive (#533)

**Progress dashboard** shows demonstration data only. `GET /api/progress`
accepts inclusive UTC `start` and `end` dates (`YYYY-MM-DD`), defaulting to the
30 days ending at the dataset's recorded `as_of`, with at most 366 days.
The existing staff stats permission applies; contractors and application-only
administrators cannot read it.

The read model admits explicitly synthetic cases, or cases with a nonempty,
wholly labelled synthetic simulation history. It opens no data files itself.
Unmarked records never contribute. Initial `Identified`, simulation aftercare
reopen, controlled reopen and explicit home closure events supply lifecycle
dates; current stage dates are not opening dates. Missing or contradictory
lifecycle evidence is excluded from historical measures with coverage counts.
Non-list histories, including null, are unknown rather than failed reads.
History elements must be dictionaries, and labelled synthetic actions must be
strings; malformed rows or actions make the lifecycle unknown, not silently
skipped. Unlabelled dictionary history and valid non-transition actions are
still ignored. History, closure and return collections must be lists of
dictionaries when present;
null, non-list collections or malformed entries make the lifecycle unknown.
Missing collections remain empty. Malformed synthetic cases still contribute
to coverage counts and remain in the unbounded archive with unknown dates.
Replay preserves event kinds: only identification starts the first episode,
accepted handover or closure closes an open episode, reopening requires a
prior closure, and a return requires an open case without starting an episode.
Repeated identification after closure is not reopening; reopening an already
open case is incomplete evidence. Distinct-time repeated lifecycle changes
without their intervening event are unknown. Identical event observations at
the same normalized UTC instant, and closing kinds corroborating that instant,
are deduplicated only until the next lifecycle-changing event. Distinct event
versions or other differing observation fields are not assumed duplicates.
Ordered same-instant close/reopen episodes
remain separate within an evidenced collection order, including zero-day
durations. Mixed-source same-instant repeated closing/opening evidence around
a reopen is unknown when duplicate observations cannot be distinguished from
interleaved episodes; collection concatenation does not establish that order.
Opened includes reopened episodes, also counted separately. Daily backlog is
the end-of-day known-lifecycle count; Monday-based weeks are clipped to the
selected dates. Time to close uses each observed episode ending in range,
calendar days and nearest-rank p90; no samples means Unknown, not zero.

Journey steps, team workload (recorded owner role), 60-day stalled signals and
recorded overdue tasks describe the current view, not reconstructed historical
owners or legal compliance. AI outcomes include only explicitly synthetic
`task=briefing`, `source=ai` records with nonempty case links all admitted and
`resolved_at` in range. Accepted/Changed/Rejected are draft reviews, never
approval. Rules/templates, missing review dates and unreviewed records are
disclosed separately. No synthetic usage records means unavailable usage, not
inferred activity. Every chart has a same-value semantic table alternative.

The overdue count shares the work queue's deadline-only evaluation at the
dataset snapshot. It does not construct per-case building blockers or full
work context; building membership does not affect recorded task deadlines.

**Closed cases** uses manager-only `GET /api/closed-cases` with `status` (exact
recorded stage), `team` (exact owner role), `q` (reference/resident/address,
maximum 200 characters), inclusive closure `start`/`end`, `page` (1-based) and
`limit` (default 20, maximum 100). Defaults are unbounded, independent of the
dashboard range. Only synthetic cases enter this demonstration archive.
Closure date is the latest observed closure after reopening; unknown dates
are included unbounded and excluded by either date filter, with a coverage
count. ID ordering is stable. Out-of-range pages clamp to the final page;
empty results have page 1 of 1. Hash URL queries retain filters/page through
reload and browser history, and applying filters resets pagination.
The legacy case/CSV endpoints are unchanged.

Invalid date ranges show inline errors linked to both date fields and focus the
start date so the range can be corrected. Service read failures retain a separate
page alert and retry action without marking valid dates as invalid.

Focused checks, from `src/api` with installed dev distributions:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_progress_dashboard test_workbench test_role_screens test_workspace_scripts -q
PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.progress_browser_check \
  --axe /path/to/axe-4.10.3.min.js --out /new/external/progress-results
```

Inspect actual ownership of `/tmp/ama-rpi-heavy.lock` and take nonblocking
`flock -n` admission before standalone heavy checks. If busy, record blocked
validation and continue independent lightweight work; resume after explicit
coordination, without queuing, polling or interrupting the owner. The complete
runner owns its lock: use `--lock-timeout 0`, never an outer `flock`.
The unit checks also partition a
combined-filter cohort across custom-size pages on JSON and SQLite, including
nonmatching cases, empty results and beyond-final-page clamping.
The browser check owns a fictional
loopback server and checks table/chart/API equality, keyboard, URL/paging,
first/final/empty paging controls and empty-page URL correction with filters retained,
failure/retry, cancellation, reflow and pinned axe. It never uses the working
dataset, Azure or a live model. These are engineering checks, not human
screen-reader/usability acceptance, full Fluent runtime adoption or WCAG
conformance.

Add `--scale` to the browser command to also exercise the existing seed-174,
version-1.2.0 wholly fictional 60,000-home fixture. The shared test overlay
maps those existing home IDs/attributes onto four explicit known lifecycle
templates, not random stock events: 15,000 open cases, 45,000 archived cases,
45,000 usable lifecycles and 15,000 unknown closure dates. The inherited
JSON/SQLite unit overlay clones each reader's initialized case templates so
archive summaries retain the complete store defaults; browser fixtures still
pass through normal store initialization. The unit check asserts exact flow,
duration, current workload and combined-filter page IDs at that scale.
Browser checks compare all six charts
and tables to the real API, retain all filters/page through reload and verify
first/final/empty/beyond boundaries with at most 20 rendered archive rows.
Recorded AI reviews stay separate and are not multiplied with the home cohort.
This constructed overlay is not the private geography register, original
980-case lineage, a performance SLA or a deployed employee-site check. No
fixture bytes are committed; browser/axe reports go to the external output.

## Employee chat with bounded skills (#530)

The employee header's "Ask the assistant" launcher opens one native dialog from
every employee workspace route. It reuses core `ChatPanel`, agents `ChatModel`
and the existing owned-thread API. The existing inline case and regulatory
panels remain available. Contractors and signed-out users have no launcher or
chat access.

The five advisory skills use the IDs and purposes from core
`assistants.REGISTRY`: `stock-prioritisation`, `assessment-preparation`,
`funding-evidence`, `works-resident-coordination` and `quality-evidence`.
An explicit selector chooses a skill or general work help; it is not permission
to invoke that assistant's proposal operation. No tool, approval, sending,
booking or domain-record write is available.

Design decision (2026-10-29): keep one chat agent with five explicit skills,
not a separate router or per-agent chat. One bounded `ChatModel` call per
question avoids a router's additional inference hop and token use; no measured
latency or cost improvement is claimed. Explicit selection makes the advisory
purpose auditable, removes a routing-model failure point and retains one
citation/output-validation and workflow-fallback path. A router offers inferred
selection but no demonstrated grounding or reliability benefit for these five
known choices. No departure from the owner-selected design is made.

`GET /api/chat/skills` requires current employee chat permission.
`POST /api/chat/threads/{id}/ask` accepts `content` and an optional `skill`.
Omitting `skill` preserves the old case-panel behavior. Explicit `"general"`
or one registry ID enables the new advisory mode. Null, unknown and nonstring
skills are rejected before message storage or inference; extra fields are
rejected. The thread schema and privacy admission are unchanged.

Opening from `#/case/{id}` binds the conversation to that case/home. Every
turn rereads the current employee and the same role-scoped case projection,
then applies the existing closed external-context allowlist and skill category
filter. Survey, funding and quality evidence not in that allowlist is explicitly
unavailable; selecting its skill does not fetch hidden records. Other routes,
including shared-building screens, use general workflow sources and disclose
that no individual case/home is visible. Navigation, session expiry, account
changes or denied access clear the dialog and abort stale UI results.
Denials during skill loading, thread creation or asking remove case context
and return focus to the workspace; session expiry returns to sign-in instead.

AI answers carry "AI suggestion, not approved"; the shared widget distinguishes
workflow-only replies without claiming they are AI-generated. Citations show permitted
record fields or named `workflow/` sources; cited AI output is still not
independently verified. Missing/failed models return plain workflow-only help,
not an uncited answer or a record change. Questions are masked and stored in
the owner's existing chat repository only after the existing DPIA, lawful-basis
and staff-notice references pass. Best-effort masking is not a privacy
guarantee; do not enter resident names or sensitive/contact details. The audit
ledger stores thread ID, actual question sequence, selected skill and outcome,
not duplicated free text. Existing retention and DPO decisions remain required.
Stored questions retain the 8,000-character limit after masking, including
when a replacement marker is longer than the original identifier. This is a
storage limit, not the inference allowance: questions over 1,000 characters
return workflow-only help without a model call.

The shared nonmodal popup uses native controls, normal Tab traversal, Escape and
return focus, polite updates, a delayed 200ms loading indicator and Fluent-derived
tokens. Reduced motion keeps a static loading signal. Automated browser/axe
evidence is not screen-reader, voice-control,
employee usability, full Fluent adoption or WCAG-conformance acceptance.

From `src/api`, with the worktree distributions installed:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_chat_panel test_chat_isolation test_chat_fixture_roles test_workspace_scripts -q
PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.employee_chat_browser_check \
  --axe /path/to/axe-4.10.3.min.js --out /new/external/employee-chat-results
```

The browser check uses an isolated constructed-data loopback server and
explicit synthetic privacy references, actual unavailable-model fallback,
intercepted answer-rendering cases and pinned axe on the open dialog.
It requires ask arrival before navigation in the transport test, then separately
settles controlled successful API promises after hide, navigation and session
change. Hide retains current reads without moving focus; navigation/session
disposal fences detached and replacement popup state. These are synthetic application-completion checks,
not evidence of a live provider response.
Actual SQL Server, live employee-site/model, hosted checks and human acceptance
are separate. The 2026-10-29 local run did not perform live verification.

Local evidence refresh (2026-10-30): two shared `ChatBehaviour` regressions in
`core/tests/test_chatthreads.py` cover all five skills and general help. They
check one call per cited answer, persisted masked questions, citations and
metadata-only skill/outcome audit after reopening, unchanged case records,
general help without a case, missing/timed-out model fallback and foreign-owner
denial without inference. JSON and SQLite ran four passing test cases; eight
focused HTTP contracts also passed, including role projection and privacy
admission. API/core Ruff, configured formatting and mypy passed.

`test_mssqlstore.MssqlChatThreads` inherits the same two regressions for the
existing owned SQL gate; inheritance is not an actual SQL pass. The requested
heavy-gate attempt timed out acquiring `/tmp/ama-rpi-heavy.lock` after 600 seconds
before executing any check. Complete API discovery, fresh employee browser/axe
and actual SQL Server were therefore not run in this refresh. These remain
required local evidence, alongside separate live verification. No employee-site,
provider, screen-reader or voice-control acceptance is claimed.

## Employee case journey workspace (#526)

Employee case routes show a six-step evidence-based journey, six-value summary
and nine native ARIA tabs. Tab selection lives in `?tab=` inside the hash;
manual arrow-key focus and Enter/Space activation retain panel DOM and drafts.
Open safety controls stay above all tabs. Funding and Resident agreement
completion require recorded confirmation, not position alone.

The [supplied design](../../docs/reference/research/ux/employee-case-workspace-redesign.md)
records the requirements and explicit chat-review exception. No API `journey`
or confidence score is added. Draft/proposal review is not an approval, consent
or safety decision. Chat answers stay advisory; request a separate proposal for
recorded source verification and review.

From `src/api`, with installed project dev distributions:

```bash
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m checks.design_system_browser_check
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m checks.case_journey_browser_check \
  --axe /path/to/axe-4.10.3.min.js --out /new/external/journey-results
```

The focused check owns a real loopback app with public constructed fixtures,
pinned axe, keyboard/reflow states and actual Chromium 200% tab zoom through a
test-only extension. No Azure, private dataset or live model is used.
Same-case redraws retain complete document review output and handlers.
Proposal snapshots survive overlapping loaders and remain bound to their
proposal revision. Funding and checklist drafts are bound to their AI record or
measure/checklist version; earlier edits remain copyable rather than being
applied to replacement evidence. Successful mutations clear only unchanged
dispatch-time values, not edits made while saving. Source verification does not
submit or discard edited proposal JSON.
Successful submissions reconcile exact dispatch-time values across live,
replaced, copy-recovery and cached controls, bound to the same evidence key.
Pending review and evidence-save actions exclude duplicate submissions while
later edits remain available. Malformed edited proposal JSON identifies and
focuses its editor, not a valid Reason; request failures are status feedback,
not inferred field invalidity. A recorded action whose reload fails requires
refresh/history checking rather than repeating the stale action.
Structured API errors retain their mutation outcome: `committed` and `uncertain`
take precedence over HTTP status, including 409 and 503. Quality and other case
submissions remain blocked across tab/measure changes and failed or older reads.
Only a case reload started after the outcome can recover those controls.
Proposal reviews similarly require a new authoritative proposal listing for
their ID/revision; a pre-outcome listing cannot unlock them. Retained document
draft and priority reviews require workspace reload/history checking instead of
inventing an approval. Upload preparation failures remain correctable locally;
lost upload confirmations cannot repeat the POST.
All employee JSON mutations share an in-flight lock keyed by endpoint, action
and target, independent of replaceable controls. Fieldless actions and rebuilt
resident, challenge and procurement controls cannot dispatch duplicate POSTs;
GET refreshes do not release these locks. Malformed mutation responses retain
unconfirmed-outcome handling instead of consuming drafts.
Raw resident and challenge forms also keep their pending/outcome presentation
in the case session. Rebuilt controls receive eventual history-check feedback.
Retained challenge drafts become usable again only after a causally fresh case
history reload; failed or older reads cannot silently unlock them.
Shared-queue refreshes preserve the latest unsubmitted reason and edited JSON,
including edits typed after a listing starts. Failed listings retain the current
cards. Changed or missing proposal revisions expose copy-only earlier edits,
never transplant them to different evidence. Explicit discard/navigation and
authentication boundaries clear queue recovery state.
Navigation and page-close warnings also cover unresolved cached drafts while
proposal controls are loading. A completed document review displays the submitted
replacement and retains later text or reason as read-only, unsaved recovery tied
to that record; its review actions stay disabled. Replacing an edited document or
resident draft requires explicit discard. Journey links retain challenge-history
pagination and switch mounted sections without discarding drafts.
Both chat question forms clear only unchanged dispatch-time text after a
successful answer; failures and text typed during the request remain unsaved.
The complete chat panel survives same-case refreshes, including pending buttons,
thread identity and conversation. Restored proposal editors retain copyable text
but cannot submit without current readiness and the viewer's own verification.
AI review counts announce changes politely from the visible summary without
re-announcing identical counts or the navigation button.

The assistants check can also use pinned axe and retain an external report:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m checks.assistants_browser_check \
  --axe /path/to/axe-4.10.3.min.js --out /new/external/assistants-results
```

Coordinate heavy runs through `/tmp/ama-rpi-heavy.lock`; use nonblocking
`flock -n` admission with short retries bounded to 40 minutes for this correction,
then release immediately after heavy checks. Screen-reader, staff usability and
post-deployment verification remain pending the owner.

## Expanded map and home summaries (#532)

Overview's expanded map also places its existing filters along the top (#551).
The compact buttons retain their counts and visible "Selected"/"Select filter"
words. Use Tab, Enter or Space to change the selection, or choose an area with
the labelled native selector. Map reads keep the controls available and focused;
loading, empty and failed-map feedback remains in the map information panel.
On exit, the same controls return to the Overview header with the current
selection. Completed remains a header summary, not an expanded-map filter.
At narrow widths or enlarged text the filter region scrolls without covering
the map; the map retains a minimum height, and exit/list paths remain available.
Coordinator flow retains its separate cohort filters.

From Overview or Coordinator flow, choose **Expand map** for a near-full-screen
map with a narrow left information panel. Select a home with a click, Enter or
Space to read its summary, then choose **Open home** to navigate. The summary
uses the map's permitted name, address, case ID, current stage and status;
Coordinator cards retain withheld names/addresses rather than fetching them.
Unknown or unavailable values are labelled. Status words and shapes remain
visible independently of colour.

In the embedded view the summary sits over the map, with a top-right close
icon. Click the map background, choose **Close home summary**, or press Escape
to dismiss it and return focus to the home marker. In the expanded view the
summary sits in the left panel. Escape closes the summary first; another Escape
or **Exit expanded map** returns to the embedded view and its toggle. Filtering,
failed refreshes and route changes remove obsolete cards. Map animations are
disabled, including for reduced motion.
Disposal immediately removes the map slot and makes its controls inactive,
including while the destination case list is still loading.

With the map or a home marker focused, unmodified arrow keys pan and `+`, `=`
or `-` zoom the map, including Shift-generated `+`. Ctrl, Meta and Alt shortcuts
remain available to the browser without moving or zooming the map.

The map area list and **Show these as a list** retain direct manual access
without map gestures. The expanded Coordinator list shortcut exits the map and
focuses Selected records. No resident consent, approval, safety or data-access
authority changes.

Run the focused constructed-data browser check from `src/api`:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m checks.map_fullscreen_browser_check \
  --axe /path/to/axe-4.10.3.min.js --out /new/external/map-results
```

The check requires integrity-pinned axe 4.10.3, uses a real loopback API, aborts
external application requests, and retains scan details and screenshots. It
covers summary-first keyboard/pointer behavior, Escape/focus, modal containment,
redraw/failure/filter cleanup, manual paths, coordinator omissions, reduced
motion and 320/390/1280px expanded layouts. Filter regressions cover all six
flags, exact selected home IDs through keyboard-opened marker summaries,
per-flag header/expanded selection round trips in both directions, area changes,
original control identity on exit, held/out-of-order reads,
all-request observation proving repeated selected-filter activation adds no read,
keyboard focus, 390x568 layout and 640px with a 32px default font. It also checks uncancelled browser
shortcuts from map/marker focus in both modes and exact ordinary/Shift-plus map
zoom changes. Session-expiry checks hold overlapping fit
responses, deliver a 401 before a successful response with bounds, and verify
that neither that response nor a collapse-triggered resize redraw touches the
disposed map. Each expiry scenario reloads the document to reset filters,
authentication initialization and instrumentation. A pending-facets navigation
check attempts to expand the obsolete map before All open cases renders and
verifies no dialog or page scroll lock survives. Enlarged-font coverage uses a
640px viewport and an actual 32px Chromium default font, checking sidebar/map
geometry, overflow and summary close/exit behavior. Acquire the shared heavy-check lock
nonblocking before execution. Automated results are not human
assistive-technology, staff usability or full WCAG acceptance.

## Workspace script recovery (#524)

When a required employee-workspace script is missing, the current screen retries
that file automatically after 250ms and, after a load error, another 500ms. Each
attempt waits at most five seconds. The two-attempt budget is shared across
navigation for that page; already-present scripts are not reloaded.
Timeouts and scripts that finish loading without the expected workspace function
stop recovery instead of risking duplicate script execution. A late response
cannot render an obsolete screen or restore its role/scope status after the
session ends or changes, even when the session transition does not abort the
route. Persistent failure retains the existing
plain-language error, status/alert and native **Reload workspace** button.

With the existing dev distributions and Chromium installed, from `src/api`:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest test_workspace_scripts -q
python3 -m checks.workspace_scripts_browser_check
```

The browser check owns a synthetic loopback server and intercepts script failures;
it never reads the working dataset or calls Azure. It covers actual-script
recovery after an observed failed initial request, retry exhaustion, missing
globals, delayed responses, navigation, sign-out and same-document 401/login.
Late-script checks wait for actual load/error settlement, measure real companion
evaluation without replacing its source, and compare the current route/status
before revisiting the recovered screen. These local checks do not identify the
historical live transport cause
or establish post-deployment acceptance. Authenticated live response status,
size, headers and cold-start/auth correlation, plus verification after an
owner-approved deployment, remain pending the owner.

Current-main local verification (2026-10-30, Refs #524) retained the already
merged runtime and existing test owners unchanged. API discovery passed 1370
tests with 318 existing opt-in/integration skips; the three workspace unit tests,
Ruff check/format and mypy passed. Actual Chromium confirmed failed-first-load
recovery without a document refresh, bounded exhaustion, native keyboard reload,
stale route/session protection and local Leaflet HTTP 200 with 147552 bytes,
correct MIME/length and no-store. Scoped pinned axe 4.10.3 detected no violations
in loading, recovered and exhausted states with reduced motion; the recovered
map retained 21 contrast-incomplete nodes, so this is not manual contrast or
whole-site accessibility acceptance. The historical live cause is unresolved;
post-deployment verification remains pending the owner.

## Capacity page compatibility (#523)

Legacy generated packages without a contract version remain readable, with
the version Unknown. This does not grant contract authority or confirm an
appointment. Capacity load failures name the unavailable data and offer
Try again; no failed read is treated as an empty result.
The external HTTP regression reopens persisted file, SQLite and SQL Server
stores without the seed, preserving procurement and audit history. SQL test
setup wipes only before initial creation, never on reopen; its local state
marker is not a SQLite filename. An unloaded application law store still
returns explicit unknown rule checks, not legal authority.
After a save, retry reloads data only, never repeats the saved action. Repeated
read failures keep the editable screen and unsaved appointment drafts; successful
recovery restores other unsaved forms, including their original event/context.
Successful reads recheck route cancellation and the session before rendering,
so an older failed-refresh sibling's delayed 401 cannot be overwritten by a retry.

The focused generated-demo browser check uses fictional geography rows and a
temporary store, never the default dataset. From the repository root, with the
source distributions and API dev dependencies installed:

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests python3 src/api/checks/capacity_browser_check.py
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests python3 src/api/checks/capacity_browser_check.py --mssql
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests python3 -m checks.capacity_browser_check --mssql --axe /path/to/axe-4.10.3.min.js
```

Both modes acquire `/tmp/ama-rpi-heavy.lock` nonblocking. Default is SQLite;
`--mssql` creates and removes only its own uniquely named local SQL Server
container, with fresh connection settings. Do not point inherited destructive
MSSQL suites at an existing database. The check covers seeded and empty
capacity, each failed read/retry, transport/structured errors, expired sessions,
navigation cancellation and the manager's actual navigation inventory.
It checks each destination's exact heading/content and successful browser reads,
compares rendered package/order IDs and counts to the browser responses, and
rejects unexpected API HTTP or transport failures. A separately constructed
fictional delegation fixture exercises real saved-form versus unsaved-form
recovery, repeated failed retries, navigation away and session expiry after a
save; it does not backfill authority into the legacy read-acceptance fixture.
For each failed-read endpoint, it also holds the older sibling and both retry
responses, expires the session through that sibling, then releases successful
retry reads and verifies sign-in remains after the retry continuation finishes.
It is a separate required check, not automatically run by the full RPI gate.
Local SQL Server/browser execution and post-deployment verification must be
recorded separately; source coverage alone does not establish live acceptance.
With `--axe`, the check verifies the repository-pinned axe-core 4.10.3 digest
before starting the app or SQL container. It scans the capacity workspace's
seeded, each failed-read and empty state for WCAG A/AA rules, prints violations
and checks needing human review, and fails on violations. Without the option,
scans are explicitly reported as not run. Initial failed-read retries are
activated with the keyboard. These focused engineering checks do not establish
full WCAG conformance, assistive-technology acceptance or live verification.

## Staff-recorded safety-consent intake (#130, #131)

`POST /api/cases/{id}/resident` reuses current authentication, role checks and
the transactional core ledger for these closed payloads. Extra fields,
including purported verification/approval, are refused. `case_id` must match
the URL; a wrong identity must go to the data owner, not be transferred.
All actions require current resident-workflow and recorded-reason rights,
including after a cached session's staff registration changes.

| Action | Required fields in addition to `action` |
| --- | --- |
| `nomination_record` | `case_id`, `kind` (`Officer nomination`/`Self-referral`), `reported_subject_ref`, `account`, `source`, `channel`, `owner` (staff email), `acknowledgement_ref`, `next_update` (YYYY-MM-DD), `non_digital_route`, `hazard_concern` (explicit false) |
| `nomination_correct` | `case_id`, `id`, `expected_version`, `reported_subject_ref`, `account`, `source`, `channel`, `next_update`, `challenge_id` (same-case existing challenge ID or null) |
| `tenure_intake` | `case_id`, `household_ref`, `expected_version` (0 initially, latest case tenure revision thereafter), `reported_tenure`, `reported_lease_interest`, `identity_state` (`Unknown`/`Ambiguous`), `source`, `owner`, `next_update` |

Channels: `Digital`, `Phone`, `Letter`, `In person`, `Trusted intermediary`.
Reported tenure: `Tenant`, `Shared owner`, `Right to buy leaseholder`,
`Preserved right to buy leaseholder`, `Leaseholder`, `Mixed block`, `Unknown`.
Missing lease-interest information must be supplied as `Unknown`, not guessed.
Both identity and tenure verification remain unknown regardless of reported
values. Original text is preserved, bounded and never silently truncated.

The response contains projected case detail. Restricted roles receive no raw
intake histories. Stale versions return the existing conflict response.
A committed write whose acknowledgement fails returns the existing explicit
409 `outcome: committed`; reload/reconcile history before another action.
No automatic sending, booking, approval, ranking or lease interpretation.
Hazard concerns return a refusal directing staff immediately to the existing
`/api/cases/{id}/hazard-raise` route; this is not automatic hazard referral.
Use emergency/manual service routes independently without waiting for intake.

See the [core boundary](../core/README.md#unverified-nomination-and-tenure-intake-130-131)
for the case-wide unresolved hold, deletion interaction, missing whole-programme
coverage and actual human approvals still required. There is no new web
interface or operational activation; digital capture is staff API capture,
not evidence of keyboard, screen-reader or representative participation.

```bash
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p test_resident_api.py -q
```

## Working form review and held Finance decisions (#96, #98, #99)

`GET /api/cases/{case_id}/form-review` returns authorized working diagnostics,
review history, recorded diagnostic manifests and unresolved decision holds.
An unavailable retained source does not fail the whole GET: its draft entry
contains only `draft_id`, `status: "Unavailable"` and a fixed recovery `notice`.
Affected values, history, attachments and recorded diagnostics stay hidden;
unrelated available drafts remain readable in the same 200 response.
`POST` accepts only `open`, `review` and `diagnose`; all other actions and extra
keys are refused. Existing authentication and Finance/resident/reason-view
checks apply on the server. No UI, model call, approval, submission or
reviewed-export path is added.

```json
{"action":"open","schema_id":"SYN-TECH","schema_version":1}
```

The example schema ID is synthetic and must already be registered. The response
includes `draft_id` and `input_version`. Individual review uses the exact keys:

```json
{
  "action": "review",
  "draft_id": "<returned draft_id>",
  "expected_version": 1,
  "field_id": "epc",
  "decision": "accept",
  "batch_id": "<same-case staged batch ID>",
  "candidate_id": "<staged candidate ID for epc>",
  "value": null,
  "reason": "Synthetic example: checked the bound source"
}
```

`correct` supplies an explicit scalar value while retaining source lineage;
`reject` requires null batch/candidate/value and preserves prior history.
`diagnose` takes only action, draft_id and expected_version. Writes increment
the draft version; stale writes return 409. Invalid input returns 400, denied
or unavailable scanned evidence on POST 403, missing case/draft 404, unavailable blob
storage 502 and storage failure 503. On storage errors, reload before retrying.
Pending/missing scans use the separate document recovery path, never a hidden
review-time scan.

Every manifest is Held with `reviewed_ready: false`. Approved-rule validation,
unit/currency verification and Board breach assessment are Not evaluated.
Three durable decision-needed entries carry no invented approval or figures;
the acceleration pause is diagnostic only, not a programme-wide hold.
See the [core boundary](../core/README.md#unapproved-working-field-review-96-98-99)
for typed conditions, source/schema freshness, JSON/SQL writer guarantees and
the still-blocked Finance/Board decisions. Raw values/history/holds are omitted
from ordinary case detail; the dedicated endpoint refuses affected historical
evidence after quarantine through the opaque per-draft GET result above.

After pip editable installation, from `src/api`:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest test_form_staging_api -q
```

This is a synthetic local engineering slice, not approved-template binding,
full reviewed application/claim export, live financial authority, a Board
envelope or complete issue acceptance.

## Specialist screen delivery (#149)

The existing workbench includes a **Specialist screens** destination. Installed
role-specific modules appear only for the signed-in existing role; this is not a
role simulator or new authorization. The shared parent alone has no installed
modules. Child PRs add independent read-only evidence views before owner review
and integration. Select a home explicitly; selection and queue page are in the
URL. Reset changes only the view. Existing case workspaces remain available.
The queue retains the projected "Safety issue open" marker and recorded task
context, including hazard awareness, response and resident-update due times,
named follow-up owners and the external service's timing authority (SA-007).
Missing times stay Unknown. Contractor responses intentionally omit staff task
context; the shared queue does not invent it or request broader access.
The manager's closed-case archive also retains its projected safety marker:
retrofit completion does not mean that a later safety concern is resolved.
Archive summaries do not supply staff task clocks; no clock is invented there.

Views reuse server-projected case reads, native controls and Fluent-derived
tokens. Missing or withheld evidence is not readiness. They never send resident
contact, change a record or approve work. Direct user, screen-reader and WCAG
acceptance, distinct professional identities and integrated-feature validation
remain separate from local engineering checks.

From `src/api`, with project dev distributions installed:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_workbench test_role_screens -q
PYTHONDONTWRITEBYTECODE=1 python -m checks.role_screens_browser_check
```

An installed child's check adds its story number, for example
`python -m checks.role_screens_browser_check 232`. Checks own a synthetic
loopback server and do not read the normal working dataset or call Azure.
The parent's scoped receipt covers its exact foundation head, not unmerged
child implementations or subsequent integration.
Its browser check also installs a test-only queue to exercise actual staff
safety projections and contractor responses without task context; this does
not install a production role screen.

## Resident chat and synthetic callback agenda (#520, building on #469)

The resident showcase has one bottom-right Chat launcher on its sign-in,
progress and error states. It opens a nonmodal window: Escape or Close chat
returns focus; moving keyboard focus outside closes it without trapping focus.
The existing Fluent-derived tokens and native controls are retained. The chat
keeps at most 10 answers in page memory, not browser storage or model memory,
and clears record-use permission and replies on sign-out/session loss.

All personal assistant requests now require the exact boolean
`"use_record": true`, including the existing topic requests. This intentionally
tightens #469's request schema. No record lookup or model call occurs without
that permission. Sign-in is not consent to assistant use or works.
`POST /demo/assistant` accepts exactly either `{"topic":"status","use_record":true}`
or `{"question":"Where is my case?","use_record":true}`. Supported topics:
status, documents, forms, home, consents, appointments, regulations and safety.
Typed questions are bounded to 500 characters and routed by host-owned rules.
Eligible non-document questions can enter the bounded generated-answer prompt;
document questions use fixed-topic guidance selection instead. Neither is kept
in durable conversation memory. Unsupported
questions abstain. No client case/home/email selector is accepted.

Rules mode recognizes bounded natural own-record questions, including "How's my
case going?", "Is my case blocked?", "What is blocking my case?", "Where is my
retrofit up to?", "What paperwork have you got?", "Do you have my documents?",
"What forms am I missing?" and "What address do you have for me?". These reuse
the existing recorded answers; they do not infer why a case is waiting beyond
the available record. Legacy question matches remain supported. The fallback
uses an ordered keyword/intent grammar that consumes one complete question
after existing safety, exclusion and specialist checks, not keyword presence
alone. Unknown wording, mixed requests and appended instructions still refuse.
Unsupported replies give four example questions and a housing-officer help path.
This finite routing is not universal language understanding or approved
resident-facing copy. No AI activation or deployment changes are made.

Document questions retain the mandatory own-case facts and source references
under the bounded Azure guidance selector below. Unlike other eligible typed
questions, document replies do not use free-form generated prose. Status/forms
retain their existing Azure route; other protected answers are labelled
workflow-only rules. Home answers use only the signed-in projection.
Operational appointment history and works-consent records are not projected:
answers state Unknown, never infer consent. Safety questions give direct
human/emergency routes and explicitly state that no report was sent.
Bounded reports of active CO/carbon monoxide alarms, smoke, electrical sparks or
shocks, and flooding or leaks involving electrics take this route before ordinary
topics, even when the question also mentions home or appointments. Routine
detector documents/status, socket improvements and unrelated water questions
retain their ordinary routes. This finite rule set is not a safety assessment
or a guarantee that every possible hazard report is recognized.

Document answers use only the authorized case's resident-facing requests and
document metadata. The case JSON contract adds `resident_document_requests`,
an array of `{id, kind, how_to_provide}`; absent/null is unknown, while `[]`
means no requests recorded. Canonical `documents` contribute only `id`, `kind`,
`generated`, `scan.status` and `resident_issues`, an explicitly resident-facing
array of `{severity: "warning"|"error", message}`. Staff notes, names, filenames,
scanner detail, hashes and document bytes are not projected. Do not copy private
staff issue text into resident-facing fields without the appropriate review.

The answer matches requested kinds to nongenerated presented documents, explains
every recorded resident issue and pending/infected/mismatch scan code, and cites
the request/document references. Receipt or a clean scan never means acceptance
or compliance. Missing data stays unknown; malformed/oversized metadata fails
explicitly rather than becoming an empty checklist. Limits: 20 requests, 40
documents, 10 issues per document, 64-character IDs, 80-character kinds/statuses
and 500-character instructions/messages. Instructions are quoted own-case data;
the housing officer confirms requirements and a secure route. Chat cannot
upload/send files. The same mandatory facts/citations remain under AI selection,
AI-off and unavailable fallback. Larger valid answers may use rules because the
existing AI payload cap is unchanged.

`infra/sql/resident-showcase.sql` adds the `documents_json` view column. A
separately authorized view application is required before deployment with this
reader; no cloud application or live data migration is implied by these sources.
Historical infected/mismatch fixtures do not imply normal upload persistence:
normal uploads reject them and rescans normally remove them.

The regulations answer cites the local Safety and Quality Standard, sections
2.3.1..2.3.3, source date 2024-04-01 and retrieval 2026-09-19. Those provisions
were compared with the [official publication](https://www.gov.uk/government/publications/safety-and-quality-standard)
on 2026-10-28. This is a bounded explanation, not a complete/current legal
corpus, legal advice, applicability decision, compliance decision or activation
of an operational rule. Other rules/currentness need qualified review.

### Local synthetic callbacks

The showcase's SQL identity/home view remains read-only. An optional, separate
local SQLite agenda demonstrates real inventory search and atomic reservations
for **synthetic callbacks only**. Nobody will call; these are not operational
officer appointments, works commitments, staff/capacity confirmations or works
consent. No operational calendar connector or new staff HTTP authority exists.
The unconfigured agenda fails explicitly with a manual contact route, rather
than returning fake free times.

An operator explicitly creates a task-owned local inventory; it is never
seeded automatically on HTTP startup. Use a fresh absolute path outside git
and a suitable exercise date:

```bash
python -m zava_forward.api.resident_demo.agenda /tmp/my-synthetic-callbacks.sqlite \
  --seed-from 2026-10-28
# Add this setting to an otherwise correctly configured local synthetic showcase:
export ZF_DEMO_AGENDA_PATH=/tmp/my-synthetic-callbacks.sqlite
python -m zava_forward.api.resident_demo
```

The seed creates seven days of weekday 30-minute slots at 09:00, 11:00 and
14:00 UK time. Stored instants are UTC; filters and displayed dates use
Europe/London, independent of browser timezone. Searches order by start then
slot ID, return the first 0..3 free future matches, and accept an earliest date
today through 90 days ahead plus any/morning/afternoon. These preferences do
not establish access needs, professional suitability or staff availability.
Ask a person about adjustments.

Asking chat about appointments automatically runs this search using the
server's UK date (and morning/afternoon when requested), then shows the shared
manual form. The explicit chat record-use permission covers that requested
search, not booking. The independent manual form works without chat/AI.
Proposals are own-case-bound and expire in 10 minutes; they do not hold slots.
The resident must check a separate confirmation for one specific time and
select Book this callback. Availability/future time and admission are checked
again. After authorization, proposal expiry and slot start are rechecked against
one fresh instant before committing; either deadline rolls back a new booking.
Transactions prevent double booking; retries reconcile the same booking.
One active callback per case is permitted until cancelled.

`POST /demo/agenda` requires session, same-origin/CSRF and `use_record:true`.
Protected view, chat, callback and sign-out requests also require exactly one
`X-Resident-Session` header containing the opaque `session_id` returned by
`GET /demo/session` or a successful login. This is a per-login binding, not a
resident selector or authentication credential; the signed HttpOnly cookie is
still required. A missing, malformed or replaced binding returns 409 with
`session_changed:true` before personal reads or callback changes. Invalid or
expired authentication returns 401. Record-use permission must be renewed after
every login, even to the same resident.

Sign-out revokes only the bound server token and deliberately sends no
`Set-Cookie` headers. The revoked HttpOnly cookie remains unusable until its
original expiry or replacement by another login. This prevents a delayed
sign-out response from deleting a newer login's authentication or CSRF cookies.
The page rechecks the actual current session before confirming sign-out.

Open tabs recheck change notifications against the current server session and
clear stale records, transcripts and permissions without adopting another tab's
identity. Server-side binding also rejects stale tabs before a notification is
delivered. Delayed responses cannot restore a previous session. Typed-ahead
questions survive earlier answers; dismissed chat does not move focus or start
a delayed callback search. The manual route remains available, including visible
retry focus on page errors and launcher focus while loading. Punctuated morning
and afternoon questions use the same word tokens as topic routing.
Exact additional fields:

| Action | Fields |
| --- | --- |
| list | `action:"list"` |
| find | `action:"find"`, `earliest:"YYYY-MM-DD"`, `period:"any"` (or morning/afternoon) |
| book | `action:"book"`, `proposal:"returned-token"`, `confirmed:true` |
| cancel | `action:"cancel"`, `reference:"own-booking-reference"`, `confirmed:true` |

Neither a typed "book" request nor AI can confirm a booking. An active callback
can be cancelled through the resident form with separate confirmation. A local
operator who already has file access can assist after verifying the synthetic
resident's cancellation request and callback reference:

```bash
python -m zava_forward.api.resident_demo.agenda /tmp/my-synthetic-callbacks.sqlite \
  --cancel RETURNED_REFERENCE --verified-synthetic-request
```

This is an operator procedure, not real identity verification or a public
unauthenticated cancellation endpoint. Residents can instead phone their
housing officer using their usual number, write or visit; the demo invents no
contact number, response time or report receipt. If a mutation response is
uncertain, check callbacks before retrying. Record-use withdrawal does not
silently cancel a reservation already made.

Focused local units and actual loopback Chromium/axe (pinned 4.10.3, existing
digest checked by the harness):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests \
  python -m unittest test_resident_chat_agenda test_resident_chat_api test_resident_assistant_api -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests \
  python -m checks.resident_assistant_browser_check \
  --axe /absolute/path/to/axe-4.10.3.min.js --out /tmp/my-resident-chat-evidence
```

Hold `/tmp/ama-rpi-heavy.lock` nonblocking for heavy runs. These checks use
constructed rows, a disposable local agenda and no real SQL, credentials,
private datasets or model transport. The browser check covers mouse/touch/
keyboard, consent, two pre-opened sign-in tabs in a shared browser context,
per-login permission resets, late notifications and obsolete session/view replies,
punctuated time filtering, typed-ahead drafts, error/loading manual-route focus,
dismissed delayed appointment replies, actual search/confirm/cancel,
320/390/1280px, reduced motion, 200% root text resizing and 320px
400%-equivalent reflow from 1280px. The latter is not native browser zoom.
Human resident/content, screen-reader/assistive-technology, real-model #164 and
live-service acceptance remain pending. Automated checks are not WCAG
conformance or whole-issue acceptance.

The standalone assistant check uses complete supported questions, such as
"Which documents are missing from my case?", "Which documents do I still need
to provide?", "How do I upload my documents?", "How do I fill in my form?" and
"What does my document warning or error mean?". Document wording also accepts
provide/send/upload questions and singular or plural warning/error meanings.
This asks how to provide a file; it does not upload one. "documents help",
"forms help", upload commands, approval requests and questions combined with
unrelated requests still receive a task-limit refusal. This finite grammar
is not general language understanding. The check asserts each newly
added reply, not earlier chat history, retaining missing-document facts,
warnings, sources, truthful rules labels, own-case isolation and the limits on
sending or making decisions. API tests cover both supported questions and
those refused inputs without enabling AI or changing resident authority.
The stale-prompt correction was delivered in #573 (Refs #571). The browser
check also sends "documents help" and "forms help" after successful document
answers: each fresh reply must refuse explicitly, retain rules metadata and
human help, and contain no Survey fact, document IDs or AI-suggestion label
borrowed from earlier replies. Positive document assertions remain unchanged.

### Preserved bounded Azure advisor (#469)

The resident showcase retains three fixed model-assisted questions through
`POST /demo/assistant` with topic status, documents or forms and the explicit
record-use boolean above. The endpoint requires the existing session, same-origin and CSRF
checks and fetches/re-authorizes the resident's own case for every request.
It never accepts a case selector, writes a case, submits a form or records consent.
Document replies use the current own-case request facts when available.
Missing or unrecognised facts stay explicitly unknown, not "nothing to send".
Document requests may be unknown in the projection; the answer says so rather
than invent a checklist.

The [design note](../../docs/architecture/resident-assistant-prototype.md)
records the 2026-10-27 owner decision: managed identity and USD20 model ceiling.
Default `FakeProvider` is deterministic local rules: no model connection or cost.
The legacy `AzureTopicProvider` remains available for compatibility.
The startup-wired `AzureAdvisor` calls regional Standard `gpt-4.1-mini`
2025-04-14. Explicit `topic` requests retain approved explanatory-sentence
selection. Document `question` requests use that same selector so missing-file,
provision and warning/error facts, references and no-approval wording cannot be
replaced by model text. Other in-scope `question` requests ask for short generated prose using
only host-supplied own-case grounding and repair-reporting guidance. Strict
output validation requires bounded nonempty text and known, unique source IDs;
source descriptions come from the host, never model-provided URLs. Text renders
as text, not HTML. These structural checks cannot prove semantic correctness;
actual-model evaluation and human content acceptance remain outstanding.
Host-owned advisory/human-help limits stay visible. A fresh authorization
check after inference/fallback prevents stale replies after revocation/expiry.

Enable only after the [SQL/infra prerequisites](../../infra/README.md#resident-azure-openai-469):
`ZF_DEMO_ASSISTANT_ENABLED=true`,
`ZF_DEMO_ASSISTANT_ENDPOINT=https://aoai-resident-469.openai.azure.com`,
`ZF_SQL_AUTH=msi` and the existing `ZF_SQL_CLIENT_ID`. No other assistant
settings or credentials are accepted. Default is off. Calls use only
`ManagedIdentityCredential`, never a developer credential chain or keys.
Accounting reserves one cent permanently, before credentials or HTTP, up to
2000 cents lifetime; five attempts per resident per rolling hour. SQL failure,
rate/cap denial and model failure return labelled deterministic advice, not
unlabelled AI success. Token usage logs contain counts only. There are no
automatic retries/refunds. The complete request is <=4096 bytes with <=256
output tokens. Reviewed inference tariff expires 2026-11-01T00:00:00Z; the
December funding horizon does not extend resident access.

#### Issue #466 acceptance evidence reconciliation (2026-10-31)

The gauges/history and advisory assistant already exist in the source baseline.
This reconciliation adds no new runtime, model activation or resident authority.
The owner request on 2026-10-31 confirms gauges/history and an advisory assistant
with AI in scope, with IoT a standing priority and resident AI staying off in
deployment behind the existing activation settings. The issue checkboxes are
not changed by this guide; the older USD5 proposal is superseded by the recorded
2026-10-27 decision below, not a fresh spending authorization.

| Issue criterion | Source evidence and boundary |
| --- | --- |
| Owner confirms scope and priority | Confirmed by the explicit 2026-10-31 owner direction: sensor gauges/history and advisory AI, IoT a standing priority, existing synthetic data and deployment AI off. This does not establish live or human acceptance. |
| Own-home gauges and history labelled synthetic | Implemented: temperature/humidity meters, static histories and equivalent table use only the signed-session home's generated readings. `test_resident_sensors.py` and `checks.resident_sensors_browser_check` cover isolation, missing/fault/empty states and text alternatives. CO2 was an issue example, not an available generated channel. |
| Grounded case status, required documents and form help with advisory notice | Implemented: own-case status and document facts, honest unknowns and general form guidance; `test_resident_assistant_api.py`, `test_resident_chat_api.py` and `checks.resident_assistant_browser_check` cover these paths. The assistant does not submit, consent or decide. |
| No other resident's data | Tested by separate synthetic sessions, forged selectors, revocation and shared-browser session changes in the resident API and browser checks. These are local engineering checks, not live identity acceptance. |
| Accessible gauges, charts and chat, with text alternatives | Existing native meters, static named SVGs, equivalent table, labelled chat controls, keyboard focus, non-colour statuses and reduced motion have automated engineering checks. Screen-reader, real-resident and full WCAG acceptance remain separate; passing axe alone does not establish conformance. |
| Model, cost cap and credential route decided and recorded | The [2026-10-27 decision](../../docs/architecture/resident-assistant-prototype.md#current-owner-decision-and-implementation-2026-10-27), delivered in merged #480, records regional Standard `gpt-4.1-mini` 2025-04-14, a permanent USD20 inference ceiling inside the resident USD30 allocation and managed identity only. Retain that existing decision; no replacement model, cap or credential route is needed. Issue-state reconciliation remains separate from this recorded decision, new spending authority or live activation. |

Default-off AI, SQL accounting prerequisites and the 2026-11-01T00:00:00Z tariff
expiry remain unchanged. No deployment, current budget headroom, authenticated
live model call or renewed cost/authority window is established by local tests.
The [current scope and AI contract](../../docs/architecture/resident-assistant-prototype.md#current-scope-and-ai-contract-2026-10-31)
distinguishes eligible generated answers from protected document guidance and
the historical fixed-topic design. Actual-model relevance, manual accessibility
and live acceptance remain separate from local scripted checks. Refs #466 only.

#### Owner deployment prerequisite for resident generated answers (#563)

The source defect was twofold: host routing sent repair questions directly to
rules, and even an enabled advisor only selected prewritten sentence IDs.
Changing an enablement setting alone did not address either defect.
`infra/resident-demo.bicep` does not supply the assistant enablement/endpoint
settings. Live settings were not inspected, so this is not a diagnosis of the
current Azure configuration. No Azure deployment or setting change was made.
For a separately authorized deployment of the fixed image, the owner must
explicitly supply the four settings above, verify existing SQL reservation
procedures/permissions and managed-identity model access, and review the
remaining rate/budget balance. Keep default-off behavior until those gates.
After 2026-11-01T00:00:00Z the existing tariff expiry deliberately returns
rules; review/renew the cost/authority envelope separately, not by bypassing it.
Authenticated live Playwright and actual-model relevance are still required
for issue acceptance; local scripted transport is not that evidence.

For authorized live checks, finish the rollout and warm `/healthz` before
signing in with a fresh browser session. Resident session and CSRF tokens are
process-bound: a restart or new revision invalidates them even when the signing
secret is unchanged. Do not reuse a pre-rollout login or wait only for signed-in
content after a reload; detect sign-in and error states explicitly. After a
successful login response, wait for the asynchronous own-case view to render
or an explicit error, not the still-visible pre-login form. Allow several
minutes for scale-to-zero startup, use bounded long health/navigation timeouts
and retries, and do not retry an uncertain login or model request blindly.

From `src/api`, with installed source distributions and dev tools:

```bash
PYTHONPATH=../core/src:../agents/src:../core/tests:../agents/tests \
  python -m unittest discover -s tests -p 'test_resident*.py' -q
ruff check . && ruff format --check . && mypy
PYTHONPATH=tests:../core/src:../agents/src:../core/tests:../agents/tests \
  python -m checks.resident_generated_answer_browser_check --out /new/external/resident-ai
```

The focused generated-answer check starts the actual loopback application with
constructed residents and a scripted Azure transport. It checks consent before
request/reservation, own-case prompt exclusion, generated-text rendering,
thin-label geometry, collapsed keyboard sources, 1280/390/320px reflow at
100%/200% text, unavailable/disabled fallback and withdrawal. No paid inference,
private data or credential lookup occurs. Full AT/WCAG and live acceptance are
not established.

Focused units: `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest
test_resident_aoai test_resident_assistant_api test_resident_assistant_provider`.
`test_resident_aoai_sql.AccountingSqlTests` exercises actual procedures only
on the opt-in task-owned loopback SQL Server and is included in local/hosted
SQL selectors. Never point those tests at Azure SQL or an existing dataset.

Focused local browser check, using only existing constructed fixtures and no SQL:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.resident_assistant_browser_check
```

Full unit discovery remains the normal API command. Browser evidence does not
establish screen-reader, user or live-service acceptance.

The focused check covers Account disclosure before sign-out and composer focus
after success or failure, including duplicate suppression and delayed logout
isolation. Busy advice disables the native submit button and keeps focus in the
textarea, with duplicate suppression. Optional reservation I/O failures return the generic assistant
503 without acquiring a token or calling the model transport in the legacy
adapter; the new advisor returns explicit rules fallback instead.

## Opt-in IoT consumer and synthetic publisher (#110, #184)

For the bounded hub-only exercise, `DeviceActivation(hub_hostname,
approval_reference, resource_group="ama")` authorizes only the explicitly
called X.509 publisher. It requires a valid Hub hostname and nonempty approval,
but does not pretend a custom Event Hub or routed consumer is ready.
`HubReceiver` rejects this activation before credential construction;
its existing `Activation`/managed-identity/routing requirements below remain.
Approval objects are caller declarations, not verification of deployed access.
The [2026-10-29 hub reconciliation and blockers](../../infra/README.md#bounded-existing-hub-exercise-2026-10-29-refs-140-184-137)
record the actual existing B1 resource, registry-permission blocker and unchanged
service-key prohibition. Local actual SQL tests do not establish live transport.

Before the single approved run, the named owner must complete and record the
[quota, cost and alert preflight](../../docs/reference/research/iot-sensor-analytics-research-plan.md#cost-and-scale-before-any-live-run).
Verify the exact reused hub's current B1 quota usage for the applicable UTC
day immediately before running; record that consumed 4-KiB-unit count as
`verified_daily_used_units`. Do not assume an unused hub or use the zero
default. Account conservatively for other traffic and attempted or uncertain
deliveries not yet reflected in the reported usage, including traffic expected
during the run. The verified usage plus the planned run's units (each body plus
the 1-KiB properties reserve, rounded up to 4-KiB units) and any such additional
traffic must leave at least 40,000 unused units from the 400,000-unit daily
allowance. Recheck if the quota day or usage changes before sending; stop if
usage or concurrent traffic cannot be reliably bounded.

Also verify actual subscription currency and remaining aggregate cost headroom,
including accrued charges and remaining commitments, within the approved
USD5 additional allowance through 31 October 2026 and the overall budget.
The historical USD60/month routed model is not additional spending authority.
Verify that the budget alert is active (enabled, with the correct budget scope,
threshold and notification recipient). Record the fresh evidence in the owner,
cost and alert references; missing, stale or insufficient quota/cost/alert
evidence blocks the run. References alone do not prove these checks.
`RunBudget` does not query live quota, verify alerts or enforce aggregate
spending, and budget alerts are not hard spending stops.

For this bounded exercise, explicitly set `RunBudget(...,
daily_used_units=verified_daily_used_units, max_messages=2,
max_per_second=1.0, max_seconds=60.0)` with those verified owner, cost and alert
references: at most two messages total, one per second globally and 60 seconds
for ONE `HubPublisher.run()` call for the entire approved bounded exercise.
Do not make repeated or concurrent calls, including from another publisher
instance or process. Each call creates a fresh pacer by default; `RunBudget`
does not cumulatively account for sends or enforce the rate across calls.
No further run or retry is approved without separate owner approval after
reconciling all attempted and uncertain deliveries, daily quota usage and
the remaining budget/window. The default 100 messages and larger supported
limits are not approved for this exercise. Before the single run, the operator
must check the UTC date/time and ensure the run fits within the remaining
approved window through
31 October 2026 UTC: stop before `2026-11-01T00:00:00Z`, and do not start if
there is insufficient time to finish within that cutoff. `RunBudget` enforces
per-run limits, not this calendar cutoff; checking and observing it remains
the operator's responsibility.

`iot_stream.HubReceiver` adds an explicitly called finite asynchronous SDK
adapter around `SensorIngestion`; it adds no HTTP route, startup task or deployed
service. `HubPublisher` sends one canonical observation/message through a
distinct `SYN-<sensor_id>` X.509 device identity. It never discovers devices,
uses twins/cloud-to-device management or retrieves a service key.
Install this project's declared dependencies with pip, including pinned
`azure-eventhub`, `azure-iot-device` and `aiohttp` for asynchronous identity.

The routed receiver and original routed publisher profile require `Activation`
with resource group `ama`, the exact Hub
hostname, matching `eh-<hub-name>.servicebus.windows.net`, `sensor-readings`,
`api-consumer`, `routing_ready=True` and a nonempty approval reference.
This is a caller assertion, **not verification or approval of deployment**.
The [infrastructure activation procedure](../../infra/README.md#keyless-consumer-and-explicit-activation)
must be separately completed first. The default bootstrap profile cannot send.
Do not treat this callable as permission to provision, enrol or read credentials.

The receiver creates only `ManagedIdentityCredential`, optionally with the
API's managed-identity client ID. It uses no developer credential chain or
connection string. An independently installed tuple of `Binding(device_id,
sensor_id, home_id)` fences the device and payload before SQL. The custom Event
Hub's sole authorized sender must remain the IoT Hub system identity: the
routed `iothub-connection-device-id` and device/X.509 authentication metadata
are accepted as byte-keyed AMQP application properties under that restricted
origin, not as arbitrary client assertions. String-key aliases, simultaneous
annotations, missing/wrong types, modules, wrong devices and changed sensor/home
claims are refused. Actual Azure routing representation remains unverified.
Independent SQL mapping, consent, calibration and policy remain mandatory.
Do not install them from telemetry or infer them from a synthetic label.

`await receiver.run(max_seconds=60, max_events=100, stop=stop_event)` returns
the existing opaque SQL receipts. Accepted and owned DQ outcomes are durable
before return. SQL/identity/envelope failure stops further admission, with a
fixed sanitized error rather than raw SDK exception text.
Constructor/startup failures use the same fixed-error boundary; any credential
or client successfully returned before failure is closed by bounded cleanup.
Each partition is
serialized; two partitions do not share an offset or imply global event order.
There is deliberately **no checkpoint store or checkpoint update**. Every
fresh finite receiver uses `starting_position="-1"` and reconciles retained
history through SQL idempotency, including SQL commits whose acknowledgements
were lost. This is a single-runner, bounded demonstration strategy, not durable
multi-instance partition ownership. Events older than the configured one-day
transport retention cannot be recovered by it; a poison transport envelope
will stop again until separately investigated, not silently skipped.

The publisher takes an exact per-binding mapping of SDK `X509` objects supplied
from separately approved certificate/key mounts. No credential lookup,
issuance, rotation or deletion is implemented. The already named exercise
credential owner, Juan Manuel Servera, must separately approve/perform the
Key Vault lifecycle and removal of every run-owned simulated identity (#185).
Do not give this code installed-device credentials or enable SDK debug tracing.
No actual identity or credential has been created or read for local tests.

Prepare frames with the [core replay API](../core/README.md#finite-synthetic-stream-replay-184).
Then call `await publisher.run(frames, budget, speed=1000, truth=restricted_truth.append)`.
`truth` is a required evaluator-owned sink, separate from telemetry and ordinary
diagnostic logs. It receives synthetic/opaque-reference/slot/fault/status
records including the selected-input digest copied from each Frame, never
values, home/device IDs or credentials. `attempt` without `sent`
is uncertain, not proof of no delivery: stop and retain the truth records for
review. Do not rerun identical frames or retry an uncertain delivery without
the separate owner approval and accounting required above; SQL idempotency
does not refund attempted messages or the exercise allowance.
`disconnect` is an explicit terminal synthetic stop, not an automatic reconnect.
Model-time spacing uses each Frame's `nominal_at`, not its observation timestamp.
For example, out-of-order suffix slots 3..4 retain their reordered payload times
while waiting the nominal 8 hours, or 28.8 seconds at speed 1000.
`burst` skips model-time spacing but still obeys the configured rate cap.
Actual send-attempt admission occurs after connection, message construction
and attempt-truth preparation, immediately before the SDK await in the same
coroutine. One limiter spans all device clients, so slow setup cannot spend an
interval and compress subsequent sends. Pause, stop and deadline are rechecked
at admission; an attempt truth record may precede a refused admission.
Normal-device altered sensor IDs are transport refusals. To exercise SQL
UNMAPPED, independently install an exact synthetic binding with that deliberately
unmapped sensor absent from SQL controls; payload truth never grants a bypass.

`RunBudget` requires owner, prior cost estimate reference and budget-alert
reference, finite messages, 1..3600 seconds, <=100 messages/second and declared
daily quota already used. These are declarations, not live billing checks.
It reserves >=40,000 of B1's 400,000 daily 4-KiB units, counting every attempted
message including duplicates and reserving 1 KiB/message for properties.
No autonomous send retry, connection retry or auto-connect is enabled.
Pause/stop flags on an optional `Pacer` are checked during pacing; stop is also
checked during connect/send. A supplied pacer's deadline must be finite and within
the validated run budget; its rate must be finite, positive and no greater than
the validated budget's rate. Invalid controls are refused before SDK client creation.
The deadline covers network waits with 0.5 seconds reserved for cleanup.
Even when cancellation interrupts cleanup, unfinished shutdown tasks are cancelled
and every cleanup task's eventual exception is observed without waiting past the
allowance for SDK cancellation acknowledgement. Cleanup failure is explicit.
Cancelling an SDK send cannot
prove it was not delivered. Cancelling/timing out a receiver does not cancel a
shielded SQL commit; its outcome remains uncertain until exact replay.
The caller must keep the store available until in-flight SQL work settles.
These controls do not establish an Azure spending stop or operational SLA.

Local regression commands, with installed distributions:

```bash
cd src/api
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_iot_stream test_sensor_ingestion -q
```

The tests use actual SDK message objects, fake network clients and temporary
constructed SQLite only. They prove code paths, not authenticated Azure
transport, actual credentials/alerts, Azure SQL restart or whole PRD AC-066.
The [issue evidence and deferrals](../../docs/reference/research/iot-sensor-analytics-research-plan.md#bounded-streaming-engineering-2026-10-27-refs-110-184)
keep every child and live gate visible.

### Synthetic handover SQL proof (#188)

`tests/test_sensor_consistency.py` writes composed backfill CSV, admits its
prefix through #110, then decodes the replay suffix using actual SDK `EventData`
and exact device bindings before the same SQL append. Ordered queries return
both phases per canonical home. The strict core report checks all 24 values
against the continuous writer reference with zero C/RH point, mean-step and
population-standard-deviation error tolerance. After reopening, whole-window
replay must return accepted replay receipts without changing readings,
deliveries, DQ, cases or audit. The existing fake-receiver seam test now also
uses the composed climate path.

```bash
cd src/api
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
  python -m unittest \
  test_sensor_consistency.SqlHandoverTests.test_composed_joint_query_statistics_and_reopened_window_replay -v
cd ../..
flock -w 600 /tmp/ama-rpi-heavy.lock python src/api/checks/sensor_sql_check.py
```

Ordinary discovery exercises SQLite. The second command explicitly selects this
same handover test alongside the existing ingestion suite on its own local SQL
Server; the test asserts the actual selected backend. The standard complete
gate does not implicitly include this sensor-specific SQL selector.
Constructed SDK origin properties and local SQL Server do not prove actual
authenticated IoT Hub delivery, Azure SQL query/restart or live handover.
Those criteria and #110 prerequisites remain unmet; no cloud execution or
issue status change is authorized by this source.

### Operator handover check for a live store (#188)

`zava_forward.api.sensor_handover_verify` runs the same strict report against
the SQL store selected by `ZF_STORE` (`sqlite` or `mssql`, so Azure SQL once an
owner provides it), using `SensorConsumer.observed_series(home_ids, windows)` for a
joint per-home query bounded to each home's reference window, with trusted
control units. The store is opened without migrations or other initialization
writes (SQLite read-only), so SELECT-only credentials suffice. Tolerances default
to zero and are declared per channel and metric. `--replay-check` needs write
access: it re-feeds the retained stored payloads for the window, in batches of
100, through the #110 consumer and requires replay receipts and an unchanged
series. Exit codes: 0 pass, 1 numeric failure, 2 refusal.

```bash
cd src/api
python -m zava_forward.api.sensor_handover_verify --reference history/readings-0000.csv \
  --handover 2024-10-04T00:00:00Z --temperature-point 0.5 --replay-check
```

The check is ready-to-run tooling; running it against Azure SQL after a live
Hub stream is the remaining owner-gated evidence for #188.

## Finite offline sensor ingestion (#110)

`sensor_ingestion.SensorIngestion(store).consume(observations, received_at=...)`
is an API-owned in-process callable, not an HTTP endpoint or live hub client.
It composes the [core SQL processor](../core/README.md#constructed-offline-sensor-consumer-110)
and returns a tuple of bounded metadata-only receipts. Trusted constructed setup
uses `adapter.consumer.configure(policy, controls)` independently of observations;
no incoming payload is control authority. No service, daemon, background thread,
public route, SDK, AI call or resident message is added.

The batch must be a materialized list/tuple of 1..100 bounded primitive dictionaries,
each <=20 keys and <=4096 serialized bytes. Envelope failures are refused before
any writes. Primitive closed-schema failures, including missing IDs, produce
digest-keyed owned DQ without inventing device identity. Only observation fields
from `sensor_faults.Packet.rows` are inputs, never truth/labels/clean rows.
Receipt time is an explicit trusted UTC whole-second string; no operational
clock window, calibration, consent or range is guessed.

The [shared observation contract and volume reference](../../docs/reference/research/iot-sensor-analytics-research-plan.md#shared-observation-contract-and-volume-2026-10-18-refs-186)
lists the imported 13 required string fields and measured synthetic example.
One record pairs temperature and RH. Three records/home/day is the unchanged
accounting baseline; finite callable batches are not adopted wire packetization
or Hub billing/throughput evidence. Stock/live identity compatibility remains a
separately reviewed downstream decision, not established by these fixtures.

Transactions are per observation. Invalid rows produce DQ and processing
continues; SQL failure/uncertain acknowledgement stops immediately.
`BatchStopped.code`, `.reference` and `.completed` contain only bounded metadata,
including the acknowledged committed prefix. `SENSOR_COMMIT_UNCERTAIN` requires
reconciliation, not an assertion that nothing persisted: replay the same finite
batch to reconcile committed prefix/uncertain outcome without another append.
Exact historical replay ignores later authority/window changes but never
readmits or advances a projection. No task or property record changes.
Malformed/inconsistent retained reading or witness raises bounded
`SENSOR_OUTCOME_MALFORMED`; `BatchStopped.completed` preserves earlier committed
rows even when a later retained timestamp or numeric value is corrupt.
Unsupported JSON raises `UNSUPPORTED_STORE_SQL_REQUIRED`; unavailable SQL never
returns a fake empty success. Restricted DQ inspection is Python-only.

From the repository root, with project distributions installed:

```bash
PYTHONPATH=src/core/tests python -m unittest discover -s src/api/tests -p test_sensor_ingestion.py -q
python src/api/checks/sensor_sql_check.py
```

The second command owns a uniquely named, memory/CPU-bounded SQL Server container
and loopback port with random process-only credentials and finally cleanup.
It exercises the same actual API suite plus the #188 handover selector, including concurrent independent
connections, reopen, real engine-trigger rollback and accepted/rejected
postcommit reconciliation. It never connects to Azure or uses private datasets.
Local SQLite/MSSQL/nonroot read-only image evidence does not meet whole AC-066:
real Hub identities/transport, Azure SQL acceptance and registered real AI remain
unexecuted. The
[2026-10-15 owner acceptance of ADR 0003](../../docs/adrs/0003-journey-derived-capabilities-runtime-fit.md#status)
selects Basic IoT Hub for the exercise, excluding cloud-to-device messages,
device twins and device management. Sizing, cost, provisioning, network and
device credential ownership remain separate decisions. No issue closure follows.

## Constructed RAI evidence register API (#126)

`GET /api/governance` remains current-registered-manager only and includes
`rai_evidence`: exactly 22 open baseline findings, explicit insufficiency,
retained claims and separate caller-declared current assessment. The governance
handler now reaches its existing manager guard before the generic staff
projection; unrelated staff and contractors still cannot read the register.
No read initializes defaults, appends audit or accepts a finding.

Optional `assessment` is one URL-encoded JSON object with exactly `source_commit`,
`task_id`, `task_version`, `release_version`, `nonapplicability_reason`. Commit is
full lowercase 40-hex. Either the three task/release fields are nonblank strings
up to 200 characters and reason is null, or they are all null and reason is
nonblank text up to 600 characters. It is a declared comparison, not server-build
or deployment attestation. Missing context is Unknown; baseline replay is history.
Unknown/repeated parameters and malformed explicit contexts return 400.

`POST /api/governance/evidence-record` accepts only this constructed claim shape:

```json
{
  "finding_id": "MAP-01",
  "baseline_commit": "1cb398c7b90bec05a5700008a97d0cfac494144a",
  "assessment": {
    "source_commit": "ab0613f3336109ff9b96560a16758ee842232715",
    "task_id": null,
    "task_version": null,
    "release_version": null,
    "nonapplicability_reason": "Constructed whole-system source inspection, not a task release"
  },
  "evidence_tier": "insufficient",
  "result": "Constructed example, not an executed qualified assessment",
  "references": ["exact source/test/observation reference"],
  "limitations": "No qualified human or live evidence",
  "decision_maker_status": "Unappointed",
  "decision_maker_ref": null,
  "event_ref": "unique-constructed-event-reference",
  "expected_revision": 0
}
```

Replace the example assessed commit and references with the actual claimed scope;
the server does not attest those assertions. Result/limitations are nonblank
strings up to 2000 characters; references are 1..20 nonblank inert strings up to
500 characters each; event reference is up to 200. Revision is a nonnegative
integer, not a boolean. Decision-maker status is Unknown/Unappointed with null
reference, or Unverified reference with nonblank reference up to 500 characters.
No supplied owner reference establishes delegation or assignment.

Evidence tier is implemented/source-tested, deployed-observed, proposed,
insufficient or independent-acceptance. All are unverified constructed claims.
Server records authenticated identity/UTC/revision and keeps prior records.
Same event/content/actor retries return the exact original without another write;
conflicting event reuse or a stale new-event revision returns 409.
Client actor/time, approval/closure promotion and unknown fields return 400.
No acceptance or closure endpoint exists. Current manager identity is checked
again inside SQL's existing shared-document writer transaction.

HTTP 409 with `outcome: committed` means persisted but acknowledgement failed:
reload history and reconcile the event reference before another action. This also
covers response encoding before headers, not a guarantee after network bytes
have been sent. JSON's documented cross-file crash boundary remains.
See the [core contract](../core/README.md#constructed-rai-evidence-claims-2026-10-18-126)
for inventory, completeness and local validation limits. Ten actual loopback HTTP
cases cover JSON/SQLite login, roles, read/write, stale binding/revision, replay,
closed schema and committed responses; no browser or web change is involved.
No finding closure, qualified assessment, real AI/Azure delivery or operational
acceptance follows from these local engineering results.

## Appointment control API and manual workbench (#87)

`POST /api/workorders/{id}/appointment-control` accepts `offer`, `authority`,
`confirm`, `outcome`, `configure`, `investigation` and `close_case` actions with a unique
`event_ref`. Current registered managers also need existing appointment contract
delegation. Contractors and forged identities cannot write. Offers record
`date`, `period`, `options`, `constraints`, minimum-necessary `instructions`,
explicit `paused`/`deferred`/`bundle` booleans and `expected_offer_id` (null for a
first offer). A named resident-update commitment must already exist on the home.
Bundles additionally need `bundle_agreed` and exact-scope competence evidence with
a nonblank textual source reference of 1 to 500 characters.

Separate confirmations carry `offer_id`, `kind` (resident/staff/capacity),
`person`, `source` and `channel`, including phone/paper/in-person manual routes.
Representative confirmation requires separately recorded, current appointment-only
authority bound to that offer/home/scope/person/validity, not works-decision or
attendance permission. Client `status` cannot grant commitment. Current work-order
projections return derived Unknown/Offer/Committed/Ended and missing/stale evidence.
Provider projections contain only assigned scope and necessary visit instructions.
The existing resident-view and recorded-reason entitlements also protect
appointment evidence from unrelated staff. Their scheduling projection retains
date, period, instructions and state, not household/authority/closure/investigation
evidence. No role entitlement is broadened.

Outcomes name the offer, cause/owner/source and explicit `verified`, `no_access`,
`preference_breach` and `abortive` facts. Retry reconciliation never adds another
visit or counter increment. Reporting thresholds for breaches/abortive visits are
Unknown. Provisional exercise threshold configuration is versioned, not policy
approval. Changed configuration evaluates existing eligible active counts
atomically, without recounting visits, duplicating tasks or resetting history.
Investigation checks, corrective action, next update and task disposition
are recorded manually; no task disposition closes the home case or resets counts.
The same route accepts explicit `action: close_case` to record a supplied HUMAN
underlying-home-case closure, separately from investigation task disposition.
Supply the exact `case_id`, staff projection's `case_version` as
`expected_case_version`, `confirmed: true`, unique `event_ref`, decision `source`,
`source_version` and `reason`. Existing current registered manager and contract
appointment authority are required. The server records actor/time, controlled
history and the active-count boundary atomically with the existing case `closed`
field. Visit/configuration history, consumed references, outstanding resident
updates, remedies and unrelated decisions remain. Reopening alone does not reset;
old event references cannot count again. This implements only the record-only
human boundary in PRD DD-006/AC-033, BRD RULE-006/AC-025 and addendum EXA-014,
not a general closure policy or technical, legal or financial approval.

The existing Capacity and work orders screen uses labelled native forms, separate
manual confirmations, textual states and inline live errors. The
selected visit date uses the existing localized date helper; period/instructions
are shown before confirmation and to the assigned provider, with Unknown and
historical-ended wording. Manual drafts warn on in-app navigation and page exit,
survive another action's refresh, and clear only after their own successful save
or explicit confirmed discard. Retained drafts keep their original offer/case
dependency references, so a refresh cannot silently rebind supplied evidence.
The separate manual home-case closure form requires an explicit checkbox and
cancellable confirmation;
the case identity, active/closed state and retained closure count are visible.
A case link preserves the #88 update owner and manual contact path. No message, booking, supplier
instruction, sanction or legal/financial approval is sent or inferred.
HTTP 409 with `outcome: committed` means the change persisted but acknowledgement
failed: reload history, do not perform a new action.
Response-only encoding failures are handled before sending headers; this does
not promise recovery of a connection after response bytes have been sent.
Run `checks/procurement_browser_check.py` with the existing API/core test paths
for local synthetic keyboard, offer/commitment, denied-route and reflow checks.
These checks are not resident validation or WCAG certification.

## Continuity epoch and retained offline evidence (#122 partial follow-up)

The new bounded register/release remediation applies the existing recorded-need
policy to `GET /api/continuity` and the control documents returned by suspension,
restart, change and reversal actions. Permitted roles retain safe IDs, registered
scope, status, epoch, proposal/decision state and communication flags; protected
narratives, arbitrary subject/version keys and unknown nested text are held.
Canonical stored evidence and full authorized responses are not redacted.
This does not change who may suspend, propose, decide or export.

Every retained task release is now checked for lifecycle completeness, including
releases with no proposal reference. Missing, truncated, malformed or contradictory
records make production incomplete and offline verification invalid, even after
the ordinary bundle digest is recomputed. Lifecycle checks allow repeated
suspension and timestamp ties supported by the writer, but cannot authenticate
wholesale consistent rewriting of unanchored history. Event timestamps accept
only integers and floats that pass floating-point finiteness validation, excluding
booleans; conversion overflow, nonfinite values and nonnumeric values explicitly
make producer evidence incomplete and offline verification invalid. This is not
a calendar-date policy; finite negative, fractional and large numeric values
retain their existing meaning. Known-empty SQL evidence
and explicit unsupported JSON storage remain distinct from unavailable evidence.
Audience-limited exports remain explicitly incomplete, never full ledger proof;
externally held canonical heads are unchanged. Local synthetic proof is not
operational acceptance of issue #122.

Durable assistant identity includes the persisted creation epoch. Suspension and
restart invalidate old queued, leased, ready and accepted work for current use,
even if sources and task release are unchanged. Detail/list/review/verification/
edit-accept and export enforce this on the server. Historical disposition and
permitted evidence remain; a fresh invocation or eligible scan creates fresh
epoch-bound work. Missing lifetime evidence fails closed. Late calls can remain
charged or unknown; no remote cancellation or exactly-once billing is promised.

Legacy text/document/priority publication uses the existing optimistic continuity
document check in the writer transaction. A competing epoch change refuses the
old publication and permits only a local quarantined-record retry, never another
provider call. Gate-aware processes refresh persisted epochs; this does not make
an image predating the gates safe. Such images must be stopped/drained or denied
serving access by an enforceable deployment boundary outside this source change.
The change/reverse register is evidence, not general serving configuration control.

Full continuity JSON bundles retain task-release reference-time snapshots, current
status/revision and release-ID lifecycle events with IDs/timestamps/associations.
Offline verification resolves ID/version/digest/task and lifecycle completeness,
in addition to bundle digest, ledger chain and optionally an externally held head.
Missing/unavailable/truncated referenced evidence is explicitly incomplete. No raw
provider requests or extra sensitive input fields are added. Self-contained
hashes cannot authenticate wholesale rewriting of unanchored task-release events.
Proposal collection and source metadata are required even for empty collections.
The verifier independently checks exact boolean flags, nonnegative integer
total/exported counts and serialized list agreement. Declared truncation is
invalid regardless of producer completeness flags or a recomputed bundle digest.
Source status distinguishes available SQL evidence, explicitly unsupported empty
JSON-store proposals, and unavailable evidence. Missing/unavailable source metadata
fails closed; legitimate unsupported JSON exports remain usable. Older bundles
without this metadata must be regenerated from retained source evidence, not
silently certified complete.

A SQL migration/schema failure is unavailable evidence, not an unsupported JSON
store or a known-empty collection. Export retains an unknown total and explicit
truncation/unavailability with the safe operator/manual-route message; it never
substitutes empty release proof or exposes driver exception text. Both the normal
HTTP producer and offline verifier reject completeness, including after an
ordinary digest is recomputed. Ordinary case/manual work remains available.

Focused regressions are in `tests/test_continuity_epoch_export.py`, using installed
`src` distributions and synthetic nonbillable providers. `ZF_CONTINUITY_MSSQL=1`
requires `ZF_ISSUE122_OWNED_SQL` and loopback-only `ZF_SQL_*`; each test creates
and drops a UUID-named database on an explicitly task-owned local container.
SQLite and actual local SQL Server evidence are distinct from Azure evidence.
The original independent Review was Not accepted (RV-001/RV-002). Authorized
correction ONE adds only the two continuity GET route kinds to the outer staff
allowlist and validates proposal collection completeness offline. Inner register
access remains limited to managers, Quality Inspector and Building Safety Liaison;
export remains manager-only. Contractor, unknown and unrelated staff denials are
retained and exercised over actual HTTP. Correction evidence is not independent
acceptance; the original adverse Review is unchanged.
Coordinator-authorized correction TWO applies the existing recorded-need policy
(`DEFAULT_REASON_ROLES`, or the configured `ZF_REASON_ROLES`) at export. A manager
with a recorded need receives full evidence and the exact canonical ledger, still
subject to independent completeness and external-head checks. A manager without
that need retains HTTP export access but receives a closed, audience-limited
summary: numeric/boolean lifetime information, known dispositions, counts and the
recorded head. Free-text evidence, identifiers, snapshots/events, raw ledger rows
and governance/version narratives are held rather than pattern-filtered.

Limited exports say `audience.scope=limited`, `full_ledger_proof=false`,
`ledger.full_proof=false` and `complete=false`, with an explicit nonsensitive
reason. The verifier rejects full-proof validation, even if producer completeness
flags and the ordinary digest are rewritten. No redacted row claims the original
hash, and the server-side canonical evidence is unchanged. Such summaries cannot
reconstruct task-release references or prove the full ledger; a separately
authorized full export is required for that purpose. Original adverse Review
and correction ONE failures remain historical evidence; correction TWO does not
constitute independent acceptance or deployment readiness.

The continuity follow-up is integrated onto the appointment-controls baseline
`3104bb69ddc26c81e0e9d2f57000dac1d99a419a` (#397). Integration preserves
both the existing appointment evidence projection and the two continuity GET
allowlist entries; it introduces no additional domain behavior. The original
continuity Review and both correction histories remain unchanged.

Manual contact, resident challenge and independent hazard transactions still use
their existing authority and safety gates during suspension. Synthetic exercise
records do not prove genuine named authority, an authorized witnessed drill,
an immutable externally held Azure head or an Azure SQL drill. These remain
unmet; this is not completion or operational acceptance of #122.

## Coordinator heatmap and lifecycle funnel (#101)

Original Review RV-001 exposed false403 for staff with a mixed-case stored email.
Correction ONE normalizes the coordinator lookup key without weakening current
identity checks. Actual JSON/SQLite HTTP regressions and a mixed-case Chromium
journey pass. Original Defects found verdict remains unchanged; independent
coordinator acceptance is still pending.

From Overview, choose **Coordinator heatmap and lifecycle funnel**. The existing
workbench/Leaflet map now has a scoped read-only coordinator mode, not a new
framework. Manual case routes and the legacy overview remain available.

```text
GET /api/coordinator?view=all&as_of=2026-10-10T12:00:00Z&area=Test
GET /api/coordinator?view=all&as_of=2026-10-10T12:00:00Z&metric=exits&metric_stage=Contact%20paused
```

Registered staff only; contractors and unknown/revoked actors are denied before
aggregation. `view=mine` (default) means current owner-code assignment; `all`
means the existing staff-wide permitted open cases, not additional case authority.
The [core contract](../core/README.md#read-only-coordinator-populations-101)
defines denominator, stopped work, draft priority, observed flow and unknowns.
Existing source filters `stage/area/wave/owner/contractor/flag/queue` and `q`
are shared by map, heatmap, funnel and record pages. `group_by` is `area`
(default), `building` or `archetype` (recorded home type, not an approved technical
classification). Missing groups remain explicitly Unknown.

`as_of` is required and selects recorded events, not historical membership;
optional `start` is inclusive UTC. The current `stage` source filter never
changes meaning when `metric_stage` drills an observed entry/exit/return/reopen.
For example, a current Contacting resident case can appear in exits from Contact
paused. Metrics also include `current`, `stopped`, `missing_geocode`,
`unknown_history`, `priority` and `filtered_out`. Unapproved priority refuses
drillthrough. `filtered_out` means source filter/search exclusions, not lifecycle
exclusion, and cannot select a group/stage cell. Unknown/empty/repeated parameters
refuse with 400; `limit=1..100` and nonnegative `offset` page stable case IDs.

Map `total` equals record selection total, including missing/invalid coordinates;
`mapped`, `missing_geocode` and `in_view` are separate. Panning narrows only
mapped viewport coverage, not the record denominator. Every count link retains
source filters and event window. Tables and native keyboard links/buttons remain
equivalents to heat colours and map gestures. **Show these as a list** focuses
the complete selected record table, including cases without coordinates.
No new map provider, licence, ranking, approval, history writer, AI or service.

From `src/api`, after editable source installation:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest \
  test_coordinator_api.CoordinatorApi test_coordinator_api.JsonCoordinatorApi -q
ZF_COORDINATOR_BROWSER=1 PYTHONPATH=tests:../core/tests:../agents/tests \
  ../../.venv/bin/python -m unittest \
  test_coordinator_api.CoordinatorApi.test_actual_browser_keyboard_filters_drill_map_unknowns_and_denials -v
```

`ZF_COORDINATOR_MSSQL=1` selects `test_coordinator_api.MssqlCoordinatorApi`
against an explicitly task-owned loopback SQL Server only. Its UUID-named
`zf_coordinator101_*` fixture databases are dropped after each test; no shared
database is eligible. The browser uses the actual local application, synthetic
SQLite, keyboard filter/exit/record/map-list/cluster navigation, coverage/unknown
labels, count parity, denials and 320/390/1280px reduced-motion reflow. Local
engineering evidence is not WCAG, human understanding, Azure or independent
coordinator acceptance.

## Historical progress report and export (#102)

Existing staff-only report paths support explicit `report=progress`:

```text
GET /api/stats?report=progress&as_of=2026-10-10T12:00:00Z&view=all&ready=2
GET /api/cases.csv?report=progress&as_of=2026-10-10T12:00:00Z&view=all&ready=2
```

Use URL encoding for offset timestamps (`+` becomes `%2B`). `as_of` is required,
timezone-aware and not future. Optional `start` must be timezone-aware and no
later than `as_of`. Both boundaries are inclusive for events; observed interval
clocks are clipped to the requested period. Supported `view` values are
`mine` (default), `all`, and manager-only `closed`. Existing stage/area/wave/
owner/contractor/flag/queue source filters are reused; their membership is
explicitly current-record selection, not historical reconstruction.
Unknown/empty/repeated parameters or invalid assumptions return 400. Contractor/
unknown roles are denied; direct Store calls enforce the same staff boundary.

The [core report contract](../core/README.md#historical-progress-evidence-and-declared-forecasts-102)
defines source mapping, partial/unknown history, independent handoff clocks
and forecast limitations. Optional `ready` declares a hypothetical ready count,
not actual consent or technical readiness. Optional positive `capacity`,
`duration`, `weeks` default to 2/1/4. Without declared `ready`, a requested
scenario is refused; with no scenario parameters Forecast is unavailable.
No model/provider is called. Forecasts cannot release work or approve outcomes.

JSON and the `progress.csv` attachment serialize the same `progress/v1` report,
including definitions, source locators, exact as-of/cohort/denominators,
unresolved exceptions, assumptions, sensitivities and Not reviewed approval.
CSV uses UTF-8, LF, standard quoting and fixed `section,value` rows; each value
is a compact sorted-key JSON cell. Parsing those cells reconstructs the exact
JSON report. Case IDs and events have stable ordering; repeat inputs produce
identical CSV. Raw identities, notes, resident fields and supplied source/
commercial evidence are not included. Empty cohorts/history remain visibly
unresolved. Default `/api/stats` and `/api/cases.csv` responses are unchanged.
No existing screen was redesigned or wired to this optional mode.

After pip editable core/agents/API installation, run from `src/api`:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest \
  test_progress_report_api.ProgressApi test_progress_report_api.JsonProgressApi -q
```

`ZF_PROGRESS_MSSQL=1` selects `test_progress_report_api.MssqlProgressApi`.
It refuses non-loopback SQL servers, creates UUID-named `zf_progress102_*`
databases and deliberately retains them: do not target shared/live systems.
Configure existing `ZF_SQL_*` privately for a uniquely named local Docker SQL
Server. SQLite and actual MSSQL exercise reload, external-writer refresh,
report/CSV parity and unchanged audit. Image checks run the authenticated
local report as UID/GID 10001 with read-only root and reduced capabilities.
These are engineering checks, not browser, WCAG, human, operational, AI or
Azure acceptance. Prospective capture now covers the actual controlled
stage/handoff/quality writers described in the core contract; absent historical
periods and nonexistent general forward/closure writers stay unknown.
The same existing HTTP 503 `outcome=committed` contract handles a committed
transition whose refresh/acknowledgement failed, without reporting rejection.
Verified operational capacity and complete historical coverage remain separate
evidence prerequisites.
The one original Review found blank-query and UTC-range handling defects;
correction ONE adds explicit refusals and failing-first regressions. Final
focused checks ran 88 tests plus eight actual loopback MSSQL tests, and the
corrected non-root image exercised exact installed source hashes and HTTP
report/export behavior. The original adverse Review is retained; these
targeted checks are not a second full Review or independent coordinator Pass.

Coordinator correction TWO addresses a reachable mixed-precision handoff:
precise offer/accept events surround legacy minute-truncated receipt events.
Reports preserve source versions and valid lifecycle sequence, expose precision
and cutoff unknowns, and never manufacture a wait duration or assert a
boundary-ambiguous event occurred before as-of. Precisely backward or otherwise
invalid history remains contradictory. New handoff writes preserve UTC
microseconds; old history is untouched. JSON/CSV retain identical definitions,
event order, as-of and denominators. The independent exact-28227fa8
Revise / Medium disposition and original adverse Review remain retained;
targeted correction evidence does not self-award acceptance.

## Resident commitments and remedy API (#88)

Existing `POST /api/cases/{case_id}/resident` and case detail remain the only
routes. The [core contract](../core/README.md#resident-commitments-and-independent-remedy-clocks-88)
defines named owners, independent clocks, legacy confirmation and SQL validation.
The existing resident panel records full commitments and shows response/remedy
status, owner and date separately, including open items after response closure.
Nothing sends messages, proves receipt, determines lease responsibility or
changes an approval. Existing non-digital service/complaint routes stay available.

Additional actions: `update_record`, `remedy_confirm`, `remedy_update` and
`service_reopen`. Remedy actions include request `id`; all four include integer
`expected_version`. Version zero means absent/unversioned, not permission to
overwrite a known record. `remedy_confirm` supplies owner/basis; remedy progress
supplies status/note and optional reassigned owner; response reopen supplies note.
Service intake additionally offers Charge query and Household dispute.
Existing service update/close request shapes remain compatible; `status` means
response, never remedy. Handoff inputs no longer create partial commitments.

`service_reassign` recovers a departed response assignee through the same endpoint.
Only an existing Retrofit Programme Manager or Programme Support Officer may
submit request `id`, integer `expected_version`, `responsibility` service/redress,
new current eligible named `owner` email and reason `note`. The existing panel
shows this form only to those roles, and shows old/new owner, actor, reason and
time in request history. No manager becomes owner implicitly. Server-side writer
validation also rejects stale versions, changed identities and non-independent
complaint/review assignments. Remedy ownership and other clocks remain unchanged.
Response status owner/date follows responsibility, not shared-person email:
redress for Closed or Independent review, otherwise service. Reassigning the
other responsibility preserves that status clock, including legacy Unknowns.

Invalid input returns 400, stale version/writer 409 and missing/current-owner
authority 403. Post-COMMIT synchronization or subsequent detail failure returns
409 with `outcome: "committed"` and explicit reload/reconcile instructions, not
a claim that nothing was recorded. Scoped resident forms retain input and inline
live errors; uncertain/committed results disable ordinary resubmit until reload.
Registered roles are server-enforced; neither a request role nor owner label
grants authority. New references and nested handoff commitment snapshots are
hidden from non-resident-view roles; contractor allowlists remain unchanged.

`test_resident_api` runs authenticated loopback HTTP with small fictional SQLite.
`ZF_RESIDENT_BROWSER=1` enables its actual Chromium journey: invalid commitment,
keyboard create/reassign, close response with remedy still open, remedy close/
reopen, response-only reopen, departed-owner manager recovery with retained
invalid input/error focus, recovered-owner update, independent response closure
and 320/390/1280 widths with reduced motion.
This is engineering evidence, not screen-reader, human usability or WCAG acceptance.

## Grant and application records (#95)

Existing `POST /api/cases/{case_id}/grant` and `/funding` routes now use
the [core current-human designation and evidence contract](../core/README.md#grant-lifecycle-and-human-exercise-designation-95).
Missing/stale staff or missing, revoked, expired, wrong-state/case/route
designation returns 403; missing event evidence, legacy unknown-currency
proposal or unsupported currency returns 400; stale SQL writers return 409.
Request-supplied roles/designations cannot confer authority. No endpoint submits
to a funder, executes payment or grants real financial authority.

Funding `approve`, `submit` and `confirm` requests keep `{action, text}`:
`text` must now contain the event-specific evidence reference (1-200 characters).
Application confirmation is explicitly labelled as application status, not a
grant award or cash receipt, and requires its own reference in the existing
panel. Application events leave the separate grant history/provider finance
unchanged. Opportunity GBP 40 million is never inherited as award/cash.
The Finance role still exposes the panel, but visibility is not designation.
No existing staff is automatically granted authority; real delegation remains
unverified and exercise authority is refused in production.

`tests/test_grant_lifecycle_api.py` uses authenticated loopback HTTP with tiny
temporary synthetic SQLite. `ZF_GRANT_BROWSER=1` additionally runs actual local
Playwright over the changed confirmation control, missing-evidence refusal and
Opportunity-only/Confirmed-application mixed state. These are focused engineering
checks, not full WCAG, human usability, real delegation or deployed acceptance.

## Per-measure quality API (#91)

The existing `POST /api/cases/{id}/quality-*` routes keep their request shapes.
`quality-submit` records checklist evidence and accepts the current
`context_revision`; when replacing Accepted/Handed over evidence it invalidates
all former same-measure acceptance/handover, not other measures. The
[core quality contract](../core/README.md#per-measure-quality-and-handover-controls-91)
describes retained lineage, independence and transactional behavior.
`quality-fix` now requires a nonempty `note` describing remediation and its
photo/document/inspection reference. `quality-reinspect` requires Fixed state.
No endpoint grants professional authority or pays anyone.

The authenticated actor, never body-supplied name/role, authorizes every write.
Contractors continue to receive 403 for all quality/finance writes; staff record
provider evidence through the existing manual route. Foreign supplier cases
remain inaccessible. Unknown/revoked staff and self-accepting identity aliases
are denied. Malformed/negative indices, missing remediation and actions on a
superseded record return 400. SQL optimistic conflicts return 409.
A confirmed committed decision whose post-commit refresh fails returns 503
with `outcome: "committed"` and explicit guidance to reload and inspect history
before retrying. It is not reported as success or rolled back; the committed
success audit and any legitimate audit prefix remain exactly once.

The existing quality panel labels remediation evidence, retains input and
focuses the missing-evidence field on failure. Replacement asks for confirmation
and displays the prior acceptance/handover as historical, with no old action
buttons. A fresh independent acceptance and resident handover remain necessary.
The actual fictional loopback Chromium journey exercised those steps, keyboard
fix submission, cancellation/confirmation, labelled controls and 320/390/1280px
reflow with reduced motion and no page errors. It also exercised an actual
post-COMMIT refresh failure, visible committed/reload guidance and reload
confirming accepted state. This is engineering evidence, not a WCAG,
screen-reader, resident-understanding or competent-human sign-off.
Existing form/navigation accessibility gaps remain outside this narrow change.

`test_role_matrix.QualityMatrix` exercises the actual authenticated SQLite HTTP
routes, contractor/foreign-case denials, forged-body refusal, remediation,
replacement, explicit committed-refresh outcome, and unchanged finance/grant
records. The shared `server.py` change is only the quality-specific exception
handler; its #95 overlap is declared. No `app.js`, `finance.py`, dataset fixture,
scenario manifest or shared SQL helper change was required.
The current BRD FR-017 describes handoff information; PRD FR-017 describes this
quality lifecycle. They are not represented as identical requirement numbers.

## Record-only finance API (#94)

`POST /api/cases/{case_id}/finance` retains its existing single-record action
contract; `GET /api/finance` retains the human exception/hold queue.
The [core finance guide](../core/README.md#record-only-finance-controls-94)
describes current identity, line matching and persistence controls.
No endpoint pays, submits banking instructions or grants authority.
External-payment statuses are notes only. Budget/commitment and grant/cash
records are unchanged by those notes.

Current registered Finance staff are rechecked for every write, including
transaction-time SQL validation. A preparer with an alias sharing email, staff
code or OID receives 403 when attempting their own approval/disposition or
hold release; distinct permitted staff with the same role are supported.
Unknown match inputs and held/stale acceptance return 400 with the existing
plain-language error. Optimistic SQL writer conflicts return 409.
Existing screens already render the returned zero-based exception `line` as a
human one-based line number; no web assets or browser behavior were changed.

`tests/test_finance_match_api.py` exercises authenticated loopback HTTP over
temporary fictional SQLite, including actual same-role identity refusals,
unknown line exceptions/queue, held disposition, external status notes and
reopened ledger invariance. Backend-only checks do not claim browser/WCAG,
company delegation, Azure or real payment acceptance.
Core correction TWO also covers SQL recovery failure after an executed audit
INSERT: no failed approval event can be flushed at lock exit. Original errors
retain explicit recovery diagnostics. The endpoint contract and web assets
are unchanged; independent coordinator closure of PR #383 remains pending.
Authorized integration onto main `bbbc924` also retains merged stock/technical
actor validation, refusal ownership and checked-document recovery. Combined
stock API/workflow/role checks ran with the required `src/api` module path;
the existing opt-in stock browser check was skipped, not newly certified.
## Provider capacity and order API (#90)

Existing authenticated package, capacity and work-order routes retain their
response shapes. `POST /api/packages` requires a nonempty `contract_version`;
omitted, empty and whitespace-only versions return 400 without creating a
package. The existing screen displays an inline error and focuses the version
field without losing other inputs. Creation is a draft, never a grant of
authority. Positive capacity requires
the [core source and trusted delegation contract](../core/README.md#evidenced-provider-capacity-and-controlled-orders-90).
There is no endpoint to appoint a contract manager.

`POST /api/packages/{id}/capacity` accepts the existing `contractor`, `offered`,
`committed`, `evidence` reference and the structured `details` object below.
IDs/version/dates must refer to a real original upload in the current local
store, not this illustrative identifier:

```json
{
  "contractor": "Fictional Provider",
  "offered": 9,
  "committed": 1,
  "evidence": "SYN-COMMITMENT",
  "details": {
    "source_case_id": "SYN-HOME",
    "document_id": "actual-upload-id",
    "source_version": "1",
    "source_date": "2026-10-17",
    "reviewed_on": "2026-10-17",
    "valid_from": "2026-10-17",
    "valid_to": "2026-12-31",
    "unit": "home-work-order",
    "case_ids": ["SYN-HOME"],
    "status": "Committed"
  }
}
```

Unknown/invalid legacy capacity stays visible with `evidence_status` and
`usable_committed: 0`, rather than becoming available. A larger offer never
permits a second order against one committed unit. Existing orders may
progress at exact quota. Issue, every appointment outcome, reissue,
completion, correction and withdrawal each append a version/issuer snapshot.
The existing case advance route cannot confirm an unbooked or unevidenced
order. Contractors receive 403 for package reads and all procurement writes;
order reads filter by their current supplier identity.

The existing Capacity screen supplies labelled original-source/version/date/
unit/home fields, explicit unknown status, keyboard submission and inline
failure focus. Human authority and resident approvals remain server checks,
not screen permissions. AI/template notes say not an instruction; accepting
a proposal never issues an order.

Run the exact HTTP and domain suites from `src/api` with installed editable
packages. The optional browser check uses only temporary fictional SQLite,
blocks non-loopback requests and exercises manager/contractor journeys:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests \
  python -m unittest test_quality_procurement test_procurement_api test_role_matrix -q
PYTHONPATH=tests:../core/tests:../agents/tests \
  python checks/procurement_browser_check.py
```

With the existing opt-in SQL Server harness configured against a disposable
local container, select `test_mssqlstore.MssqlProcurement` and
`test_mssqlstore.MssqlProcurementApi`. Never point its destructive fixture
reset at shared/live SQL. Local browser widths 320/390/1280, keyboard and
reduced-motion checks are not human, screen-reader or full WCAG acceptance.
No live orders, payments, AI inference, company delegation or Azure SQL were
exercised. Existing #78 provenance and #97 forms contracts remain unchanged.

Shared-transaction integration coverage also selects
`test_mssqlstore.MssqlStockDecisions`,
`test_mssqlstore.MssqlFinanceSignoffs`,
`test_mssqlstore.MssqlStoreTests` and
`test_mssqlstore.MssqlImproveTests` against that disposable local server.
The finance suite replays existing budget, matching, approval-separation and
signoff controls; it does not incorporate another unmerged finance topic.
For merged #94's exact finance-match and recovery controls, additionally
select `test_finance_match_controls.MssqlFinanceChecks` with
`ZF_FINANCE_MSSQL=1` against the same disposable local server. That existing
fixture creates and removes only its uniquely named test databases.

## Consultation record API and unknown hold (#92)

Authenticated managers may POST
`/api/packages/{package-id}/consultation` with exactly:

```json
{
  "status": "unknown",
  "decided_by": "Fictional human adviser, authority unverified",
  "reason": "Supplied human decision for review, not Legal approval",
  "source_case_id": "SYN-HOME",
  "document_id": "actual-upload-id",
  "source_version": "1",
  "expected_version": 0
}
```

Status permits `applies`, `complete`, `not_applicable`, `unknown`; expected version
is the current consultation-history length. The route returns refreshed packages/
orders, HTTP 400 for invalid/source inputs, 403 for non-manager or unregistered
identities, and 409 for a stale record version. Caller-supplied recorder/time/
authority fields and bulk requests are refused. Package responses expose
`consultation_status: "unknown"`, `consultation_authority: "Unverified"` and
the supplied decision history with server provenance. The recorder is not
presented as Legal and no supplied positive claim clears confirmation.

The [core boundary](../core/README.md#consultation-records-and-confirmation-holds-92)
explains the missing verified Legal capability and genuine let/renew seam.
The 2026-10-18 owner decision limits holds to consultation-dependent actions;
ordinary service order issue/reissue/correction/booking/advance retain their
independent controls without a blanket consultation prerequisite. Existing
explicit building dependency scope still holds affected instructions (HTTP 409
with `reasons`), and final case advancement retains its case-wide building gate.
Neither source hashes nor supplied complete/not_applicable records release
those holds or confer Legal authority. Unknown let/renew routes remain HTTP 404,
not a successful unsupported transition. All affected regression classes now run
without consultation-guard bypasses. No browser/UI changes were made or newly validated.
Exact #92 criteria remain partial; no issue closure or legal activation is claimed.

## Form schema and candidate API (#97)

This is unapproved schema registration and candidate-only collection, not a
form approval, reviewed draft, field-review workflow or submission endpoint.
Every request requires authentication and current registered staff rights:
the intersection of existing Finance-view, resident-record-view and
reason-view permissions. Normally only the Programme Manager has all three.
Schema metadata never grants permission. Other roles cannot read retained
raw values or source/locator metadata through these endpoints.

| Method and path | Contract |
| --- | --- |
| `POST /api/form-schemas` | Register the next immutable schema version, 201; always `Unapproved` |
| `GET /api/form-schemas` | `{"schemas":[...]}` with definition, digest, actor/time and null approval evidence |
| `POST /api/cases/{case_id}/form-candidates` | Append one source-bound batch, 201; returns staged candidates or owned manual recovery |
| `GET /api/cases/{case_id}/form-candidates` | `{"batches":[...]}`; current-rights and source-presence/clean-scan check on every read |

Schema requests contain exactly `id`, `version`, `form_type`, `template`,
`reviewer`, `funding`, `rule_refs` and `fields`. Version is a positive sequential
integer starting at one per schema ID. Form type is `technical`,
`work-package`, `invoice` or `funding`. `template`, calculation and rule
references contain `id`, string `version` and `evidence_ref`.
The reviewer is an existing staff email, not an inferred approval.

`funding` contains `status`, `scheme_id`, `route`, `evidence_ref`.
`Unknown` and `Not applicable` require null references; funding forms cannot
be not applicable. `Evidenced` requires a scheme ID, supplied evidence
reference and route `competitive`, `allocation`, `award-return` or `claim`.
This records supplied metadata only, not actual approved scheme authority.

Each field contains exactly `id`, `section_id`, `type`, `unit`, `options`,
`required`, `required_when`, `source_authority`, `evidence_required`,
`calculation_ref`, `category`. Types and units are described in the
[core guide](../core/README.md#form-schema-registry-and-candidate-staging-97).
Options are nonempty unique finite scalars for enum fields only. Conditions
are `{field_id, equals}` references to another declared field, never executable
expressions. Source policies are `{kind, rank, evidence_ref}` with unique
existing document kinds/positive precedence ranks; evidence requirements are
nonempty text references. `category` is `value` or a human-only
`declaration`, `signature`, `attestation`, `consent` or `approval`.
Only `value` fields can receive candidates. Bounds are 200 fields/candidates
per request and 16,000 characters per raw value.

For an already registered unapproved `SYN-TECH` version one and an actual
uploaded text document containing `EPC D`, the staging request shape is:

```json
{
  "schema_id": "SYN-TECH",
  "schema_version": 1,
  "document_id": "actual-upload-id",
  "processing": {
    "kind": "text",
    "parser": "synthetic-importer",
    "parser_version": "test-1",
    "model_version": null,
    "route_evidence": null,
    "error_record": null
  },
  "candidates": [
    {"field_id": "epc", "raw_value": "D", "locator": {"start": 4, "end": 5}}
  ]
}
```

This example is not an approved template. Hash/version/date are copied from
the actual uploaded source, not accepted from the request. Text spans and
CSV cells are verified against exact source bytes; parser/model identity is
separately labelled `Supplied, unverified`. OCR imports use `kind: "ocr"`,
`{page, region}` locator, and supplied `route_evidence`/`error_record`; they
retain asserted lineage with `Unverified OCR import`, never claim pixel
verification or approve/run an OCR route. Unsupported/unreadable sources
record manual recovery with no invented candidates.

Malformed/forged keys and source mismatch return 400, denied identity/rights,
human-only fields or source-policy mismatch 403, missing/foreign case or
source 404, concurrency conflict 409, source-store outage 502 and unexpected
storage failure 503 with a metadata-only diagnostic. Reload after an uncertain
failure before retrying. Unknown funding routes and all unapproved versions
remain unusable for approved preparation; candidates never become accepted
fields or change source, consent, grants, payment or submission state.

The fixture exercise starts a responsive ephemeral loopback HTTP app over
temporary synthetic SQLite, authenticates fixture staff, registers/stages/reads,
checks forbidden paths and never calls inference:

```bash
PYTHONPATH="$PWD/src/api:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python -m unittest discover -s src/api/tests -p test_form_staging_api.py -v
```

Run from the repository root with editable src packages installed. No UI
change, actual human approval, live AI/Azure/SQL Server, approved template
binding or #98 review/validation/pack/staleness acceptance is claimed.

## Controlled bulk preview API (#78)

Two additive authenticated POST routes expose the
[core administrative contract](../core/README.md#controlled-administrative-bulk-edits-78).
No web assets, role screen or existing case action changes. Trusted-proxy
requests still need the existing `X-ZF-CSRF: 1` header. Contractors and unknown
roles are denied; a role-visible screen cannot grant editing authority.

`POST /api/bulk-edits/preview` accepts exactly:

```json
{
  "case_ids": ["ZF-1", "ZF-2"],
  "changes": {
    "case_reason": "to check the supplied administrative reference"
  },
  "source": "SYN-REGISTER",
  "source_version": "v3",
  "reason": "Correct the constructed case explanation"
}
```

Select 1-100 distinct IDs. Allowed fields are `case_reason`,
`handoff_due_at` and `handoff_next_action`; handoff fields require an existing
active handoff. No null/empty values, inferred source/version, silent
truncation, extra keys, role/actor override or arbitrary nested JSON is accepted.
This route is also the preview path for a single permitted administrative edit.
It does not replace existing evidence, ownership or controlled workflows.

The 200 response contains `preview_id`, `status`, actor, source/version/reason
and ordered `records`. Each record has `case_id`, `changes` with field
`old`/`new`, `failures` and an outcome. Examples of a successful preview record:

```json
{
  "case_id": "ZF-1",
  "changes": {
    "case_reason": {
      "old": "to agree a visit",
      "new": "to check the supplied administrative reference"
    }
  },
  "failures": [],
  "outcome": "would_apply"
}
```

| Situation | Preview / apply behavior |
| --- | --- |
| All targets valid | `pending`, per-case `would_apply` or `no_change`; no case mutation |
| Any missing/noneditable/invalid target | `blocked`, failures for that ID, no inaccessible values; valid changed peers `batch_blocked` |
| All unchanged | `pending`, all `no_change`; apply records a batch result but no fabricated field history |
| Unknown keys/controlled fields/malformed request | 400 with explicit error and metadata-only refusal audit |
| Foreign creator or current authority/OID revoked | 403, no target content or edits |
| Stale, corrupted, blocked or consumed preview | 409, fresh preview required; no partial batch |
| Unexpected storage failure | 503 with explicitly uncertain outcome; inspect case history and request a fresh preview before retry |

After inspecting every record, `POST /api/bulk-edits/apply` accepts only:

```json
{"preview_id": "the-server-returned-preview-id"}
```

No new target/change is accepted at apply. Only the same current creator can
apply it, and all permission/freshness checks repeat under the SQL writer lock.
Success returns `status: applied` with each result `applied` or `no_change`.
The retained source/version/actor/time/reason and old/new fields are visible
in existing case detail `edit_history`, with normal note-visibility redaction.
Batch result and history survive SQLite reopening. Replaying a consumed
preview is denied, including after an uncertain commit acknowledgement.
Immutable issued outcomes, empty failures, exact ordered target/record coverage
and complete snapshots are required both before staging and at SQL commit.
Mutable status alone cannot enable blocked records; cached and persisted
status-only resets are refused with no case/history/success-audit changes.
No-op targets are also permission/freshness checked inside the transaction.

Technical, consent, safety, procurement, budget, invoice, payment, claim,
quality, defect/complaint closure and contractor-instruction fields are absent
from the allowlist and are rejected server-side, including mixed allowed plus
forbidden requests. Ownership transfer still requires receiver acceptance.
Resident-update commitments, independent hazard clocks and approvals are never
changed by an administrative due-date or next-action edit.

| Issue #78 criterion | Bounded evidence |
| --- | --- |
| Edits retain source/version/actor/time/reason | `test_exact_preview_before_apply_and_provenance_reopens`, exact history/audit equality and monotonic version tests |
| Targets, changes, failures, per-case outcomes before apply | Core and real loopback HTTP exact-shape tests, mixed missing/foreign/valid and no-op targets; zero pre-apply mutation |
| No controlled bulk approvals | Closed allowlist tests across all controlled categories, actual HTTP denials, creator/role/OID and transactional stale/guardrail races |

Correction TWO implements the earlier RV-002 evidence-upload and handoff
caller/API/UI gap using required explicit inputs and complete immutable
per-change events, not fabricated defaults or wider bulk fields; see the
[single-record core contract](../core/README.md#single-record-upload-and-handoff-change-sources-correction-two).
Original Review and review512a59c4 Revise remain historical evidence;
coordinator independent reassessment of the final head is required.
FR-005/006/007 here use PRD numbering;
the same-number BRD entries concern lifecycle and technical release. This is
not full PRD, human usability, WCAG, live SQL Server or operational acceptance.
The bulk UI is unchanged. The directly dependent upload/offer/accept forms
were changed and exercised in local Chromium as described below; no general
UI/WCAG or user-acceptance claim is implied.

### Upload and handoff explicit change metadata (correction TWO)

`POST /api/cases/{id}/upload` now requires `source`, `source_version`, `reason`
in addition to existing `name`, `kind` and base64 `data`. For example:

```json
{
  "name": "survey.txt",
  "kind": "Survey",
  "data": "U3ludGhldGljIGV2aWRlbmNl",
  "source": "SYN supplied survey register",
  "source_version": "register revision 7",
  "reason": "Add the supplied survey evidence"
}
```

`offer-handoff`, legacy `handover`, and `accept-handoff` require the same
three source strings plus `handoff_version`, the current number of
`handoff_history` events in case detail (zero if absent). Acceptance example:

```json
{
  "source": "SYN handoff request register",
  "source_version": "request revision 2",
  "reason": "Take responsibility for the documented next action",
  "handoff_version": 1
}
```

Use the actual current history count, not the example value. Source/version/
reason must be nonblank strings at most 200/100/300 characters. Missing old
payload metadata now returns 400 with the field and fix; stale handoff returns
409/reload; wrong recipient or revoked actor returns 403. Requests cannot
override server actor/time/change-version/old-new fields. These inputs assert
what the person checked, not source authority or an approval. The file hash
and server change version never substitute for supplied source version.

Upload returns ordinary case detail with document source fields and
`document_history`. Offer/accept return enriched `handoff_history`. Each
complete event binds exact old/new references/ownership and registered
actor/UTC time/version and is identically retained in append-only audit,
transactionally with case changes in SQL. No accepted field, finance/safety/
consent/quality approval, contractor instruction or bulk owner change is added.
Older history is not rewritten; absent metadata displays Unknown (legacy).
Roles without note visibility do not gain source/reason/change access.

Existing native/Fluent-token upload/offer/accept UI now collects these fields,
supports Enter submission and browser required-field validation, retains input
on errors with a focusable polite inline message, and disables only during a
save. Named recipient must still accept. Do not retry blindly after a storage
failure: reload history to check an uncertain commit first.

Local synthetic browser reproduction, using the already-installed Playwright:

```bash
PYTHONPATH=src/api:src/core/tests:src/agents/tests \
  .venv/bin/python src/api/checks/provenance_browser_check.py
```

The check creates responsive loopback HTTP and temporary SQLite fixtures,
blocks external requests, exercises missing-field focus and keyboard upload/
offer/accept, stale inline refusal/input retention, recipient ownership,
390px reflow/reduced motion and event/audit equality after reopen. No private
stock, inference, live platform, actual template authority or WCAG/screen-reader
conformance is claimed.

## Regulatory evaluation and card cadence labels (#216)

`GET /api/law/cards` and `GET /api/law/cards/{card_id}` add a read-only
`source_freshness` object to every returned card/version. It includes
`status` (`in_cadence`, `out_of_cadence`, `unknown`), plain-language `label`,
`as_of` and per-source monitoring evidence. The same object accompanies
bounded regulatory chat cards; the panel renders the card link, text label
and historical as-of date without a colour-only signal. Older stored turns
without the field explicitly show unknown cadence.

Retained versions in storage do not acquire this read-only field. The lifecycle
HTTP regression compares the complete decorated history before/after reopening
and every retained storage field after removing only the additive decoration.
A loaded law store with no sources returns draft cards with unknown cadence
and role-visible unknown checks, without publishing alerts. An unavailable law
store instead returns 503/unknown for check/alert requests. Post-commit safety
intake logs the unavailable-store exception and returns
`rule_checks.status: unknown` with the human safety route; saved work is not rolled back. That
diagnostic is not an uncaught test error or evidence that a rule passed.

Cadence is measured from a successful configured source-monitor observation,
not a retrieval timestamp or inferred legal commencement. Missing evidence is
unknown; known overdue evidence remains labelled even if another source is
unknown. An overdue label does not approve, retire or disable a rule, resolve
a source conflict or suppress an independent hazard alert. Cards retain all
existing source/version/approval gates. This is not a live-currentness claim.

The [per-check evaluation audit](../agents/README.md#regulatory-evaluation-gates-216)
records exact citation/refusal development grading, critical hazard omissions,
a generated stateless 60,000-home baseline, and explicit human/continuing-stock
gaps. There is no overall pass. With no measured staff comparison, the report
recommends cards-only shipment. Existing chat remains disabled by default and
available only under its explicit synthetic-development admission; this change
does not approve operational chat or activate a release.

Local validation starts a responsive loopback app on an ephemeral port using
temporary synthetic SQLite data, checks health, authenticates fixture staff,
reads collection/history labels and a cited turn, and proves retained alerts
unchanged. Outbound inference is forbidden by the harness:

```bash
PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python3 -m unittest test_regulatory_chat_api test_rule_alerts -q
```

Human comprehension/accessibility, actual staff classifications and
acknowledgements, live Azure SQL and continuing-stock acceptance are not
established by these checks. No Azure changes or private data are required.

## Home-specific cited chat, offline synthetic slice (#214)

The existing home/case chat panel contains an optional cited regulatory lookup.
It is hidden unless the [core synthetic admission contract](../core/README.md#synthetic-home-specific-cited-chat-214)
passes. It supports hazard and automated-decision source lookup, restores owned
historical turns, shows provision/fact IDs with status and dates, and exposes a
one-action doubt button. Excerpts remain quotes, never an assessment that law
applies or a duty is satisfied. No model is called, even if ordinary Foundry
credentials are configured. The API retrieves; the agents library renders a
fixed five-part answer. No sixth assistant or live AI task is activated.

| Method and path | Contract |
| --- | --- |
| `GET /api/chat/regulatory/status` | Synthetic admission, warning, own-role retention review and bounded audit-only usage; 403 when disabled or unauthorized |
| `GET /api/chat/regulatory/usage` | Metadata-only current-user/current-role/UTC-day recorded outcomes; same synthetic/privacy/capability guards, no message reads |
| `POST /api/chat/regulatory/threads` | `{"case_id":"ZF-1"}`; owned thread bound to that home/case |
| `GET /api/chat/regulatory/threads/{id}` | Owner-only historical messages, source snapshots and current role/case checks |
| `POST /api/chat/regulatory/threads/{id}/ask` | `{"content":"What do the hazard sources say for this home?"}`; exact answer/refusal, zero-call usage, or conflicting sources with atomic `escalation` receipt |
| `POST /api/chat/regulatory/threads/{id}/doubt` | `{"turn":2}`; atomically copy that stored question/answer pair into the named exercise owner's isolated inbox |
| `GET /api/chat/regulatory/inbox` | Juan Manuel Servera's provisioned exercise principal only; no access to senders' threads or memory |

No client owner, role, facts, model, source version or date overrides are
accepted. Generic chat ask/messages/proposals cannot bypass this bounded path.
Generic history uses the same regulatory guard. Missing/ambiguous named owner
or an invalid pair returns 400; role/field refusal 403; foreign/missing thread
or case 404; a concurrent/archive conflict 409. Unexpected failures log an
explicit 503 and warn that a turn/receipt may already be durable; reload before
retrying. A successful doubt response means a local exercise inbox copy, not
email delivery, actual human review or legal approval. The named recipient
must already be uniquely provisioned in the synthetic staff register; the
application does not create an account or invent an operational delegation.

The panel offers the named owner's inbox and current case's copied turns.
Copies remain separately owned/deletable under existing chat storage; sender
deletion does not retract a copy already explicitly sent. Operational retention,
rights handling and actual staff use remain unapproved. Ordinary case workflow,
human safety routes, deterministic cards and rule-engine alerts stay independent.

### Acceptance audit (2026-10-16)

Issue checkboxes are deliberately untouched; the coordinator owns merge-time
updates. "Pass" below means observed bounded offline engineering evidence,
not full ADR 0005 adoption or operational acceptance.

| #214 criterion | Offline result and evidence | Remaining unmet boundary |
| --- | --- | --- |
| Every statement cites a provision/fact with status/dates; unsupported dropped | Pass for exact excerpt/fact fragments: `test_every_fragment_is_exact_and_cited`, snapshot/hash and size tests. Unsupported questions return no factual fragments | No generated-prose claim validation or actual-model evaluation; unknown effective dates stay null |
| Role-scoped categories and question minimisation | Pass: core minimisation tests, API revocation and foreign-thread denial; fresh SQL staff read. No health/contact/free-text/memory retrieval | Purpose coverage limited to two source lookups; actual company field/purpose ratification unmet |
| No legal conclusions/advice, future law active or inferred terms | Pass for closed output surface and frozen refusal cases; source-gate and interpretation tests | Partial for arbitrary legal-intent recognition: lexical classifier is not general semantic understanding. Live legal/source approval unmet |
| Conflicting sources both shown and escalated | Partial: changed approved versions and disagreeing same-purpose cards show both, no winner, `requires_human`; explicit doubt route works | Arbitrary semantic contradictions cannot be detected. Actual human resolution not performed; no automatic private-content sharing |
| One-action doubt to named owner | Pass locally: atomic selected-pair copy, idempotent receipt, missing owner denial, role recheck, rollback/reopen and owner-only HTTP inbox tests | No live notification or human acknowledgement; actual delegation/provisioning unmet |
| Retrieved text is data, with injection tests | Pass structurally: malicious source text is an inert quote; zero provider/tool calls, safe DOM and no controlled writes | No actual-model injection test or general model-safety claim |
| Model-negative never suppresses rule-engine alert | Pass for offline negative/unavailable-answer dataflow: retained alerts and safety hold equality in `test_card_conflict_and_no_rule_alert_suppression` | No actual model-negative provider run; this path has no model or rule write capability |
| Turns stored with sources | Pass in JSON/SQLite: full versioned envelope, evidence IDs, immutable historical snapshots, restart and isolated handoff tests | Azure SQL execution, approved retention/privacy and continuing-stock acceptance not run |

The [frozen evaluation](../agents/evals/regulatory_chat_results.json) records
3/3 exact cited answers and 10/10 expected refusals. The test comparator uses
the same deterministic cards with actual provision links: six joined permitted
home facts across three answers versus none in cards alone, with three
structural card/provision/home lookups versus one joined request. This is
bounded offline lookup value only, not measured staff effort or AI superiority.
Real inference, held-out evaluation, staff comprehension, live approval,
60,000-home stock and Azure acceptance remain unmet and are not disguised by
passing local tests.

Install the editable core/agents/API packages and declared development tools
with pip. From the repository root:

```bash
PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python3 -m unittest test_regulatory_chat_api test_regulatory_chat \
  test_regulatory_answers -q
```

The HTTP harness starts a loopback application on an ephemeral port over only
temporary synthetic SQL data, checks health/case responsiveness, exercises the
actual cited routes, historical reads and explicit owner handoff, forbids
outbound inference, then stops the server. Browser interaction and human
accessibility/comprehension are not established by HTTP/static DOM tests.

## Regulatory security, privacy and audit (#217)

On trusted-proxy ingress, all regulatory endpoints require the separate
`ZavaForward.RegulatoryChat` capability in addition to a permitted staff role.
RuleAuthor and RuleOwner do not imply chat access. Capabilities require a unique
provisioned principal binding; email fallback cannot grant them. Generic history,
archive and delete routes enforce the same capability for regulatory threads;
thread lists omit them when it is absent. Existing owner/role/home isolation
remains. The claim-derived staff role cannot regain hazard facts from a wider
register role. Local password mode remains a synthetic development convenience,
not evidence of Entra authentication or operational segregation.

The regulatory panel displays the existing special-category/free-text warning
and unknown or simulated retention. Status returns `privacy` with draft DPIA
state, `dpo_reviewed=false`, `deletion_enabled=false`, own-role regulatory thread
IDs/counts and unknown per-class law/card/check/alert/audit periods. Simulated
CHAT_RETENTION settings list review-due ages only; they are not a purge or an
approved schedule. Both archived sender threads and separately owned referral
copies require DPO retention/rights/hold alignment.

| #217 acceptance criterion | Evidence and honest disposition |
| --- | --- |
| DPIA with DPO completed before live data use | Unmet. [Draft for Juan Manuel Servera's DPO review](../../docs/reference/research/chat-memory-dpia.md#regulatory-assistant-dpia-draft-for-dpo-review-2026-10-16-refs-217), no completed consultation/sign-off or live-data permission |
| Chat/check retention with DPO-set periods | Unmet. Existing chat settings reused for metadata-only simulated review; all real periods, check/alert disposal, holds, backups and immutable history alignment require DPO review |
| Minimum Foundry fields and special-category purpose controls | Partial. Existing offline retrieval excludes health, contact, narrative, memory and unrelated home fields; role/purpose tests pass and no provider is called. No regulatory Foundry query or actual-provider privacy evidence exists |
| Separate Entra author, approver and chat roles | Partial. Distinct capability mapping, registration/script parity, no-self-approval and HTTP denials pass locally. Actual tenant assignments, ingress and revocation not tested or applied |
| Rule changes, approvals, checks, alerts and turns audit-logged | Locally demonstrated with append-only rule/check/alert events and transactional SQL turn/referral metadata audit; failure rollback, restart, idempotency and chain checks pass. Azure SQL/ledger archive evidence not collected; JSON separate-file atomicity remains unsupported |
| Prompt-injection and cross-role disclosure tests pass | Met for this offline synthetic slice: injected question/source containment, no controlled writes, no health-canary disclosure, current claim role versus register, capability denial on direct/generic routes, foreign threads and role-change denial. No actual-model adversarial or production assurance |
| Art 22A to 22C proposal/flag-only, named human and reasons | Partial. No chat decision-write path; version-2 significant-decision check requires explicit reasons beyond an evidence ID. Actual human authority/reasons/contestability and legal assessment remain unverified; no statutory compliance claim |

Issue checkboxes remain unchanged for the merge coordinator. ADR 0005 acceptance
permits synthetic development only. This slice uses no actual staff/resident
data, Azure changes or model calls and claims no operational approval.

With installed projects and tools, run from the repository root:

```bash
PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests" \
  python3 -m unittest test_regulatory_chat_api test_auth test_rule_alerts \
  test_regulatory_chat test_regulatory_privacy test_rule_engine test_rulecards \
  test_chat_privacy test_chatthreads test_regulatory_answers -q
PYTHONPATH="$PWD/infra/tests" python3 -m unittest test_identity_rbac -q
```
No Azure resources or private data are required or accessed.

## Rule-card approval API (#211)

The existing law store now exposes exercise rule cards, without an AI call or
approval tool for agents. Configure the existing `ZF_LAW_DB`/`ZF_LAW_BLOBS` local
test doubles or `ZF_LAW_STORE=mssql` deployment backend. Startup retains two
labelled, unassigned draft seed cards. Creating a later assigned-email version
does not approve it or change the seed's retained history.

| Method and path | Contract |
| --- | --- |
| `GET /api/law/cards` | Latest version of each card, with exercise label and approval history |
| `GET /api/law/cards/{card_id}` | Every version and event, plus currently eligible active version |
| `GET /api/law/cards/reviews` | Source-change review records; no automatic interpretation |
| `POST /api/law/cards` | New immutable exercise draft; authenticated rule author required |
| `POST /api/law/cards/{card_id}/{version}/approve` | Named owner, distinct from the version's author |
| `POST /api/law/cards/{card_id}/{version}/activate` | Named owner; version must be approved |
| `POST /api/law/cards/{card_id}/{version}/hold` | Named owner; active card and nonempty `note` required |
| `POST /api/law/cards/{card_id}/{version}/release` | Named owner; held card only |
| `POST /api/law/cards/{card_id}/{version}/retire` | Named owner; approved, active or held card only |

Draft body (synthetic example, replace the owner with a provisioned staff email):

```json
{
  "card_id": "synthetic-example",
  "title": "Exercise human review",
  "trigger": "Synthetic proposed resident decision",
  "applicability": "Synthetic exercise only",
  "provisions": ["Illustrative citation, requires owner verification"],
  "clock": "No operational duration approved",
  "safe_default": "Route to the human review queue",
  "escalation_role": "Named exercise owner",
  "approver": "owner@example.test",
  "effective": "2026-10-16",
  "retirement": null
}
```

Other POST bodies are `{}`, except hold: `{"note":"Exercise source doubt"}`.
Actor, author, role, event date and exercise status are server-derived; attempts
to supply those fields are rejected. Dates must be canonical ISO dates, with
retirement after effective date. Domain/state denials return 409, malformed HTTP
fields 400, insufficient capability 403, absent authentication 401 and an
unconfigured law store 503. Unknown card history/routes return 404.

All reads require an existing staff law-view role; contractors/unknown roles are
denied. All writes additionally require the trusted-proxy provider and dedicated
Entra claims `ZavaForward.RuleAuthor` or `ZavaForward.RuleOwner`, respectively.
These reserved capabilities cannot supply a workbench role themselves, even
through `ZF_ROLE_MAP`. They are derived only after one unique tenant/object-ID
match to provisioned staff. Email fallback still permits existing workbench
login but never rule authority. Password sessions and staff-file `rule_roles`
cannot grant write authority. Existing `X-ZF-CSRF: 1` protection applies.
The canonical provisioned email is retained, not a claimed email or display name.
Having both capabilities never permits self-approval.

These are code-level contracts, not tenant role assignments or legal delegation.
The ingress must validate principals and prevent direct access; local synthetic
principal tests do not verify signatures or hosted ingress. Legal/Compliance/DPO
owner nomination in #209 is not approval of any card. Approval events remain
explicitly simulated, and non-exercise cards remain refused. Legacy display-name
events are preserved verbatim and do not confer new email-bound authority.
A rule-card UI, real card/legal approvals, real tenant assignments and SQL
Server/Azure acceptance are not delivered by this slice. The bounded exercise
engine integration in #212 is described below; it supplies no missing approval.
The current infrastructure registration script/manifest defines only workbench
roles; adding and assigning the two dedicated rule capabilities is still an
explicit administrator deployment follow-up, not an implicit role grant.

The local app exercise in `tests/test_auth.py:RuleHttpTests` starts a loopback
HTTP server over temporary synthetic data, checks health and app responses,
executes the lifecycle and deny matrix, reopens persistence, then stops the
server and removes its temporary files. Run it from `src/api`:

```bash
PYTHONPATH="$PWD/src:$PWD/tests:$PWD/../core/src:$PWD/../core/tests:$PWD/../agents/src:$PWD/../agents/tests" \
  python3 -m unittest tests.test_auth.RuleHttpTests -q
```

## Deterministic step-alert API (#212)

The API composes the [bounded core engine](../core/README.md#deterministic-checks-and-alerts-212)
over the existing SQL case store and law SQL adapter. JSON-only case stores
cannot execute checks. There are no new approvals in delivered data: seeds stay
unapproved exercise drafts, and prose-only cards cannot execute a guessed clock.
An author may add the optional `check` contract documented in core when
proposing a new version; the existing human approval lifecycle still applies.

| Method and path | Contract |
| --- | --- |
| `GET /api/law/alerts?case={case_id}` | Role-scoped open alerts, grouped per home, ordered by due time and harm; omit `case` for the role's cross-home view. Includes owner-classified false-positive counts/rate and unclassified denominator. |
| `POST /api/law/checks/{case_id}` | Empty object only. Recheck persisted SQL facts with a server-derived data trigger; return only checks in the caller's alert audience. No supplied facts, clock, awareness date, owner or suppression. |
| `POST /api/law/alerts/{alert_id}/acknowledge` | Exact named owner and trusted rule-owner capability; body `{"note":"Human acknowledgement evidence"}`. |
| `POST /api/law/alerts/{alert_id}/outcome` | Same authority, with human action/outcome evidence in `note`; breach risk must already be acknowledged. |
| `POST /api/law/alerts/{alert_id}/false_positive` | Same authority; retained classification evidence only, never suppression or risk resolution. |
| `POST /api/law/alerts/{alert_id}/confirmed` | Same authority; alternative retained classification. |

Hazard audiences are Building Safety Liaison, Resident Liaison Officer and
Retrofit Programme Manager. Decision-safeguard audiences are Retrofit
Coordinator and Retrofit Programme Manager. The exact named owner may also
read their alerts, subject to an authenticated supported staff role.
Contractors and unknown roles cannot access either checks or alerts.
Existing case authorization is rechecked for case-specific routes; all
currently supported staff have case-read scope. Field-need projection also
withholds disposition notes from roles without that need. No raw hazard notes,
resident details or proposal text are included in check evidence pointers.
Guessed alert IDs or unrelated owners are denied. Password sessions cannot
acknowledge, close or classify alerts. All authority and disposition timestamps
are server-derived; attempted overrides are rejected.

Successful ordinary case mutations trigger a check after commit, using
`step_transition` if the journey stage changed and `data_change` otherwise.
Package/work-order, import and early-return AI/document routes are covered on
the next scheduled SQL sweep, not synchronously by those endpoints. The core
CLI is the bounded schedule entry point; no hosted timer is configured here.
Data-trigger retries retain the original checkpoint time; a fresh scheduled
minute is required to advance an unchanged clock.

Alerts contain the safe action, named decision owner, clock/due time if
applicable, exact citation/status, original evaluation time, current-control
availability, and latest check result/time. This is not an independently
refreshed compliance certificate. Advisory alerts disappear when a newer check
is clear or the control is inactive. An unresolved breach stays visible and
requires its owner outcome even if later checks change. No disposition releases
a safety hold or sends a resident message.

Unconfigured or failed engines return 503/unknown on alert service requests.
For committed case work, `rule_checks.status: unknown` and the manual safety
route are included in the successful case response, and the failure is logged;
no successful or fresh persisted check is invented. Emergency reporting,
referral, receipt, acceptance and independent human hazard work do not depend
on engine availability. Continue the existing human emergency/hazard service,
never wait for an alert, AI or a legal interpretation.

Local core/API tests establish these bounded contracts, not live-platform
acceptance. Alerts are API/step metadata only: no workbench alert UI, production
timer, source/card legal approval, tenant capability assignment, staff
comprehension/precision trial or continuing-stock Azure/SQL Server acceptance
is delivered. The decision-safeguard evidence contract has no general-purpose
writer in this slice; absent evidence remains unknown. Refs #212 remains open.

## Stock reconciliation API (#84)

`POST /api/cases/{id}/stock-reconciliation` records an unresolved staff query:

```json
{
  "field": "epc",
  "query_owner": "sam@example.test",
  "left": {
    "value": "D",
    "source_id": "SYN-REGISTER-84",
    "date": "2026-01-01",
    "version": "1",
    "validation_state": "Unvalidated"
  },
  "right": {
    "value": "E",
    "source_id": "SYN-SURVEY-84",
    "date": "2026-02-01",
    "version": "2",
    "validation_state": "Disputed"
  }
}
```

The example is constructed, not a real home. Allowed fields are `epc`, `type`
and `built`; the owner must be registered non-contractor staff. Each assertion
needs exactly the shown fields; validation is `Unvalidated`, `Validated`,
`Disputed` or `Unknown`. Dates cannot be future; EPC is A-G, build year an
integer and home type bounded text. Equal values and identical source/version
pairs are rejected. The authenticated session supplies recorder identity.
Invalid inputs return 400, unauthenticated requests 401, denied roles/bulk
requests 403. The response is the projected case detail; contractors receive
neither comparisons nor technical decisions.

Opening additionally requires the registered case owner or programme/manager
role. Staff role membership alone does not grant responsibility for every case.

`POST /api/cases/{id}/stock-query-event` appends a disposition:

```json
{
  "query_id": "SQ-1",
  "action": "withdraw",
  "reason": "Duplicate of another recorded query"
}
```

The original raiser or a programme/manager role may withdraw. For a human
reconciliation attestation use `"action": "resolve"` and add a nonempty
`"evidence": "SYN-HUMAN-REVIEW-84"` reference. Resolution is restricted to
registered named humans with the existing Retrofit Programme Manager or
Programme Support Officer role. The server binds identity from the session,
not the body; agents cannot resolve or sign off. Every disposition needs a
reason, refers to a query on this case and is terminal. Invalid/repeated
dispositions return 400; unauthorized requests return 403.

The response derives each query's current `Unresolved`, `Withdrawn` or
`Reconciled` status and retains the separate `stock_reconciliation_events`
history (event ID, query ID, status, action, reason, optional evidence,
timestamp and recorder identity). The original comparison remains unchanged
in storage. The read-only panel shows the status and human event provenance.
Only unresolved queries block technical approval; disposition never releases
other stock, safety, building or independent approval gates. No source or
home field is automatically selected/updated. Source-authority, resolution
rules and eligibility stay Unknown/owner-approval-needed, not an approved
operational reconciliation policy.

Stock and technical writes also recheck the current SQL staff identity/role/OID,
even for an existing authenticated session whose cached staff record is stale.
Changed or removed identities receive 403; their old session cannot retain
approval authority. The writer transaction revalidates before commit. A known
precommit SQL failure leaves neither a new case version nor its success audit;
the original error propagates, with recovery uncertainty explicitly reported.
No new endpoint, role grant or sign-off competence attestation is introduced.
Original Review, 2026-10-17: **Not accepted**, RV-001. Authorized correction ONE
clears failed pending work before recovery reads and restores known cache
snapshots; early/persistent read failures now preserve the original error and
cannot flush the failed success event on exit or a later save. A failed reload
logs uncertainty and forces retry on the next operation, not a success fallback.
Bounded independent verification closes RV-001 for this correction after 91
focused tests and two snapshot probes; the original adverse Review is retained.

The case view displays both values, source metadata and query owner, with
authority/resolution/eligibility explicitly `Unknown`. A different case shows
its own comparisons, never a carried-over rationale. Existing technical forms
record named human decisions, not AI approval; separate sign-offs show the
design version each person reviewed. Conflict, building and hazard holds reuse
the [core controls](../core/README.md#stock-comparisons-and-human-technical-sign-offs-84).
No stock source wins automatically, no resident decision is inferred and no
case is silently excluded or automatically reprioritised.

Support status and input coverage are explicit in staff detail/list. Missing
flags are `Unknown`, not `"None"`; compatibility Boolean notice indicators
still represent observed support only. Existing governed AI proposal paths
remain available, with release admission and human approval unchanged.

Local synthetic HTTP tests run from `src/api`:

```bash
PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_stock_reconciliation_api.py' -v
ZF_STOCK_BROWSER=1 PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_stock_reconciliation_api.py' -v
```

The second command requires the existing development Playwright dependency
and Chromium. It runs the real loopback application with synthetic SQL state,
checks rendered values, source metadata, owner, Unknown labels, heading/keyboard
access and navigation to another case. The default unit suite skips that
opt-in browser method. This is engineering evidence, not direct human
accessibility/competence acceptance, live inference, SQL Server or Azure proof.

The selected changed-path local SQL Server parity suite is separate from
browser evidence. In a throwaway local SQL Server database only, using the
existing `ZF_TEST_MSSQL=1` and localhost `ZF_SQL_*` settings:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_mssqlstore.MssqlStockDecisions -v
```

Initially eight tests passed on 2026-10-17; correction ONE passed ten, reusing canonical constructed core cases for
comparison/disposition and four sign-off success, current actor denial,
second-connection authority change, transactional case/audit failures,
reopen/no delayed audit and context cleanup. Added early/persistent actual
recovery-read failures exercise technical/comparison/terminal paths, original
error, empty pending state, released locks, failed retry and later recovery.
Transactional refusal errors retain their original identity on reload failure.
This is local SQL Server adapter
evidence, not Azure/Entra acceptance or approved professional/source authority.
Source-authority/resolution/eligibility rules, operational delegation and
real-platform acceptance remain unmet; nomination/tenure routing is separate.

A working case-management application for the Zava Forward retrofit programme.
It follows the simplicity requirements SA-001 to SA-010 in the
[PRD](../../docs/prds/zava-forward-retrofit-programme-demonstrator.md) and the
[prototype learnings review](../../docs/reference/research/ux/prototype-learnings-and-simplicity-review.md).

This file is the former `mvp/README.md` (ADR 0006, issue #199, M6), split by owning project. It keeps
the staff-facing behaviour, configuration, sign-in, local run, honest limits and container checks of
the `api` project. Domain modules are documented in [core](../core/README.md) (law store, rule cards,
SQL stores, governance, ledger, chat storage, continuity and synthetic tools), the ledger digest job in
[orchestrator](../orchestrator/README.md), and the assistants, AI evaluation harness and dated
assistant validation record in [agents](../agents/README.md). The index of projects is
[src/README.md](../README.md).

Paths such as `tests/test_x.py` and `web/` below are relative to `src/api/` unless a `src/` path is
given. Module names without a path (`store`, `ranking`, `projection`, `quality`, `procurement`,
`finance`, `documents` and so on) are `zava_forward.core.<module>` in `src/core/src/zava_forward/core/`.
Run the suites from `src/api` with
`PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests`, after
`pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`. When `ZF_DATA` is not
set, the data file defaults to `~/.zava-forward/data/zavaforward.json`, outside
the checkout. `ZF_DATA` accepts an explicit JSON file or a data directory;
an explicit filename is preserved. Runtime and generator resolve the same folder.

## Resident decisions and representative API (#86)

The resident panel records only supplied human decisions. Answer and answered-by
selectors start blank; the displayed default is `Not recorded`. The historical
case-wide answer is labelled as history, with no consent editor; its legacy
`decision` endpoint remains role-checked history only and cannot release work.
First record a technical design, then the exact measure scope and source.
The [core contract](../core/README.md#resident-decisions-and-representatives-86)
defines currentness, authority, release dependencies and evidence limits.

Authenticated resident-workflow staff use `POST /api/cases/{id}/resident`:

For decision/scope/authority/safe-contact recording and disclosure checks,
only registered named Liaison Officers (Neighbourhood/Resident Engagement) and
Retrofit Coordinators may write. Managers and Programme Support view only;
their attempts, including the legacy `decision` route, return 403. Existing
complaint/redress actions retain separate named-owner restrictions. The panel
uses server-projected `can_record_resident`, rather than treating every manager
as a resident recorder. Other staff do not receive private evidence narratives.
Contractor detail contains `resident_readiness: [{"measure": "...", "flag":
"Proceed"}]` (or `Hold`), never decision reasons, wishes, authority or safe routes.
Unrelated vulnerability restrictions remain unchanged for staff.

Staff detail includes `resident_retention`: five calendar years from first
recorded resident contact, including withdrawal and expired authority. Unknown
first-contact history is explicit. `GET /api/retention` includes due
`doc_id: "resident-decisions"` entries for manager review. A manager posts
`{"id": "resident-decisions"}` to `/api/cases/{id}/retention-approve` to remove
the current resident payload; legal hold returns 403, not-yet-due or unknown
origin returns 400. At expiry, work and representative disclosure reliance hold
even before deletion. See the [core retention contract](../core/README.md#resident-decisions-and-representatives-86)
for the exact deletion inventory and ledger/backups/cross-case limitations.

| `action` | Required input and control |
| --- | --- |
| `scope_record` | `measure`, `scope`, integer current `design_version`, `source`; creates a new context revision and no answer |
| `decision_record` | `measure`, integer `context_revision`, supplied `status`, `answered_by`, `source`; `note` for decline/pause/withdrawal; `representative_ref` for representative; `review_ref` when accepting after a review flag |
| `safe_contact_record` | Resident-confirmed `safe_contact_ref`, supplied `source`; increments contact history, does not send anything |
| `representative_record` | `representative_ref`, `measure`, integer `context_revision`, `status`, `tasks`, `source`, `authority_date`, `review_date`, `resident_wishes`, current `safe_contact_ref`; appends authority version |
| `disclosure_check` | `representative_ref`, `measure`, integer `context_revision`, `task`; checks current task authority only, sends nothing |
| `service_open` | Existing service fields (route, summary, desired outcome, handler/redress owners, next update); `Independent review` also needs `review_measure`, integer `review_decision_version`, `review_reference` |
| `service_update`, `service_close` | Existing request ID/status/update/outcome; independent review is update/close-only for its named independent reviewer |

Answer statuses: Waiting, Accepted, Declined, Paused, Withdrawn. Authority
statuses: Confirmed, Unclear, Disputed, Revoked. Tasks: Receive information,
Communicate, Attend, Works decision. Review and authority dates use YYYY-MM-DD;
authority cannot start in the future, review follows evidence, and reliance
stops on the review date. The UI records one task per authority version; the API
supports a list of evidenced tasks. Register separate task/scope authority
references when multiple active authorities are needed; latest version of each
reference is authoritative, never the most recent representative globally.

The API ignores forged recorder/actor fields. Missing/stale/invalid context,
source or authority returns 400, wrong staff/reviewer role returns 403, and
blocked controlled release returns 409. `disclosure_check` is not a send token:
no downstream transport consumes it and no message is sent. Legacy
representative-addressed templates remain refused; authorized staff AI
proposals are non-addressed drafts and still require human review.

New decision versions contain server-derived `recorder_identity`; new independent
requests bind `reviewed_identity` to the selected exact measure/decision version.
Opening or reassigning redress to the original recorder returns 403 even after an
email change when the historical code or oid matches. Missing/insufficient legacy
identity also returns 403 with an explicit `Unknown` error, without case or
successful-audit mutation. Detail derives `recorder_identity_status` and
`reviewed_identity_status` without rewriting old evidence. Unbound legacy requests
never acquire a snapshot from today's staff or a reused decision ordinal after
retention deletion. Other service/complaint and consent paths remain available
under existing controls. New identifiers retain the existing resident-view
boundary and are omitted from other staff/contractor detail and exports.

Work-order issue/reissue/correction requires `resident_bindings`, for example:

```json
{"resident_bindings": [{"measure": "Loft insulation", "context_revision": 1}]}
```

The manager UI accepts `Measure|revision; Measure|revision`, with no inferred
binding from free-text scope. Booking/completion checks the saved version.
Quality evidence accepts an explicit integer `context_revision`; unbound
evidence can be recorded via the API but cannot be accepted or handed over.
The quality UI asks which scope revision the evidence covers. A withdrawn
sibling cannot block an explicitly independent bound work order or QA record.

Complaints and independent review stay available after pause/closure and AI
failure. They record an owned request, not delivery to the association's formal
complaints service. The panel directs staff to the named officer and accessible
non-digital route without inventing a real complaints URL, response timetable
or delegation. The real route, human independence/accessibility and
without-detriment acceptance remain unproven.

`tests/test_resident_api.py` starts the actual app on loopback with synthetic
staff/home data and SQLite, checking health/static assets, authentication,
decisions/withdrawal, redress, authority/privacy and restart. Core semantic tests
also use a synthetic AI adapter, not live model inference. Real inference,
SQL Server/Azure and human acceptance remain unmet; no private data or new
deployment is used. Docker build/run depends on CI when local daemon access is
denied.

## Incident and restart contract (#221)

Existing `POST /api/continuity/suspend` records a seeded `critical incident`
or `guardrail breach` in `trigger`, plus `scope`, `reason`, `incident_owner`,
`containment`, `comms_owner`, `comms_audience`, `evidence`, `resident_impact`,
`remediation` and `restart_authority`. Missing new fields are visibly unavailable
so incomplete reports never prevent immediate containment. Impacts and versions
are derived inside the SQL write, not trusted from an HTTP preview.

`restart-propose` takes `id`, `corrective_evidence`, `test_id`, `result: Pass`
and `evidence_class: constructed-fixture`. This is explicitly a recorded
constructed claim, not a server-run test or actual acceptance. Incomplete
incident/version evidence refuses restart. Proposal history is retained.
`restart-decide` takes `id`, current `epoch`, exact `proposal_digest`,
`decision` (`Restart` or `Keep suspended`) and matching `authority_ref`.
Missing, failed, altered, stale, self-approved, untrusted and version-drifted
evidence is refused and audited.
Legacy impact completeness includes exact prior-release references/bindings and
retained version evidence; missing historical references deny constructed
restart, not immediate containment.

The decision endpoint requires the trusted-proxy route and the separately
provisioned `ZavaForward.AIRestart` claim, mapped through the existing uniquely
OID-bound capability helper, plus a current registered manager distinct from
the suspender and proposer. Password login and email fallback cannot supply
this capability; stored staff capability fields are not sign-in grants.
No actual holder is provisioned by this change. Local SQL revalidation cannot
prove remote claim revocation or professional appointment.
Authenticated password-route attempts reach the same denial wrapper and retain
one bounded denial, while invalid/stale/inactive identity claims are labelled
unverified rather than attributed as verified staff. Denials do not mutate the
incident and survive document rollback/reopen.

A successful `Restart` is constructed-only: the record exposes `actual_hold:
true` and the missing actual authority. It never restores actual-provider
dispatch or reliance, even after release replacement/provider switch/reopen.
JSON can contain incidents and preserve manual work but cannot qualify AI
restart. Committed actions with failed acknowledgement return 409 and
`outcome: committed`; reload before retrying. Ordinary denials remain 400/403
under existing API conventions. No new UI or live activation is introduced.
Fresh constructed ready/accepted list, detail, source export and bundle export
share eligibility semantics. Bundle projection uses the current trusted provider,
not caller flags; provider switches/reopen preserve actual holds. Invalid task/
scope/event history stays noncurrent without breaking generic evidence export.

The issue's synthetic drill is `test_operator_suspension`; the already selected
native SQL gate runs
`test_assistants.MssqlDurabilityTests.test_operator_incident_drill` against its
owned disposable database. These are engineering checks, not actual OD-35
authority, threshold approval, competent evaluation or human drill acceptance.

## RAI task release API (#219)

`GET /api/assistants` now includes role-filtered `registered_tasks` for the
merged eleven-task registry: intended/prohibited use, stakeholders, current
`binding`, selected `release` (ID/version/digest), structured `release_denial`
and the explicit OQ-017 authority gap. Existing five-assistant fields remain.
Configured JSON-store AI denies without durable SQL release evidence; use
SQLite locally or Azure SQL for deployment, not a JSON bypass.

`POST /api/assistants/releases` uses the existing authenticated Programme
Manager plus `ZF_ASSIST_RELEASE_APPROVERS` allowlist. Copy the task's current
binding and supply the [core contract](../core/README.md#task-bound-rai-release-records-219)
fields, `task` (assistant ID or `legacy:<retained-task>`), `evidence_class`,
`serving_model`, residual-risk note and future ISO expiry. The server records
the authenticated approver, never a client-supplied approver identity. Posting
a replacement revokes previous active records for that task across endpoints
and deployments; it does not overwrite historical proposals. Suspend/revoke
release routes are unchanged. Replacing a release does not clear the independent
incident hold; actual restart remains blocked as described above.

Denials expose missing evidence, the unappointed authority/project contact and
manual route, and persist in assistant events or the legacy audit/comparison
record. Web draft notes show the denial reason. Superseded priority proposals
are visibly non-actionable; server-side accept/edit checks remain authoritative.
Release does not grant sending, works consent, safety, financial or domain-write
authority. It permits bounded proposals that still require human review.

Local synthetic HTTP exercise (no real AI, Azure or private data):

```bash
cd src/api
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_assistants.ApiTests.test_release_record_local_http -v
```

This starts the real App on an ephemeral loopback port, checks health,
authenticated registry/release/invoke/detail/revoke routes, zero calls while
denied, one nonbillable scripted provider call when released, unapproved output
and unchanged domain state. It shuts down the listener and removes its temporary
synthetic files. Direct human, live model and Azure acceptance are not implied.

## Hazard referral and retrofit hold API (#85)

Authenticated staff use the existing safety panel on open or closed retrofit
records. It labels observations as unverified, shows source/awareness, referral
destination, follow-up owner, whole-home hold scope, separate sent/received/
accepted evidence, external service response/resident-update times and explicit
unknowns. It sends no referral or resident communication itself. Use the
existing hazard service directly for urgent concerns; neither AI nor a
retrofit hold may delay that route.

| Path after `/api/cases/{id}/` | Body and control |
| --- | --- |
| `hazard-raise` | Reported `category`, `priority`, optional `note`, required `source`, timezone-aware `aware_at` not in the future; staff, including closed retrofit records |
| `hazard-refer` | `index`, `to`, external case/job `job`, sending `evidence`; staff; prospective binding for active legacy records |
| `hazard-receive` | `index`, receipt `evidence`; named safety receiver, once |
| `hazard-accept` | `index`, acceptance `evidence`; named safety receiver, after receipt, once |
| `hazard-times` | `index`, external timing `evidence`, at least one of timezone-aware `response_due_at`, `responded_at`, `resident_update_due_at`, `resident_updated_at`; accepting receiver; no overwrite |
| `hazard-repaired` | `index`, external repair `evidence`; accepting receiver; observation only |
| `hazard-release` | `index`, release reason `note`, external supporting `evidence`; independent safety-role actor, after repair evidence; home retrofit hold only |

Missing evidence/invalid state or index returns 400; wrong role/receiver or
non-independent release returns 403. Active holds return 409 on controlled
retrofit progression. No classify, pause-clock, reset-clock or close-hazard API
exists. Server-supplied actors and home scope ignore forged client authority.
All actions are manual, one-case decisions; consent and other home/building
gates stay independent. See the [core contract](../core/README.md#hazard-referral-and-home-retrofit-holds-85).

The listed release-role checks are demonstrator safeguards, not ratified
release authority. Repairs, Safety and Housing owner approval of release
responsibility, response/resident-update timing and escalation policy remains
outstanding (RV-002). Human-recorded due times do not establish an approved
service timetable. These acceptance criteria remain unchecked.

`tests/test_hazard_api.py` runs a real HTTP application on loopback with
fictional staff/home data and SQLite state. It exercises health/static serving,
authenticated closed-record intake, receipt/acceptance/timing/repair/release,
role isolation, legacy binding, restart durability and refusal of cached sessions
after current staff role/OID changes. This is local synthetic
application evidence, not real model inference, verified service transport,
Azure deployment or human/browser acceptance. The canonical
`test_mssqlstore.MssqlHazardReferral` adapter separately exercised actual local
SQL Server durability and transaction-time current caller/destination checks
on 2026-10-17 (16 run, one JSON-only skip), using a task-owned disposable
loopback container and tiny fictional cases. That does not prove Azure or
verified external receipt.
The existing AI release and human-review gates are unchanged; no fallback or
model output can waive a hold. Full #85 acceptance and the mandatory
real-platform application exercise remain unmet without the outstanding
owner/live evidence. Docker image checks are delegated to CI if the local
daemon is inaccessible.

The existing endpoints and screen require no new fields or UI changes for the
current-actor correction. They still record human assertions, not service
commands: no resident message, hazard classification, calculated statutory
clock or external closure occurs. Independent restart identity now compares
recorded normalized email/code/OID, not case-sensitive email alone. SQL refuses
and discards a failed event and its success audit while preserving earlier audit.
If synchronization fails after an acknowledged SQL commit, it reports the
committed outcome and never replays already-committed audit. The one independent
Review's original Not accepted finding is retained; correction ONE has local
regression/actual SQL evidence, not independent final-head closure.
For JSON, a post-save audit failure is explicitly a potentially persisted outcome
requiring reload/reconciliation, not an invitation to retry blindly. See the
[backend evidence boundary](../core/README.md#current-hazard-actor-and-persistence-evidence-2026-10-17).
No new browser run or accessibility acceptance is claimed for this backend-only
change; the Fluent 2/native screen and manual paths are unchanged.

## Design-system foundations (#150)

The [design-system inventory](../../docs/reference/research/ux/design-system.md)
records the owner's Fluent UI (Fluent 2) adoption decision, the sourced token
mapping, seven component states and AI draft-review boundaries. This is a partial
native-foundation/non-colour slice, not a completed Fluent UI runtime migration.
Markers use circle/O, square/W and triangle/! with matching key and status names.
Clusters show home and safety counts (including zero); filter tiles visibly say
"Selected". Overview data tables use named keyboard-scrollable regions on narrow
screens. Existing consent, approval, AI and server authority are unchanged.

From `src/api`, after installing the projects and `.[dev]` with pip:

```bash
python -m playwright install chromium
python -m checks.design_system_browser_check
```

This check starts the real API on a temporary loopback port against 505 fictional
homes from the shared test fixture. Real map APIs exercise point and cluster modes;
only basemap tiles are replaced by a synthetic pixel, so no external tile service
or private dataset is used. It checks rendered tokens, non-colour signals,
keyboard navigation, 320/390/1280px reflow, forced colours and reduced motion.
The source API CI job runs it with pinned Playwright as a development-only
dependency; production requirements/images do not gain a browser dependency.
Human/screen-reader acceptance, full Fluent component integration and live
AI/SQL Server/Azure validation are not established by these local checks.

## Shared workbench information architecture (#152)

`/api/me` includes `navigation` entries with `href`, `label` and `scope`,
computed by the API from existing endpoint/Finance/manager rules. The client
renders these entries without a new role map. Metadata is not authorization:
direct API calls retain all existing server checks. The default remains the
signed-in person's assigned cases, or assigned contractor jobs; programme
directories and overview are explicitly labelled broader scopes. There is no
role simulator. No role-specific screen redesign or new permission is included.

The shell has a keyboard skip link, named navigation, visible/semantic current
destination and a persistent scope/result announcement. Each staff case row has
one case-opening link, plain recorded status and a recorded next action, not an
AI-invented workflow decision. Cases open full screen. Back to the list keeps
the last mine/all scope and filters, but deliberately reloads page one: it does
not promise restored pagination, selected row, scroll position or row focus.
Direct case entry falls back to the own queue.

"Reset my queue" clears search, stage, authority area, wave, owner, flag, work queue, sort
and all-cases override; it restores own cases in the existing safety-first
policy order, focuses the reset control and announces refreshed results.
Obsolete loads/debounce are cancelled on route replacement; failed loads show
an explicit retry, and session expiry returns to sign-in. An empty own queue
is distinguished from no filter matches. Reset does not modify records.
Cancelling a pending briefing invalidates its cached panel so the next queue
requests it again; a completed briefing remains cached. Briefing failures show
an explicit retry. The browser check holds responses across My cases -> All
cases -> My cases and verifies recovery without stale-response replacement.
It waits for the visible "Reading case summaries..." state within Today's
briefing and verifies complete scope/count response fixtures. PR #517's
deterministic 30-second timeout followed #516's loading-copy change: the
check still expected "Reading your cases...", not a CDN or app-readiness failure.
Safety reports and stopped-work details remain expanded ahead of routine case
forms, with existing named owners, external timings and explicit unknowns.
Contractors retain their minimum-necessary projection, not staff safety data.

The versioned [shared-IA manifest](./checks/workbench-manifest.json) declares
eight implemented auth roles, exact synthetic own queues/navigation and all
eleven PRD perspectives/nine workflows with partial or deferred coverage.
It is not full AC-034/043, accepted role mapping or validated user research.
From `src/api`, using the installed src packages and `.[dev]`:

```bash
python -m checks.workbench_browser_check
python -m checks.design_system_browser_check
```

The second command is the existing CI entry point and runs both browser suites.
Each starts and stops its own healthy loopback API with constructed data in an
automatically cleaned, ignored repository-root `.venv/` scratch subdirectory;
no credentials, model endpoints or private data settings are inherited.
The IA checks cover eight roles, mine/all/reset/back/history, delayed and failed
requests, expiry, contractor projection, queue/case reflow at 320/390/768/1024/
1280 CSS pixels and 200% root text enlargement. This is Chromium engineering
evidence, not browser-zoom, screen-reader or human acceptance. The baseline
also exercises return from a queue with more than 50 rows.

Supported devices/browsers and field/mobile use still need the owner's
decision. The full eleven-profile/nine-workflow journey manifest remains
incomplete. AI routes, real-provider configuration and human review/release
gates are unchanged; the isolated checks make no live model call and do not
satisfy mandatory real-inference/SQL Server/Azure exercise acceptance.
No SQL, deployment, resident consent or controlled approval behavior changed.
Local Docker access was permission denied; image evidence must come from CI.

## Role task queues and shared case context (#76)

### Queue signal completion (#77, 2026-10-17)

The existing Queue definitions disclosure now also defines all five Show only
signals, including extra support, 60-day stage waiting, resident decision and
funding states. Sidebar terms and descriptions stack for readability. Missing
support stays unknown; a waiting signal is not a statutory deadline and no
signal grants consent, funding approval or safety-service authority.

The live workspace status explicitly names the authenticated perspective,
workflow stage, search and own/all-cases scope. The existing Stage filter is
the workflow-stage scope, not a scenario picker or the optional AI "Workflow
only" setting. Stage narrows the chosen own/all scope within existing rights;
it never replaces the authenticated role. No role simulator is added.

Reset consumes both `work_queues.default.view` and its filters/order, keeping
first-page/null-selection, logical focus and result announcements. The current
`work-queues-1` default remains own/urgent. Selecting a case continues to reload
that case's recorded rationale and proposed reviewers; an empty reviewer list
explicitly shows proposed owner Unknown, leaving current ownership unchanged.

The existing `python -m checks.workbench_browser_check` runs the real local
app/API with three constructed cases, discriminating surnames and an alternate
server all/name default. It checks exact rendered IDs/order/scope, reset's
offset=0/no-cursor request, two cases' own rationale/reviewers, unknown reviewer,
expanded definitions at 320/390/1280px and reduced motion. Optional
`ZF_QUEUE_SCREENSHOTS` saves synthetic-only screenshots to a chosen directory.
This is first-page request evidence, not a three-case multipage test.
No real model, private stock, SQL Server or Azure is exercised. Full scenario
workflow coverage, operational definition ratification, human/screen-reader
acceptance and mandatory live-platform application acceptance remain unmet.

This is a bounded offline extension of the existing role workbench, not a new
identity provider, role simulator, permission policy or operational acceptance.
The [parity audit](../../docs/architecture/mvp-to-src-parity-matrix.md#role-task-queue-offline-slice-2026-10-16)
records each issue criterion before and after the change. The authenticated
role still determines access; own/all scope, queue, search and other filters
intersect and never grant rights.

Staff `/api/me` now publishes `work_queues`: version `work-queues-1`, six
definitions, availability/limitations, default filter state and null selection.
The single existing reset consumes that server default, restores own cases in
the existing deterministic order on page one, focuses itself and announces
scope, all filters, version and result count. No case is selected automatically.
No changes to records, ranking, assignments or approvals result from filtering
or reset. No matches and no assigned open cases remain distinct.

`GET /api/cases?queue=new` and `/api/cases.csv?queue=new` use the same filter
before totals, ordering and pagination. Other filters/sorts still apply.
Unknown queue IDs return 400 on both endpoints; an unavailable approved-priority
queue returns an empty result, with its explanation in the visible definitions.
Contractors cannot use staff queues and receive no new context or staff metadata.
Queue selection retains the snapshot-scoped case-ID hot cache; SQL stores load
misses from transactionally maintained indexed membership columns. See the
[60,000-case write-cold/repeat measurements and remaining ranking/refresh costs](../core/README.md#generated-60000-case-queue-timing-327-2026-10-16).
Filtering and reset do not change that authorisation boundary.

| Queue ID | Visible definition and source |
| --- | --- |
| `new` | Current `stage_since` is between zero and seven days old, inclusive. This describes arrival in the current stage, not case creation. |
| `priority` | Open cases under an explicitly approved ranking policy with a named owner. The existing policy is draft, so this queue is unavailable/empty. Accepted AI advice never qualifies as approved programme priority. |
| `stale` | Last supplied EPC record's `documents.at` is older than 30 days, Survey older than 180 days, or a technical sign-off explicitly needs reassessment. Record timestamps are review triggers, not certificate expiry or proof of source validity/currentness. |
| `blocked` | Existing safety, unresolved stock and applicable shared-building stops, plus unmet funding/resident/technical prerequisites at `Final checks before ordering`. Future-step requirements stay visible with `current_stop=false`, but do not join this queue or replace the current-stage reason/action. |
| `overdue` | An outstanding recorded handoff acceptance, case resident-update or external safety-service response/update deadline is strictly before the snapshot. Each completion is checked independently; accepting a handoff does not complete a resident-update commitment. No deadline is invented from stage age. |
| `unowned` | Handoff Offered, Received or Escalated, with no accepted receiver. A proposed receiver is not a confirmed owner, and the sender keeps chase responsibility. Accepted/Completed/Declined/Withdrawn are excluded. |

Evaluation uses the dataset `as_of`, with date-only values interpreted at UTC
midnight. This reproducible snapshot is displayed, not presented as a live
safety-service clock. Missing, malformed or future observation/record dates
remain Unknown; timezone-less datetime values are Unknown. Future deadlines
are not overdue; equal deadlines become overdue only after the snapshot.
External timing authority remains with the existing hazard and repairs service.
Legacy `noticed` alone cannot establish precise awareness or elapsed hours.

Staff list/detail share the same `work` object: case/current owner, reason,
one next action, origin/evidence/version/snapshot, blocker step/reason/named
owner/responsible role/action, separate handoff owners, evidence-review status,
outstanding deadlines and recorded hazard-clock observations. Safety/stock/
building stops take precedence over a pending handoff, current-stage return
or final-check prerequisite. A role-only responsibility keeps named owner
Unknown; no person is assigned by inference. Missing next action prompts
the case owner to record it rather than fabricating a workflow instruction.

The case, current-context part of history, proposed-reviewer panel and
"Task sources" disclosure reuse this same object. Historical events retain
their event-time owner/reason; context refresh never rewrites those events.
Case switching cancels obsolete loads and binds the displayed context to the
selected case. Domain source comparisons and sign-off records remain intact.
Human-written reason/action/source aliases follow existing need-to-know rules
before serialization, including derived list/status fields; this does not
approve the operational role/redaction matrix.

The new core semantics/store tests and real loopback SQLite HTTP tests use
constructed data, exact threshold/lifecycle expectations and 120 interleaved
matching/nonmatching cases to verify pre-page filtering, cursor totals/order,
sorting and CSV agreement. The extended existing Playwright check exercises
the actual local app, all eight implemented roles, visible definitions,
queue membership, current-context agreement, case switching, delayed responses,
all-filter reset, focus/status and responsive layout. An alternate server
default proves reset is not hardcoded in the browser.

From the repository root, with `/tmp/zf164` already containing the project
development dependencies (pip only), for targeted checks:

```bash
ROOT="$PWD"
BASE="$ROOT/src/core/src:$ROOT/src/agents/src:$ROOT/src/api/src"
(cd src/core && PYTHONPATH="$ROOT/src/core/tests:$BASE" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_taskqueues.py' -v)
(cd src/api && PYTHONPATH="$ROOT/src/api/tests:$ROOT/src/core/tests:$ROOT/src/agents/tests:$BASE" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_task_queue_api.py' -v)
(cd src/api && PYTHONPATH="$BASE" /tmp/zf164/bin/python -m checks.workbench_browser_check)
```

Operational queue-definition ratification, named ranking-policy approval and
OQ-005/OD-14/OD-19 role/field/redaction/delegation decisions remain open.
These engineering checks do not establish direct human accessibility/usability,
real AI, SQL Server, Azure deployment or complete eleven-profile/nine-workflow
acceptance. Refs #76; the issue is not closed by this slice.

## Return and handoff API (#83)

All mutations below are authenticated, one-case human actions. The server
supplies authority and receiving/current owner; client-supplied authority or
owner fields cannot override them. Source references are human-recorded text,
not automatically verified evidence.

| Path after `/api/cases/{id}/` | Body and control |
| --- | --- |
| `return` | `to_stage`, `reason`, `source`, `next_action`; authorised staff, earlier stage only |
| `reopen` | `reason`, `source`, `next_action`; manager, closed case only |
| `offer-handoff` | `to`, required `source`, `source_version`, `reason`, current `handoff_version`; optional `note`, `urgency` (Routine/Urgent), timezone-aware `due_at`, `next_action`, `resident_update_to`, `resident_update_due_at`; owner or manager |
| `receive-handoff` | Empty object; named receiver, Sent only; not acceptance |
| `accept-handoff` | Required `source`, `source_version`, `reason`, current `handoff_version`; named receiver only, Sent/Received/Escalated |
| `decline-handoff` | `reason`; named receiver, Sent/Received/Escalated |
| `withdraw-handoff` | Empty object; sender or manager, Sent/Received/Escalated |
| `escalate-handoff` | `to` (manager email), `reason`; sender or manager, Sent/Received |
| `complete-handoff` | `note`; accepting current owner, Accepted only |
| `handover` | Legacy alias for an offer with the same required source/version/reason/handoff-version metadata; never immediate reassignment |

`GET /api/handoffs` returns unaccepted work visible to the sender, receiver and
managers, including canonical `status` and separately labelled responsibility
fields. Persisted `state` keeps Offered/Declined compatibility; detail returns
versioned `returns` and `handoff_history`. Unauthorized or replayed transitions
return an explicit error without a transition. New return/reopen requests
without source/next action now fail with HTTP 400.

BG-010's approved-time escalation criterion stays unmet: due dates are
human-selected and escalation is manual; OD-09 policy and operational acceptance
are not available. No timer, automatic resident contact, live model effectiveness,
SQL Server result or Azure deployment is claimed by local synthetic tests.
AI assistance remains available under its existing configuration/release/human
review gates; this deterministic workflow adds no model authority.

## Building shared context (issue #75)

Staff can follow an explicitly linked home to `#/building/{building_id}` and
back to either linked home. `GET /api/buildings/{building_id}` returns the
[core source-backed model](../core/README.md#building-shared-context-issue-75),
with separate systems, dependencies, stopped-work reasons, works and shared
costs. Missing/unknown data is labelled, not interpreted as an approval.
Linked homes expose only their case ID, stage and closed flag in this view,
not resident details, home evidence, decisions or allocations.

Only existing staff roles can read buildings; contractors and unknown roles
receive 403, unauthenticated requests 401, missing records 404 and invalid
building data 400. Building costs and home `cost_allocation` are returned only
to the existing `FINANCE_VIEW` roles. Other staff see a restricted-cost notice,
with amounts omitted server-side. The building screen is read-only and cannot
approve, instruct works, release safety restrictions, contact residents or pay.
Home AI assistance remains available through its existing proposal-only and
human-review paths; shared free text and costs are not added to prompts.

`tests/test_buildings.py` starts the real application on loopback with a
wholly fictional two-home SQLite fixture. It checks health/static serving,
authenticated navigation, role/amount isolation, scoped blocked advancement,
unaffected sibling advancement and availability of the existing assistant
registry. No live model inference, Azure deployment, actual SQL Server or
human/browser accessibility acceptance is implied. There is no register
editor or automatic retrofit of building data into an already populated store.

`tests/test_mssqlstore.py` adds five constructed building semantic tests and
replays the same three HTTP tests on the existing disposable SQL harness.
From `src/api`, with installed source distributions:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_mssqlstore.MssqlBuildings test_mssqlstore.MssqlBuildingHttp -v
```

These tests are destructive. Enable `ZF_TEST_MSSQL=1` only with `ZF_SQL_*`
explicitly targeting a task-owned throwaway local SQL Server/database, never a
configured or pilot dataset. Use a sanitized environment with
`ZF_DOC_STORE=local`, `ZF_SCANNER=local`, `ZF_AUTH=password`, `ZF_ENV=test`
and task-owned local `TMPDIR`, `ZF_DOC_DIR` and `ZF_DIGEST_DIR`; do not inherit
blob, AI, identity or private-path settings. Delete the exact owned container
and its database after the run. Without opt-in, the eight tests are **Not run**,
not passing SQL evidence.

The added checks cover seed-free reopen, full shared record and separate home
allocations/evidence, committed hold visibility across independent sessions,
stale shared-document refusal, both home/package scope dimensions and missing
resident/funding/technical/QA approvals. This is local constructed-engine
conformance only, not Azure, operational register/update rights, allocation
policy, human/accessibility acceptance or live application acceptance.

## What staff see

The #344 public edge now targets the existing immutable src API, not a rebuilt
legacy app. Deployment and tenant prerequisites are documented in the
[public browser continuation](../../infra/README.md#public-browser-continuation-2026-10-16-344).
Welcome/health are intentionally public; workbench pages require Entra and
protected JSON APIs must return 401 without a user. Browser redirect mode is
the infrastructure default (`entraBearerOnly=false`), not successful sign-in.
The proof's invalid registration/absent staff block real-user acceptance (#349).
The [dated feature audit](../../docs/architecture/mvp-to-src-parity-matrix.md#public-deployment-feature-audit-2026-10-16)
separates image presence, public intercepts and rendered/authorized behavior;
missing deployment/data/model/photo/law prerequisites are tracked by #350.

* Sign in once and land on "My cases today", with open safety issues first.
* A full-screen case card: contact details, preferences and support needs, a
  plain status line, owner, contractor, next visit and history.
* Log a call, record the resident's own answer, hand a case to a colleague and
  draft a message. Nothing is sent automatically.
* "Ready to book" is checked on the server: the resident's decision, funding
  and any open safety issue must all be confirmed. Unknown never passes.
* Filter the list by stage, local authority, wave, owner or flag, and sort by
  urgency, longest wait, last contact, name or next visit.
* The default "Most urgent first" order is a deterministic ranking
  (`src/core/src/zava_forward/core/ranking.py`): open safety issue, then priority support or an
  adjustment, then longest time in stage, then earlier stage, then case id as
  the fixed tie-break. Each card shows its rank and plain reasons, the list
  header shows the policy version, policy hash and as-of date, and
  `GET /api/ranking/policy` returns the versioned rules. The rules live in
  versioned files in `src/core/src/zava_forward/core/policies/` (for example `ranking-v1.json`) with a policy
  id, version, owner, status, effective date and a SHA-256 content hash over
  the canonical JSON. Every file is verified when loaded and a mismatch stops
  the load. Old versions stay in the folder and can be re-run. Ranking takes
  the case data, a policy and an explicit `as_of` date and reads no clock.
  `GET /api/ranking/snapshot?policy=1.0.0` (managers only) returns the
  snapshot: policy version and hash, as-of, and per case the rank, reason codes
  and deciding rule. It is also written beside the data when it changes. The
  policy owner is "to be named" and the rule order is an unsigned draft.
* "Suggest my top 5" on My cases asks AI for a second opinion beside the
  rule-based order, labelled "AI suggestion, not approved", with a cited reason
  per case. It is stored in a separate recommendations list and is never read
  by the ranking, owners, stages or queues. A person accepts, edits (untick
  cases) or rejects it, with a reason for edit and reject, and the answer goes
  in the audit log. Without a model a rules-based template is used.
* The case list loads 50 at a time ("Show more"; the API allows up to 100 and
  returns the total). The Overview map is requested by viewport and shows grid
  clusters with counts when more than 500 homes are in view. List and map totals
  agree for the same filter. The CSV download still returns the whole filtered list.
* Filters sit in a left panel and update the list without reloading the page.
  The briefing is cached until case data changes.
* Overview: counts that filter the map when clicked, a zoomable OpenStreetMap
  of open cases (Leaflet bundled in `web/vendor`; circle/O normal, square/W waiting
  60+ days, triangle/! open safety issue; status names and matching list),
  charts by stage, authority, wave and waiting time,
  contractor and team workload. Visits lists booked appointments by day.
  The dated synthetic generator now guarantees six additional forward
  assessment visits and retains historical attended/no-access/cancelled
  contrasts. See the [coverage recipe](../../docs/reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13)
  for reproducible dates, queue counts, private outputs and safety limits.
* "Who could take this on": top three colleagues with plain reasons (role
  fit for the stage, current workload, who already knows the resident).
* AI assistance, always a draft for a person: a morning briefing, a drafted
  message, a "catch me up" summary, funding application wording, and reading
  an uploaded document. It runs on Azure OpenAI through the managed identity.
  Output is checked, every run is audited, and a plain template is used when
  the model is unavailable. Each output carries source citations that must
  resolve to a real field or record of the case (for example "Stage: Survey
  booked", "Case history 2026-09-30"). They are checked on the server: output
  whose citations do not resolve is marked Unverified, uncited summary bullets
  and uncited priority items are dropped, and the sources are shown beside the
  "AI suggestion, not approved" label. Output stays "Not reviewed" until a person accepts, edits or
  rejects it. Workflow-only mode (request flag `mode: "workflow"`, the "Workflow
  only" tick box, or `ZF_AI=off`) skips the model for every task and is
  recorded. Each task leaves a comparison record (case ids, AI output,
  workflow-only output, fallback reason, reviewer action and override) in the
  recommendation store, in both the JSON and the sqlite store.
* Documents: upload pdf, png, jpg, docx, xlsx, csv or txt (5 MB), see an
  evidence checklist (EPC, survey, design, consent) and download files.
  Every upload is scanned before it can be downloaded or read by the document
  assistant (`doc_controls.py`; `ZF_SCANNER=local|defender`). The local scanner
  is a labelled synthetic test: a marker and a type check, not an antivirus
  engine. The Defender scanner reads the Defender for Storage blob tag through a
  fake transport only, and a pending result keeps the file unavailable. A
  programme manager lists documents past their retention trigger
  (`GET /api/retention`), approves each deletion (`retention-approve`) and can
  place or release a case legal hold (`legal-hold`, `legal-hold-release`); a
  hold blocks deletion. Periods are synthetic-demo placeholders, not an approved
  schedule, and the deletion log keeps no file name or content.
  The [bounded SQL rescan job](../orchestrator/README.md#bounded-document-rescan-job-117)
  now supplies an offline schedulable invocation, not a hosted timer or Defender
  activation. Its worker retains unavailable infected/mismatched bytes and holds;
  it cannot approve deletion or release a hold. Existing API/manual behavior
  and owner approval boundaries are unchanged.
* Funding: a person moves each application through draft, approved,
  submitted and confirmed. Approval needs complete evidence and the Grants
  and Evidence Officer or a manager. The system never submits anything.
* A hash-chained audit log records every change. `GET /api/audit-check`
  (manager) and `python -m zava_forward.core.ledger` verify the chain; a digest of
  the head can be written to `ZF_DIGEST_DIR` (`POST /api/ledger/digest`) and is
  re-checked on verify. The digest is a local file, not yet an immutable Blob.
* Role-based field projection is enforced on the server (`projection.py`).
  Contractors see only their own cases with "needs notice" and a named contact
  (the case owner), never the vulnerability reason, resident name or contact
  details. Staff see the reason only for the roles in `ZF_REASON_ROLES`
  (default Resident Liaison Officer, Building Safety Liaison, Retrofit Programme
  Manager); others see "Extra support noted". Every role is tested against every
  endpoint (`tests/test_role_matrix.py`, plus `tests/test_role_endpoint_inventory.py`,
  which fails when a server route is missing from its inventory and checks
  contractor canaries across API, CSV export, search, audit and AI prompts).
  Free-text notes (decided for the exercise): no pattern redaction, which gives
  false assurance. Free-text fields are excluded by allow-list from contractor
  responses and AI prompts, and roles without a recorded need see "Held for
  roles with a recorded need" for contact notes and outcomes, appointment and
  hazard notes. The reason-role list remains a proposal (OD-14, OD-19).
* Workflow screens on the case page: return to an earlier stage or reopen a
  closed case (manager), recording reason, source reference, next action,
  authenticated authority and existing receiving owner. Offer, record receipt,
  accept, decline, manually escalate to a manager, withdraw or complete a handoff.
  Receipt does not imply acceptance; the sender keeps case/chase ownership until
  the named receiver accepts. Pending sender/receiver/manager work lists and case
  detail distinguish accountability, destination, proposed/confirmed receiver,
  chase owner, urgency, due date, next action and resident-update commitment.
  Missing values remain unknown; no message is sent automatically. Existing
  resident-update commitments survive every transition and subsequent offers.
  Safety referral has separately evidenced receipt/acceptance and an
  evidence-backed independent home-hold release; see the #85 contract above.
  All actions use server-side checks; the old `handover` endpoint now offers
  rather than immediately reassigning. See the [core contract](../core/README.md#return-reopen-and-handoff-accountability-83).
* Contractor screens: "My jobs" and a job page show only the address, stage,
  next visit, "needs notice" and a named contact. The server projects the data
  (`projection.py`); the screens never request resident detail. The rank and
  reasons are not sent to contractors either.
* Quality acceptance (FR-017, `quality.py`): per measure, evidence against a
  versioned checklist (every check needs a note of what was seen), then accept
  or return with a defect and an owner, fix, reinspect, resident handover and
  aftercare notes. States move one step at a time on the server and are
  audited. Whoever accepts must differ from whoever submitted, recorded or
  fixed the work, and nothing is accepted automatically. Provider submissions
  are stored as evidence only.
* Procurement and capacity (FR-016, `procurement.py`): packages with period,
  versioned scope and contract reference; offered capacity kept apart from
  capacity committed with evidence; controlled work orders (each change a new
  version with its issuer, none issued beyond evidenced commitment);
  appointment outcomes, completion and correction. Managers get "Capacity and
  work orders"; contractors see only their own orders, with "needs notice" and
  no reason. Packages and orders are held as one document in the JSON file or
  the sqlite `meta` table, so they work in both stores.
* Documents sit behind a `DocumentStore` interface (`documents.py`). The local
  filesystem store is the default (`ZF_DOC_STORE=local`, `ZF_DOC_DIR`). The Azure
  Blob store (`ZF_DOC_STORE=blob`) uses urllib against the Blob REST API with a
  SAS token (`ZF_BLOB_SAS`) or a managed identity token (`ZF_BLOB_CLIENT_ID`
  optional); config is `ZF_BLOB_ACCOUNT_URL` and `ZF_BLOB_CONTAINER`. Uploads
  allow an extension list and 5 MB, need a staff role (contractors cannot
  upload or download) and write audit entries for upload, download and failure.
* The map has a "Show the map areas as a list" alternative: a keyboard and
  screen reader list of clusters (zoom in) or homes (open case), with a polite
  live status line. The tile provider comes from `ZF_TILE_URL` (https only) and
  the CSP follows it. With `ZF_ENV=production` and no `ZF_TILE_URL` no tiles
  load and only the list works.

* Staff time capture (PR-004) is off by default. It records only when
  `ZF_TIME_CAPTURE=on`, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION` and
  `ZF_TIME_NOTICE_APPROVED` each hold a reference, one manager has requested
  enabling (`POST /api/time/request-enable`, audit
  `time_capture_enable_requested`) and a manager in a different role has taken
  the audited enabling action (`POST /api/time/enable`, audit
  `time_capture_enabled`, which names the requester; void if a reference later
  changes), and the person has acknowledged the staff notice
  (`POST /api/time/acknowledge`, audited); own entries only; screens at `#/time`;
  reports are manager-only, aggregated and suppress groups under
  `ZF_TIME_MIN_GROUP` (default 5). The enabling record, entries and
  acknowledgements are tables (`time_request`, `time_enabled`, `time_entry`,
  `notice_ack`) in the shared SQL store (SQLite, or Azure SQL with
  `ZF_STORE=mssql`), apart from case data, with portable DDL. Only the JSON demo
  store falls back to a local SQLite file (`ZF_TIME_DB`). Why the requester and
  the enabler differ: one role should not both propose and switch on monitoring
  of staff. The demo data has a single manager role, so enabling there needs a
  second user with the `Programme Support Officer` role (Entra app role
  `ZavaForward.SupportOfficer`); the status reason says so.
  `DPIA_APPROVED` rejects missing/blank values and bare `yes`, `true`, `on` or
  `1`, ignoring case and surrounding whitespace. Use a reference such as `D1`
  or `DPIA-2026-007`; valid references keep the existing whitespace trimming.
  Rejection prevents new enabling requests, activations, notice acknowledgements
  and time entries, even with matching historical controls; history is retained.
  Changing to a different valid reference still requires a new request and
  activation. This checks reference presence only, not authenticity or legal
  approval. Actual DPIA review, staff consultation, notice approval and
  administrator ratification remain human prerequisites, not results of this
  string check.
* Download any list for Excel, and check a spreadsheet: columns are matched
  for you, rows to fix are listed and the file is never changed.

* Finance, grants, sign-offs and resident decisions (FR-018, FR-019, FR-013,
  FR-014; code in `finance.py`, `grants.py`, `signoffs.py`,
  `resident_decisions.py`, `controls.py`):
  * Budgets, commitments, invoice or valuation intake, line-level match
    exceptions, payment holds and a Finance decision are recorded per case
    (`POST /api/cases/{id}/finance`, queue at `GET /api/finance`). Nothing is
    ever paid; payment status is a note. Unknown inputs (no budget, no
    milestone evidence) block a match.
  * Grant stages (opportunity, award, claimable, submitted, accepted or
    rejected, cash received) are kept apart from invoices, each with a source
    and a second approver (`/grant`; also shown in the funding list).
  * Assessment, design, building and coordination sign-offs by separate roles
    with a design version; a design change sends only the affected sign-offs
    back for human reassessment, and missing items join the "ready" checks
    once a design is recorded (`/technical`).
  * The resident's answer is recorded per measure with versions, pauses and
    withdrawals, starts as "Not recorded" and is never inferred; service and
    complaint requests carry a desired outcome, a redress owner and coded
    contact needs (`/resident`).
  * Whoever prepares an approval cannot give it, and these refuse any bulk
    request. Contractors get none of it and other staff roles do not see
    finance or grant detail.

## Conversation panel (issue #159)

An optional, collapsed panel on the case card ("Ask the assistant about this case") for staff roles that may chat.
It is never needed to finish a task: every ordinary control stays on the page and works when chat is refused or
the model is down.

* `POST /api/chat/threads/{id}/ask` returns `{kind, reply, citations, label, model, workflow_only}`. The logic is
  `zava_forward.core.chat_panel` (core); the provider call is `zava_forward.agents.chat.ChatModel` (agents),
  composed in `server.py` in process until #144. Thread storage, consent gate (`CHAT_DPIA_REF`,
  `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF`), redaction and per-user isolation are the merged #160 to #163 code.
* Every turn re-reads the staff role and the case through the user's own projection, so a revoked role or a case
  out of scope stops the next turn (403 or 404).
* Citations are ids of the projected case facts (`ZF-1/stage`). Uncited or unknown citations are dropped; with none
  left, or no case facts, the panel abstains and says so. Every reply carries "AI suggestion, not approved".
* A model failure (`disabled`, `timeout`, `provider-unavailable` or an unusable reply) returns `kind: fallback`,
  `workflow_only: true` and a plain message. A reply that carries tool or record-change syntax is withheld.
* `POST /api/chat/threads/{id}/proposals` with a `capability` calls the existing `Assistants.invoke`, so the request
  follows the existing source check and independent role review. The chat has no other write path.
* Web: `web/chat.js` (a `details` disclosure, a labelled form, an `aria-live="polite"` log and a `role="status"`
  line). Tests: `tests/test_chat_panel.py`, `core/tests/test_chat_panel.py`, `agents/tests/test_chat_model.py`.
* Not evidenced here: a screen-reader test (needs a manual run with a named reader), a live model run (no Azure
  endpoint locally) and real chat data (DPIA, lawful basis and notice references are unset, so storage stays refused).

### Staff chat hardening (2026-10-27, #157)

`GET /api/chat/status` returns the canonical special-category warning,
unapproved retention status and engineering caps for permitted staff only.
The question field remains disabled until its warning loads and uses
`aria-describedby`. A failed fetch has an explicit ordinary-workflow route.
Refusals announce the human route, not a misleading model-outage message.

Both `/ask` and legacy `/messages` use the cited panel; `/messages` retains
`reply`, `label`, `model` and `withheld` and adds the panel fields. Legacy
uncited answers and memory prompting are intentionally removed from that HTTP
route. Direct memory lifecycle/assembly remains separately testable and off by
default; neither HTTP route activates it. Sources are complete JSON, bounded
to 16,000 combined system/prompt characters, with at most 12 user questions /
4,000 history characters and a 1,000-character new question. Selected advisory
skill instructions count toward the same combined system/prompt cap.
Completion-time source checks apply the same skill filter as dispatch.
Oversize returns
workflow-only. There is one provider attempt, no retries, default 600 output
tokens. These caps do not approve role budgets, token prices, spend or expiry.

`ChatModel` requires admission before and after dispatch. The server requires
registered live authority and the existing continuity/release gate. No approved
conversational task/release exists, so general staff model calls remain denied;
synthetic privacy references cannot enable them. The regulatory offline
extractive path and independent proposal-review path are unchanged.

Each turn returns `consumption` and records one content-free `chat.turn` audit
event with calls, validated tokens or null/Unknown, outcome and bounds. A
post-call permission/case/thread rejection still records incurred consumption
but releases no answer. Changed projected sources withhold the completion.
Decoded answer text is checked for tool syntax as well as the raw JSON.
Consumption accounting is not a transactional exactly-once billing system:
process/storage failure remains an operational reconciliation requirement.

Local Chromium covers warning fetch failure, keyboard disclosure/submission,
focus return, refusal status, live-log attributes and 390px visibility:

```bash
# From src/api, after pip editable installs:
ZF_BROWSER_TESTS=1 PYTHONPATH=tests:../core/tests:../agents/tests \
  python3 -m unittest test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log -q
```

Default unit discovery skips this opt-in browser method; explicit execution
requires installed Chromium. The complete local RPI gate owns this exact case
in its required `browser` group with `ZF_BROWSER_TESTS=1`, verbose unittest
execution counts and a retained external log. Its exact ID/reason skip is
accepted only in API general discovery, never in the required browser stage.
The trusted command inventory and receipt verification enforce the selector,
flag and shared-fixture paths; unexpected skips still fail closed (Refs #572).
This is not a named human screen-reader test or
complete WCAG acceptance. DPO/Legal/provider/retention/access decisions,
independent held-out/serving-model/human evaluation, approved thresholds and
finite role budgets remain blockers. All five issues remain Refs, including
parent stabilization #440.

## Configuration

| Variable | Purpose |
| --- | --- |
| `ZF_STORE` | `json` (default), `sqlite` or `mssql` (Azure SQL, see below) |
| `ZF_SQL_SERVER`, `ZF_SQL_DATABASE`, `ZF_SQL_AUTH`, `ZF_SQL_CLIENT_ID`, `ZF_SQL_PORT`, `ZF_SQL_TRUST_CERT`, `ZF_SQL_TOKEN`, `ZF_SQL_USER`, `ZF_SQL_PASSWORD` | Azure SQL connection; `ZF_SQL_AUTH` is `msi` (default), `default`, `token` or `password` (CI container only) |
| `ZF_SQLITE`, `ZF_STATE`, `ZF_DATA`, `ZF_DIGEST_DIR` | database file, state folder, seed data, ledger digests |
| `ZF_AUTH` | `password` (dev, default) or `trusted-proxy` (Entra) |
| `ZF_ENV` | `production` refuses the password provider and the OSM tile default |
| `ZF_SESSION_KEY` | signs dev session cookies; set the same value on every replica |
| `ZF_ENTRA_TENANT_ID`, `ZF_TRUSTED_PROXY`, `ZF_ROLE_MAP`, `ZF_AUTH_EMAIL_FALLBACK` | Entra provider |
| `ZF_REASON_ROLES` | roles that may see a vulnerability reason |
| `ZF_TILE_URL`, `ZF_TILE_ATTRIBUTION` | map tile provider |
| `ZF_TIME_CAPTURE`, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION`, `ZF_TIME_NOTICE_APPROVED`, `ZF_TIME_DB`, `ZF_TIME_MIN_GROUP` | time capture |
| `ZF_DOC_STORE`, `ZF_DOC_DIR`, `ZF_BLOB_ACCOUNT_URL`, `ZF_BLOB_CONTAINER`, `ZF_BLOB_SAS`, `ZF_BLOB_CLIENT_ID` | document store |
| `ZF_SCANNER` | `local` (default) or `defender` content scanner |

### Employee briefing and Azure OpenAI settings

The employee `/api/briefing` uses all permitted open programme cases for the
existing manager roles, Retrofit Programme Manager and Programme Support
Officer (owner decision 2026-10-28). Today's briefing labels this scope
"All programme cases". Other staff receive "My assigned cases", selecting
only open cases whose `owner_code` exactly equals their business `code`.
Both scopes retain deterministic ranking and provide at most 8 cases to AI.
Workflow-only and fallback templates include at most the first 3 cases.
The panel shows the full permitted candidate count and the number included
for the final AI or template response. Cache hits recheck permitted IDs without
projecting list cards; misses summarize only the selected eight cases.
Existing case/role and field permissions still apply, including to model facts.
This does not grant consent, authorize work or approve an AI suggestion.

My cases and its assignment counts remain personal for every role. A business
role or permission to open a case never assigns that case to the user.
Entra uses the verified tenant and object ID; only one enabled matching roster
row restores its existing workload code. Email/display-name matching does not.
The 2026-10-25 synthetic baseline merge deliberately omitted staff rows.
An unbound Entra manager can therefore receive a programme briefing while
having zero personal assignments. An unbound non-manager retains an empty
assignment-only briefing. Check the authorized `/api/me` identity and
own/all queue totals before asking the programme owner to assign or hand off
work through the existing controls; do not infer assignments from a role/email.
The current signed-in owner's mapping was not inspected on 2026-10-27.

Focused synthetic JSON/SQLite regression and real-server browser label check,
from `src/api` with the project distributions installed:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest test_ai_tasks test_assistant_release -q
python3 -m checks.employee_briefing_browser_check
```

These are local engineering checks, not live Entra, SQL Server, real-model,
screen-reader or user acceptance.

Employee AI uses `zava_forward.core.ai.Ai`, not the separate resident
`ZF_DEMO_ASSISTANT_*` settings. Configure the employee API container as follows
only after the existing approval/activation prerequisites:

| Setting or prerequisite | Employee purpose |
| --- | --- |
| `AI_ENDPOINT` | Azure OpenAI HTTPS resource base URL, without `/openai/deployments/...`; required to configure employee AI |
| `AI_DEPLOYMENT` | Actual standard/fast deployment name; defaults to `standard` |
| `AI_DEPLOYMENT_STRONG` | Actual capable deployment name for stronger/document tasks; defaults to `capable` |
| `AI_MODEL_VERSION` | Released standard model identity as returned in the provider's `model` field; default `unattested` is not release attestation |
| `AI_MODEL_VERSION_STRONG` | Released capable model identity; defaults to `AI_MODEL_VERSION` |
| `AZURE_CLIENT_ID` | Attached user-assigned managed identity client ID used for token selection; not `ZF_SQL_CLIENT_ID` |
| Platform identity transport | Container Apps supplies `IDENTITY_ENDPOINT` and `IDENTITY_HEADER`; do not copy, print or manually provision their values |
| Identity and network | Selected identity needs Cognitive Services OpenAI User on the intended resource, and permitted DNS/network access to it |
| Per-task activation | Current matching human-approved release, evaluated configuration/model binding, budget/usage limits and no incident suspension; endpoint presence does not authorize dispatch |
| `ZF_AI` | `off`, `workflow` or `workflow-only` deliberately bypasses AI; the UI's workflow-only choice also bypasses it |

No API key or `AZURE_OPENAI_ENDPOINT` setting is read by this employee adapter.
The API version is currently `2024-10-21`. Missing `AI_ENDPOINT` returns the
labelled rules/template path with `AI is not configured`; model, network,
identity or release failures have separate fallback reasons. A template is
not proof that real AI ran. The source infrastructure's `enableApiAi` option
wires endpoint/deployments and API model access when deliberately enabled;
do not enable it or borrow the resident model's budget/release implicitly.

### Employee workspace asset recovery and redeploy

The selected route checks its required shared-script exports before rendering.
A missing file such as `/ops.js` shows its path and **Reload workspace**,
which refetches the document/scripts while keeping the case URL and session.
Ordinary API errors retain **Try again**, which retries without a page reload.
Unrelated map/specialist modules do not become prerequisites for ordinary cases.
No quality controls are silently omitted.

Read-only inspection on 2026-10-27 found
`ca-cutover-test-demo-api` in `ama`, revision `0000006` created
2026-10-25T12:18:25Z, using
`sha256:0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e`.
Its installed index already loads `/ops.js` before `/app.js`; deployed ops.js
SHA-256 `d28b705ffa88f386cb1b23ca4db9be93dd09d2bcbc6ea2fee3a4f12d0e466cd3`
matches source. It does not predate that wiring. Current source serves exact
files with JavaScript MIME, same-origin CSP, `no-store` and `nosniff`; no named
ops allowlist exists. A local constructed case named ZF-2026-0597 renders in
Chromium. This is not a read of the owner's case or proof of its live behavior.
Anonymous deployed `/app` is denied by platform authentication. The exact
original authenticated script HTTP/execution failure remains unproven: retain
the owner's browser Network/Console evidence for `/ops.js`, redirects/status,
MIME and CSP rather than calling this a confirmed missing-wire fix.
Safe deployed environment-name inspection found none of `AI_ENDPOINT`,
`AI_DEPLOYMENT` or `AI_DEPLOYMENT_STRONG`; no secret values were read.
The existing employee Foundry account `aif-cutover-test-rzsrg` advertises
`https://aif-cutover-test-rzsrg.openai.azure.com/` for the OpenAI API, but its
management-plane deployment list was empty on 2026-10-27. Setting that endpoint
alone is therefore insufficient: an operator needs separately authorized model
deployments and release evidence, or an explicitly approved replacement
resource, before configuring the two deployment names. The resident
`aoai-resident-469` resource and its budget are not an employee fallback.

An owner-authorized redeploy needs a newly reviewed immutable employee API
image built with `docker build -f src/api/Dockerfile src`, containing the
updated API web assets and core package. Preserve existing SQL/Blob/Entra
configuration, identities, probes and data. Configure the employee AI settings
above separately under its release/budget authorization if AI is wanted.
Then verify the exact serving digest, authenticated script responses/order,
case quality panel, own/all assignment counts, template reasons and (only when
approved) a registered real-model task. These source/local checks neither
deploy nor satisfy Azure, human or whole-issue acceptance.

Focused synthetic regression from `src/api`, with installed dev distributions:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest test_ui_support test_auth test_ai_tasks -q
python3 -m checks.employee_workspace_browser_check
```

### Entra ID on Container Apps

Code: `auth.py`. The current demonstrator uses this provider in Azure;
the owner confirmed working workbench sign-in on 2026-10-12. Local tests and
provisioning checks do not substitute for each user's consent/acceptance.

* Create an app registration (single tenant) and define app roles whose values
  match the map (default `ZavaForward.Coordinator`, `.LiaisonOfficer`,
  `.ProgrammeManager`, `.Contractor` and so on, see `DEFAULT_ROLE_MAP`) or
  supply `ZF_ROLE_MAP` JSON. Assign users and groups to them.
* Enable built-in authentication on the Container App with "require
  authentication" so unauthenticated requests are blocked, and make the ingress
  the only route to the container so `X-MS-CLIENT-PRINCIPAL` cannot be forged.
* Set `ZF_AUTH=trusted-proxy`, `ZF_TRUSTED_PROXY=1`, `ZF_ENTRA_TENANT_ID` and
  `ZF_ENV=production`. The platform principal type must be `aad` or `Bearer`,
  from that tenant, with exactly one distinct mapped role; the role comes from
  the validated platform principal, never the staff file.
* Provision each staff record with the Entra object id (`oid`). Email matching
  is off unless `ZF_AUTH_EMAIL_FALLBACK=1`. Contractor guests need the same.
  Use the [tenant staff initializer](../../infra/README.md#tenant-staff-and-application-role-initialization)
  to reconcile enabled tenant members, app roles and SQL bindings together.
  It replaces current generated staff/owner labels while preserving workload
  codes and historical actors, then restarts the startup-cached roster.
  Assigning an enterprise-app role without this binding still fails closed.
* Sign-out redirects through `/.auth/logout` to the public welcome;
  "Use another account" instead enters `/sign-in?switch=1` directly with
  `prompt=select_account`, without signing out of Microsoft first. Choosing
  another account is deliberate, not automatic; cancelling need not clear
  the previous session. See [flow diagnostics and acceptance](../../infra/README.md#account-selection-and-safe-flow-diagnostics).
  State-changing requests need an
  `X-ZF-CSRF` header under this provider.

The public `/` page shows Zava Forward and its logo without loading workbench
scripts or data. Its button enters `/sign-in`; `/app` is protected. Production
session/role failures show Microsoft sign-in or an authorisation message,
never the local shared-password form.

The native account panel shows the authenticated Entra display name/email,
existing workbench role and own Microsoft profile photo. It does not rewrite
synthetic staff records or broaden contractor projections. Escape/outside
click closes the panel; keyboard focus and a 375-pixel layout are supported.
Missing photos/access errors display initials and an explicit status.

`/api/account/photo` authenticates and authorises the current user before
fetching the fixed Graph `/me/photo/$value` URL. The delegated platform token
stays server-side, redirects are refused, and timeout/type/signature/2 MiB
limits apply. There is at most one provider refresh attempt for token expiry.
See [staged token-store setup and permissions](../../infra/README.md#public-welcome-and-microsoft-account-photos).
This uses only delegated own-user `User.Read`, not tenant-wide application
photo access. Local password development shows initials without requesting
Microsoft tokens.

The CSP permits temporary `blob:` URLs only for images, so the server-proxied
photo can render; script/default/frame source permissions are unchanged.

## Run it locally

The working data is built from the private stock-geography register. It holds
real OpenStreetMap addresses with invented residents, contractors and staff, so
it is git-ignored, binds to loopback only and must never be committed, deployed
or shared. The repository must stay private.

```bash
python3 -m pip install --no-deps -e src/core -e src/agents -e src/api   # modules moved in M1 to M5 (ADR 0006)
python3 support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py --seed 20260901   # writes to ZF_DATA, default ~/.zava-forward/data/zavaforward.json
ZF_PASSWORD=choose-a-password python3 -m zava_forward.api
```

Open `http://127.0.0.1:8088` and sign in with a staff email from the data (for
example `aisha.rahman@zavanorthhomes.example`). Without `ZF_PASSWORD` a random
password is printed at start-up. The data builder shifts all dates so the
history ends today and prints no real personal data.

## Honest limits

Current scope is the continuing exercise, not production acceptance. Dated
earlier observations remain in the ADRs and pinned #58 evidence; they must not
be read as the current deployment state. The
[current infrastructure handover](../../infra/README.md#current-exercise-handover-2026-10-13)
records the tested/deployed image and identity initialization.

* The data is constructed. The generator (`zf_names.py`, `build_mvp_dataset.py`)
  makes names, phone numbers on Ofcom drama ranges and example email domains.
  The product screens do not say so; this README and the repository do.
* The 2026-10-12 rebuild ran the retained 980-case programme on real Azure SQL
  with workload-identity reads/writes, both real model tiers and restart
  persistence checks. Blob is the configured evidence store. Generated stock
  remains 60,000 homes; it is not 60,000 live SQL programme cases. No Azure
  load, full recovery, backup-restoration or production acceptance is claimed.
* Shared-password sign-in remains local development only; production rejects
  it. Azure uses built-in Entra authentication, app roles and explicit SQL
  staff bindings. The owner reports working administrator/Coordinator sign-in.
  A tenant-member Contractor allocation now exists, but browser acceptance
  for all roles, B2B guests, own photo and actual different-account replacement
  remains unproved. Unit principals and an anonymous chooser are not that proof.
  Contractor status text can still mention a safety stop and free-text notes
  are not redacted.
* AI needs `AI_ENDPOINT` (and optionally `AI_DEPLOYMENT`,
  `AI_DEPLOYMENT_STRONG`) and a managed identity with the Cognitive Services
  OpenAI User role. Both model tiers were exercised with `source=ai`; a
  template result alone is not real-inference acceptance. Nothing is
  sent; there is no live integration with housing or repairs systems.
* In development the map loads tiles from tile.openstreetmap.org unless
  `ZF_TILE_URL` is set. No licensed provider has been chosen or tested.
  The live demo app has `ZF_TILE_URL` set to the public OSM tile URL under a
  scoped, time-limited owner approval for synthetic data only (see
  [infra README](../../infra/README.md)); that is not a production provider choice.
  See the
  [tile provider options review](../../docs/reference/research/ux/map-tile-provider-options.md)
  (#119) for dated, unverified-where-stated licence, cost and privacy options.
* Local development defaults to local state/documents; Azure selects the
  SQL/Blob backends through configuration. Do not apply local-disk durability
  claims to that deployment or infer tested Blob restoration/erasure from
  configuration alone. Upload checks are an extension list and a size cap:
  no content sniffing or malware scan. Local files/digests on Container Apps
  remain ephemeral and do not establish external immutable audit anchoring.
* Scale: the in-memory store handles 60,000 synthetic cases for filtered pages
  in tens of milliseconds (about 0.6 s for the first, cold ranking build). The
  sqlite store answers list pages, search, sorts and counts in SQL at 60,000
  cases in roughly 50 to 150 ms on a development machine. These are dev
  machine figures, not production latency, and not Azure SQL.
* The ranking policy is a hash-checked file but not signed off: no named
  owner yet. The hash detects edits, it does not prove who approved them.
  Snapshots are written when a manager requests one and the data has changed,
  as a file, not on every change or in a database table. The as-of date is the
  date the store was first loaded, and day counts come from the stored
  `days_in_stage`, not recomputed from it. AI value against the deterministic
  order is only captured as the overlap on each recommendation record.
* SQL Server parity tests and live Azure SQL checks supplement sqlite tests;
  neither establishes production scale or every full-workflow requirement.
  Lists, search, sorts and counts
  use SQL, but case detail, map, statistics, visits, facets, the CSV export,
  the closed list and every write still use the in-memory copy that is kept
  in step with the database. Keyset paging covers the default sort only.
* Quality and procurement: checklists are examples, not signed-off standards;
  there is no contractor login to submit evidence (a staff member records it on
  their behalf); capacity is counted in homes, not hours or money; procurement
  data is one document, so two managers writing at once get a conflict and
  retry; the screens were syntax-checked and exercised through the API, not
  run in a browser or with a screen reader.
* Time capture is enabled by environment references plus a requested and
  separately enabled audited action; the screens were exercised through the
  API, not in a browser. The staff notice text is a draft and the
  consultation reference is a flag, not evidence of the consultation. The AI
  evaluation uses a scripted model, so it checks behaviour, not model quality:
  latency, run-to-run variation and added value are scripted figures, not
  live-model measurements, and the golden cases are small and constructed.
  Citations prove a cited fact exists in the case, not that the claim made from
  it is right, and document reading cites the document record, not a passage.
* Browser checks: `src/api/checks/browser_check.py` drives the real server with
  Playwright (login, list with rank and reasons, show more, return, reopen,
  map list). It is run by hand, is not in the unittest run or CI, and was
  run in desktop Chromium only. No screen reader or mobile run was done.
* The Dockerfile pins a base digest and runs as UID 10001 with no data baked in.
  Versioned images have been deployed; MVP CI test/image/mssql jobs and both
  validation workflows passed for source head `8ca4a3d` on 2026-10-13.
  The deployed account-switch image is linked in the infrastructure handover,
  not assumed rebuilt from later documentation-only commits. Future edits need
  their own checks; a scorer's successful execution is not product acceptance.
* Finance and sign-off rules are a proposal on constructed data: the role
  mapping (for example Quality Inspector for assessment) is a stand-in for the
  PAS 2035 roles, matching is simple exact comparison, amounts are not tied to a
  real ledger, there is no supplier or contract master, and the screens were
  syntax-checked but not run in a browser or with a screen reader. The product
  now has the closed administrative bulk contract described above; controlled
  finance/sign-off approval refusal remains independent of that allowlist.
* Retention periods and legal bases remain proposals for the DPO and Legal.

## Container hardening checks in CI

The `image` job in `.github/workflows/mvp-ci.yml` builds the image and checks:

* it runs as UID 10001 and contains no working data;
* it starts and answers `/healthz` with `--read-only --cap-drop ALL
  --security-opt no-new-privileges`, with only `/tmp` and `/state` (`ZF_STATE`)
  mounted as tmpfs, the seed data mounted read-only, and writes to `/state`
  succeed while writes to `/app` and `/` fail;
* a Trivy scan fails the job on any HIGH or CRITICAL finding that has a fix
  available (`ignore-unfixed`). Unfixed findings in the pinned Debian base are
  not blocked, so they are visible in a local `trivy image` run but not
  gated. The fix for a fixable OS package is the `apt-get upgrade` in the
  Dockerfile, never an ignore file;
* an SPDX SBOM (`zavaforward-mvp-sbom` artifact) is generated and uploaded.

Actions are pinned by commit SHA. The workflow result on GitHub is what proves
these checks; running the same commands locally is only a preview. Document
files default to `ZF_STATE/docs`, or set `ZF_DOC_DIR`; the app writes nowhere
else. The SQL Server integration job is not part of this job.

## Tests

```bash
cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -v
(cd ../orchestrator && PYTHONPATH=../core/tests python3 -m unittest discover -s tests -v)
```

The tests also cover the SQL store (including `test_sqlreads.py`), documents, ledger, role matrix, workflows, auth and time capture. They use small fixtures and a generated 60,000-case dataset, and need no
private data. The AI tests use a scripted model or the template path (no network).

Browser check (needs python3 playwright and chromium, and the built dataset):
`python3 src/api/checks/browser_check.py` (the dataset at `ZF_DATA`).

## Regulatory alert and home chat UX (#215)

Synthetic development only under ADR 0005, accepted on 2026-10-16. The home
view now presents `/api/law/alerts?case=<id>` outside the optional chat. Each
visible alert shows what was noticed, source ID/status/effective/retrieval
dates, safe action, decision owner, clock and recorded due time. Latest check
and current-control status distinguish retained breach risk from an active
control. The browser does not calculate statutory deadlines, acknowledge
alerts, release holds or alter approvals. No visible alerts is not a safety
or compliance conclusion. Coverage stays unknown when the service says unknown
or cannot be reached. Refresh failures remove old results rather than present
them as current.

The existing bounded regulatory chat renders source excerpts, home facts,
unknowns, safe next action and human decision owner as separate sections.
Source quotations and stored evidence are unchanged. Plain-language
explanations are on by default and can be toggled with a labelled checkbox;
they explain the interface, not the law. Provision links open a source record
in a new tab, with an explicit warning. Missing sources, unsupported terms,
disabled lookup and outages have visible text and a human route, not a silent
success. Source excerpts retain snapshot/currentness and truncation caveats.
The existing doubt action sends the actual turn to Juan Manuel Servera's
synthetic exercise inbox; its receipt is not legal approval or a resident
message. Failed referrals are explicit and retryable.

### Synthetic completion boundary (2026-10-27, #208)

Supported conflicts now automatically reach the named exercise inbox with
both source versions, the original question and a durable sender receipt.
Automatic/manual routing deduplicates one stored thread/turn, not repeated ask
requests. History restores the actual receipt and marks the doubt button sent;
no human decision or legal resolution is implied. Sender/recipient provisioning,
role and case scope are rechecked inside the transaction. Trusted-proxy referral
also requires the recipient's separately recorded chat capability; actual
tenant assignment remains unverified, not inferred from a job title.

Chat displays calls per question (zero), current-role/UTC-day recorded outcomes,
the zero inference allowance and explicit Unknown service cost. Alerts display
zero calls per deterministic check/alert; historical records without metadata
say usage was not recorded. These are not quotes, spend authorization or staff
benefit measurements. The bounded `/usage` result is audit-only, potentially
partial, never an exact total; see the [core consumption contract](../core/README.md#offline-regulatory-consumption-2026-10-27-208).
Usage follows the existing draft DPIA/retention/access controls, not a new
retention exemption.
After an answer is shown, the lookup clears unchanged submitted text and
re-enables its control without waiting for the background usage refresh.
A failed refresh reports unavailable usage separately; it does not replace
the answer or block the next question.

The local pinned-axe harness exercises automatic conflict routing/restoration,
usage, keyboard/plain mode, seven staff roles and supplier denial, 320/390/1280
widths, enlarged text, reduced motion and failure paths. This is scoped browser
engineering evidence, not WCAG conformance or repairs/housing/grants
comprehension acceptance. All original human/live criteria remain unmet.

### Audience patterns and delivery boundary

These patterns follow the [regulatory literacy research](../../docs/reference/research/ux/regulatory-literacy-for-journeys.md),
not validated staff needs or new legal advice. Role guidance never grants
access: existing server projection and alert audiences still govern every read.
All staff see data-minimisation guidance and the named exercise doubt owner.

| Issue audience | Know at least / alert pattern | Home-chat and doubt pattern | Existing account / evidence boundary |
| --- | --- | --- | --- |
| Repairs and intake, including housing/contact staff | Recognise a possible damp, mould or emergency report; record awareness without guessing; use the human hazard route without waiting. Show the recorded clock and safe action, not an inferred legal deadline. | Ask for hazard sources and recorded home facts; uncertainty goes to the human safety service and exercise owner. | Resident Liaison Officer guidance and scoped hazard alerts exercised locally. There is no distinct repairs account or validated operational procedure. |
| Building Safety | Categorisation, recorded clocks and independent evidence need human judgement; completion is not assurance. | Compare cited source records; interpretive questions go to Juan Manuel Servera as exercise owner, never to an automatic hold release. | Building Safety Liaison guidance exercised; existing owner capabilities are unchanged. |
| Assessor and coordinator | Appointed PAS roles, risk path and independent evidence matter. Only an overview is held; licensed text and contract incorporation are unverified. | Identify the missing licensed/contract source and ask the appointed coordinator/Compliance; no invented PAS requirement. | Retrofit Coordinator and Quality Inspector guidance exercised. No separate assessor role is created. |
| Programme | A policy target is not a duty in force, completed task, investment approval or award. Read source status and dependencies. | Source lookup may inform a proposal; applicability, source conflict and approval stay human. | Retrofit Programme Manager and Programme Support Officer guidance exercised. |
| Finance and grants | Obtain the actual award letter/agreement; an allocation annex does not authorise a claim or commitment. | Requests for binding grant/contract terms have no supported answer without the actual document; refer to funding owner/Finance, with exercise legal doubt to Juan Manuel Servera. | Grants and Evidence Officer guidance exercised; no new financial approval or grant lookup capability is claimed. |
| Data handlers | Purpose limits, sensitive health/vulnerability data, consent versus other lawful bases and meaningful human involvement in significant decisions. | Do not type personal details; use bounded automated-decision source lookup where supported and the exercise DPO doubt route. | Cross-cutting guidance for all seven staff account roles exercised. No new data-handler access role. |
| Suppliers | Follow agreed contract/scheme requirements; contract and TrustMark terms are not held. Obtain them from the named contact/contracts manager. Safety intake cannot wait. | Staff chat is unavailable; named-contact human route in the supplier home view. A supplier chat/alert interface remains design-only. | Existing Contractor view guidance exercised; law/alert/chat endpoint denial retained. No supplier rights added. |

Supplementary design-only patterns: leasehold-service staff must obtain the
actual lease and Legal review before explaining responsibility. Residents and
representatives need a human-reviewed plain explanation of choices, safe
contact, complaints/redress and a non-digital route, not a legal-duty lesson.
Neither audience receives a new chat interface or invented source in this slice.

### Local engineering checks

Unit discovery requires only the installed runtime distributions, not Playwright
or a browser. The regulatory and capacity harnesses import their browser APIs
only when browser operations run; target-size boundary, axe-integrity and capacity
scanner-result assertions always run in the unit suite. Subprocess regressions
also block Playwright imports even when the dev extra is installed; the capacity
regression executes all four scanner/pin tests under that blocker and confirms
browser execution still fails explicitly without Playwright. From the repository root:

```bash
python3 -m venv /tmp/v215c
/tmp/v215c/bin/pip install -e src/core -e src/agents -e src/api
(cd src/api && PYTHONPATH="$PWD/../core/tests:$PWD/../agents/tests" \
  /tmp/v215c/bin/python -m unittest discover -s tests -q)
```

Install `src/api[dev]` in that venv before running Ruff, mypy or browser checks.
Playwright stays dev-only; asking to run a browser check without it fails
explicitly rather than skipping browser coverage.

The browser check uses the actual loopback HTTP app, SQL case store, law store
and wholly constructed `regulatory_fixture` data. It does not read `ZF_DATA`
or private working files. Provider calls are blocked; browser network access
outside loopback is aborted. A pinned local axe script runs inside Chromium;
no application content is sent to the download host. From the repository root,
after installing the project distributions and API dev extras with pip:

```bash
python3 -m playwright install chromium
curl -fsSL https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js \
  -o /tmp/axe-4.10.3.min.js
export PYTHONPATH="$PWD/src/api/tests:$PWD/src/core/tests:$PWD/src/agents/tests"
python3 src/api/checks/regulatory_ux_check.py \
  --axe /tmp/axe-4.10.3.min.js --out /tmp/regulatory-ux-results.json
python3 -m unittest test_regulatory_chat_api test_rule_alerts test_chat_panel \
  test_chat_isolation test_accessibility_baseline test_design_system test_role_matrix -q
(cd src/api && python3 -m unittest test_regulatory_ux_check -q)
(cd src/api && ruff check . && ruff format --isolated --line-length 100 --check checks/regulatory_ux_check.py && mypy)
```

The check verifies the axe 4.10.3 SHA-256 before execution:
`880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`.
API tests precede core tests in the absolute `PYTHONPATH` to avoid colliding
test module names. Checks cover WCAG 2.2 A/AA axe tags on the changed surfaces,
native Enter/Space controls, Tab/Shift-Tab traversal, visible focus, post-answer
and doubt focus, text statuses, 320/390/1280px reflow and 200% text sizing.
Every exercised state also measures visible enabled controls, links and
disclosure summaries: at least 24px width/height, preserving the cited-lookup
summary's stronger shipped 44px height. Citation links now have a 24px
inline-block target rather than an 18px inline text box. The supplier guidance
is static and has no interactive targets.
Two further cited-answer states (`cited-answer-fade-35pct` and `-50pct`) re-enable
the lookup button, freeze its transitions part-way and scan it, because a
disabled-to-enabled background fade with an instant text colour change produced
a transient 4.29:1 `color-contrast` failure on hosted runners (#151, refs only).
Buttons now transition only `border-color`; `--motion` and its reduced-motion
override are unchanged. This covers the lookup button, not every control.
The test also checks persisted doubt/history, missing sources, retained risk
after source change, service outage, disabled lookup, staff guidance and
contractor denial. It is an engineering check, not a complete WCAG conformance
assessment, human screen-reader test or operational release gate.

Observed locally on 2026-10-16: 17 axe states had zero detected violations;
eight states retained `color-contrast` incomplete results for textareas whose
background axe could not establish (reported as partially obscured). Those
results require further assessment, not a pass declaration. Keyboard traversal,
focus and reflow assertions passed. The 86 targeted API and 33 core regression
tests, API ruff/format and strict mypy passed. These observations do not satisfy
the full WCAG criterion or the staff comprehension criterion.

The `src-api` job in [source CI](../../.github/workflows/src-ci.yml) now runs
this UX regression check next to `checks.design_system_browser_check`, using
the same installed Chromium and an absolute API/core/agents test path.
It fetches the pinned axe version with bounded retries/timeouts; the harness
verifies the SHA-256 before executing it. A failed download emits a CI warning
and omits only axe, never the target-size, keyboard, reflow, role or local API
assertions. Supplied wrong-hash content fails rather than downgrading. JSON
results explicitly record axe execution/skipping and are uploaded as
`regulatory-ux-results`. To run without axe locally:

```bash
python3 src/api/checks/regulatory_ux_check.py --out /tmp/regulatory-ux-no-axe.json
```

Review follow-up on 2026-10-16: the exact new CI shell block passed locally both
with a successful download and a deliberately failed curl. Both paths checked
142 targets across 17 states, minimum measured width/height 24px; cited-lookup
summary height 44px. The axe path retained the same eight contrast incompletes.
Deleting `.regulatory summary{cursor:pointer;min-height:2.75rem;padding:.5rem 0}`
from the served stylesheet failed the actual browser check at `cited-answer`:
the summary measured 1198 x 24px, below its 44px design floor. Restoring the rule
passed both CI paths. The unstyled 24px summary alone is not an AA violation;
the stronger assertion protects the existing intended target. Three harness
unit tests also cover 24px boundaries, static supplier content and corrupt axe.
The subsequent CI import-boundary repair adds a fourth harness test that
rejects any discovery-time Playwright import, without skipping those assertions.
After merging current main, the runtime-only `/tmp/v215c` environment reproduced
the eager-import failure. With browser imports deferred, all 561 API tests pass
(110 opt-in skips), both before and after installing Playwright 1.64.0.
API Ruff/format and strict mypy pass; both source CI browser harnesses pass
against the synthetic loopback app. Regulatory results remain 17 states,
142 targets, zero detected axe violations and eight incomplete contrast states.
The 86 targeted API and 33 core tests, design-system browser check and API
ruff/format/mypy passed. Hosted CI is pending, not claimed passed: the owner
requested push without waiting. Full issue acceptance remains unchanged.

### Staff comprehension protocol (Not run; unmet)

Before actual staff use, obtain participant/research authorization and privacy
review from the relevant real owners; the exercise owner decision does not
provide these. Recruit at least three authorised participants from each of
repairs, housing and grants, including keyboard/assistive-technology users where
possible. Obtain informed voluntary consent, accessible/non-digital instructions
and the right to stop. Use only fictional homes, sources and exercise identities.
Do not record actual resident information, private staff identifiers or unconsented
audio/video. Agree storage, access, retention and deletion before collection.

Give each participant the same five tasks without legal coaching: recognise an
urgent hazard while chat is unavailable; identify noticed/source/status/action/
owner/clock; distinguish future/unknown evidence from an active control; handle
a missing grant/contract source without inventing terms; and route a doubtful
turn and explain what its receipt does not approve. Counterbalance deterministic
cards with provision links against chat on equivalent fictional tasks. Record
task success, unsafe actions, source/status/owner comprehension, completion time,
assistance, accessibility barriers and confidence, using anonymous study codes.

Predeclare success as at least 90% correct required answers overall and at least
80% in each participant group, with zero critical errors (delayed hazard intake,
invented approval/consent/terms, future-as-active duty, or a claim that a doubt
receipt establishes compliance). Two reviewers independently score against a
frozen answer key; reconcile disagreements with reasons. Report denominators,
failures, group differences and uncertainty, not just averages. Small formative
samples cannot establish generalised staff comprehension or chat value.
Stop a task immediately if real personal information or a safety misconception
appears; explain the safe route, record the failure and revise before a new
approved round. The human owner reviews results before any staff-use decision.
No participants were tested here; no comprehension result or chat-value pass is
claimed.

### Issue criterion audit

| #215 criterion | Local disposition | Evidence and remaining gap |
| --- | --- | --- |
| Patterns defined per role with know-at-least content | Met as synthetic design/implemented existing-role guidance | Seven-audience matrix above, real role-loop browser assertions and supplier human-route/denial check. Separate repairs, Finance, resident and supplier-chat journeys are not delivered or user-validated. |
| Each alert states noticed/source/status/safe action/owner/clock | Met for the existing scoped alert contracts | Browser asserts required fields against a real SQL-backed breach-risk alert; current-control state, empty visibility and outage are explicit. No new rule coverage is claimed. |
| WCAG 2.2 AA, no colour-only status, keyboard, plain language | Partial; full criterion unmet | Automated axe and keyboard checks cover changed surfaces, textual statuses, focus, toggles and reflow. Comprehensive manual/assistive-technology conformance remains unassessed. |
| Doubt and no-source states explicitly designed | Met in bounded synthetic slice | Persisted exercise inbox receipt, visible unsupported/missing-source state, disabled/outage text and manual owner route. No real owner notification or approval claimed. |
| Comprehension tested with repairs, housing and grants staff | Unmet / Not run | Protocol only. Actual staff testing is unavailable and remains required before use. |

No issue checkboxes are changed by this implementation. Real delegates,
verified applicable sources, operational acceptance and the ADR 0005 measured
chat-value ship test remain open.

### Affected-person challenge API and workbench (#220)

`POST /api/cases/{id}/resident` reuses the existing authenticated resident action
route for `challenge_open` and `challenge_resolve`. See the
[core field and version contract](../core/README.md#version-bound-affected-person-challenges-220).
The permitted case response includes `challenge_targets` and retained
`affected_challenges`; neither is exposed without both existing resident-view
and recorded-reason entitlements. Client actor/time overrides are rejected.
SQL validates current identities, target/human-decision tokens and correction
dependencies again at writer time. A saved operation whose acknowledgement
cannot be projected/encoded is explicitly reported as HTTP 409 with
`outcome: "committed"`; do not blindly retry it.

The case workbench uses labelled native forms for supplied Digital or
staff-recorded Phone/Letter/In person evidence, a named human owner, explanation,
manual route, next update and terminal supplied resolution. It preserves unsaved
drafts and their original version bindings across unrelated case refreshes,
warns on navigation and confirms correction recording. Stale suggestions and
historical human reviews have explicit text rather than colour-only status.
No resident consent, refusal, sanction, remedy outcome, unrelated closure or
safety-clock change is inferred; urgent safety intake must not wait for a
challenge.

History is paged in bounded windows of 50 with keyboard-operable Older/Newer
controls and URL-bound page state. Every retained target and open or resolved
challenge remains reachable; the window is not a retention or action cutoff.
The suggestion-reference field accepts an exact retained reference, with
suggestions from the visible page. Browsing suggestions preserves the opening
draft and its original binding; leaving a page with an unsaved resolution asks
before discarding it. A refresh can move a dirty resolution outside the current
50-record window; its original form stays inside guarded challenge history,
with its values and version binding intact. Cancelled paging preserves it.
Confirmed paging discards it before drawing the destination page, so a record
never has two resolution forms or competing label targets.

The issue-specific browser check runs the actual app against an isolated public
synthetic SQLite fixture, with loopback-only traffic and no model call:

```bash
PYTHONPATH=src/core/tests:src/agents/tests:src/api/tests:src/api python3 \
  src/api/checks/challenge_browser_check.py \
  --axe /path/to/verified-axe-4.10.3.min.js --out /tmp/challenge-browser.json
```

The pinned axe content hash is checked against the existing regulatory browser
harness. Checks cover keyboard entry/error focus, cancelled navigation and
correction, unrelated-refresh draft retention, permitted/denied views, expanded
forms at 320/390/1280px, target sizes and reduced motion. Automated checks are
scoped engineering evidence, not comprehensive WCAG, screen-reader, resident or
human acceptance. The unchanged full gate's native SQL selectors are general
regression, not issue-specific native SQL challenge acceptance.

Add `--history` to the same browser command for the historical regression. It
creates 52 actual workflow-only targets and 52 HTTP-recorded challenges, then
opens a new challenge against the oldest target, resolves the oldest open
challenge, reads an older resolved explanation, checks exact selective
invalidation and denied projections, and reloads the URL-bound bounded pages.

Add `--navigation` instead to delay a committed challenge POST acknowledgement
while confirming navigation to another case and to the list. The write is
neither cancelled nor retried. The form captures its dispatch route signal and
does not refresh the old case after that route is aborted.

Fields remain editable during a pending challenge opening or resolution POST.
Success compares their current values with the submitted snapshot. Later edits
remain in the original guarded draft with explicit feedback that only submitted
values were recorded. The submit button stays disabled, and even an implicit
or programmatic submit cannot duplicate the pending or acknowledged write.
Neither cancellation nor automatic retry is used for a committed write.
Add `--pending-draft` to the same browser command for delayed-acknowledgement
opening and resolution regressions: compare submitted versus retained values,
actual persisted evidence, live feedback, navigation guard and exact write
counts. This is synthetic browser evidence, not human acceptance.

Add `--refresh-draft` instead for the 50-to-51 refresh/paging regression. It
retains the actual dirty CH-1 form across a newly recorded challenge, checks
unique form/input IDs and native label targets, cancels the guarded page change,
then explicitly confirms discard and navigates older/newer history. Only the
new opening writes; paging never resolves or retries a challenge.

Priority generation, latest and review responses retain correct stale/actionable
flags but withhold `challenge_ids` unless the requesting reader currently has
both resident-information and recorded-reason rights, even for policy corrections
on another case.

## Synthetic resident feedback preview (#444)

A separate, read-only, loopback-only web page for owner feedback on what a resident could see.
It is invented data only: not enrolment, not a live service and not an approved resident design.
The staff `server.py`, `auth.py`, projection and store are unchanged and are not imported.

Build a disposable fixture and start one server per subject from a clean environment. The
start-up guard refuses any `ZF_`, `AI_`, `IDENTITY_`, `MSI_`, `AZURE_`, `MSSQL`,
`APPLICATIONINSIGHTS`, `OPENAI` or `SQL` variable:

```bash
pip install -e ../core -e ../agents -e .
env -i PATH="$PATH" HOME="$HOME" python3 -m zava_forward.api.resident_preview --build-fixture /tmp/ama-444-preview-data
env -i PATH="$PATH" HOME="$HOME" python3 -m zava_forward.api.resident_preview \
  --data-dir /tmp/ama-444-preview-data --subject SYN-RES-A --port 8444
```

* Identity is the `--subject` this server process was started with. No password, role selector,
  cookie, header, query or path value chooses who is viewing, and resident routes take no case id.
* Routes: `/` page, `/resident/view` JSON, `/resident/about` limits, `/healthz`. Writes return
  405. Messages, uploads, downloads, appointment replies, consent and AI return 403 and the page
  shows them as unavailable. `/api/*` and every staff route are 404.
* The Host header must be a loopback name with the bound port. Only `127.0.0.1` or `::1` binds.
* The grant file is re-read on every request, so revocation and expiry apply to the next request.
  Malformed, ambiguous, unknown or unlisted grants deny.
* Subjects: `SYN-RES-A` (confirmed appointment), `SYN-RES-B` (offer only), `SYN-REP-B`
  (confirmed representative, receive information and attend), `SYN-REP-WRONG` (grant names a task
  the domain record does not confirm), and the denied `SYN-RES-EXPIRED`, `SYN-RES-REVOKED`,
  `SYN-RES-AMBIG` and `SYN-RES-NOGRANT`.
* Tests: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests/test_resident_preview_api.py`
  (real local server, authorization and isolation) and `python -m checks.resident_preview_browser_check`
  (Chromium on the real server: keyboard, focus, error, 320 px reflow, reduced motion).

Limits: the preview is not WCAG conformance evidence, not an external accessibility audit and
not live Azure, SQL or AI acceptance. See the [core boundary](../core/README.md#resident-owned-preview-boundary-444).

### Threat model for the synthetic preview (#444)

This section states what the preview protects, what it trusts, and what it does not defend
against. It is documentation of the existing design, not a security certification, not an
authentication design and not an approved resident design. Evidence is labelled
`test` (a named existing test exercises it) or `inspected` (read in the code, not tested).

Scope and non-goals:

* A loopback-only, read-only, synthetic feedback page for the owner. It is not suitable for
  public hosting, tunnels, shared hosts or real residents, and it has no password, session, TLS
  or account system by design.
* A cloud showcase is separate work (issue 462). It needs its own cloud composition, identity
  and review. It must not relax the loopback, environment and path guards described here.

Assets and trust boundaries:

* Protected: staff-only case data (notes, safeguarding, finance, staff identifiers, chat,
  memory, other homes and cases) and the grant fixture. Shown: only the allowlisted resident
  fields (home, measures, progress, next step, appointments, help).
* Trusted, server-owned: the start-up arguments (`--subject`, dataset, fixture), the process
  environment and the files on disk. Untrusted: every HTTP request and any text inside dataset
  fields.
* Actors considered: the owner starting the process, another user or process on the same host,
  a web page on another origin, and a request with a forged Host, subject, path or method.

| Threat | Control | Evidence |
| --- | --- | --- |
| Viewer claims another identity (header, cookie, query, path) | Identity is only the process `--subject`; routes take no case id | test: `test_claimed_identity_is_ignored_everywhere`, `test_server_owned_identity_each_process_shows_only_its_own_case` |
| Reading another case or staff data | Positive allowlist view built field by field; no staff payload or `projection.py`; staff routes absent | test: `test_every_view_is_canary_free_and_isolated`, `test_new_staff_field_stays_hidden_until_mapped`, `test_staff_routes_do_not_exist`, `test_every_response_body_is_canary_free` |
| Missing, unknown, expired, revoked, not-yet-valid, ambiguous or malformed grant | Default deny on every request; the grants file is re-read each time | test: `test_denials`, `test_expiry_applies_at_the_next_request`, `test_revocation_applies_at_the_next_request`, `test_malformed_grants_deny`, `test_denied_subjects_get_403_and_no_data` |
| Representative without current authority | Domain authority record checked per task and measure; malformed record denies | test: `test_valid_representative_sees_only_covered_tasks`, `test_no_current_authority_denies`, `test_malformed_authority_record_denies_not_crashes`, `test_representative_and_wrong_authority` |
| Offer shown as a confirmed arrangement, or unknown shown as known | Only `Committed` is confirmed; other states are offers or counted unknown; unmapped stage stays unknown | test: `test_resident_b_offer_is_not_a_confirmed_arrangement`, `test_ended_or_paused_offer_is_not_shown_as_a_live_offer`, `test_unknown_appointment_state_is_counted_not_confirmed`, `test_progress_text_is_mapped_and_unknown_stays_unknown`, `test_booked_stages_do_not_claim_a_booking` |
| Use of messaging, uploads, downloads, consent or AI | Those paths return 403 for every method and the page shows them as unavailable | test: `test_unavailable_features_are_server_denied_for_every_method` |
| Writes or store mutation | Known routes reject non-GET methods with 405; the view never mutates; the store is a private temporary copy | test: `test_writes_are_refused_and_store_unchanged`, `test_view_does_not_mutate_the_store`, `test_open_store_works_on_a_private_copy` |
| Remote exposure | `safe_start` binds only `127.0.0.1` or `::1` and refuses any other host | test: `test_refuses_non_loopback_hosts`, `test_refuses_unsafe_configuration` |
| Forged Host header (a rebinding-style request) | The Host must be a loopback name with the bound port; this is an extra request guard, not authentication | test: `test_host_header_must_be_loopback_with_the_bound_port` (a live DNS-rebinding test does not exist) |
| Cloud, store, AI or real data entering the process | Refuses `ZF_`, `AI_`, `IDENTITY_`, `MSI_`, `AZURE_`, `MSSQL`, `APPLICATIONINSIGHTS`, `OPENAI` and `SQL` variables, symlinks, the normal data location and `~/.zava-forward`, and unmarked or mismatched files | test: `test_refuses_cloud_store_ai_and_normal_data_environment`, `test_refuses_missing_symlink_and_normal_location`, `test_refuses_unmarked_or_mismatched_files`, `test_refuses_files_under_the_normal_data_location` |
| Staff server code reachable from the page | The resident module imports no staff server or auth module | test: `test_resident_module_does_not_load_the_staff_server` |
| Script injection, framing, cross-origin reads, caching | Strict CSP (`default-src 'none'`, same-origin script, style, image and connect, no forms, no framing), `nosniff`, `X-Frame-Options: DENY`, `no-referrer`, `no-store`, same-origin resource policy; only fixed asset paths are served | test: `test_health_pages_and_security_headers` asserts only `no-store` and `default-src 'none'` on the page assets; inspected: the other CSP directives, `nosniff`, `X-Frame-Options`, `no-referrer`, the resource policy, their presence on JSON and error responses, and `resident.js` sets text with `textContent` and has no `innerHTML` use, and the fixed asset allowlist (no malicious-text or traversal test) |
| Calls to external services | No external endpoint or third-party load is configured; the page makes a same-origin fetch to its own view route; CSP `connect-src 'self'` | inspected only; egress is not tested |

Residual risks and limits:

* Same-host users and processes can reach the loopback port and, with file access, can alter
  the grants file, which is re-read on every request without an integrity or ownership check.
  The preview assumes a single trusted local user.
* There is no request log, rate limit, concurrency bound or workload bound
  (`ThreadingHTTPServer`; the grants file is re-read per request), so it is not resilient to
  availability attacks. Unexpected errors outside the controlled grant denials are not uniformly
  handled and can end a response or print diagnostics to the process console.
* The dataset, cases and representative-authority records load once at start-up. Only the grants
  file is re-read per request, so a change to dataset or representative authority needs a
  restart. This was reviewed as a Low follow-up.
* The fixture is invented. It is not evidence about real residents, and no human accessibility
  or security review, screen-reader audit or conformance claim is made.

## Synthetic resident showcase (#462)

A separate, read-only web page where a demo resident signs in with a fake `example.com` email and
one shared demonstration password, then sees only their own invented home record from the existing
homes SQL database. It is a temporary owner showcase, not resident enrolment, not real resident
identity and not production authentication. It is a different composition from the loopback-only
#444 preview above: that preview and its fixture guard are unchanged and are not imported.

### Startup compatibility after resident chat (#525)

An image-only update does not update the SQL view. The resident reader now
selects 17 named columns from `resident_showcase.v_resident_case`, including
`documents_json` added by #525. Startup reads that view and builds the admitted
resident map **before binding HTTP**, even when nobody opens chat and AI is
disabled. The old 16-column view causes SQL `Invalid column name
'documents_json'`; the service prints `Refusing to start: SQL read failed
(ProgrammingError).` and exits 2. Missing projection is not an empty document
list and must not be bypassed with fabricated facts or broader SQL permissions.

Local Docker diagnosis on 2026-10-29 reproduced that failure with the unchanged
main image and the pre-#525 view on a throwaway SQL Server. Applying only the
current [SQL boundary template](../../infra/sql/resident-showcase.sql) to that
local database made the same image/settings serve successfully. This isolates
a sufficient local failure mode, not the verified cause of the historical
Azure revision failure: its console was unavailable, and live schema, secret
resolution, identity and connectivity were not inspected.

Before a separately authorized rollout, have the responsible operator verify
and, if needed, review/apply that current view through the existing
[SQL boundary process](../../infra/README.md#synthetic-resident-showcase-sql-boundary-issue-462),
then verify the resident principal can run the reader's exact projection.
Applying the view must not extend allowlist windows, admit new residents or
grant base-table access. Rebuilding/retrying the image alone cannot supply
the missing column.

There is **no new mandatory app setting** for resident chat.
`ZF_DEMO_AGENDA_PATH` is optional local synthetic callback inventory, not a
startup remedy; leave it unset unless explicitly provisioning that inventory.
`ZF_DEMO_ASSISTANT_ENABLED` defaults to `false`; an endpoint is needed only
when deliberately enabling the separately gated AI integration. Keep the
existing port 8089, image bind `0.0.0.0` and exact Host allowlist. The image's
HTTP healthcheck sends an allowed Host; it cannot succeed until SQL admission
has completed. A public health response from an older ready revision does not
establish that a newly failed revision started.

### Runtime and access controls

* Server: `python -m zava_forward.api.resident_demo`, image `src/api/Dockerfile.resident-demo`
  (`docker build -f src/api/Dockerfile.resident-demo src`; non-root uid 10001; no data or state
  volume, no staff, Entra or AI settings, no secret in the image).
* Configuration (environment only; the server refuses to start on any missing, expired, mixed or
  unsafe value, and never echoes a value):
  `ZF_DEMO_EXPIRES_AT` (explicit UTC, in the future, no later than the packaged
  `resident-demo.json` cap, currently 2027-02-01T00:00:00Z (configuration may
  equal the cap, serving ends exclusively at that instant, after January 31 UTC);
  startup and requests refuse at/after the configured expiry),
  `ZF_DEMO_ALLOWED_HOSTS` (exact host names), `ZF_DEMO_PASSWORD_VERIFIER` (a scrypt verifier, never
  the password), `ZF_DEMO_SESSION_KEY` (base64url, 32 bytes or more), `ZF_SQL_SERVER`,
  `ZF_SQL_DATABASE`, optional `ZF_SQL_CLIENT_ID` for managed-identity sign-in, `PORT`, `ZF_DEMO_BIND`.
  Any `ZF_STORE*`, `ZF_ENTRA*`, `ZF_AI*`, `AI_*`, `AZURE_OPENAI*`, `ZF_DATA*` or `ZF_STATE*` setting
  stops start-up. A loopback-only SQL test server may use `ZF_SQL_AUTH=password`.
* Secrets: the verifier and session key come from a named vault or configuration reference at
  deployment. Nothing in this repository holds a password or its verifier. Tests use an unmistakable
  fake constant. A real shared password has not been generated.
* Sign-in: `POST /demo/login` with CSRF (signed double-submit cookie and header), a same-origin
  `Origin`, a JSON body of at most 2 KiB, an exact `Host` allowlist and a source-address limiter
  (5 failures per source, 60 overall per 10 minutes). The source is the TCP peer by default, which
  is one shared bucket behind an ingress. With `ZF_DEMO_CLIENT_ADDRESS=ingress-rightmost` the source
  is the last `X-Forwarded-For` entry, which Azure Container Apps ingress appends
  ([Microsoft Learn ingress overview](https://learn.microsoft.com/azure/container-apps/ingress-overview),
  retrieved 2026-10-25); earlier entries are client-controlled and ignored. A missing, non-IP, port-
  or bracket-bearing last entry falls back to the peer bucket (stricter). Use that setting only for
  direct Container Apps ingress: another proxy in front would make the last entry that proxy
  (hypothesis, not tested). Residuals: the overall cap can still be exhausted by a distributed
  attacker, which blocks sign-in until the window passes, and users behind one NAT share a bucket. Wrong
  password, unknown email and non-example domain all return the same 401 after the same work.
  Because the password is shared, knowing a showcase email is enough to view that invented record by
  design. That is why only synthetic allowlisted rows are reachable.
* Session: `__Host-zfdemo` (HttpOnly) and `__Host-zfdemo-csrf`, both Secure and SameSite=Strict,
  30 minutes absolute and never past the showcase end. A restart ends every session and logout
  revokes the session. The session holds an opaque handle, never a case id, email or URL.
* Account control (#467): the top-right Account disclosure shows the signed-in synthetic email
  and Sign out, matching the employee site's native account panel. Escape closes it and returns
  focus to Account. Successful sign-out returns focus to the sign-in heading. The authorised
  `/demo/view` includes only that account's canonical `account.email`; anonymous/session responses
  do not include it. Hidden/error/signed-out account controls clear their displayed email.
  The focused no-SQL browser check runs from `src/api` with
  `PYTHONPATH=tests python -m checks.resident_account_check`, using only constructed test rows and the actual
  loopback HTTP app. It checks keyboard/focus, restored identity, narrow widths and logout recovery;
  it does not establish human screen-reader or accessibility acceptance.
* Reads: every protected request re-reads the case through the allowlist view and re-checks
  admission, so a revoked, expired, duplicated or unprovenanced row is denied on the next request.
  The email in the start-up map is bound to the case: a row whose email no longer equals it is denied
  on login and on every request, including live sessions, until restart. There is no row cache.
  Adding a resident or changing an email needs a restart. The page shows only the positive-allowlist fields
  (own account email, home address, planned measures, plain-language progress and next step, help, and what is
  unavailable). Anything else is hidden until it is mapped.
* SQL boundary: [`infra/sql/resident-showcase.sql`](../../infra/sql/resident-showcase.sql) creates
  the schema, an EMPTY allowlist table (rows need named human approval, provenance and a window ending
  by the shared 2027-02-01T00:00:00Z exclusive cutoff), the view and a read-only
  principal that has SELECT on that view only. The
  [`resident_showcase_sql.py`](../../infra/scripts/resident_showcase_sql.py) script renders it and
  only dry-runs unless `--apply` is used from an approved private job.
* Offline verifier: the owner chooses and keeps the password. Run `(umask 077; python3 infra/scripts/resident_demo_verifier.py > owner-only-file)`
  (the subshell makes the file mode 0600 from creation) in an interactive terminal on an owner-controlled machine (no arguments). It prompts twice with
  hidden input, rejects weak or predictable passwords with a generic reason, and prints only the
  scrypt verifier. The verifier is credential-derived sensitive material: keep it in a password
  manager or owner-only file and never in chat or git. The plaintext is briefly in process memory;
  the rules reject predictable patterns and are not proof of strength, so a password-manager random
  value is recommended. Tests use fake fixtures only; no real password has been entered.
* Tests: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_resident_demo_api`
  (real loopback socket, fake reader and fake password) and, with a loopback throwaway SQL Server
  (`ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_PORT`, `ZF_SQL_PASSWORD`),
  `src/core/tests/test_resident_showcase_sql.py` for the view and principal. The browser check is
  `ZF_SQL_PORT=... ZF_SQL_PASSWORD=... python -m checks.resident_demo_browser_check`: it drives the
  real server in Chromium over real SQL with the real `__Host-` cookies, a keyboard-only sign-in, a
  forged-cookie 401, cross-case denial and logout replay. Logout deliberately sends no
  `Set-Cookie`, so a delayed response cannot overwrite a newer login. The normal and
  failed-logout retry checks verify that the retained token receives 401 with its original
  session fence and `/demo/session` returns 200 with `signed_in: false` and `session_id: null`;
  cookie deletion is not the logout contract.

Live criteria still blocked (not proven here): remaining budget headroom, live email-to-case
equality in the homes database, the private job that creates the view and principal, the Key Vault
secret retrieval role and client, and any deployment. The page is not WCAG conformance evidence.

The #521 source renewal covers January 31, 2027 UTC, but does not deploy an
image, renew configured app/secret expiries or extend existing SQL row windows.
The [rotation, conditional cost estimate and pending live-apply plan](../../infra/README.md#january-authority-source-renewal-2026-10-28-refs-521)
requires separate exact owner confirmation and a fresh USD700 all-in headroom
check. The independent resident model tariff and SQL inference admission cutoff
are unchanged; extending resident access does not authorize later paid inference.

### Own-home synthetic sensor history (#468)

`GET /demo/view` includes `sensors` with `synthetic: true`, a non-live notice and
up to 48 stored observations in chronological order. Each observation contains
UTC `observed_at`, nullable `temperature_c`/`humidity_pct` and explicit channel
statuses. It contains no home, sensor or reading IDs. Signed-session case
selection and fresh admission checks are unchanged; URL/header home selectors
have no authority.

The source view definition optionally reads the existing generated
`dbo.sensor_register` and `dbo.sensor_reading` tables from
[`sensor_backfill`](../core/src/zava_forward/core/synthetic/sensor_backfill.py).
Both register and reading home IDs must exactly match the case's `home.stock_id`,
and both source labels must be `SYNTHETIC`, using binary comparisons plus
length checks after common Unicode conversion (no trimming or SQL space-padding
equivalence). The
principal still has SELECT on only the resident view. No request generates data,
opens an exported snapshot or reads a private stock file.

At a separately authorised view apply, absent sensor tables produce an empty
history, not invented readings. Existing deployed view definitions do not have
the new columns: coordinate any later application deployment with that reviewed
view update. Creating/loading the tables, applying the view, changing grants
and deploying are not performed or authorised by this source increment.
Source/mocked checks do not prove T-SQL compilation or live data availability.

The UI shows the latest stored observation, including its unavailable state,
not an older apparently normal replacement. Missing channels, out-of-range
values and labelled OUTLIER/STUCK faults have text and gaps rather than zero
gauges. The fictional generator ranges (-10 to 45 degrees C and 0 to 100 percent)
are display bounds, not health limits. Two static SVG histories have unit labels
and an equivalent keyboard-accessible data table. No animation or chart library
is added. This is not safety advice or a WCAG conformance claim.

With editable core/agents/API and API development dependencies installed, run
the SQL-free constructed-reader browser exercise from `src/api`:

```bash
python -m checks.resident_sensors_browser_check
```

It starts the actual HTTP app on loopback with fresh fictional output from the
existing sensor generator, uses real demo cookies and Chromium, and closes the
server after checking own-home values, isolation, table, missing/fault/empty
states, keyboard focus, reduced motion and 320/390/1280 px reflow. It does not
use the SQL-configured application entry point, Azure or private datasets.
