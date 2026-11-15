# Details 153 c2

Edit: remove `painted = true;` at the top of `paint` and add it as the last statement after the `content.replaceChildren(...)` call. A throw in building children or in replaceChildren then leaves `painted` false, so the catch renders the retry button and the notice uses `briefingRetryAction(false, ...)`.

Test (in `src/api/tests/test_app_js_notices_content.py`): extract `briefingRetryAction` and the catch-branch behaviour via node with a stubbed `h`, `content` and a `paint` copied from app.js source between `const paint = b => {` and `let sequence`; run with a bad payload (`b` null) so paint throws, then assert the retry button text and notice text match.
