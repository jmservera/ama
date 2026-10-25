"use strict";
(function () {
  var statusEl = document.getElementById("status");
  var errorEl = document.getElementById("error");
  var errorTitle = document.getElementById("error-title");
  var errorText = document.getElementById("error-text");
  var content = document.getElementById("content");
  var signin = document.getElementById("signin");
  var form = document.getElementById("signin-form");
  var signinError = document.getElementById("signin-error");
  var signinButton = document.getElementById("signin-button");
  var signoutRow = document.getElementById("signout-row");
  var csrf = "";

  function el(tag, text, cls) {
    var node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = String(text);
    if (cls) node.className = cls;
    return node;
  }

  function card(title, cls) {
    var section = el("section", null, "card" + (cls ? " " + cls : ""));
    var heading = el("h2", title);
    heading.id = "h-" + title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    section.setAttribute("aria-labelledby", heading.id);
    section.appendChild(heading);
    return section;
  }

  function render(view) {
    content.textContent = "";
    if (view.banner) {
      var note = card("About this showcase");
      note.appendChild(el("p", view.banner));
      content.appendChild(note);
    }
    if (view.home) {
      var home = card("Your home");
      home.appendChild(el("p", [view.home.address, view.home.town, view.home.postcode].filter(Boolean).join(", ")));
      content.appendChild(home);
    }
    if (view.measures && view.measures.length) {
      var measures = card("Planned improvements");
      var ml = el("ul");
      view.measures.forEach(function (m) { ml.appendChild(el("li", m)); });
      measures.appendChild(ml);
      content.appendChild(measures);
    }
    if (view.progress) {
      var progress = card("Where things are");
      progress.appendChild(el("p", view.progress));
      if (view.closed) progress.appendChild(el("p", view.closed));
      content.appendChild(progress);
    }
    if (view.next_step) {
      var next = card("What happens next");
      next.appendChild(el("p", view.next_step));
      content.appendChild(next);
    }
    var help = card("Help and other ways to reach us");
    help.appendChild(el("p", view.help.summary));
    var hl = el("ul");
    view.help.routes.forEach(function (r) { hl.appendChild(el("li", r)); });
    help.appendChild(hl);
    help.appendChild(el("p", view.help.note));
    content.appendChild(help);

    var unavailable = card("Not available in this showcase");
    var ul = el("ul", null, "unavail");
    view.unavailable.forEach(function (u) {
      var li = el("li");
      var b = el("button", u.feature);
      b.type = "button";
      b.disabled = true;
      b.setAttribute("aria-disabled", "true");
      li.appendChild(b);
      li.appendChild(el("span", u.reason, "why"));
      ul.appendChild(li);
    });
    unavailable.appendChild(ul);
    content.appendChild(unavailable);

    errorEl.hidden = true;
    signin.hidden = true;
    content.hidden = false;
    signoutRow.hidden = false;
    statusEl.textContent = "";
  }

  function showSignin(message) {
    content.hidden = true;
    signoutRow.hidden = true;
    errorEl.hidden = true;
    statusEl.textContent = "";
    signin.hidden = false;
    if (message) {
      signinError.textContent = message;
      signinError.hidden = false;
      signinError.focus();
    } else {
      signinError.hidden = true;
    }
  }

  function fail(message) {
    content.hidden = true;
    signin.hidden = true;
    signoutRow.hidden = true;
    statusEl.textContent = "";
    errorText.textContent = message;
    errorEl.hidden = false;
    errorTitle.focus();
  }

  function api(path, options) {
    options = options || {};
    var headers = { Accept: "application/json" };
    if (options.body) headers["Content-Type"] = "application/json";
    if (options.method === "POST") headers["X-CSRF-Token"] = csrf;
    return fetch(path, { method: options.method || "GET", headers: headers, body: options.body, cache: "no-store", credentials: "same-origin" })
      .then(function (r) {
        return r.json().then(function (body) { return { ok: r.ok, status: r.status, body: body }; });
      });
  }

  function loadView() {
    statusEl.textContent = "Loading your progress\u2026";
    return api("/demo/view").then(function (res) {
      if (res.ok) render(res.body);
      else if (res.status === 401) showSignin("Please sign in again.");
      else fail(res.body.error || "Something went wrong.");
    });
  }

  function start() {
    errorEl.hidden = true;
    statusEl.textContent = "Loading\u2026";
    api("/demo/session")
      .then(function (res) {
        if (!res.ok) { fail(res.body.error || "The showcase is not available right now."); return; }
        csrf = res.body.csrf;
        if (res.body.signed_in) return loadView();
        showSignin();
      })
      .catch(function () {
        fail("We could not reach the showcase. Check your connection, then try again.");
      });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    if (!email.trim() || !password) {
      signinError.textContent = "Enter your email address and the password.";
      signinError.hidden = false;
      signinError.focus();
      return;
    }
    signinButton.disabled = true;
    signinError.hidden = true;
    api("/demo/login", { method: "POST", body: JSON.stringify({ email: email, password: password }) })
      .then(function (res) {
        document.getElementById("password").value = "";
        if (res.ok) {
          csrf = res.body.csrf || csrf;
          return loadView();
        }
        if (res.status === 403) { start(); return; }
        showSignin(res.body.error || "We could not sign you in.");
      })
      .catch(function () {
        showSignin("We could not reach the showcase. Try again.");
      })
      .then(function () { signinButton.disabled = false; });
  });

  document.getElementById("signout").addEventListener("click", function () {
    api("/demo/logout", { method: "POST", body: "{}" }).then(function () {
      content.textContent = "";
      csrf = "";
      start();
    }).catch(function () { fail("We could not sign you out. Close this page to end the session."); });
  });

  document.getElementById("retry").addEventListener("click", start);
  start();
})();
