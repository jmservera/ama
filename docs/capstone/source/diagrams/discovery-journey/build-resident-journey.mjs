import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const directory = dirname(fileURLToPath(import.meta.url));
const repository = resolve(directory, "../../../../..");
const palette = {
  black: "#000000",
  green: "#173F35",
  ivory: "#FAF9F6",
  amber: "#885500",
  paleGreen: "#E8F1ED",
  paleAmber: "#FFF1D6",
  white: "#FFFFFF",
};
const sourceInputs = [
  ["brief", "docs/case_study_48_original.md", "## Business Challenge", "Case-study fact; requested autonomy and outcomes are not results"],
  ["profile", "docs/reference/research/company/company-profile-research.md", "### Resident Trust, Consent, and Accessibility", "Sector synthesis and unknown company details"],
  ["challenge", "docs/reference/research/company/agent-request-challenge.md", "## Purpose and Method", "Eight role research instruments; not interviews"],
  ["coordination", "docs/reference/research/company/agent-request-challenge.md", "## Contractor and Resident Coordination Agent", "Sector-informed hypothesis and bounded design proposal"],
  ["quality", "docs/reference/research/company/agent-request-challenge.md", "## Quality Verification Agent", "Sector-informed hypothesis; no AI quality acceptance"],
  ["atlas", "docs/reference/research/ux/customer-journeys/customer-journey-atlas.md", "## Evidence and scope", "Nine role research instruments; 27 companion maps plus one atlas map"],
  ["themes", "docs/reference/research/ux/customer-journeys/customer-journey-atlas.md", "## Five design themes and tensions", "Cross-role synthesis hypotheses, not independent resident evidence"],
  ["resident", "docs/reference/research/ux/customer-journeys/residents.md", "## Current journey A: rented resident household", "All five moments, actions, pains and gains are hypotheses"],
  ["assisted", "docs/reference/research/ux/customer-journeys/residents.md", "### Shared frame and assisted service", "Proposed accessible service; not completed usability or AT validation"],
  ["programme", "docs/reference/research/ux/customer-journeys/programme.md", "## Current-state journey hypotheses", "Professional-role hypotheses; distinct technical and QA decisions"],
  ["finance", "docs/reference/research/ux/customer-journeys/finance.md", "## Evidence boundary and financial tensions", "Finance hypotheses; award, claim and cash remain distinct"],
  ["addendum", "docs/case_study_48_addendum.md", "### Regulatory Evidence and Service Design", "Maintained proposal; resident rights and bounded assistance"],
  ["delivery", "docs/reference/research/ux/customer-journeys/customer-journey-atlas.md", "## Publication reconciliation", "Historical operator evidence; not human acceptance or measured benefit"],
  ["appointments", "docs/reference/research/ux/customer-journeys/residents.md", "### Appointment control engineering boundary", "Bounded synthetic engineering evidence; no live service acceptance"],
  ["independent-qa", "docs/reference/research/ux/customer-journeys/programme.md", "## Quality control engineering continuation", "Bounded synthetic engineering evidence; professional authority unverified"],
  ["commitments", "docs/reference/research/ux/customer-journeys/residents.md", "## Resident commitment and remedy criterion audit", "Bounded record and local engineering evidence; no delivered message or human acceptance"],
  ["sector-research", "docs/reference/research/sector/housing-association-primer.md", "## Source and Evidence Status", "Official statistics and regulator publications are sector context; secondary sources remain separately classified"],
  ["safety-standard", "docs/reference/regulatory/social-housing-regulation/social-housing-safety-and-quality-standard-2024.md", "2.3.1  Registered providers", "Regulatory standard, effective 2024-04-01; local snapshot 2026-09-19, not a fresh currentness check"],
  ["hazard-guidance", "docs/reference/regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md", "## 3 Awareness, triage and categorisation of hazards", "Official non-statutory guidance; local snapshot 2026-09-19; no clock interpretation or activation"],
  ["resident-adjustments", "docs/reference/regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md", "### 3.5", "Official non-statutory guidance on contact preferences and adjustments; not observed resident preferences"],
  ["pas-overview", "docs/reference/regulatory/retrofit-standards-and-funding/pas-2035-2023-bsi-overview.md", "## Conduct effective retrofits with PAS 2035", "Standards-body overview only, snapshot 2026-09-19; not the licensed standard or evidence of compliance"],
  ["source-policy", "docs/reference/regulatory/README.md", "## Authority and Use", "Dated source hierarchy; no fresh legal-currentness check"],
];
const sources = Object.fromEntries(sourceInputs.map(([key, path, anchor, classification]) => {
  const bytes = readFileSync(resolve(repository, path));
  const lines = bytes.toString("utf8").split(/\r?\n/);
  const line = lines.findIndex((entry) => entry.trimStart().startsWith(anchor.trimStart())) + 1;
  assert(line > 0, `Missing evidence anchor: ${path}: ${anchor}`);
  return [key, {
    path,
    line,
    section: lines[line - 1].replace(/^#+\s*/, "").trim(),
    sha256: createHash("sha256").update(bytes).digest("hex"),
    classification,
    localLink: `${relative(directory, resolve(repository, path)).replaceAll("\\", "/")}#L${line}`,
  }];
}));

const moments = [
  { key: "contact", title: "01  Contact", owner: "Housing", action: "Call / be heard", pain: "Story repeated", gain: "Clear contact", sources: ["resident", "assisted", "coordination"] },
  { key: "survey", title: "02  Survey", owner: "Assessor", action: "Plan visit", pain: "Needs missed", gain: "Visit support", sources: ["resident", "programme", "assisted"] },
  { key: "choice", title: "03  Decide", owner: "Resident", action: "Choose works", pain: "Rushed choice", gain: "Pause / defer", sources: ["resident", "coordination", "addendum"] },
  { key: "works", title: "04  Installation", owner: "Programme", action: "Keep routines", pain: "Disrupted day", gain: "Agreed visit", sources: ["resident", "programme", "appointments"] },
  { key: "aftercare", title: "05  Live with it", owner: "QA / Housing", action: "Use / query", pain: "Concern lost", gain: "Owned help", sources: ["resident", "quality", "independent-qa", "finance"] },
];
const rows = [
  { key: "action", label: "Do / need", top: 378, fill: palette.white, stroke: palette.green },
  { key: "pain", label: "Pain (hyp.)", top: 496, fill: palette.paleAmber, stroke: palette.amber },
  { key: "gain", label: "Gain (prop.)", top: 614, fill: palette.paleGreen, stroke: palette.green },
];
const metadata = {
  title: "Zava Forward: a resident's retrofit journey",
  date: "2026-10-30",
  canvas: { width: 1600, height: 900 },
  status: "Desk-research hypothesis; direct resident validation pending",
  method: "Case brief and official-sector research -> nine role RESEARCH INSTRUMENTS -> 28 journey HYPOTHESES -> pain/gain synthesis -> bounded design choices and tests",
  counting: "The 2026-09-26 agent-request challenge used eight instruments; the 2026-10-14 atlas used nine, including the Executive Reviewer. The 28 maps are 27 companion maps plus one leasehold-service staff map; two subjourneys and six later synthetic portal scripts are not additional stage maps.",
  geometrySource: "build-resident-journey.mjs",
  svgBoundary: "Standard-library SVG preview generated from the same native element geometry; not a native Excalidraw export",
  authority: "Human roles are proposed responsibilities, not verified postholder appointments. Gains are proposed responses, not delivered resident benefits. Independent QA, assisted routes, works choice and the separate human safety route remain mandatory design boundaries.",
  sources,
};
const elements = [];

function common(id, type, x, y, width, height, evidence = []) {
  assert(!elements.some((element) => element.id === id), `Duplicate id: ${id}`);
  return {
    id, type, x, y, width, height,
    angle: 0,
    strokeColor: palette.green,
    backgroundColor: "transparent",
    fillStyle: "solid",
    strokeWidth: 1.5,
    strokeStyle: "solid",
    roughness: 0,
    opacity: 100,
    groupIds: [],
    frameId: null,
    roundness: null,
    seed: elements.length + 101,
    version: 1,
    versionNonce: elements.length + 201,
    isDeleted: false,
    boundElements: null,
    updated: 1793318400000,
    link: evidence.length ? sources[evidence[0]].localLink : null,
    locked: false,
    customData: { evidence: evidence.map((key) => ({ key, ...sources[key] })) },
  };
}

function text(id, value, x, y, width, size = 34, evidence = [], containerId = null, align = "left") {
  const element = {
    ...common(id, "text", x, y, width, size * 2.5, evidence),
    strokeColor: palette.black,
    text: value,
    originalText: value,
    fontSize: size,
    fontFamily: 2,
    textAlign: align,
    verticalAlign: "middle",
    containerId,
    lineHeight: 2.5,
    autoResize: false,
  };
  elements.push(element);
  return element;
}

elements.push({
  ...common("journey-wrapper", "rectangle", 32, 222, 1536, 496, ["resident", "atlas"]),
  strokeColor: "transparent",
  strokeWidth: 0,
  customData: { role: "wrapper", ...metadata },
});
text("journey-title", metadata.title, 48, 12, 1504, 48, ["resident"]);
text("hypothesis-notice", metadata.status, 48, 124, 1504, 34, ["atlas", "resident"]);
text("human-label", "Human role", 48, 286, 224, 34, ["profile"]);

moments.forEach((moment, index) => {
  const left = 300 + index * 252;
  text(`${moment.key}-title`, moment.title, left + 6, 212, 232, 34, moment.sources, null, "center");
  text(`${moment.key}-owner`, moment.owner, left + 6, 286, 232, 34, moment.sources, null, "center");
  rows.forEach((row) => {
    const boxId = `${moment.key}-${row.key}`;
    const labelId = `${boxId}-text`;
    elements.push({
      ...common(boxId, "rectangle", left, row.top, 244, 104, moment.sources),
      strokeColor: row.stroke,
      backgroundColor: row.fill,
      boundElements: [{ id: labelId, type: "text" }],
      customData: { role: "leaf", moment: moment.key, row: row.key, traceId: `D0${index + 1}`, classification: row.key === "gain" ? "Proposed design response; gain unmeasured" : "Desk-research journey hypothesis", evidence: moment.sources.map((key) => ({ key, ...sources[key] })) },
    });
    text(labelId, moment[row.key], left + 8, row.top + 9.5, 228, 34, moment.sources, boxId, "center");
  });
});
rows.forEach((row) => text(`${row.key}-label`, row.label, 48, row.top + 9.5, 224, 34, ["resident"]));
text("retained-boundaries", "Phone / letter / assisted visits; independent QA; urgent safety -> human repairs.", 48, 722, 1504, 34, ["resident", "assisted", "quality"]);
text("discovery-trace", "Brief + official sources > 9 role instruments > 28 maps > bounded design", 48, 810, 1504, 34, ["brief", "atlas", "themes", "challenge", "sector-research", "safety-standard", "hazard-guidance", "resident-adjustments", "pas-overview"]);

const drawing = {
  type: "excalidraw",
  version: 2,
  source: "GitHub Copilot / bounded DT presentation collaboration",
  elements,
  appState: { viewBackgroundColor: palette.ivory, gridSize: null, name: "Zava Forward resident journey hypotheses" },
  files: {},
};

function validate() {
  assert.equal(moments.length, 5);
  assert.equal(rows.length, 3);
  const ids = new Map(elements.map((element) => [element.id, element]));
  assert.equal(ids.size, elements.length);
  assert.equal(elements.filter((element) => element.customData?.role === "leaf").length, 15);
  for (const element of elements) {
    assert([element.x, element.y, element.width, element.height].every(Number.isFinite), element.id);
    assert(element.width > 0 && element.height > 0, element.id);
    assert(element.x >= 0 && element.y >= 0 && element.x + element.width <= 1600 && element.y + element.height <= 900, `Canvas overflow: ${element.id}`);
    if (element.type === "text") {
      assert.equal(element.strokeColor, palette.black, element.id);
      assert(element.fontSize >= 34, `Below 25.5pt at 96dpi: ${element.id}`);
      assert(!element.text.includes("\n"), `Wrapped cell: ${element.id}`);
      assert.equal(element.height, element.fontSize * 2.5, element.id);
      if (element.containerId) {
        const container = ids.get(element.containerId);
        assert(container?.boundElements.some((entry) => entry.id === element.id && entry.type === "text"), `Missing reciprocal binding: ${element.id}`);
        assert(element.x >= container.x && element.y >= container.y && element.x + element.width <= container.x + container.width && element.y + element.height <= container.y + container.height, `Cell overflow: ${element.id}`);
      }
    }
    if (element.customData?.role === "wrapper") assert.equal(element.backgroundColor, "transparent");
    for (const bound of element.boundElements ?? []) assert.equal(ids.get(bound.id)?.containerId, element.id);
  }
  assert.equal(ids.get("hypothesis-notice").text, metadata.status);
}

function escapeXml(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&apos;");
}

function svgFromDrawing() {
  const markup = elements.map((element) => {
    if (element.type === "rectangle") {
      return `<rect id="${element.id}" x="${element.x}" y="${element.y}" width="${element.width}" height="${element.height}" fill="${element.backgroundColor === "transparent" ? "none" : element.backgroundColor}" stroke="${element.strokeColor === "transparent" ? "none" : element.strokeColor}" stroke-width="${element.strokeWidth}"/>`;
    }
    assert.equal(element.type, "text");
    const horizontal = element.textAlign === "center" ? element.x + element.width / 2 : element.x;
    return `<text id="${element.id}" x="${horizontal}" y="${element.y + element.height / 2}" font-family="Helvetica, Arial, sans-serif" font-size="${element.fontSize}" fill="#000000" text-anchor="${element.textAlign === "center" ? "middle" : "start"}" dominant-baseline="central">${escapeXml(element.text)}</text>`;
  });
  return [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title description">',
    `<title id="title">${escapeXml(metadata.title)}</title>`,
    `<desc id="description">${escapeXml(`${metadata.status}. Five resident moments; three rows: actions and needs, pain hypotheses, proposed gains. Human roles are proposed. ${metadata.authority} Read text-equivalent.md for full stage descriptions, source provisions, decision tests and presentation notes.`)}</desc>`,
    `<metadata>${escapeXml(JSON.stringify(metadata))}</metadata>`,
    `<rect width="1600" height="900" fill="${palette.ivory}"/>`,
    ...markup,
    "</svg>",
    "",
  ].join("\n");
}

function validateHandoff() {
  const handoff = readFileSync(resolve(directory, "text-equivalent.md"), "utf8").replace(/^\uFEFF/, "").replaceAll("\r\n", "\n");
  assert(handoff.includes(metadata.status));
  assert(handoff.startsWith("---\n"));
  assert(!/^# /m.test(handoff), "Frontmatter title must not be duplicated as an H1.");
  assert(!/[\t]| +$/m.test(handoff), "Markdown whitespace defect.");
  assert(!/[^\x00-\x7F]/.test(handoff), "Unexpected non-ASCII content.");
  for (const moment of moments) {
    for (const key of ["action", "pain", "gain"]) assert(handoff.includes(moment[key]), `Missing text equivalent: ${moment.key}/${key}`);
  }
  let linkCount = 0;
  for (const match of handoff.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    const [target, fragment] = match[1].split("#");
    assert(!/^[a-z]+:/i.test(target), "Handoff links must resolve to local public repository evidence.");
    const destination = resolve(directory, decodeURIComponent(target));
    assert(!relative(repository, destination).startsWith(".."), `Out-of-repository link: ${target}`);
    const content = readFileSync(destination, "utf8");
    if (fragment?.startsWith("L")) {
      assert(/^L\d+$/.test(fragment), `Invalid line reference: ${fragment}`);
      assert(Number(fragment.slice(1)) <= content.split(/\r?\n/).length, `Missing line: ${target}#${fragment}`);
    } else if (fragment) {
      const headings = [...content.matchAll(/^#{1,6}\s+(.+)$/gm)].map((entry) => entry[1].toLowerCase().replace(/[^\w\s-]/g, "").replace(/\s/g, "-"));
      assert(headings.includes(fragment), `Missing heading: ${target}#${fragment}`);
    }
    linkCount += 1;
  }
  const notes = [...handoff.matchAll(/### Page (8|13) Speaker Notes\n\n```text\n([\s\S]*?)\n```/g)];
  assert.equal(notes.length, 2);
  for (const [, page, script] of notes) {
    const words = script.match(/\b[\w]+(?:['-][\w]+)*\b/g).length;
    assert(words >= 120 && words <= 160, `Page ${page} script is ${words} words, outside the intended roughly 60-second range.`);
    console.log(`Page ${page}: ${words} spoken words; timing is an estimate, not a rehearsal result.`);
  }
  console.log(`Validated ${linkCount} local Markdown links and both complete speaker scripts.`);
}

validate();
validateHandoff();
const outputs = new Map([
  ["resident-journey.excalidraw", `${JSON.stringify(drawing, null, 2)}\n`],
  ["resident-journey.svg", svgFromDrawing()],
]);
for (const [filename, content] of outputs) {
  const destination = resolve(directory, filename);
  assert.equal(dirname(destination), directory);
  if (process.argv.includes("--check")) assert.equal(readFileSync(destination, "utf8"), content, `Stale generated asset: ${filename}`);
  else writeFileSync(destination, content, { encoding: "utf8" });
}
console.log(`Validated ${elements.length} native elements, 15 single-line cells, five moments, three rows, reciprocal bindings, 1600x900 bounds and ${Object.keys(sources).length} source locators.`);
console.log(`All visible text is black, minimum 34px (25.5pt at 96dpi). ${process.argv.includes("--check") ? "Generated files match source." : "Native JSON and same-geometry SVG generated."}`);