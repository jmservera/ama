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
  rule: "#C7D8CF",
  muted: "#50655E",
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
  { key: "action", label: "ACTION /\nNEED", top: 180, fill: palette.ivory, color: palette.green },
  { key: "pain", label: "PAIN\nTO TEST", top: 302, fill: palette.paleAmber, color: palette.amber },
  { key: "gain", label: "GAIN\nSOUGHT", top: 424, fill: palette.paleGreen, color: palette.green },
];
const metadata = {
  title: "Zava Forward: a resident's retrofit journey",
  date: "2026-10-30",
  canvas: { width: 1600, height: 560 },
  status: "Desk-research hypothesis; direct resident validation pending",
  method: "Case brief and official-sector research -> nine role RESEARCH INSTRUMENTS -> 28 journey HYPOTHESES -> pain/gain synthesis -> bounded design choices and tests",
  counting: "The 2026-09-26 agent-request challenge used eight instruments; the 2026-10-14 atlas used nine, including the Executive Reviewer. The 28 maps are 27 companion maps plus one leasehold-service staff map; two subjourneys and six later synthetic portal scripts are not additional stage maps.",
  geometrySource: "build-resident-journey.mjs",
  svgBoundary: "Same-geometry SVG from the editable Excalidraw elements; no observed or quantified sentiment curve",
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

function text(id, value, x, y, width, size = 38, evidence = [], containerId = null, align = "left", color = palette.green) {
  const element = {
    ...common(id, "text", x, y, width, value.split("\n").length * size * 1.14, evidence),
    strokeColor: color,
    text: value,
    originalText: value,
    fontSize: size,
    fontFamily: 2,
    textAlign: align,
    verticalAlign: "middle",
    containerId,
    lineHeight: 1.14,
    autoResize: false,
  };
  elements.push(element);
  return element;
}

function line(id, points, color = palette.green, width = 2.5, evidence = []) {
  const left = Math.min(...points.map(([x]) => x));
  const top = Math.min(...points.map(([, y]) => y));
  const right = Math.max(...points.map(([x]) => x));
  const bottom = Math.max(...points.map(([, y]) => y));
  elements.push({
    ...common(id, "line", left, top, right - left, bottom - top, evidence),
    strokeColor: color,
    strokeWidth: width,
    points: points.map(([x, y]) => [x - left, y - top]),
    lastCommittedPoint: null,
    startBinding: null,
    endBinding: null,
    startArrowhead: null,
    endArrowhead: null,
  });
}

function rectangle(id, x, y, width, height, fill, evidence = [], extra = {}) {
  elements.push({
    ...common(id, "rectangle", x, y, width, height, evidence),
    backgroundColor: fill,
    strokeColor: "transparent",
    strokeWidth: 0,
    ...extra,
  });
}

function icon(moment, cx) {
  elements.push({
    ...common(`${moment.key}-icon-disc`, "ellipse", cx - 36, 4, 72, 72, moment.sources),
    backgroundColor: palette.paleGreen,
    customData: { role: "touchpoint-icon", evidence: moment.sources.map((key) => ({ key, ...sources[key] })) },
  });
  const stroke = (suffix, points) => line(`${moment.key}-icon-${suffix}`, points.map(([x, y]) => [cx + x, y]), palette.green, 2.8, moment.sources);
  if (moment.key === "contact") {
    stroke("bubble", [[-21, 21], [21, 21], [21, 49], [-5, 49], [-16, 59], [-12, 49], [-21, 49], [-21, 21]]);
    stroke("message-one", [[-12, 31], [12, 31]]);
    stroke("message-two", [[-12, 39], [5, 39]]);
  } else if (moment.key === "survey") {
    stroke("clipboard", [[-18, 19], [18, 19], [18, 60], [-18, 60], [-18, 19]]);
    stroke("clip", [[-8, 24], [-8, 15], [8, 15], [8, 24], [-8, 24]]);
    [35, 44, 53].forEach((y, index) => stroke(`row-${index}`, [[-9, y], [10, y]]));
  } else if (moment.key === "choice") {
    stroke("shield", [[0, 15], [21, 23], [18, 44], [10, 55], [0, 63], [-10, 55], [-18, 44], [-21, 23], [0, 15]]);
    stroke("check", [[-10, 38], [-2, 46], [13, 30]]);
  } else if (moment.key === "works") {
    stroke("roof", [[-25, 35], [0, 15], [25, 35]]);
    stroke("home", [[-18, 30], [-18, 61], [18, 61], [18, 30]]);
    stroke("door", [[-5, 61], [-5, 44], [6, 44], [6, 61]]);
  } else {
    stroke("care", [[0, 58], [-22, 38], [-22, 27], [-14, 19], [-5, 19], [0, 26], [5, 19], [14, 19], [22, 27], [22, 38], [0, 58]]);
  }
}

const displays = {
  contact: ["Call /\nbe heard", "Story\nrepeated", "Clear\ncontact"],
  survey: ["Plan\nvisit", "Needs\nmissed", "Visit\nsupport"],
  choice: ["Choose\nworks", "Rushed\nchoice", "Pause /\ndefer"],
  works: ["Keep\nroutines", "Disrupted\nday", "Agreed\nvisit"],
  aftercare: ["Use /\nquery", "Concern\nlost", "Owned\nhelp"],
};

rectangle("journey-canvas", 0, 0, 1600, 560, palette.ivory, ["resident", "atlas"], {
  customData: { role: "canvas", ...metadata },
});
line("touchpoint-rail", [[353, 40], [1433, 40]], palette.rule, 3.5, ["resident"]);
text("human-label", "Human role", 0, 131, 204, 29, ["profile"], null, "left", palette.muted);

moments.forEach((moment, index) => {
  const left = 226 + index * 270;
  icon(moment, left + 127);
  text(`${moment.key}-title`, moment.title.replace(/\s+/g, " "), left, 86, 254, 34, moment.sources, null, "center");
  text(`${moment.key}-owner`, moment.owner, left, 131, 254, 29, moment.sources, null, "center", palette.muted);
  rows.forEach((row, rowIndex) => {
    const boxId = `${moment.key}-${row.key}`;
    const labelId = `${boxId}-text`;
    rectangle(boxId, left, row.top, 254, 104, row.fill, moment.sources, {
      boundElements: [{ id: labelId, type: "text" }],
      customData: { role: "leaf", moment: moment.key, row: row.key, traceId: `D0${index + 1}`, classification: row.key === "gain" ? "Proposed design response; gain unmeasured" : "Desk-research journey hypothesis", evidence: moment.sources.map((key) => ({ key, ...sources[key] })) },
    });
    text(labelId, displays[moment.key][rowIndex], left + 8, row.top + 8.5, 238, 38, moment.sources, boxId, "center", row.color);
  });
});
rows.forEach((row) => {
  rectangle(`${row.key}-accent`, 0, row.top + 9, 5, 86, row.color, ["resident"]);
  text(`${row.key}-label`, row.label, 20, row.top + 15, 184, 30, ["resident"], null, "left", row.color);
});

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
    assert(element.width >= 0 && element.height >= 0 && (element.width > 0 || element.height > 0), element.id);
    assert(element.x >= 0 && element.y >= 0 && element.x + element.width <= metadata.canvas.width && element.y + element.height <= metadata.canvas.height, `Canvas overflow: ${element.id}`);
    if (element.type === "text") {
      assert(element.fontSize >= 29, `Unreadable diagram label: ${element.id}`);
      assert(element.text.split("\n").length <= 2, `Overloaded cell: ${element.id}`);
      assert.equal(element.height, element.text.split("\n").length * element.fontSize * 1.14, element.id);
      if (element.containerId) {
        const container = ids.get(element.containerId);
        assert(container?.boundElements.some((entry) => entry.id === element.id && entry.type === "text"), `Missing reciprocal binding: ${element.id}`);
        assert(element.x >= container.x && element.y >= container.y && element.x + element.width <= container.x + container.width && element.y + element.height <= container.y + container.height, `Cell overflow: ${element.id}`);
      }
    }
    if (element.type === "line") {
      assert(element.points.length >= 2, `Missing line points: ${element.id}`);
      assert(element.points.every((point) => point.length === 2 && point.every(Number.isFinite)), element.id);
      assert.equal(element.startBinding, null);
      assert.equal(element.endBinding, null);
    }
    for (const bound of element.boundElements ?? []) assert.equal(ids.get(bound.id)?.containerId, element.id);
  }
  assert.equal(elements.filter((element) => element.customData?.role === "touchpoint-icon").length, 5);
  for (const moment of moments) {
    for (const key of ["action", "pain", "gain"]) {
      const displayed = ids.get(`${moment.key}-${key}-text`).text.replaceAll("\n", " ");
      assert.equal(displayed, moment[key], `Changed source claim: ${moment.key}/${key}`);
    }
  }
}

function escapeXml(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&apos;");
}

function svgFromDrawing() {
  const markup = elements.map((element) => {
    if (element.type === "rectangle") {
      return `<rect id="${element.id}" x="${element.x}" y="${element.y}" width="${element.width}" height="${element.height}" fill="${element.backgroundColor === "transparent" ? "none" : element.backgroundColor}" stroke="${element.strokeColor === "transparent" ? "none" : element.strokeColor}" stroke-width="${element.strokeWidth}"/>`;
    }
    if (element.type === "ellipse") {
      return `<ellipse id="${element.id}" cx="${element.x + element.width / 2}" cy="${element.y + element.height / 2}" rx="${element.width / 2}" ry="${element.height / 2}" fill="${element.backgroundColor}" stroke="${element.strokeColor}" stroke-width="${element.strokeWidth}"/>`;
    }
    if (element.type === "line") {
      const points = element.points.map(([x, y]) => `${element.x + x},${element.y + y}`).join(" ");
      return `<polyline id="${element.id}" points="${points}" fill="none" stroke="${element.strokeColor}" stroke-width="${element.strokeWidth}" stroke-linecap="round" stroke-linejoin="round"/>`;
    }
    assert.equal(element.type, "text");
    const horizontal = element.textAlign === "center" ? element.x + element.width / 2 : element.x;
    const lines = element.text.split("\n").map((value, index) =>
      `<tspan x="${horizontal}" y="${element.y + element.fontSize * (0.88 + index * element.lineHeight)}">${escapeXml(value)}</tspan>`);
    return `<text id="${element.id}" font-family="Arial, Helvetica, sans-serif" font-size="${element.fontSize}" fill="${element.strokeColor}" text-anchor="${element.textAlign === "center" ? "middle" : "start"}">${lines.join("")}</text>`;
  });
  return [
    `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="560" viewBox="0 0 1600 560" role="img" aria-labelledby="title description">`,
    `<title id="title">${escapeXml(metadata.title)}</title>`,
    `<desc id="description">${escapeXml(`${metadata.status}. Five resident moments; three rows: actions and needs, pain hypotheses, proposed gains. Human roles are proposed. ${metadata.authority} Read text-equivalent.md for full stage descriptions, source provisions, decision tests and presentation notes.`)}</desc>`,
    `<metadata>${escapeXml(JSON.stringify(metadata))}</metadata>`,
    `<rect width="1600" height="560" fill="${palette.ivory}"/>`,
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
console.log(`Validated ${elements.length} native elements, 15 two-line cells, five illustrated touchpoints, reciprocal bindings, 1600x560 bounds and ${Object.keys(sources).length} source locators.`);
console.log(`Cell text is 38px; labels are at least 29px. ${process.argv.includes("--check") ? "Generated files match source." : "Native JSON and same-geometry SVG generated."}`);