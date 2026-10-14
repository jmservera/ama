window.addEventListener("message", async (event) => {
  if (event.source !== parent || event.data?.type !== "render-diagram" || typeof event.data.source !== "string") return;
  try {
    const mermaid = globalThis.workbenchMermaid;
    if (!mermaid) throw new Error("The local Mermaid renderer failed to load.");
    mermaid.initialize({
      startOnLoad: false, securityLevel: "strict", htmlLabels: false,
      flowchart: { htmlLabels: false }, suppressErrorRendering: true,
      secure: ["secure", "securityLevel", "startOnLoad", "maxTextSize", "htmlLabels", "flowchart"],
    });
    const { svg } = await mermaid.render("diagram", event.data.source);
    parent.postMessage({ type: "diagram-result", svg }, "*");
  } catch (error) {
    parent.postMessage({ type: "diagram-result", error: error.message }, "*");
  }
});
