"use strict";

const AsyncAction = (() => {
  const pending = new WeakMap();
  const notices = new WeakMap();
  function feedback(label, control, region) {
    const status = document.createElement("span");
    status.className = "async-feedback";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    status.setAttribute("aria-atomic", "true");
    status.textContent = `${label}: working...`;
    if (region) region.append(status);
    else if (control) control.after(status);
    else document.getElementById("action-status")?.append(status);
    const timer = setTimeout(() => {
      if (!status.isConnected) return;
      const spinner = document.createElement("span");
      spinner.className = "async-spinner";
      spinner.setAttribute("aria-hidden", "true");
      status.prepend(spinner);
    }, 200);
    const remove = () => {
      clearTimeout(timer);
      status.remove();
      if (control && notices.get(control) === remove) notices.delete(control);
    };
    if (control) notices.set(control, remove);
    return {
      finish(error) {
        clearTimeout(timer);
        status.querySelector(".async-spinner")?.remove();
        if (error && error.name !== "AbortError") {
          status.classList.add("err");
          status.textContent = `${label}: ${error.message}. Try again.`;
        } else remove();
      },
    };
  }
  function run(control, task, label, region) {
    if (control && pending.has(control)) return pending.get(control);
    if (control) notices.get(control)?.();
    const button = control?.tagName === "FORM"
      ? control.querySelector('button[type="submit"], button:not([type])') : control;
    const originalDisabled = button?.disabled;
    const busy = control?.getAttribute("aria-busy");
    let result;
    try { result = task(); }
    catch (error) {
      const notice = feedback(label || "Action", control, region);
      notice.finish(error);
      return Promise.resolve();
    }
    if (!result || typeof result.then !== "function") return result;
    const notice = feedback(label || button?.textContent.trim() || "Loading", control, region);
    control?.setAttribute("aria-busy", "true");
    const ownsDisabled = button && !button.disabled && button.getAttribute("aria-disabled") !== "true";
    if (ownsDisabled) button.disabled = true;
    // Existing handlers own any later disabled changes, including permanent refusals.
    const observer = button ? new MutationObserver(() => { changed = true; }) : null;
    let changed = false;
    observer?.observe(button, { attributes: true, attributeFilter: ["disabled"] });
    const done = Promise.resolve(result).then(
      value => { notice.finish(); return value; },
      error => { notice.finish(error); },
    ).finally(() => {
      changed ||= Boolean(observer?.takeRecords().length);
      observer?.disconnect();
      if (ownsDisabled && !changed) button.disabled = originalDisabled;
      if (control) {
        if (busy === null) control.removeAttribute("aria-busy");
        else control.setAttribute("aria-busy", busy);
        pending.delete(control);
      }
    });
    if (control) pending.set(control, done);
    return done;
  }
  const handler = task => event => {
    if (event.type === "submit") event.preventDefault();
    const control = event.currentTarget;
    return run(control, () => task(event),
      control.getAttribute("aria-label") || control.labels?.[0]?.textContent.trim()
      || (control.tagName === "FORM" ? event.submitter?.textContent.trim() : control.textContent.trim())
      || "Updating");
  };
  return { run, handler, feedback };
})();
