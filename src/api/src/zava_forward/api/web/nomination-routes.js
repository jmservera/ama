// Submits the standalone referral, correction and challenge forms as JSON.
// The server reads JSON bodies only, and the CSP blocks inline scripts.
(() => {
  const form_ids = /^(nomination-ack-|nomination-correct-|challenge-open-route)/;

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
    const feedback = document.getElementById(`${formId}-feedback`);
    const say = (text) => {
      if (!feedback) return;
      feedback.textContent = text;
      feedback.focus();
    };
    const button = form.querySelector("button[type='submit']");
    if (button) button.disabled = true;
    try {
      const res = await fetch(form.getAttribute("action"), {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-ZF-CSRF": "1" },
        body: JSON.stringify(payload(form)),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        say("Recorded. Reloading the updated routes.");
        window.location.reload();
        return;
      }
      say(data.error || "Could not record that. Check the fields and try again.");
    } catch {
      say("Could not reach the service. Nothing was recorded; try again.");
    }
    if (button) button.disabled = false;
  }

  document.addEventListener("submit", submit);
})();
