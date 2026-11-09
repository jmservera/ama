import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { scene, sources } from "../capstone/source/diagrams/architecture/build-architecture.mjs";

const directory = dirname(fileURLToPath(import.meta.url));
const repository = resolve(directory, "../..");
const originalArtifactHead = "b671116d571b76ebbbc9e277a791e67f781609cd";
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const colour = { ink: "#173F35", azure: "#0078D4", amber: "#885500", paleAmber: "#FFF1D6" };

function extension(name, width, height) {
  const d = scene(`8 November ${name} source continuation`, width, height,
    "Retains original core IDs, icons and bindings; source-coded telemetry and separately gated resident/averages targets. Not a live inventory.");
  const node = (id, box, title, body, evidence, gated = false) =>
    d.node(`nov08-${id}`, box, title, body, { titleSize: name === "technical" ? 36 : 28,
      bodySize: name === "technical" ? 28 : 24, evidence, dashed: gated,
      fill: gated ? colour.paleAmber : "#FFFFFF" });
  const arrow = (id, points, from, to, evidence, gated = false, both = false) =>
    d.arrow(`nov08-${id}`, points, gated ? colour.azure : colour.ink, gated, both, evidence,
      [`nov08-${from}`, `nov08-${to}`]);
  if (name === "executive") {
    d.text("nov08-heading", "8 NOVEMBER SOURCE CONTINUATION / HOME TELEMETRY + AVERAGES + RESIDENT WEBSITE", 72, 1270, 1780, 28, colour.azure);
    node("homes", [72, 1340, 240, 168], "Home sensors", "Consent + checks\nSynthetic exercise\nLive use: gated", ["sensors"], true);
    node("hub", [360, 1340, 270, 168], "Azure IoT Hub", "B1 / private Hub\nHub MI route\nRouting-ready gate", ["deviceTransport"], true);
    node("event-hubs", [680, 1340, 270, 168], "Event Hubs", "Dedicated transport\nAPI receives via PE\nNot a history store", ["deviceTransport", "stream"], true);
    node("service", [1000, 1340, 410, 168], "API telemetry service", "Validate / deduplicate / append\nRead-only history + averages\nAnalysis read-only; no tasks", ["intake", "consumer", "analysis", "averages"]);
    node("store", [1460, 1340, 388, 168], "Azure SQL telemetry", "Retained per-home readings\nRestricted delivery / DQ history\nNot an unrestricted AI feed", ["consumer", "sql"]);
    node("averages", [72, 1570, 810, 180], "Household history + averages responsibility", "Current: exercise means computed on read from retained readings.\nTARGET: stored per-home averages in existing SQL, separately gated.\nNo materialization worker, schema or quality-helper integration is built.", ["analysis", "averages", "qualityHelper"], true);
    node("resident", [960, 1570, 410, 180], "Resident website", "Separate from staff sign-in\nOwn-case + assisted choice\nShared-case / external ID: target", ["resident", "residentDeployment"], true);
    node("resident-sql", [1460, 1570, 388, 180], "Separate showcase SQL", "Dependency supplied separately\nSynthetic session today\nShared staff SQL not proved", ["residentDeployment"], true);
    node("resident-model", [1460, 1810, 388, 150], "Optional resident AI", "Public Sweden Central model\nOff by default; outside core\nNot a private/UK claim", ["residentModel"], true);
    arrow("sensor-ingress", [[312, 1424], [360, 1424]], "homes", "hub", ["deviceTransport"], true);
    arrow("hub-route", [[630, 1424], [680, 1424]], "hub", "event-hubs", ["deviceTransport"], true);
    arrow("receive", [[950, 1424], [1000, 1424]], "event-hubs", "service", ["stream"], true);
    arrow("retention", [[1410, 1424], [1460, 1424]], "service", "store", ["consumer"], false, true);
    arrow("averages-read", [[882, 1660], [920, 1660], [920, 1535], [1205, 1535], [1205, 1508]], "averages", "service", ["analysis", "averages"]);
    arrow("resident-data", [[1370, 1660], [1460, 1660]], "resident", "resident-sql", ["residentDeployment"], true);
    arrow("resident-ai", [[1165, 1750], [1165, 1885], [1460, 1885]], "resident", "resident-model", ["residentModel"], true, true);
    d.arrow("nov08-shared-api", [[1300, 1340], [1300, 1320], [1895, 1320], [1895, 775], [1200, 775], [1200, 740]], colour.azure, true, false, ["intake"]).customData.externalEndpoints = true;
    d.arrow("nov08-same-sql", [[1800, 1340], [1880, 1340], [1880, 975], [715, 975], [715, 950]], colour.ink, false, false, ["consumer", "sql"]).customData.externalEndpoints = true;
    d.text("nov08-release", "Insufficient / stale / declined -> manual review.\nAverages are context, not diagnosis, consent, quality acceptance or safety release.", 72, 1830, 1010, 26, colour.ink, "left", ["analysis"]);
  } else {
    d.text("nov08-heading", "8 NOVEMBER SOURCE CONTINUATION / NOT A NEW CLOUD INVENTORY OR LIVE MONITORING ACCEPTANCE", 72, 2900, 2700, 34, colour.azure);
    node("homes", [72, 3000, 420, 190], "Home sensors", "Synthetic exercise today\nConsent / calibration checks\nDevice ID, not staff sign-in", ["sensors", "simulator"], true);
    node("hub", [562, 3000, 440, 190], "Azure IoT Hub", "Basic B1 / private Hub\nHub MI trusted-service route\nRouting-ready gate separate", ["deviceTransport"], true);
    node("event-hubs", [1072, 3000, 440, 190], "Event Hubs transport", "Dedicated sensor stream\nAPI initiates receive via PE\nShort retention, not history", ["deviceTransport", "stream"], true);
    node("service", [1582, 3000, 580, 190], "Shared API telemetry service", "Finite SDK receive + intake composition\nValidate / deduplicate / SQL append\nBad input -> owned data-quality exception", ["intake", "consumer", "stream"]);
    node("store", [2232, 3000, 540, 190], "Same Azure SQL: telemetry", "Retained per-home readings\nRestricted delivery / DQ history\nNot an unrestricted AI feed", ["consumer", "sql"]);
    node("averages", [72, 3300, 1300, 240], "Telemetry history / per-home averages capability", "Read-only retained analysis uses trusted consent + readings.\nExercise baseline / early / late window means computed on read.\nInsufficient / stale / declined -> manual review; no priority effect.\nNo task creation, diagnosis, consent authority or safety release.", ["analysis", "averages"]);
    node("average-target", [1482, 3300, 1290, 240], "TARGET: persisted household averages / history service", "Existing shared API + Azure SQL are the proposed responsibility boundary.\nAverage materialization/persistence is not implemented; no new Azure service adopted.\nQuality Verification post-retrofit linkage remains a separately gated target.\nCurrent quality-evidence helper uses measures / checklists / documents, not telemetry.", ["analysis", "averages", "qualityHelper"], true);
    node("resident", [72, 3670, 740, 230], "Separate resident website", "Own-case scoped access + assisted choice\nSynthetic showcase session, not staff Entra enrolment\nShared-case / external identity: gated target", ["resident", "residentDeployment"], true);
    node("resident-sql", [962, 3670, 760, 230], "Independently supplied showcase SQL", "Own-case dependency passed to resident-demo.bicep\nNot proof of shared-case/staff SQL integration\nNo assumed credentials or accepted network reachability", ["residentDeployment"], true);
    node("resident-model", [1872, 3670, 900, 230], "Optional resident OpenAI / outside core boundary", "Public Sweden Central Standard model, off by default\nSeparate resident assistant deployment, not UK/private core\nReal-data authority, privacy and provider acceptance remain gated", ["residentModel"], true);
    arrow("sensor-ingress", [[492, 3095], [562, 3095]], "homes", "hub", ["deviceTransport"], true);
    arrow("hub-route", [[1002, 3095], [1072, 3095]], "hub", "event-hubs", ["deviceTransport"], true);
    arrow("receive", [[1582, 3095], [1512, 3095]], "service", "event-hubs", ["stream", "deviceTransport"], true);
    arrow("retention", [[2162, 3095], [2232, 3095]], "service", "store", ["consumer"], false, true);
    arrow("analysis-read", [[1372, 3420], [1420, 3420], [1420, 3240], [2502, 3240], [2502, 3190]], "averages", "store", ["analysis", "averages"]);
    arrow("materialization-target", [[2120, 3300], [2120, 3240], [2600, 3240], [2600, 3190]], "average-target", "store", ["averages"], true);
    arrow("resident-data", [[812, 3785], [962, 3785]], "resident", "resident-sql", ["residentDeployment"], true);
    arrow("resident-ai", [[620, 3900], [620, 3950], [2322, 3950], [2322, 3900]], "resident", "resident-model", ["residentModel"], true, true);
    d.arrow("nov08-shared-api", [[2100, 3000], [2100, 2970], [2790, 2970], [2790, 1405], [1808, 1405], [1808, 1180], [1645, 1180]], colour.azure, true, false, ["intake"]).customData.externalEndpoints = true;
    d.arrow("nov08-same-sql", [[2600, 3000], [2600, 2980], [2805, 2980], [2805, 1075], [2580, 1075], [2580, 970], [2540, 970]], colour.ink, false, false, ["consumer", "sql"]).customData.externalEndpoints = true;
    d.text("nov08-release", "SOURCE-CODED / GATED TARGETS ARE DISTINCT. No ADX/Fabric/standalone analytics worker, stored averages implementation or new infrastructure adoption.\nPeople retain consent, professional judgement, quality acceptance and release. Missing/stale/declined data never means a safe home.", 72, 4000, 2700, 28, colour.ink, "left", ["analysis", "qualityHelper"]);
  }
  return d;
}

for (const [name, width, height] of [["executive", 1920, 2010], ["technical", 2850, 4100]]) {
  const relative = `docs/architecture/zava-forward-${name}-architecture.excalidraw`;
  const original = JSON.parse(execFileSync("git", ["show", `${originalArtifactHead}:${relative}`], { cwd: repository, maxBuffer: 4 * 1024 * 1024 }));
  const added = extension(name, width, height).drawing();
  const originalIds = original.elements.map((element) => element.id);
  original.elements[0].height = height;
  for (const element of original.elements) {
    const data = element.customData ??= {};
    data.sources = (data.sources ?? []).map((path) => path.replace("mvp/README.md", "src/api/README.md")
      .replace("mvp/web/", "src/api/src/zava_forward/api/web/")
      .replace("mvp/zavaforward_mvp/auth.py", "src/api/src/zava_forward/api/auth.py")
      .replace("mvp/zavaforward_mvp/server.py", "src/api/src/zava_forward/api/server.py")
      .replace("mvp/zavaforward_mvp/token_store.py", "src/orchestrator/src/zava_forward/orchestrator/token_store.py")
      .replace("mvp/zavaforward_mvp/", "src/core/src/zava_forward/core/"));
    data.evidence = data.sources.map((path) => {
      const file = path.split("#")[0];
      const bytes = readFileSync(resolve(repository, file));
      return { path: file, line: 1, sha256: sha(bytes), classification: "Retained original core topology; current migrated source locator, not renewed live acceptance" };
    });
    if (element.type === "text") {
      element.text = element.text.replace("No resident portal needed", "Assisted choice stays")
        .replace("Resident contact is staff-assisted", "Resident website is separate / gated")
        .replace("Validated principal -> SQL staff binding -> server-side role/case/field checks",
          "Validated principal -> tenant/object/app roles -> role/case/field checks")
        .replace("PR #68 / 14 October 2026", "8 November 2026 continuation / original PR #68 layout")
        .replace("PR #68 source baseline / 14 October 2026", "8 November 2026 continuation / original PR #68 topology");
      element.originalText = element.text;
    }
  }
  original.elements.push(...added.elements.filter((element) => element.id !== "canvas"));
  original.files = { ...original.files, ...added.files };
  original.customData = { ...original.customData, date: "2026-11-08", originalArtifactHead,
    source_basis_head: originalArtifactHead,
    source_basis: "8 November authoring-start checkout; exact current source inputs are identified by embedded file hashes",
    scope: "8 November source continuation with retained original core layout; new source-coded telemetry and gated averages/resident targets, not a fresh live inventory",
    sources, originalElementIds: originalIds };
  const byId = new Map(original.elements.map((element) => [element.id, element]));
  for (const [id, sourceName, targetName] of [["nov08-shared-api", "nov08-service", name === "executive" ? "workbench" : "api"],
    ["nov08-same-sql", "nov08-store", "sql"]]) {
    const arrow = byId.get(id);
    delete arrow.customData.externalEndpoints;
    const source = byId.get(sourceName);
    const target = original.elements.find((element) => element.customData?.name === targetName);
    for (const [end, node] of [["start", source], ["end", target]]) {
      arrow[`${end}Binding`] = { elementId: node.id, focus: 0, gap: 0 };
      (node.boundElements ??= []).push({ id, type: "arrow" });
    }
  }
  assert.equal(byId.size, original.elements.length);
  const content = `${JSON.stringify(original, null, 2)}\n`;
  const destination = resolve(repository, relative);
  if (process.argv.includes("--check")) assert.equal(readFileSync(destination, "utf8"), content, `Stale native source: ${relative}`);
  else writeFileSync(destination, content);
  console.log(`${name}: original ${originalIds.length} editable elements retained; ${original.elements.length - originalIds.length} new elements ${process.argv.includes("--check") ? "verified" : "generated"}.`);
}
