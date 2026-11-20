"use strict";

// One labelled-field pattern for every form. h() comes from app.js and is resolved at call time.
//
// Fields.fieldBlock({ id, name, label, hint, required, optional, control }) returns
// { block, control, fail(message), clear() } and builds:
//   <div class="field">
//     <label for="{id}">{label}</label>               " (required)" or " (optional)" is added; required wins
//     <p class="field-hint" id="{id}-hint">{hint}</p> only when hint is given; linked by aria-describedby
//     {control}                                       the input, select or textarea the caller built
//     <p class="field-error" id="{id}-error" hidden></p>
//   </div>
// fail(message) shows the error, marks the control invalid and moves focus to it; clear() undoes that.
// Error text: "{What is wrong}. Owner: you. Next action: {fix}, then choose {Button label} again."
//
// Fields.checkRow({ id, label, hint, control }) returns { block, control } and builds:
//   <div class="check">
//     {control}                                       the checkbox or radio, before its label
//     <label for="{id}">{label}</label>
//     <p class="field-hint" id="{id}-hint">{hint}</p> only when hint is given; linked by aria-describedby
//   </div>
const Fields = (() => {
  const tokens = value => String(value || "").split(/\s+/).filter(Boolean);
  const describedWith = (control, id) => {
    const current = tokens(control.getAttribute("aria-describedby"));
    return (current.includes(id) ? current : [...current, id]).join(" ");
  };
  // The id ties label, hint and error to the control. It comes from the caller or the control itself.
  function identify(id, label, control) {
    const own = id || control.getAttribute("id");
    if (!own || !label) throw new TypeError("A field needs an id and a visible label.");
    control.setAttribute("id", own);
    return own;
  }
  function fieldBlock({ id, name, label, hint, required, optional, control }) {
    const fieldId = identify(id, label, control);
    const hintId = `${fieldId}-hint`;
    const errorId = `${fieldId}-error`;
    const error = h("p", { class: "field-error", id: errorId, hidden: true });
    if (name) control.setAttribute("name", name);
    if (hint) control.setAttribute("aria-describedby", describedWith(control, hintId));
    const suffix = required ? " (required)" : optional ? " (optional)" : "";
    const block = h("div", { class: "field" },
      h("label", { for: fieldId }, `${label}${suffix}`),
      hint ? h("p", { class: "field-hint", id: hintId }, hint) : null,
      control, error);
    return {
      block, control,
      fail(message) {
        error.textContent = message;
        error.hidden = false;
        control.setAttribute("aria-describedby", describedWith(control, errorId));
        control.setAttribute("aria-invalid", "true");
        control.focus();
      },
      clear() {
        error.hidden = true;
        error.textContent = "";
        control.removeAttribute("aria-invalid");
        const rest = tokens(control.getAttribute("aria-describedby")).filter(token => token !== errorId);
        if (rest.length) control.setAttribute("aria-describedby", rest.join(" "));
        else control.removeAttribute("aria-describedby");
      },
    };
  }
  function checkRow({ id, label, hint, control }) {
    const fieldId = identify(id, label, control);
    const hintId = `${fieldId}-hint`;
    if (hint) control.setAttribute("aria-describedby", describedWith(control, hintId));
    const block = h("div", { class: "check" },
      control,
      h("label", { for: fieldId }, label),
      hint ? h("p", { class: "field-hint", id: hintId }, hint) : null);
    return { block, control };
  }
  return { fieldBlock, checkRow };
})();
