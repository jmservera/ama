import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const directory = dirname(fileURLToPath(import.meta.url));
const repository = resolve(directory, "../../../../..");
const colours = {
  ink: "#173F35", muted: "#50655E", paper: "#FAF9F6", green: "#E8F1ED",
  rule: "#C7D8CF", white: "#FFFFFF", purple: "#61437C", palePurple: "#EEE8F4",
  amber: "#885500", paleAmber: "#FFF1D6", azure: "#0078D4", paleAzure: "#EDF5FC",
};
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const xml = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&apos;");

function source(path, anchor, classification) {
  const bytes = readFileSync(resolve(repository, path));
  const lines = bytes.toString("utf8").split(/\r?\n/);
  const line = lines.findIndex((entry) => entry.trimStart().startsWith(anchor.trimStart())) + 1;
  assert(line > 0, `Missing source anchor: ${path}: ${anchor}`);
  return { path, line, anchor, sha256: digest(bytes), classification };
}

function sourceAt(path, line, classification) {
  const bytes = readFileSync(resolve(repository, path));
  const lines = bytes.toString("utf8").split(/\r?\n/);
  assert(Number.isInteger(line) && line > 0 && line <= lines.length, `Missing source line: ${path}:${line}`);
  return { path, line, anchor: lines[line - 1].trim(), sha256: digest(bytes), classification };
}

const sources = {
  identity: source("src/api/src/zava_forward/api/auth.py", "class TrustedProxyProvider:", "Source-coded employee principal checks; platform authentication is a separate dependency"),
  roles: source("src/api/src/zava_forward/api/auth.py", "DEFAULT_ROLE_MAP = {", "Application role mapping, not unrestricted company-account access"),
  gates: source("src/core/src/zava_forward/core/gates.py", "def transition_allowed(", "Explicit coded state-flow; unknown gates do not pass"),
  transition: source("src/core/src/zava_forward/core/store.py", "    def advance(", "Controlled human case transition, not an AI action"),
  advice: source("src/agents/README.md", "### Five retrofit assistants", "Five source-coded proposal helpers; activation/benefit acceptance separate"),
  chat: source("src/api/README.md", "## Employee chat with bounded skills", "One selected skill and bounded call; no tools or case writes"),
  files: source("src/importer/README.md", "* Excel transition", "Read-only file tooling; live OneDrive connector not established"),
  sensors: source("docs/reference/research/iot-sensor-analytics-research-plan.md", "## Bounded streaming engineering", "Source/dated synthetic exercise; live device/consent/analysis acceptance separate"),
  resident: source("src/core/src/zava_forward/core/resident_preview.py", "FIELD_CATALOG =", "Field-limited resident view; separate identity and own-case grants"),
  infrastructure: sourceAt("infra/main.bicep", 70, "Selected shared-API source realization; enableApiAi and background workloads have independent conditions"),
  network: sourceAt("infra/modules/network.bicep", 27, "Authored VNet/subnets/NSGs/private DNS; not an observed live allocation"),
  compute: sourceAt("infra/modules/containerapps.bicep", 119, "Shared API/EasyAuth and conditional workloads; direct-demo and internal profiles are distinct"),
  sql: sourceAt("infra/modules/sql.bicep", 34, "Managed SQL service outside VNet; contained-user/grant initialization separate"),
  storage: sourceAt("infra/modules/storage.bicep", 58, "Authored Blob containers and queues; quarantine/retention configuration is not accepted scanner or erasure proof"),
  model: sourceAt("infra/modules/foundry.bicep", 16, "Foundry account/project/deployments; direct API inference conditional; GlobalStandard is not UK processing proof"),
  deviceTransport: sourceAt("infra/modules/iothub.bicep", 50, "B1 Hub/private Event Hub adapter; routing-ready, SDK wiring and live consumer acceptance separate"),
  workloadIdentity: sourceAt("infra/modules/identity.bicep", 6, "Four workload managed identities; not employee or resident sign-in"),
  registry: sourceAt("infra/modules/registry.bicep", 15, "Private registry and MI image pull; placeholder workload operation not established"),
  vault: sourceAt("infra/modules/keyvault.bicep", 15, "Private Key Vault; secret-reference resolution by workload identity"),
  monitoring: sourceAt("infra/modules/monitoring.bicep", 14, "Log Analytics/App Insights/AMPLS; platform diagnostics are not complete application tracing"),
  alerts: sourceAt("infra/modules/operationalMonitoring.bicep", 17, "Candidate alerts gated; budgets notify rather than hard-stop spending"),
  productionEdge: sourceAt("infra/modules/edge.bicep", 23, "Alternative Front Door/WAF/private-origin entrance; connection acceptance per deployment"),
  tokens: sourceAt("infra/modules/authTokenStore.bicep", 15, "Optional separate token-only Blob/renewal job; requires ready state"),
  residentDeployment: sourceAt("infra/resident-demo.bicep", 14, "Separate synthetic resident showcase; its configured SQL dependency does not prove shared staff SQL"),
  residentModel: sourceAt("infra/resident-assistant.bicep", 24, "Optional separate public Sweden Central Standard model; default off, not inside the UK/private core"),
  simulator: sourceAt("infra/live-simulator-job.bicep", 18, "Conditional synthetic job and referenced existing certificate mount; not provisioned by main"),
};

function scene(name, width, height, status) {
  const elements = [];
  const files = {};
  let currentFrame = null;
  const metadata = {
    name, date: "2026-11-08",
    model_basis_head: "c50e9f0b888e267d5949cab09069d31b6c740e3b",
    source_head: "fa7ae0c9770e890f82482456bfcb8e97f1e05429",
    width, height, status, sources,
  };
  function base(id, type, box, evidence = []) {
    assert(!elements.some((entry) => entry.id === id), `Duplicate element: ${id}`);
    return {
      id, type, x: box[0], y: box[1], width: box[2], height: box[3],
      angle: 0, strokeColor: colours.ink, backgroundColor: "transparent",
      fillStyle: "solid", strokeWidth: 2, strokeStyle: "solid", roughness: 0,
      opacity: 100, groupIds: [], frameId: currentFrame, roundness: null,
      seed: elements.length + 101, version: 1, versionNonce: elements.length + 201,
      isDeleted: false, boundElements: null, updated: 1794096000000,
      link: null, locked: false,
      customData: { evidence: evidence.map((key) => ({ key, ...sources[key] })) },
    };
  }
  function rectangle(id, box, fill = colours.white, stroke = colours.rule, dashed = false, evidence = []) {
    const element = { ...base(id, "rectangle", box, evidence), backgroundColor: fill,
      strokeColor: stroke, strokeStyle: dashed ? "dashed" : "solid" };
    elements.push(element);
    return element;
  }
  function frame(id, box, label) {
    elements.push({ ...base(id, "frame", box), name: label });
    currentFrame = id;
  }
  function endFrame() { currentFrame = null; }
  function text(id, value, x, y, w, size = 28, colour = colours.ink, align = "left", evidence = []) {
    const element = {
      ...base(id, "text", [x, y, w, value.split("\n").length * size * 1.15], evidence),
      strokeColor: colour, text: value, originalText: value, fontSize: size,
      fontFamily: 2, textAlign: align, verticalAlign: "top",
      containerId: null, lineHeight: 1.15, autoResize: false,
    };
    elements.push(element);
    return element;
  }
  function arrow(id, points, colour = colours.ink, dashed = false, both = false, evidence = []) {
    const xs = points.map((point) => point[0]), ys = points.map((point) => point[1]);
    const x = Math.min(...xs), y = Math.min(...ys);
    elements.push({
      ...base(id, "arrow", [x, y, Math.max(...xs) - x, Math.max(...ys) - y], evidence),
      strokeColor: colour, strokeStyle: dashed ? "dashed" : "solid",
      strokeWidth: 3, points: points.map(([px, py]) => [px - x, py - y]),
      lastCommittedPoint: null, startBinding: null, endBinding: null,
      startArrowhead: both ? "triangle" : null, endArrowhead: "triangle",
      elbowed: false,
    });
  }
  function node(id, box, title, body, { fill = colours.white, colour = colours.ink,
    dashed = false, evidence = [], titleSize = 34, bodySize = 26 } = {}) {
    rectangle(id, box, fill, dashed ? colours.amber : colours.rule, dashed, evidence);
    const heading = text(`${id}-title`, title, box[0] + 20, box[1] + 14, box[2] - 40, titleSize, colour, "left", evidence);
    const top = box[1] + 18 + title.split("\n").length * titleSize * 1.15;
    const detail = text(`${id}-body`, body, box[0] + 20, top, box[2] - 40, bodySize, colour, "left", evidence);
    heading.customData.container = id;
    detail.customData.container = id;
  }
  function icon(id, path, box) {
    const bytes = readFileSync(resolve(repository, path));
    const svg = bytes.toString("utf8");
    const viewBox = svg.match(/\bviewBox=["']([\d.\s-]+)["']/);
    assert(viewBox, `Icon has no declared aspect ratio: ${path}`);
    const [, , sw, sh] = viewBox[1].trim().split(/\s+/).map(Number);
    assert(sw > 0 && sh > 0 && !/\b(?:href|src)=["']https?:/i.test(svg), `Invalid/non-local icon: ${path}`);
    const scale = Math.min(box[2] / sw, box[3] / sh);
    const contained = [box[0] + (box[2] - sw * scale) / 2, box[1] + (box[3] - sh * scale) / 2, sw * scale, sh * scale];
    const fileId = digest(bytes);
    files[fileId] = { id: fileId, mimeType: "image/svg+xml", dataURL: `data:image/svg+xml;base64,${bytes.toString("base64")}`, created: 1794096000000, lastRetrieved: 1794096000000 };
    elements.push({ ...base(id, "image", contained), fileId, status: "saved", scale: [1, 1], crop: null,
      customData: { evidence: [], icon_source: { path, sha256: fileId, aspect_ratio: sw / sh, rights: "Microsoft architecture icons; unchanged bytes and aspect ratio" } } });
  }
  function service(id, box, iconName, title, body, evidence = [], dashed = false) {
    rectangle(id, box, colours.white, dashed ? colours.azure : colours.rule, dashed, evidence);
    icon(`${id}-icon`, `docs/architecture/assets/azure/${iconName}.svg`, [box[0] + 18, box[1] + 27, 70, 70]);
    const heading = text(`${id}-title`, title, box[0] + 108, box[1] + 16, box[2] - 130, 40, colours.ink, "left", evidence);
    const detail = text(`${id}-body`, body, box[0] + 108, box[1] + 71, box[2] - 130, 32, colours.muted, "left", evidence);
    heading.customData.container = id; detail.customData.container = id;
  }
  function badge(id, value, x, y, evidence = []) {
    const width = value.length > 2 ? 64 : 48;
    elements.push({ ...base(id, "ellipse", [x, y, width, 48], evidence), backgroundColor: colours.azure, strokeColor: colours.azure });
    text(`${id}-number`, value, x, y + 4, width, value.length > 2 ? 28 : 32, colours.white, "center", evidence);
  }
  function validate() {
    const byId = new Map(elements.map((element) => [element.id, element]));
    for (const element of elements) {
      assert([element.x, element.y, element.width, element.height].every(Number.isFinite), element.id);
      assert(element.width >= 0 && element.height >= 0, element.id);
      assert(element.x >= 0 && element.y >= 0 && element.x + element.width <= width && element.y + element.height <= height, `Canvas overflow: ${element.id}`);
      if (element.type === "text") {
        assert(element.fontSize >= 24, `Unreadable label: ${element.id}`);
        assert(element.text.length > 0, element.id);
        if (element.customData.container) {
          const container = byId.get(element.customData.container);
          assert(container && element.x >= container.x && element.y >= container.y &&
            element.x + element.width <= container.x + container.width &&
            element.y + element.height <= container.y + container.height, `Node text overflow: ${element.id}`);
        }
      }
      if (element.type === "arrow") assert(element.points.length >= 2 && element.points.every((point) => point.every(Number.isFinite)), element.id);
      if (element.type === "image") {
        assert(files[element.fileId], `Missing embedded icon: ${element.id}`);
        assert(Math.abs(element.width / element.height - element.customData.icon_source.aspect_ratio) < 1e-9, `Distorted icon: ${element.id}`);
        assert.deepEqual(element.scale, [1, 1]);
        assert.equal(element.crop, null);
      }
      if (element.frameId) {
        const container = byId.get(element.frameId);
        assert(container?.type === "frame" && element.x >= container.x && element.y >= container.y &&
          element.x + element.width <= container.x + container.width &&
          element.y + element.height <= container.y + container.height, `Frame overflow: ${element.id}`);
      }
      assert(element.customData.evidence.every((entry) => entry.path && entry.line > 0 && entry.sha256), element.id);
    }
    assert(!elements.some((element) => element.type === "image" && /https?:/.test(files[element.fileId].dataURL)));
  }
  function drawing() {
    validate();
    return { type: "excalidraw", version: 2, source: "Original Zava Forward presentation diagram",
      elements, appState: { viewBackgroundColor: colours.paper, gridSize: null, name }, files };
  }
  function svg(frameId = null) {
    validate();
    const selected = frameId ? elements.filter((element) => element.frameId === frameId) : elements;
    const selectedFrame = frameId ? elements.find((element) => element.id === frameId) : null;
    assert(!frameId || selectedFrame?.type === "frame", `Missing export frame: ${frameId}`);
    const viewport = selectedFrame ? [selectedFrame.x, selectedFrame.y, selectedFrame.width, selectedFrame.height] : [0, 0, width, height];
    const markers = Object.entries(colours).map(([key, colour]) =>
      `<marker id="arrow-${key}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="${colour}"/></marker>`).join("");
    const markup = selected.map((element) => {
      const colourKey = Object.keys(colours).find((key) => colours[key] === element.strokeColor);
      const dash = element.strokeStyle === "dashed" ? ' stroke-dasharray="10 7"' : "";
      if (element.type === "frame") return "";
      if (element.type === "rectangle") return `<rect id="${element.id}" x="${element.x}" y="${element.y}" width="${element.width}" height="${element.height}" fill="${element.backgroundColor}" stroke="${element.strokeColor}" stroke-width="${element.strokeWidth}"${dash}/>`;
      if (element.type === "ellipse") return `<ellipse id="${element.id}" cx="${element.x + element.width / 2}" cy="${element.y + element.height / 2}" rx="${element.width / 2}" ry="${element.height / 2}" fill="${element.backgroundColor}" stroke="${element.strokeColor}" stroke-width="${element.strokeWidth}"/>`;
      if (element.type === "arrow" || element.type === "line") {
        const points = element.points.map(([x, y]) => `${element.x + x},${element.y + y}`).join(" ");
        const heads = element.type === "arrow" ? ` marker-end="url(#arrow-${colourKey})"${element.startArrowhead ? ` marker-start="url(#arrow-${colourKey})"` : ""}` : "";
        return `<polyline id="${element.id}" points="${points}" fill="none" stroke="${element.strokeColor}" stroke-width="${element.strokeWidth}" stroke-linejoin="round"${dash}${heads}/>`;
      }
      if (element.type === "image") return `<image id="${element.id}" x="${element.x}" y="${element.y}" width="${element.width}" height="${element.height}" preserveAspectRatio="xMidYMid meet" href="${files[element.fileId].dataURL}"/>`;
      assert.equal(element.type, "text");
      const x = element.textAlign === "center" ? element.x + element.width / 2 : element.x;
      const lines = element.text.split("\n").map((value, index) => `<tspan x="${x}" y="${element.y + element.fontSize * (.88 + index * element.lineHeight)}">${xml(value)}</tspan>`).join("");
      return `<text id="${element.id}" font-family="Arial, Helvetica, sans-serif" font-size="${element.fontSize}" fill="${element.strokeColor}" text-anchor="${element.textAlign === "center" ? "middle" : "start"}">${lines}</text>`;
    });
    return [
      `<svg xmlns="http://www.w3.org/2000/svg" width="${viewport[2]}" height="${viewport[3]}" viewBox="${viewport.join(" ")}" role="img" aria-labelledby="title description">`,
      `<title id="title">${xml(name)}</title><desc id="description">${xml(status)}. Read text-equivalent.md for relationships, source locators and acceptance limits.</desc>`,
      `<metadata>${xml(JSON.stringify(metadata))}</metadata><defs>${markers}</defs>`,
      `<rect width="${width}" height="${height}" fill="${colours.paper}"/>`, ...markup, "</svg>", "",
    ].join("\n");
  }
  rectangle("canvas", [0, 0, width, height], colours.paper, "transparent");
  return { rectangle, text, arrow, node, icon, service, badge, frame, endFrame, drawing, svg, metadata };
}

function cxo() {
  const d = scene("Zava Forward: people, case control, evidence and advice", 1600, 620,
    "Conceptual application/data-scope view; not a network map or live inventory. Dashed paths are separately gated integration/activation; residents retain assisted choice.");
  d.rectangle("application-boundary", [404, 12, 1168, 570], colours.paper, colours.ink);
  d.text("boundary-label", "APPLICATION + CONTROLLED CASE DATA / LOGICAL SCOPE", 430, 20, 1090, 24);
  d.node("company", [30, 58, 328, 118], "Company login", "Same Microsoft account\nApp permissions differ", { titleSize: 30, evidence: ["identity", "roles"] });
  d.node("resident", [30, 192, 328, 118], "Resident option", "Separate sign-in\nOwn-case link gated", { titleSize: 30, dashed: true, evidence: ["resident", "residentDeployment"] });
  d.node("excel", [30, 326, 328, 118], "Excel / OneDrive", "File preview today\nConnector: not live", { titleSize: 30, evidence: ["files"] });
  d.node("devices", [30, 460, 328, 118], "Home sensors", "Validated readings\nLive route: gated", { titleSize: 30, dashed: true, evidence: ["sensors"] });
  d.node("workbench", [430, 58, 530, 210], "Staff Workbench", "Roles for coordination, liaison,\nFinance, Quality and Programme.\nOne owned next action.", { fill: colours.green, titleSize: 40, bodySize: 30, evidence: ["roles", "gates"] });
  d.node("api", [430, 322, 530, 222], "Case service + API", "Rules + role/case/field checks\nPeople approve real actions\nManual work remains available", { fill: colours.green, titleSize: 40, bodySize: 30, evidence: ["transition", "gates"] });
  d.node("case-records", [1090, 58, 444, 140], "Case database", "State, owners and audit\nControlled updates via API", { titleSize: 38, bodySize: 28, evidence: ["transition", "sql"] });
  d.node("evidence-files", [1090, 238, 444, 140], "Evidence storage", "Files + versions + scan status\nMetadata links to the case", { titleSize: 38, bodySize: 28, evidence: ["storage"] });
  d.node("advice", [1090, 408, 444, 170], "AI advice", "Approved task facts only\nDrafts returned for review\nNo consent or sign-off", { fill: colours.palePurple, colour: colours.purple, dashed: true, titleSize: 38, bodySize: 28, evidence: ["advice", "chat"] });
  d.arrow("staff-entry", [[360, 110], [420, 110]], colours.ink, false, false, ["identity", "roles"]);
  d.arrow("resident-projection", [[360, 251], [386, 251], [386, 350], [420, 350]], colours.amber, true, false, ["resident"]);
  d.arrow("file-preview", [[360, 385], [420, 385]], colours.ink, false, false, ["files"]);
  d.arrow("sensor-admission", [[360, 519], [420, 519]], colours.amber, true, false, ["sensors"]);
  d.arrow("controlled-action", [[695, 276], [695, 312]], colours.ink, false, false, ["gates", "transition"]);
  d.arrow("record-access", [[970, 354], [1010, 354], [1010, 119], [1080, 119]], colours.ink, false, true, ["transition"]);
  d.arrow("file-access", [[970, 422], [1050, 422], [1050, 287], [1080, 287]], colours.ink, false, true, ["advice"]);
  d.arrow("scoped-model", [[970, 500], [1080, 469]], colours.purple, true, true, ["advice", "chat"]);
  d.text("control-caption", "SECURITY: scoped access   |   PRIVACY: necessary facts only   |   ASSURANCE: versions, audit and human release", 30, 590, 1535, 24);
  return d;
}

function azure() {
  const d = scene("Zava Forward: Azure reference architecture and gated alternatives", 2400, 1740,
    "Source-realization view of the direct-demo shared API. Core is a presentation frame; conditional device, operations and alternative/resident insets complete the full drawing. PaaS services are outside the VNet. No live inventory, UK inference, compliance or activation is certified.");
  d.frame("core", [0, 0, 2400, 810], "Core application source realization");
  d.text("core-label", "SHARED-API SOURCE REALIZATION / DIRECT-DEMO PROFILE", 30, 20, 2310, 32);
  d.text("external-label", "PEOPLE / EXISTING FILES", 30, 95, 670, 28, colours.muted);
  d.rectangle("vnet", [770, 80, 860, 638], colours.paleAzure, colours.azure);
  d.text("vnet-label", "VNet: ACA subnets + private-endpoint subnet", 800, 94, 790, 32, colours.azure, "left", ["network"]);
  d.text("managed-services-label", "MANAGED SERVICES / OUTSIDE THE VNet", 1710, 85, 660, 28, colours.muted);
  d.node("staff", [30, 150, 302, 146], "Staff", "Company account\nAssigned app roles", { titleSize: 42, bodySize: 32, evidence: ["identity", "roles"] });
  d.service("entra", [384, 150, 332, 164], "entra", "Entra app", "Tenant\nApp roles", ["identity", "compute"]);
  d.node("shared-files", [30, 368, 560, 170], "Excel / evidence files", "Controlled file input\nLive OneDrive connector not claimed", { titleSize: 40, bodySize: 30, evidence: ["files"] });
  d.rectangle("aca-environment", [802, 298, 520, 356], colours.white, colours.azure);
  d.text("aca-environment-label", "External demo ACA environment", 824, 314, 478, 28, colours.azure, "left", ["compute", "network"]);
  d.service("api", [824, 366, 476, 232], "aca", "Workbench + API", "EasyAuth principal\nCoded gates + 5 helpers\nOne selected-skill chat", ["compute", "roles", "gates", "chat"]);
  d.text("api-identity-badge", "API managed identity", 840, 607, 450, 30, colours.azure, "left", ["workloadIdentity"]);
  d.rectangle("private-endpoints", [1430, 150, 174, 508], colours.white, colours.azure);
  d.icon("pe-icon", "docs/architecture/assets/azure/endpoint.svg", [1479, 172, 70, 70]);
  d.text("pe-label", "Private\nendpoints", 1444, 253, 146, 30, colours.azure, "center", ["network"]);
  d.text("pe-list", "SQL / Blob\nAI / Queue\nVault / ACR\nIoT Hub\nEvent Hubs\nMonitor\nTokens (opt.)", 1440, 335, 155, 24, colours.muted, "center", ["network", "deviceTransport", "monitoring", "tokens"]);
  d.text("network-controls", "NSGs + linked private DNS; services are not VNet-hosted", 800, 676, 798, 28, colours.azure, "left", ["network"]);
  d.service("sql", [1760, 150, 604, 150], "sql", "Azure SQL", "Cases, metadata, audit\nSeparate grant setup", ["sql"]);
  d.service("blob", [1760, 342, 604, 150], "blob", "Blob Storage", "Evidence bytes + versions\nQuarantine, exports and digests", ["storage"]);
  d.service("foundry", [1760, 534, 604, 196], "foundry", "Foundry / OpenAI", "Account, project, deployments\nConditional drafts + usage\nGlobalStandard: not UK-only", ["model", "infrastructure"], true);
  d.arrow("staff-signin", [[342, 224], [374, 224]], colours.ink, false, false, ["identity"]); d.badge("flow1", "1", 320, 171, ["identity"]);
  d.arrow("verified-principal", [[726, 224], [910, 224], [910, 356]], colours.ink, false, false, ["roles", "compute"]); d.badge("flow2", "2", 839, 236, ["roles"]);
  d.arrow("file-input", [[600, 453], [814, 453]], colours.ink, false, false, ["files"]); d.badge("flow4", "4", 667, 400, ["files"]);
  d.arrow("records", [[1310, 411], [1360, 411], [1360, 225], [1750, 225]], colours.ink, false, false, ["sql"]); d.badge("flow3", "3", 1668, 176, ["sql"]);
  d.arrow("evidence", [[1310, 469], [1376, 469], [1376, 558], [1660, 558], [1660, 417], [1750, 417]], colours.ink, false, false, ["storage"]); d.badge("flow4store", "4", 1668, 366, ["storage"]);
  d.arrow("model-proposal", [[1310, 529], [1360, 529], [1360, 621], [1750, 621]], colours.purple, true, true, ["model", "advice"]); d.badge("flow5", "5/6", 1658, 570, ["model"]);
  d.text("human-boundary", "People own consent, technical sign-off, Finance and release. AI returns advice, never case authority.", 30, 756, 2310, 30, colours.ink, "left", ["transition", "advice"]);
  d.endFrame();

  d.text("device-branch-caption", "CONDITIONAL DEVICE PATH / ROUTING + SDK + LIVE ACCEPTANCE STILL GATED", 30, 842, 2310, 30, colours.azure);
  d.node("device", [30, 895, 384, 174], "Simulated devices", "Individual credentials\nPrivate reachability\nNot staff sign-in", { titleSize: 36, bodySize: 30, dashed: true, evidence: ["simulator", "deviceTransport"] });
  d.rectangle("hub", [500, 895, 412, 174], colours.white, colours.azure, true, ["deviceTransport"]);
  d.icon("hub-icon", "docs/capstone/source/diagrams/architecture/icons/iot-hub.svg", [516, 925, 70, 70]);
  d.text("hub-label", "Azure IoT Hub", 607, 915, 288, 38); d.text("hub-detail", "B1 / one unit\nDevice boundary", 607, 968, 286, 30, colours.muted);
  d.rectangle("telemetry", [1046, 895, 474, 174], colours.white, colours.azure, true, ["deviceTransport"]);
  d.icon("telemetry-icon", "docs/capstone/source/diagrams/architecture/icons/event-hubs.svg", [1062, 925, 70, 70]);
  d.text("telemetry-label", "Event Hubs", 1152, 915, 345, 38); d.text("telemetry-detail", "Private telemetry adapter\nHub sender / API receiver", 1152, 968, 345, 28, colours.muted);
  d.node("intake", [1680, 895, 684, 174], "API intake checks", "Validate / deduplicate / append\nBad input -> owned data-quality exception\nNo diagnosis or automatic safety release", { titleSize: 38, bodySize: 30, dashed: true, evidence: ["deviceTransport", "sensors"] });
  d.arrow("device-hub", [[424, 982], [490, 982]], colours.azure, true, false, ["deviceTransport"]); d.badge("flow8", "8", 439, 928, ["deviceTransport"]);
  d.arrow("hub-route", [[922, 982], [1036, 982]], colours.azure, true, false, ["deviceTransport"]); d.badge("flow9", "9", 954, 928, ["deviceTransport"]);
  d.arrow("api-receive", [[1670, 982], [1530, 982]], colours.azure, true, false, ["deviceTransport"]); d.badge("flow10", "10", 1572, 928, ["deviceTransport"]);
  d.arrow("accepted-reading", [[2220, 1079], [2220, 1128], [2350, 1128]], colours.azure, true, false, ["sensors", "sql"]);
  d.badge("flow11", "11", 1650, 1088, ["sensors"]);
  d.text("same-sql-reference", "Append to the same SQL case DB", 1712, 1095, 630, 26, colours.azure, "left", ["sensors", "sql"]);
  d.text("device-limit", "8: private Hub access   9: Hub MI route   10: API receive PE", 30, 1088, 1550, 24, colours.muted);
  d.text("simulator-reference", "Simulator job uses an existing certificate mount. Main does not configure the API consumer; routing/SDK activation remains separate.", 30, 1118, 2310, 24, colours.muted, "left", ["simulator", "deviceTransport"]);

  d.rectangle("operations-band", [30, 1150, 2334, 172], colours.white, colours.rule);
  d.text("operations-label", "SECURITY + OPERATIONS / SUPPORT DEPENDENCIES, NOT REQUEST HOPS", 50, 1163, 2290, 26, colours.muted);
  d.icon("identity-support", "docs/architecture/assets/azure/identity.svg", [50, 1210, 50, 50]);
  d.icon("vault-support", "docs/architecture/assets/azure/vault.svg", [112, 1210, 50, 50]);
  d.icon("registry-support", "docs/architecture/assets/azure/registry.svg", [174, 1210, 50, 50]);
  d.text("identity-support-label", "Managed identities\nKey Vault / Registry", 244, 1205, 442, 30, colours.ink, "left", ["workloadIdentity", "vault", "registry"]);
  d.icon("network-support", "docs/architecture/assets/azure/dns.svg", [718, 1210, 50, 50]);
  d.text("network-support-label", "Private DNS + NSGs\nDaily digest / optional tokens", 790, 1205, 444, 30, colours.ink, "left", ["network", "tokens", "compute"]);
  d.icon("monitor-support", "docs/architecture/assets/azure/monitor.svg", [1260, 1210, 50, 50]);
  d.text("monitor-support-label", "Logs / App Insights / AMPLS\nIoT/EH metrics only", 1332, 1205, 488, 30, colours.ink, "left", ["monitoring", "deviceTransport"]);
  d.icon("cost-support", "docs/architecture/assets/azure/cost.svg", [1860, 1210, 50, 50]);
  d.text("cost-support-label", "Alerts + budgets (notify)\nCandidate alerts default off", 1932, 1205, 410, 28, colours.ink, "left", ["alerts"]);

  d.node("production-option", [30, 1380, 748, 252], "Alternative: private production entry", "Front Door Premium + WAF\nPrivate Link -> internal ACA\nNot alongside direct-demo ingress\nOrigin/connection acceptance per deployment", { fill: colours.paleAmber, dashed: true, titleSize: 34, bodySize: 29, evidence: ["productionEdge", "infrastructure"] });
  d.node("background-option", [816, 1380, 748, 252], "Authored background workloads", "Separate worker, importer and orchestrator\nTask / import / poison queues\nDaily digest + optional token-renewal jobs\nPlaceholder/transport operation not proved", { fill: colours.paleAmber, dashed: true, titleSize: 34, bodySize: 29, evidence: ["compute", "storage", "tokens"] });
  d.node("resident-option", [1602, 1380, 762, 252], "7 / Separate resident showcase", "SQL own-case dependency supplied separately\nSynthetic session, not staff Entra enrolment\nOptional public OpenAI: Sweden Central\nExternal identity + shared-case target: proposed", { fill: colours.paleAmber, dashed: true, titleSize: 34, bodySize: 29, evidence: ["residentDeployment", "residentModel"] });
  d.text("legend", "SOLID: source-realization   BLUE DASH: authored/gated dependency   PURPLE DASH: conditional AI   AMBER: alternative/showcase", 30, 1660, 2310, 26, colours.muted);
  d.text("acceptance", "Region/quota, runtime grant narrowing, retention/erasure, model geography and human acceptance remain separate release gates.", 30, 1700, 2310, 26, colours.ink);
  return d;
}

const diagrams = new Map([["cxo-architecture", cxo()], ["azure-architecture", azure()]]);
for (const [name, diagram] of diagrams) {
  const outputs = new Map([
    [`${name}.excalidraw`, `${JSON.stringify(diagram.drawing(), null, 2)}\n`],
    [`${name}.svg`, diagram.svg()],
  ]);
  if (name === "azure-architecture") outputs.set("azure-core.svg", diagram.svg("core"));
  for (const [filename, content] of outputs) {
    const path = resolve(directory, filename);
    if (process.argv.includes("--check")) assert.equal(readFileSync(path, "utf8"), content, `Stale derivative: ${filename}`);
    else writeFileSync(path, content, "utf8");
  }
  console.log(`${name}: editable source and same-geometry SVG ${process.argv.includes("--check") ? "verified" : "generated"}.`);
}
