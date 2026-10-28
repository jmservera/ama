"use strict";

const CaseWorkspace = (() => {
  const steps = [
    { name: "Survey", tab: "survey", stages: ["Home identified", "Checking lease", "Rescheduled", "Contacting resident", "Contact paused", "Survey being booked", "Survey booked", "Survey write-up"] },
    { name: "Assessment", tab: "survey", stages: ["Design starting", "Design in progress", "Design awaiting approval", "Design being corrected", "Waiting on other works"] },
    { name: "Funding", tab: "funding", stages: ["Funding check", "Final checks before ordering"] },
    { name: "Resident agreement", tab: "resident", stages: ["Waiting for resident decision", "Resident paused works"] },
    { name: "Contractor", tab: "contractor", stages: ["Waiting for block programme", "With contractor", "Install booked", "Works under way"] },
    { name: "Quality and handover", tab: "quality", stages: ["Handover to arrange", "Quality check", "Closing down", "Aftercare issue"] },
  ];
  const stageStep = Object.fromEntries(steps.flatMap((step, index) => step.stages.map(stage => [stage, index])));
  const blockerSteps = {
    "Final checks: funding": 2, "Final checks: resident decision": 3,
    "Final checks: technical review": 1, "Stock review": 1,
  };
  const blockerIndex = (blocker, current) => blockerSteps[blocker.step] ?? current;
  const currentIndex = c => stageStep[c.stage] ?? -1;
  const waiting = p => p.state === "ready" && Boolean(p.output) && !p.stale;
  function journey(c) {
    const current = currentIndex(c);
    return steps.map((step, index) => {
      const blockers = (c.work?.blockers || []).filter(b => blockerIndex(b, current) === index);
      let state = index < current ? "done" : "upcoming";
      let text = state === "done" ? "Done" : "Not started";
      if (index < current && ((index === 2 && c.funding?.status !== "Confirmed")
          || (index === 3 && c.decision?.status !== "Accepted"))) {
        state = "upcoming"; text = "Earlier step not confirmed";
      }
      if (index === current) { state = "current"; text = "Current"; }
      if (blockers.length) {
        state = "blocked";
        text = `${index === current ? "Current, blocked" : "Blocked"}: ${blockers.map(b => b.reason).join(" ")}`;
      }
      if (c.closed) { state = "done"; text = "Done"; }
      return { name: step.name, tab: step.tab, state, text, current: !c.closed && index === current };
    });
  }
  function defaultTab(c) {
    const blocker = c.work?.blockers?.find(b => b.current_stop);
    return c.closed ? "overview" : blocker ? "blockers" : "overview";
  }
  function nextTab(c) {
    if (c.work?.source?.endsWith("/handoff")) return "quality";
    const blocker = c.work?.blockers?.find(b => b.current_stop);
    if (blocker) return "blockers";
    if (c.closed || c.can_advance) return "overview";
    if (["Contacting resident", "Contact paused", "Rescheduled", "Survey being booked", "Survey booked"].includes(c.stage)) return "resident";
    return steps[currentIndex(c)]?.tab || "overview";
  }
  function summary(c) {
    const work = c.work || {};
    const first = work.blockers?.[0];
    const offered = c.handoff && ["Offered", "Received", "Escalated"].includes(c.handoff.state);
    return {
      status: c.status || "Status not recorded",
      step: steps[currentIndex(c)] ? `${steps[currentIndex(c)].name}: ${c.stage}, ${c.days_in_stage ?? "Unknown"} days` : "Step unknown",
      next: work.next_action || `Ask ${c.owner || "Unknown"} to record the next action.`,
      owner: `${c.owner || "Unknown"}${c.owner_role ? `, ${c.owner_role}` : ""}${offered ? `. Offered to ${c.handoff.proposed_receiver || c.handoff.to_name || "Unknown"}, not yet confirmed` : ""}`,
      blockers: first ? `${work.blockers.length} blockers. ${first.reason} Owner: ${first.owner || "Unknown"}. Next action: ${first.next_action || "Ask the case owner to record the next action."}` : "No recorded blockers.",
      overdue: work.overdue?.length || 0,
    };
  }
  function enhance(c, definitions, safety, assistant, drafts) {
    const values = summary(c);
    const section = h("section", { class: "case-summary", "aria-label": "Case summary" });
    const aiCount = h("span", { role: "status", "aria-live": "polite", "aria-atomic": "true", "data-case-ai-count": "" });
    const aiState = h("span", {});
    const aiValue = h("dd", { "data-case-ai-summary": "" }, aiCount, " ", aiState);
    const aiTab = definitions.find(tab => tab.id === "ai");
    const counts = () => {
      const records = new Map([...app.querySelectorAll(".aimeta[data-record-id]")].map(node => [node.dataset.recordId, node]));
      const draftCount = [...records.values()].filter(node => node.dataset.reviewState === "Not reviewed").length;
      const count = Number(assistant.dataset.waiting || 0) + draftCount;
      const unknown = assistant.dataset.assistance?.startsWith("AI assistance unavailable");
      const loading = !assistant.hasAttribute("data-waiting");
      const state = aiMode.workflow ? "Workflow-only mode." : assistant.dataset.assistance || "Loading assistance. Ordinary case work continues.";
      const text = unknown ? `AI review count unavailable.${draftCount ? ` ${draftCount} local drafts to review.` : ""}` : loading ? "AI review count loading." : count ? `${count} AI suggestions waiting for review.` : "No AI suggestions waiting.";
      if (aiCount.textContent !== text) aiCount.textContent = text;
      if (aiState.textContent !== state) aiState.textContent = state;
      const label = `AI assistance (${unknown ? `review count unavailable${draftCount ? `; ${draftCount} local drafts to review` : ""}` : loading ? "loading" : `${count} to review`})`;
      if (aiTab.button && aiTab.button.textContent !== label) aiTab.button.textContent = label;
    };
    const item = (name, value, button) => h("div", {}, h("dt", {}, name), h("dd", {}, value, button));
    const jump = (tab, text) => h("button", { class: "alt", type: "button", onclick: () => select(tab, true, true) }, text);
    section.append(h("dl", {},
      item("Status", h("span", { class: `status-line ${c.hazards.some(x => !x.released) ? "danger" : c.closed ? "ok" : "wait"}` }, values.status)),
      item("Current step", values.step),
      item("Next action", values.next, jump(nextTab(c), "Open next action")),
      item("Owner", values.owner),
      item("Blockers", `${values.blockers}${values.overdue ? ` ${values.overdue} overdue tasks.` : ""}`, jump("blockers", "See all blockers")),
      h("div", {}, h("dt", {}, "AI"), aiValue)));
    const aiJump = jump("ai", "Review AI suggestions");
    aiValue.append(aiJump);
    const nav = h("nav", { class: "case-journey", "aria-label": "Retrofit journey" },
      h("ol", { class: "stepper" }, journey(c).map(step => h("li", {
        class: `step ${step.state}`, "aria-current": step.current ? "step" : null,
      }, h("a", { href: `#/case/${encodeURIComponent(c.id)}?tab=${step.tab}`, "data-case-tab": step.tab },
        h("span", { class: "step-glyph", "aria-hidden": "true" }, { done: "\u2713", current: "\u25cf", blocked: "\u26d4", upcoming: "\u25cb" }[step.state]),
        h("span", { class: "step-name" }, step.name), h("span", { class: "step-state" }, step.text))))));
    const tabs = h("div", { role: "tablist", "aria-label": "Case sections" });
    const tabRegion = h("div", { class: "case-tabs-scroll", role: "region", "aria-label": "Case section tabs", tabindex: 0 }, tabs);
    let active;
    function syncLinks() {
      nav.querySelectorAll("a[data-case-tab]").forEach(link => {
        const query = new URLSearchParams(location.hash.split("?")[1] || "");
        query.set("tab", link.dataset.caseTab);
        link.setAttribute("href", `#/case/${encodeURIComponent(c.id)}?${query}`);
      });
    }
    function select(id, updateUrl = false, focusHeading = false) {
      const selected = definitions.find(tab => tab.id === id) || definitions.find(tab => tab.id === defaultTab(c));
      active = selected.id;
      for (const tab of definitions) {
        const chosen = tab === selected;
        tab.button.setAttribute("aria-selected", String(chosen));
        tab.button.tabIndex = chosen ? 0 : -1;
        tab.panel.hidden = !chosen;
      }
      if (updateUrl) {
        const query = new URLSearchParams(location.hash.split("?")[1] || "");
        query.set("tab", active);
        history.pushState(null, "", `#/case/${encodeURIComponent(c.id)}?${query}`);
        displayedHash = location.hash;
      }
      syncLinks();
      if (focusHeading) selected.panel.querySelector("h2").focus();
    }
    definitions.forEach((tab, index) => {
      const heading = tab.panel.querySelector("h2");
      heading.tabIndex = -1;
      tab.panel.setAttribute("role", "tabpanel");
      tab.panel.setAttribute("aria-labelledby", `case-tab-${tab.id}`);
      tab.panel.tabIndex = 0;
      tab.button = h("button", { type: "button", role: "tab", id: `case-tab-${tab.id}`,
        "aria-controls": tab.panel.id, onclick: () => select(tab.id, true),
        onfocus: event => event.currentTarget.scrollIntoView({ block: "nearest", inline: "nearest" }),
        onkeydown: event => {
          const positions = { ArrowRight: (index + 1) % definitions.length, ArrowLeft: (index + definitions.length - 1) % definitions.length, Home: 0, End: definitions.length - 1 };
          if (event.key in positions) {
            event.preventDefault();
            definitions[positions[event.key]].button.focus();
          }
        } }, tab.label);
      tabs.append(tab.button);
    });
    const observer = new MutationObserver(counts);
    observer.observe(assistant, { attributes: true, attributeFilter: ["data-waiting", "data-assistance"] });
    observer.observe(drafts, { subtree: true, childList: true, attributes: true, attributeFilter: ["data-review-state"] });
    app.addEventListener("ai-review-change", counts);
    select(new URLSearchParams(location.hash.split("?")[1] || "").get("tab"));
    counts();
    return { top: [section, safety, nav, tabRegion].filter(Boolean), select, counts, syncLinks,
      dispose: () => { observer.disconnect(); app.removeEventListener("ai-review-change", counts); } };
  }
  return { steps, stageStep, journey, summary, defaultTab, nextTab, waiting, enhance };
})();
