// Submits the standalone referral, correction and challenge forms as JSON.
// The server reads JSON bodies only, and the CSP blocks inline scripts.
(() => {
  const form_ids = /^(nomination-ack-|nomination-correct-|challenge-open-route)/;

  // One write at a time per page; a recorded or uncertain write locks every form until reload.
  let busy = false;
  let locked = false;

  function setButtons(disabled) {
    for (const form of document.querySelectorAll("form")) {
      if (!form_ids.test(form.getAttribute("id") || "")) continue;
      const button = form.querySelector("button[type='submit']");
      if (button) button.disabled = disabled;
    }
  }

  function payload(form) {
    const body = {};
    for (const [name, value] of new FormData(form).entries()) {
      if (typeof value !== "string" || value.trim() === "") continue;
      body[name] = name === "expected_version" ? Number(value) : value;
    }
    // The correction route requires the key and treats null as "no linked challenge".
    if (body.action === "nomination_correct" && !body.challenge_id) body.challenge_id = null;
    if (body.action === "challenge_open") {
      const option = form.querySelector("[name='proposal_id']")?.selectedOptions[0];
      body.proposal_version = option?.dataset.proposalVersion;
      body.decision_version = option?.dataset.decisionVersion;
    }
    if (body.channel !== "staff_recorded_non_digital") delete body.assisted_channel;
    if (body.raised_by !== "Representative") delete body.representative_ref;
    return body;
  }

  async function submit(event) {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    // A hidden input named "id" shadows form.id, so read the attribute.
    const formId = form.getAttribute("id") || "";
    if (!form_ids.test(formId)) return;
    event.preventDefault();
    if (busy || locked) return;
    const feedback = document.getElementById(`${formId}-feedback`);
    const say = (text) => {
      if (!feedback) return;
      feedback.textContent = text;
      feedback.focus();
    };
    busy = true;
    setButtons(true);
    try {
      const res = await fetch(form.getAttribute("action"), {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-ZF-CSRF": "1" },
        body: JSON.stringify(payload(form)),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        locked = true;
        say("Recorded. Reloading the updated routes.");
        window.location.reload();
        return;
      }
      // A server error may have committed the write, so only a client refusal unlocks the forms.
      if (res.status >= 500) {
        locked = true;
        say("The service reported a fault, so the result is unknown. Reload this page to check before trying again.");
        return;
      }
      say(data.error || "Could not record that. Check the fields and try again.");
    } catch {
      locked = true;
      say("The service did not answer, so the result is unknown. Reload this page to check before trying again.");
    }
    busy = false;
    if (!locked) setButtons(false);
  }

  document.addEventListener("submit", submit);
})();
