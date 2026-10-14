"""Create editable, source-linked Excalidraw architecture views."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import zipfile

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/architecture"
WORK = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
COLORS = {
    "ink": "#173f35", "muted": "#50635d", "paper": "#faf9f6",
    "observed": "#1d7563", "configured": "#286b91",
    "conditional": "#7053a0", "deferred": "#9c6619", "human": "#173f35",
}
FILLS = {
    "observed": "#ffffff", "configured": "#f1f7fb",
    "conditional": "#f5f1fb", "deferred": "#fff7e9", "human": "#eef4ee",
}
ICONS = {
    "aca": "other/02884-icon-service-Worker-Container-App.svg",
    "environment": "other/02989-icon-service-Container-Apps-Environments.svg",
    "sql": "databases/10130-icon-service-SQL-Database.svg",
    "blob": "storage/10086-icon-service-Storage-Accounts.svg",
    "queue": "general/10840-icon-service-Storage-Queue.svg",
    "openai": "ai + machine learning/03438-icon-service-Azure-OpenAI.svg",
    "foundry": "ai + machine learning/035746832-icon-service-AI-Foundry.svg",
    "entra": "identity/10232-icon-service-App-Registrations.svg",
    "identity": "identity/10227-icon-service-Managed-Identities.svg",
    "vault": "security/10245-icon-service-Key-Vaults.svg",
    "registry": "containers/10105-icon-service-Container-Registries.svg",
    "logs": "analytics/00009-icon-service-Log-Analytics-Workspaces.svg",
    "insights": "devops/00012-icon-service-Application-Insights.svg",
    "monitor": "monitor/00001-icon-service-Monitor.svg",
    "cost": "general/10019-icon-service-Cost-Management.svg",
    "vnet": "networking/10061-icon-service-Virtual-Networks.svg",
    "endpoint": "other/02579-icon-service-Private-Endpoints.svg",
    "dns": "networking/10064-icon-service-DNS-Zones.svg",
    "nsg": "networking/10067-icon-service-Network-Security-Groups.svg",
    "edge": "networking/10073-icon-service-Front-Door-and-CDN-Profiles.svg",
}
SOURCES = {
    "handover": ["infra/README.md#five-assistant-version-current-handover"],
    "app": ["infra/modules/containerapps.bicep", "mvp/zavaforward_mvp/server.py"],
    "assist": ["mvp/zavaforward_mvp/assistants.py", "docs/adrs/0002-pilot-readiness-architecture.md#five-assistant-exercise-runtime-2026-10-13"],
    "auth": ["infra/modules/containerapps.bicep", "mvp/zavaforward_mvp/auth.py", "infra/scripts/initialize-workbench-staff.py"],
    "sql": ["infra/modules/sql.bicep", "mvp/zavaforward_mvp/mssqlstore.py"],
    "blob": ["infra/modules/storage.bicep", "mvp/zavaforward_mvp/documents.py"],
    "model": ["infra/modules/foundry.bicep", "infra/main.bicep", "mvp/zavaforward_mvp/ai.py"],
    "tokens": ["infra/modules/authTokenStore.bicep", "mvp/zavaforward_mvp/token_store.py"],
    "photo": ["mvp/zavaforward_mvp/profile.py", "mvp/zavaforward_mvp/server.py"],
    "monitor": ["infra/modules/monitoring.bicep", "infra/main.bicep"],
    "network": ["infra/modules/network.bicep", "infra/modules/privateEndpoint.bicep", "infra/README.md#deployment-profile"],
    "workers": ["infra/modules/containerapps.bicep", "docs/adrs/0001-azure-architecture.md#decisions"],
    "m365": ["docs/adrs/0001-azure-architecture.md#m365-configuration-integration-and-use", "infra/scripts/grant-sharepoint-access.sh"],
}


def key(value):
    return hashlib.sha256(value.encode()).hexdigest()[:20]


def extract_icons(pack):
    directory = OUT / "assets/azure"
    directory.mkdir(parents=True, exist_ok=True)
    provenance = {}
    with zipfile.ZipFile(pack) as archive:
        for name, entry in ICONS.items():
            full = "Azure_Public_Service_Icons/Icons/" + entry
            raw = archive.read(full)
            path = directory / f"{name}.svg"
            path.write_bytes(raw)
            path.chmod(0o644)
            provenance[name] = {"entry": full, "sha256": hashlib.sha256(raw).hexdigest()}
    return provenance


class Scene:
    def __init__(self, name, width, height, commit):
        self.name, self.width, self.height = name, width, height
        self.elements, self.files, self.nodes, self.flows = [], {}, {}, []
        self.overflows = []
        self.commit = commit
        self.rect("artboard", 0, 0, width, height, fill=COLORS["paper"], stroke=COLORS["paper"])["locked"] = True

    def element(self, name, kind, x, y, width, height, **props):
        element = dict(
            id=key(self.name + name), type=kind, x=x, y=y, width=width, height=height,
            angle=0, strokeColor=COLORS["ink"], backgroundColor="transparent",
            fillStyle="solid", strokeWidth=1.6, strokeStyle="solid", roughness=0,
            opacity=100, groupIds=[], frameId=None, roundness=None,
            seed=int(key(name)[:7], 16), version=1, versionNonce=int(key(name + "v")[:7], 16),
            isDeleted=False, boundElements=None, updated=1791972000000,
            link=None, locked=False,
        )
        element.update(props)
        self.elements.append(element)
        return element

    def rect(self, name, x, y, width, height, fill="#ffffff", stroke=None, dashed=False, group=None, data=None):
        return self.element(name, "rectangle", x, y, width, height,
                            backgroundColor=fill, strokeColor=stroke or COLORS["configured"],
                            strokeStyle="dashed" if dashed else "solid",
                            roundness={"type": 3}, groupIds=[group] if group else [],
                            customData=data or {})

    def text(self, name, value, x, y, width, height, size=22, color=None, group=None, role="text"):
        font = ImageFont.truetype(FONT, size)
        lines = []
        for paragraph in value.split("\n"):
            line = ""
            for word in paragraph.split():
                candidate = f"{line} {word}".strip()
                if font.getlength(candidate) > width - 6 and line:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
        actual_height = len(lines) * size * 1.25
        if actual_height > height:
            self.overflows.append(f"{name}: needs {actual_height}px; region has {height}px")
        text = "\n".join(lines)
        return self.element(name, "text", x, y, width, actual_height,
                            text=text, originalText=text, fontSize=size, fontFamily=2,
                            textAlign="left", verticalAlign="top", containerId=None,
                            lineHeight=1.25, autoResize=True, strokeWidth=1,
                            strokeColor=color or COLORS["ink"], groupIds=[group] if group else [],
                            customData={"role": role, "layoutBounds": [x, y, width, height]})

    def icon(self, name, icon, x, y, size=48, group=None):
        raw = (OUT / f"assets/azure/{icon}.svg").read_bytes()
        root = ET.fromstring(raw)
        view = root.get("viewBox")
        if view:
            _, _, w, h = map(float, view.split())
        else:
            w, h = float(root.get("width")), float(root.get("height"))
        scale = size / max(w, h)
        file_id = hashlib.sha1(raw).hexdigest()
        self.files[file_id] = dict(id=file_id, mimeType="image/svg+xml",
                                  dataURL="data:image/svg+xml;base64," + base64.b64encode(raw).decode(),
                                  created=1791972000000, lastRetrieved=1791972000000)
        return self.element(name, "image", x + (size - w * scale) / 2, y + (size - h * scale) / 2,
                            w * scale, h * scale, fileId=file_id, status="saved", scale=[1, 1], crop=None,
                            groupIds=[group] if group else [], customData={"azureIcon": icon})

    def card(self, name, x, y, width, height, title, body, status="configured", icon=None,
             sources=(), title_size=24, body_size=20):
        group = key(self.name + name + "group")
        node = self.rect(name, x, y, width, height, FILLS[status], COLORS[status],
                         dashed=status in ("conditional", "deferred"), group=group,
                         data={"role": "service", "name": name, "status": status, "sources": list(sources)})
        self.nodes[name] = node
        compact = height <= 160
        shallow = height <= 110
        if not shallow:
            self.text(name + "-status", status.upper(), x + 20, y + 12, width - 40, 20,
                      size=13, color=COLORS[status], group=group)
        top = 15 if shallow else 32
        reserve = 54 if shallow else 82 if compact else 112
        title_x = x + (82 if icon else 20)
        if icon:
            self.icon(name + "-icon", icon, x + 20, y + top + 2, 46 if compact else 52, group)
        self.text(name + "-title", title, title_x, y + top, width - (102 if icon else 40),
                  reserve - top - 6, size=title_size, group=group, role="title")
        self.text(name + "-body", body, x + 20, y + reserve, width - 40, height - reserve - 12,
                  size=body_size, color=COLORS["muted"], group=group, role="body")
        return node

    def boundary(self, name, x, y, width, height, label, color="configured", fill="#f5f8f8"):
        node = self.rect(name, x, y, width, height, fill, COLORS[color], dashed=color == "deferred",
                         data={"role": "boundary"})
        self.text(name + "-label", label, x + 20, y + 16, width - 40, 40, size=24, color=COLORS[color])
        return node

    def flow(self, name, source, target, label, start=("r", .5), end=("l", .5),
             via=(), status="observed", label_at=None, sources=(), both=False):
        first, last = self.nodes[source], self.nodes[target]

        def port(node, spec, outgoing):
            side, fraction = spec
            x, y, w, h = (node[k] for k in ("x", "y", "width", "height"))
            gap = 9
            return {"l": (x - gap, y + h * fraction), "r": (x + w + gap, y + h * fraction),
                    "t": (x + w * fraction, y - gap), "b": (x + w * fraction, y + h + gap)}[side]

        points = [port(first, start, True), *via, port(last, end, False)]
        origin = points[0]
        relative = [[x - origin[0], y - origin[1]] for x, y in points]
        arrow = self.element(
            name, "arrow", *origin, max(x for x, _ in relative) - min(x for x, _ in relative),
            max(y for _, y in relative) - min(y for _, y in relative),
            points=relative, startArrowhead="arrow" if both else None, endArrowhead="arrow",
            startBinding={"elementId": first["id"], "focus": 2 * start[1] - 1, "gap": 9},
            endBinding={"elementId": last["id"], "focus": 2 * end[1] - 1, "gap": 9},
            elbowed=False, strokeColor=COLORS[status], strokeWidth=2,
            strokeStyle="dashed" if status in ("conditional", "deferred", "configured") else "solid",
            customData={"role": "flow", "source": source, "target": target, "status": status, "sources": list(sources)},
        )
        for node in (first, last):
            if node["boundElements"] is None:
                node["boundElements"] = []
            node["boundElements"].append({"id": arrow["id"], "type": "arrow"})
        self.flows.append({"id": name, "source": source, "target": target, "label": label,
                           "status": status, "sources": list(sources)})
        if label_at:
            x, y, width = label_at
            self.rect(name + "-label-bg", x - 4, y - 3, width + 8, 54, COLORS["paper"], COLORS["paper"],
                      data={"role": "flow-label-background"})
            self.text(name + "-label", label, x, y, width, 52, size=18, color=COLORS[status], role="flow-label")
        return arrow

    def write(self):
        if self.overflows:
            raise ValueError(f"{self.name} text overflow:\n" + "\n".join(self.overflows))
        label_roles = {"flow-label", "flow-label-background"}
        self.elements = (
            [element for element in self.elements if element.get("customData", {}).get("role") not in label_roles]
            + [element for element in self.elements if element.get("customData", {}).get("role") in label_roles]
        )
        result = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
                  "elements": self.elements, "files": self.files,
                  "appState": {"viewBackgroundColor": COLORS["paper"], "gridSize": None,
                               "exportBackground": True, "exportEmbedScene": True, "theme": "light"},
                  "customData": {"sourceCommit": self.commit, "pr": 68, "date": "2026-10-14",
                                 "scope": "Static PR sources; not a fresh Azure inventory",
                                 "flows": self.flows}}
        for element in self.elements:
            for source in element.get("customData", {}).get("sources", []):
                if not (ROOT / source.split("#")[0]).is_file():
                    raise ValueError(f"Missing source: {source}")
        destination = OUT / f"zava-forward-{self.name}-architecture.excalidraw"
        destination.write_text(json.dumps(result, indent=2) + "\n")
        destination.chmod(0o644)
        return {"name": self.name, "elements": len(self.elements), "nodes": len(self.nodes),
                "flows": len(self.flows), "icons": len(self.files), "sourceCommit": self.commit}


def executive(commit):
    s = Scene("executive", 1920, 1260, commit)
    s.text("title", "One workflow. Evidence first. People decide.", 72, 60, 1780, 78, 48, role="heading")
    s.text("subtitle", "Zava Forward / executive architecture / PR #68 / 14 October 2026", 74, 145, 1760, 36, 24)
    s.rect("purpose", 72, 210, 1776, 94, COLORS["ink"], COLORS["ink"])
    s.text("purpose-copy", "Connect staff, evidence and bounded AI support.\nKeep resident choice and accountable approval with people.",
           100, 227, 1710, 72, 26, "#ffffff")
    s.boundary("azure", 72, 334, 1776, 652, "Solution overview / synthetic exercise", fill="#edf3ee")
    s.card("identity", 560, 370, 660, 92, "Microsoft Entra ID", "Microsoft sign-in / role-limited access",
           icon="entra", sources=SOURCES["auth"], title_size=22, body_size=20)
    s.card("people", 112, 490, 320, 250, "Staff assist residents", "Phone, letter, officer help\nRecord resident choice\nNo resident portal needed",
           "human", sources=["docs/prds/zava-forward-retrofit-programme-demonstrator.md"], title_size=25, body_size=22)
    s.card("workbench", 560, 490, 660, 250, "Azure Container Apps", "One staff workbench + controlled workflow\nRules, permissions and human review\nFive bounded assists in this same API",
           "observed", "aca", SOURCES["app"] + SOURCES["assist"], title_size=28, body_size=24)
    s.card("model", 1380, 490, 410, 250, "Azure OpenAI", "Draft text, citations and usage\nNo workflow or SQL credentials\nFive-assistant authority is OFF",
           "conditional", "openai", SOURCES["model"] + SOURCES["handover"], title_size=27, body_size=22)
    s.card("decision", 112, 800, 320, 150, "People own approval", "Consent / independent QA\nFinance / work release", "human",
           sources=["docs/adrs/0002-pilot-readiness-architecture.md"], title_size=22, body_size=19)
    s.card("sql", 560, 800, 310, 150, "Azure SQL", "Cases, decisions and audit\nProposals + usage", "observed", "sql",
           SOURCES["sql"] + SOURCES["handover"], title_size=23, body_size=19)
    s.card("blob", 910, 800, 310, 150, "Azure Blob Storage", "Document files\nHashes + metadata in SQL", "configured", "blob",
           SOURCES["blob"], title_size=22, body_size=19)
    s.flow("staff-work", "people", "workbench", "Work", label_at=(456, 600, 80), sources=SOURCES["app"])
    s.flow("sign-in", "identity", "workbench", "Sign-in", start=("b", .5), end=("t", .5), status="configured", sources=SOURCES["auth"])
    s.flow("draft", "workbench", "model", "Scoped call\nDraft only", status="conditional", both=True,
           label_at=(1238, 596, 120), sources=SOURCES["assist"] + SOURCES["model"])
    s.flow("records", "workbench", "sql", "Controlled state", start=("b", .23), end=("t", .5), sources=SOURCES["sql"])
    s.flow("documents", "workbench", "blob", "Documents", start=("b", .77), end=("t", .5), status="configured", sources=SOURCES["blob"])
    s.flow("approval", "decision", "workbench", "Human gates", start=("r", .5), end=("l", .87),
           via=((492, 875), (492, 707.5)), sources=["docs/adrs/0002-pilot-readiness-architecture.md"])
    s.text("capabilities", "Stock / assessment / funding / coordination / quality evidence", 580, 708, 620, 27, 18, COLORS["muted"],
           group=s.nodes["workbench"]["groupIds"][0])
    s.rect("current-note", 72, 1022, 856, 146, "#f5f1fb", "#7053a0")
    s.text("current-title", "Current evidence, not autonomous operation", 94, 1040, 812, 36, 25)
    s.text("current-body", "Five operator model paths and SQL restart persistence observed.\nNormal five-assistant authority absent; proactive scans OFF.\nManual case work remains available.",
           94, 1086, 812, 78, 20, COLORS["muted"])
    s.rect("value-note", 958, 1022, 890, 146, "#fff7e9", "#9c6619")
    s.text("value-title", "Intended value: less chasing, fewer evidence gaps", 980, 1040, 846, 36, 25)
    s.text("value-body", "Human consent, safety, quality and Finance gates stay in place.\nBenefits need paired measurement; no production approval.\nM365 and separate workers are not prerequisites for this core.",
           980, 1086, 846, 78, 20, COLORS["muted"])
    s.text("legend", "Solid green: documented core interaction   /   Blue: configured dependency   /   Purple dashed: conditional model path",
           74, 1195, 1770, 32, 20)
    return s.write()


def technical(commit):
    s = Scene("technical", 2850, 2870, commit)
    s.text("title", "Zava Forward / service architecture", 72, 48, 2690, 80, 48, role="heading")
    s.text("subtitle", "CTO + technical architects / PR #68 source baseline / 14 October 2026 / static view, not a live Azure inventory",
           74, 132, 2660, 40, 25)
    s.text("legend", "GREEN: documented core   |   BLUE: source-configured   |   PURPLE: conditional / OFF   |   AMBER: deferred, not working services",
           74, 199, 2670, 45, 24)
    s.boundary("rg", 610, 340, 1990, 1660, "Azure resource group ama / UK South exercise / development public-network exceptions", fill="#f3f6f6")
    s.boundary("environment", 650, 665, 1040, 775, "Container Apps environment / VNet + mTLS configured", fill="#e9f1ee")
    s.card("entra", 72, 420, 440, 180, "Microsoft Entra ID", "Existing workbench registration\nApp roles + tenant issuer", "configured", "entra", SOURCES["auth"], body_size=19)
    s.card("staff", 72, 720, 440, 180, "Staff browser", "Public welcome; protected /app + APIs\nResident contact is staff-assisted", "human",
           sources=SOURCES["app"], title_size=25, body_size=19)
    s.card("maps", 72, 1010, 440, 175, "Configured map tile provider", "Browser-only HTTPS tile requests\nList / cluster alternative stays usable", "configured",
           sources=["mvp/zavaforward_mvp/server.py", "mvp/web/app.js"], title_size=23, body_size=18)
    s.card("graph", 72, 1290, 440, 180, "Microsoft Graph", "Delegated own-user User.Read\nGET /me/photo/$value; server proxy", "configured", sources=SOURCES["photo"], body_size=19)
    s.card("identity", 650, 420, 440, 180, "Managed identities", "API + token maintenance identities\nSeparate deferred worker identities", "configured", "identity",
           ["infra/modules/identity.bicep", "infra/modules/authTokenStore.bicep"], body_size=19)
    s.card("vault", 1240, 420, 450, 180, "Azure Key Vault", "Entra client secret + token-store SAS\nAPI read; maintenance writes one secret", "configured", "vault",
           ["infra/modules/keyvault.bicep"] + SOURCES["tokens"], body_size=19)
    s.card("model", 1820, 420, 720, 265, "Microsoft Foundry / Azure OpenAI", "Account + project; standard and capable deployments\nstandard: gpt-4.1-mini / capable: gpt-4.1\nAPI managed-identity invocation; typed output validation\nNo Foundry Agent Service / autonomous manager deployed",
           "conditional", "foundry", SOURCES["model"] + SOURCES["handover"], title_size=25, body_size=22)
    s.icon("model-openai", "openai", 2460, 460, 52, s.nodes["model"]["groupIds"][0])
    s.card("auth", 695, 755, 950, 155, "Container Apps HTTPS ingress + EasyAuth", "443 -> 8088 / /healthz probe / public welcome, protected /app + APIs\nValidated principal -> SQL staff binding -> server-side role/case/field checks",
           "configured", "environment", SOURCES["auth"], title_size=25, body_size=21)
    s.card("api", 695, 1010, 950, 270, "ca-forward-test-api / UI + Python API", "One deployable, not five microservices\nDeterministic workflow / ranking / consent / independent approvals\nFive shared assists: capture -> reserve -> infer -> validate -> store draft\nSQL owns dedupe, leases, durable limits and source-verified review",
           "observed", "aca", SOURCES["app"] + SOURCES["assist"] + SOURCES["handover"], title_size=26, body_size=22)
    s.text("api-limits", "Normal five-assistant authority absent / proactive OFF.\nDisabled or failed assistance never blocks ordinary case controls.",
           725, 1310, 880, 70, 23, COLORS["conditional"])
    s.card("sql", 1820, 815, 720, 240, "Azure SQL Database / retrofit", "Entra-only / serverless / append-only ledger events\nCases, row versions, audit, proposals, snapshots, leases + usage\nShort transactions; model call outside database locks\n14-day PITR configured; restore acceptance remains separate",
           "observed", "sql", SOURCES["sql"] + SOURCES["handover"], title_size=25, body_size=20)
    s.card("blob", 1820, 1190, 720, 200, "Azure Blob Storage / evidence", "Private containers; upload / download through the API\nDocument bytes in Blob; references + content hashes in SQL\nFive-assistant capture uses permitted metadata, not whole files",
           "configured", "blob", SOURCES["blob"] + SOURCES["assist"], title_size=25, body_size=19)
    s.card("tokens", 650, 1515, 440, 180, "Separate auth-token Blob store", "Private auth-tokens / EasyAuth SAS\nNo browser token retrieval", "configured", "blob", SOURCES["tokens"], title_size=22, body_size=19)
    s.card("renewal", 1240, 1515, 450, 180, "Container Apps renewal job", "03:00 UTC / 5-day user-delegation SAS\nOwn identity; one Key Vault secret write", "configured", "aca",
           SOURCES["tokens"] + SOURCES["app"], title_size=22, body_size=19)
    s.card("registry", 1820, 1515, 720, 180, "Azure Container Registry", "Digest-pinned image pull with workload identities\nOperator builds; CI tests, scans and produces SBOM, not auto-deploy",
           "configured", "registry", ["infra/modules/registry.bicep", ".github/workflows/mvp-ci.yml", "infra/README.md"], title_size=25, body_size=20)
    s.card("logs", 650, 1795, 540, 175, "Azure Monitor / Log Analytics", "Resource / container diagnostics + SQL audit\nAPI structured-trace coverage not established", "configured", "logs", SOURCES["monitor"], title_size=22, body_size=18)
    s.icon("monitor-icon", "monitor", 1130, 1840, 35, s.nodes["logs"]["groupIds"][0])
    s.card("insights", 1280, 1795, 410, 175, "Application Insights", "Workspace-linked component\nConnection string; tracing unproved", "configured", "insights", SOURCES["monitor"] + SOURCES["app"], title_size=22, body_size=18)
    s.card("alerts", 1820, 1795, 720, 175, "Alerts / action group / Cost Management", "API 5xx + restarts / SQL CPU / model client errors -> email\nBudget: 80% actual + 100% forecast; alerts are not a hard cap",
           "configured", "cost", SOURCES["monitor"], title_size=23, body_size=19)
    s.flow("browser-login", "staff", "entra", "Sign-in", start=("t", .5), end=("b", .5), status="configured", label_at=(322, 637, 165), sources=SOURCES["auth"])
    s.flow("browser-app", "staff", "auth", "HTTPS", start=("r", .53), end=("l", .45), label_at=(538, 816, 115), sources=SOURCES["app"])
    s.flow("issuer", "entra", "auth", "Issuer / roles", start=("r", .5), end=("l", .1), via=((560, 510), (560, 770.5)), status="configured", sources=SOURCES["auth"])
    s.flow("auth-app", "auth", "api", "Verified principal", start=("b", .5), end=("t", .5), status="configured", label_at=(1190, 945, 240), sources=SOURCES["auth"])
    s.flow("api-sql", "api", "sql", "SQL / MI", start=("r", .24), end=("l", .6), label_at=(1669, 1056, 132), sources=SOURCES["sql"])
    s.flow("api-blob", "api", "blob", "Blob / MI", start=("r", .87), end=("l", .43), label_at=(1669, 1230, 130), status="configured", sources=SOURCES["blob"])
    s.flow("api-model", "api", "model", "Scoped model\nrequest / usage", start=("r", .05), end=("l", .72),
           via=((1735, 1023.5), (1735, 610.8)), status="conditional", both=True, label_at=(1708, 710, 155), sources=SOURCES["model"] + SOURCES["assist"])
    s.flow("secret-reference", "vault", "auth", "Secret refs", start=("b", .52), end=("t", .81), status="configured", sources=SOURCES["auth"] + SOURCES["tokens"])
    s.flow("own-photo", "api", "graph", "Delegated own-photo\nrequest / image", start=("l", .68), end=("r", .45),
           via=((588, 1193.6), (588, 1371)), status="configured", label_at=(94, 1490, 410), sources=SOURCES["photo"])
    s.flow("browser-tiles", "staff", "maps", "Tile images", start=("b", .35), end=("t", .35), status="configured", label_at=(290, 947, 200), sources=["mvp/web/app.js"])
    s.flow("sas-key", "renewal", "tokens", "Delegation key", start=("l", .5), end=("r", .5), status="configured", label_at=(1098, 1585, 130), sources=SOURCES["tokens"])
    s.flow("sas-secret", "renewal", "vault", "Rotate one SAS secret", start=("r", .2), end=("r", .4),
           via=((1775, 1551), (1775, 492)), status="configured", sources=SOURCES["tokens"])
    s.flow("token-store", "auth", "tokens", "EasyAuth SAS access", start=("l", .78), end=("t", .23),
           via=((626, 875.9), (626, 1460), (751.2, 1460)), status="configured", sources=SOURCES["tokens"] + SOURCES["auth"])
    s.flow("image-pull", "api", "registry", "Identity image pull", start=("b", .88), end=("l", .18),
           via=((1745, 1435), (1745, 1547.4)), status="configured", sources=["infra/modules/registry.bicep", "infra/modules/containerapps.bicep"])
    s.flow("workspace", "insights", "logs", "Workspace link", start=("l", .5), end=("r", .5), status="configured", sources=SOURCES["monitor"])
    s.flow("resource-diagnostics", "sql", "logs", "Diagnostics bus", start=("r", .6), end=("r", .25),
           via=((2570, 959), (2570, 1745), (1210, 1745), (1210, 1838.75)), status="configured", sources=SOURCES["monitor"] + SOURCES["sql"])
    s.flow("metric-alerts", "model", "alerts", "Resource metric alerts", start=("r", .75), end=("r", .45),
           via=((2590, 618.75), (2590, 1873.75)), status="configured", sources=SOURCES["monitor"])
    s.boundary("network-note", 72, 1555, 440, 420, "Network topology / IaC", fill="#f1f7fb")
    s.icon("vnet-icon", "vnet", 96, 1622, 45)
    s.icon("endpoint-icon", "endpoint", 164, 1622, 45)
    s.icon("dns-icon", "dns", 232, 1622, 45)
    s.icon("nsg-icon", "nsg", 300, 1622, 45)
    s.text("network-detail", "VNet default: 10.40.0.0/16\nsnet-aca: 10.40.0.0/23\nsnet-pe: 10.40.4.0/24\nPrivate endpoints + DNS + NSGs\nSQL / Blob / Queue / KV / ACR\nFoundry / Monitor (AMPLS)\nDev also permits public access.\nNo private-only production claim.\nPaaS boxes are NOT VNet-hosted.",
           96, 1690, 392, 265, 20, COLORS["muted"])
    s.boundary("deferred", 610, 2095, 1990, 600, "Deferred ADR 0001 topology / placeholder workloads, not the five-assistant runtime", color="deferred", fill="#fffbf4")
    s.card("agents", 650, 2175, 520, 200, "Separate agent Container App", "Placeholder / KEDA agent-tasks scale 0-5\nProposed context + proposals through API only\nNo SQL / Blob / Key Vault credential", "deferred", "aca", SOURCES["workers"], title_size=22, body_size=19)
    s.card("queues", 1300, 2175, 550, 200, "Azure Queue Storage", "agent-tasks + agent-tasks-poison\nimport-jobs + import-jobs-poison\nDefined resources, not running business flows", "deferred", "queue", SOURCES["blob"] + SOURCES["workers"], body_size=19)
    s.card("orchestrator", 1980, 2175, 560, 200, "Container Apps orchestrator job", "Placeholder / five-minute schedule\nProposed deterministic checkpoints through API\nEnqueues tasks; not an autonomous supervisor", "deferred", "aca", SOURCES["workers"], title_size=22, body_size=19)
    s.card("import", 650, 2465, 520, 200, "Container Apps import job", "Placeholder / import-jobs event scale 0-2\nProposed validated import to limited SQL role\nQuarantine via Blob; no workbook write-back", "deferred", "aca", SOURCES["workers"], title_size=22, body_size=19)
    s.card("other-containers", 1300, 2465, 550, 200, "Same evidence storage account", "imports / quarantine / exports / audit-archive\nContainers defined in Bicep\nImmutable digest anchoring NOT implemented", "deferred", "blob", SOURCES["blob"] + ["mvp/README.md"], title_size=22, body_size=19)
    s.card("edge", 1980, 2465, 560, 200, "Front Door Premium + WAF", "Intended public edge / private backend\nNot deployed in this Bicep or exercise\nCurrent development ingress stays direct", "deferred", "edge", ["docs/adrs/0001-azure-architecture.md#decisions"], title_size=23, body_size=19)
    s.card("m365", 72, 2095, 440, 300, "M365 / external connectors", "SharePoint / Excel import: proposed\nSites.Selected + per-site grant\nTeams Workflows: optional ops alerts\nNo live sending, submission or approval\nNot a second system of record",
           "conditional", sources=SOURCES["m365"] + SOURCES["monitor"], title_size=24, body_size=20)
    s.flow("schedule-queue", "orchestrator", "queues", "agent-tasks", start=("l", .5), end=("r", .5), status="deferred", sources=SOURCES["workers"])
    s.flow("queue-agents", "queues", "agents", "KEDA / tasks", start=("l", .5), end=("r", .5), status="deferred", label_at=(1186, 2210, 98), sources=SOURCES["workers"])
    s.flow("queue-import", "queues", "import", "import-jobs", start=("l", .9), end=("r", .45),
           via=((1240, 2346), (1240, 2550.5)), status="deferred", label_at=(1165, 2397, 170), sources=SOURCES["workers"])
    s.flow("import-blob", "import", "other-containers", "Quarantine", start=("r", .75), end=("l", .75), status="deferred", label_at=(1186, 2600, 98), sources=SOURCES["workers"])
    s.flow("agents-api", "agents", "api", "Proposed API\ncontract only", start=("l", .2), end=("l", .93),
           via=((568, 2213), (568, 1261.1)), status="deferred", label_at=(532, 2010, 260), sources=SOURCES["workers"])
    s.flow("orchestrator-api", "orchestrator", "api", "Proposed checkpoints through API",
           start=("r", .25), end=("r", .96),
           via=((2670, 2225), (2670, 1410), (1710, 1410), (1710, 1269.2)),
           status="deferred", sources=SOURCES["workers"])
    s.flow("agents-model", "agents", "model", "Proposed model invocation",
           start=("b", .65), end=("r", .85),
           via=((988, 2420), (2760, 2420), (2760, 645.25)),
           status="deferred", sources=SOURCES["workers"] + SOURCES["model"])
    s.flow("sharepoint-import", "m365", "import", "Proposed one-way\nsnapshot import", start=("r", .8), end=("l", .45),
           via=((590, 2335), (590, 2555)), status="conditional",
           label_at=(95, 2435, 370), sources=SOURCES["m365"] + SOURCES["workers"])
    s.flow("import-sql", "import", "sql", "Proposed limited\nSQL import role", start=("l", .6), end=("r", .85),
           via=((548, 2579), (548, 1720), (2550, 1720), (2550, 1019)), status="deferred", sources=SOURCES["workers"])
    s.flow("ops-teams", "alerts", "m365", "Optional Teams\nWorkflows alert", start=("b", .65), end=("r", .3),
           via=((2288, 2045), (555, 2045), (555, 2185)), status="conditional", label_at=(1500, 2010, 360), sources=SOURCES["monitor"])
    s.text("notes", "Five-assistant inference never holds database locks and never approves domain changes. Responses are implicit unless double-headed.\nBlue arrows are configured relationships, not proof of end-to-end telemetry or private-only access. Deferred boxes are not working code.\nEmail / Teams alerts do not replace owned safety response. Historical Decision 1 evaluation is not a current API runtime dependency.",
           74, 2730, 2680, 108, 23, COLORS["muted"])
    return s.write()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--icon-pack", type=Path, required=True)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    provenance = extract_icons(args.icon_pack)
    results = [executive(commit), technical(commit)]
    (WORK / "source-manifest.json").write_text(json.dumps({
        "sourceCommit": commit, "pr": 68, "diagrams": results, "icons": provenance,
        "iconSource": "https://learn.microsoft.com/en-us/azure/architecture/icons/",
        "iconPack": "Azure_Public_Service_Icons_V24.zip", "retrieved": "2026-10-14",
    }, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
