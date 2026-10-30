"use strict";

window.ChatWidget = (() => {
  function node(tag, text, attrs = {}) {
    const element = document.createElement(tag);
    if (text) element.textContent = text;
    for (const [name, value] of Object.entries(attrs)) element.setAttribute(name, value);
    return element;
  }
  function decorateLauncher(launcher) {
    launcher.className = "chat-widget-launcher";
    launcher.setAttribute("aria-label", "Chat");
    launcher.setAttribute("aria-haspopup", "dialog");
    launcher.setAttribute("aria-expanded", "false");
    launcher.replaceChildren();
    const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    icon.setAttribute("viewBox", "0 0 24 24");
    icon.setAttribute("width", "24");
    icon.setAttribute("height", "24");
    icon.setAttribute("aria-hidden", "true");
    const path = document.createElementNS(icon.namespaceURI, "path");
    path.setAttribute("d", "M4 3h16v13H9l-5 5V3zm4 5h8M8 12h6");
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", "currentColor");
    path.setAttribute("stroke-width", "2");
    icon.append(path);
    launcher.append(icon);
  }
  function create({ id, title, launcher, questionLabel, skillLabel, maxLength = 1000, resizable = false }) {
    let active = true, timer = null;
    launcher ||= node("button", "", { type: "button" });
    decorateLauncher(launcher);
    launcher.setAttribute("aria-controls", id);
    const root = node("section", "", { id, class: "chat-widget", role: "dialog", "aria-labelledby": `${id}-title` });
    root.hidden = true;
    const heading = node("h2", title, { id: `${id}-title`, tabindex: "-1" });
    const close = node("button", "Close chat", { type: "button", class: "chat-widget-close" });
    const header = node("div", "", { class: "chat-widget-header" });
    header.append(heading, close);
    const intro = node("details", "", { class: "chat-widget-intro" });
    intro.append(node("summary", "About this chat"));
    const log = node("div", "", { class: "chat-widget-log", role: "log", "aria-live": "polite", "aria-relevant": "additions", "aria-label": `${title} conversation`, tabindex: "0" });
    const form = node("form", "", { class: "chat-widget-composer" });
    const beforeInput = node("div");
    const input = node("textarea", "", { id: `${id}-question`, name: "question", autocomplete: "off", rows: "2", maxlength: String(maxLength), "aria-label": questionLabel });
    const select = node("select", "", { id: `${id}-skill`, name: "skill", autocomplete: "off", "aria-label": skillLabel });
    const tools = node("div", "", { class: "chat-widget-tools" });
    const reason = node("small", "Attachments and voice input are not supported in this chat. Use the existing document or contact routes.", { id: `${id}-unsupported`, class: "chat-widget-meta" });
    const attach = node("button", "Attach", { type: "button", disabled: "", "aria-describedby": reason.id });
    const voice = node("button", "Voice", { type: "button", disabled: "", "aria-describedby": reason.id });
    const send = node("button", "Send", { type: "submit" });
    tools.append(select, attach, voice, send);
    const status = node("p", "", { role: "status", "aria-live": "polite", "aria-atomic": "true", class: "chat-widget-status" });
    const loading = node("span", "Working...", { class: "chat-widget-loading", "aria-hidden": "true" });
    loading.hidden = true;
    const error = node("p", "", { id: `${id}-error`, role: "alert", "aria-live": "polite", "aria-atomic": "true", class: "chat-widget-error", tabindex: "-1" });
    error.hidden = true;
    form.append(beforeInput, input, tools, reason);
    root.append(header, intro, log, status, loading, error, form);
    document.body.append(launcher, root);
    let docked = false;
    if (resizable) {
      root.classList.add("chat-widget-resizable");
      const dock = node("button", "Dock to right edge", { type: "button", "aria-pressed": "false", class: "chat-widget-close" });
      const sizes = node("details", "", { class: "chat-widget-size" });
      sizes.append(node("summary", "Chat size"));
      sizes.append(node("p", "Adjust the width and height. Docking uses the full screen height. Sizes stay within the screen and keep a minimum reading area."));
      sizes.append(dock);
      const controls = {};
      for (const [dimension, value] of [["width", 35], ["height", 70]]) {
        const label = node("label", `Preferred ${dimension} (% of screen)`, { for: `${id}-${dimension}` });
        const range = node("input", "", { type: "range", id: `${id}-${dimension}`, name: dimension, autocomplete: "off", min: "20", max: "100", step: "1", value: String(value) });
        const output = node("output", `${value}%`, { for: range.id, "aria-hidden": "true" });
        label.append(output);
        sizes.append(label, range);
        controls[dimension] = range;
        range.addEventListener("input", () => {
          resize(() => {
            root.style.setProperty(`--chat-${dimension}`, `${range.value}${dimension === "width" ? "vw" : "dvh"}`);
            output.textContent = `${range.value}%`;
          });
        });
      }
      dock.addEventListener("click", () => {
        resize(() => {
          docked = !docked;
          root.classList.toggle("chat-widget-docked", docked);
          dock.setAttribute("aria-pressed", String(docked));
          controls.height.disabled = docked;
          launcher.hidden = docked;
        });
      });
      root.insertBefore(sizes, log);
    }
    function resize(change) {
      const follow = following();
      const top = log.getBoundingClientRect().top;
      const anchor = [...log.children].find(item => item.getBoundingClientRect().bottom > top);
      const box = anchor?.getBoundingClientRect();
      const fraction = box ? (top - box.top) / box.height : 0;
      change();
      if (follow) bottom();
      else if (anchor) {
        const after = anchor.getBoundingClientRect();
        log.scrollTop += after.top - log.getBoundingClientRect().top + fraction * after.height;
      }
    }
    function hide(returnFocus = true) {
      root.hidden = true;
      launcher.hidden = false;
      launcher.setAttribute("aria-expanded", "false");
      if (returnFocus && active) launcher.focus();
    }
    function open() {
      if (!active) return;
      root.hidden = false;
      launcher.hidden = docked;
      launcher.setAttribute("aria-expanded", "true");
      heading.focus();
      bottom();
    }
    function bottom() { log.scrollTop = log.scrollHeight; }
    function following() {
      return log.scrollHeight - log.clientHeight - log.scrollTop <= 1
        && !log.contains(document.activeElement);
    }
    function preserveBottom(change) {
      const follow = following();
      change();
      if (follow) bottom();
    }
    function setStatus(text) {
      preserveBottom(() => { status.textContent = text; });
    }
    function busy(value) {
      clearTimeout(timer);
      preserveBottom(() => { loading.hidden = true; });
      if (value && document.activeElement === send && !root.hidden) input.focus();
      send.disabled = value;
      select.disabled = value;
      form.setAttribute("aria-busy", String(value));
      if (value) timer = setTimeout(() => {
        if (active) preserveBottom(() => { loading.hidden = false; });
      }, 200);
    }
    function message(role, text, { label = "", sources = [], detail = "" } = {}) {
      const follow = following();
      const item = node("article", "", { class: `chat-widget-message chat-widget-${role}` });
      item.append(node("strong", role === "user" ? "You" : "Assistant"));
      if (label) item.append(node("small", label, { class: "chat-widget-meta" }));
      item.append(node("p", text));
      if (detail) item.append(node("small", detail, { class: "chat-widget-meta" }));
      if (role !== "user") {
        const details = node("details");
        details.append(node("summary", `Sources (${sources.length})`));
        const list = node("ul");
        for (const source of sources) list.append(node("li", source));
        details.append(list);
        if (!sources.length) details.append(node("p", "No supporting source was provided. Check with a person before relying on this reply."));
        item.append(details);
      }
      log.append(item);
      if (follow) bottom();
      return item;
    }
    launcher.onclick = () => root.hidden ? open() : hide();
    close.onclick = () => hide();
    root.addEventListener("keydown", event => {
      if (event.key === "Escape") { event.preventDefault(); hide(); }
    });
    function externalFocus(event) {
      if (!root.hidden && !root.contains(event.target) && !launcher.contains(event.target)) hide(false);
    }
    document.addEventListener("focusin", externalFocus);
    input.addEventListener("keydown", event => {
      if (event.key === "Enter" && !event.shiftKey && !event.isComposing && event.keyCode !== 229) {
        event.preventDefault();
        if (!send.disabled) form.requestSubmit();
      }
    });
    return {
      root, launcher, heading, intro, log, form, beforeInput, input, select, send, status, error,
      node, open, hide, busy, message, setStatus,
      fail(text) {
        preserveBottom(() => {
          error.textContent = text; error.hidden = false; status.textContent = "";
        });
      },
      clearError() {
        preserveBottom(() => { error.textContent = ""; error.hidden = true; });
      },
      focusInput() { if (active && !root.hidden) input.focus(); },
      dispose() {
        active = false;
        clearTimeout(timer);
        document.removeEventListener("focusin", externalFocus);
        root.remove();
        launcher.hidden = false;
        launcher.setAttribute("aria-expanded", "false");
      },
    };
  }
  return { create, decorateLauncher };
})();
