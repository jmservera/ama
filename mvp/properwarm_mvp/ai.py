"""AI assistance, bounded by design.

The model only drafts text for a person to read, change and use. It cannot
change a case, send anything or decide anything. Each request carries only the
fields it needs, output is checked before it is shown, every run is recorded in
the audit log, and a plain template is used if the model is unavailable.
"""
import base64
import json
import os
import re
import time
import threading
from hashlib import sha256
import urllib.request
import urllib.error

from .decision import inference_guard

SCOPE = "https://cognitiveservices.azure.com"
FORBIDDEN = re.compile(r"\b(i have sent|has been sent|we have sent|i've sent|email sent|message sent)\b", re.I)


class Ai:
    def __init__(self):
        self.endpoint = os.environ.get("AI_ENDPOINT", "").rstrip("/")
        self.fast = os.environ.get("AI_DEPLOYMENT", "standard")
        self.strong = os.environ.get("AI_DEPLOYMENT_STRONG", "capable")
        self.token = None
        self.expires = 0
        self.local = threading.local()

    def _exercise_guard(self, task, text, kind="case_facts"):
        if os.environ.get("PW_EXERCISE") != "1":
            return None
        return inference_guard(task, "generative-drafting",
                               permissions=("evidence.read", "drafts.assist"),
                               source_kinds=(kind,), source_count=1,
                               text_chars=len(json.dumps(text)), field="narrative")

    @property
    def configured(self):
        return bool(self.endpoint)

    def _token(self):
        import time
        if self.token and time.time() < self.expires - 120:
            return self.token
        ep, hdr = os.environ.get("IDENTITY_ENDPOINT"), os.environ.get("IDENTITY_HEADER")
        if ep:
            req = urllib.request.Request(f"{ep}?resource={SCOPE}&api-version=2019-08-01", headers={"X-IDENTITY-HEADER": hdr})
        else:
            req = urllib.request.Request(f"http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource={SCOPE}",
                                         headers={"Metadata": "true"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.load(r)
        self.token = data["access_token"]
        self.expires = float(data.get("expires_on", time.time() + 1800))
        return self.token

    def _chat(self, deployment, system, user, max_tokens=700):
        body = json.dumps({"messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                           "max_tokens": max_tokens, "temperature": 0.3}).encode()
        req = urllib.request.Request(f"{self.endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-10-21",
                                     data=body, headers={"Authorization": f"Bearer {self._token()}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=40) as r:
            response = json.load(r)
        self.local.provenance = dict(provider="azure-openai", deployment=deployment,
                                     model=response.get("model"), usage=response.get("usage"),
                                     provider_request_id=response.get("id"),
                                     request_hash=sha256(body).hexdigest())
        return response["choices"][0]["message"]["content"].strip()

    def run(self, task, system, user, template, strong=False, check=None, off=False):
        """Return dict(text, source, model, validated, reason, latency_ms). Falls back to the template on any failure.

        off=True is the explicit workflow-only mode: the model is not called.
        """
        t0 = time.perf_counter()

        def out(**kw):
            return dict(kw, task=task, latency_ms=round((time.perf_counter() - t0) * 1000, 1),
                        provenance=getattr(self.local, "provenance", None),
                        assistance_status="succeeded" if kw.get("source") == "ai" else "manual",
                        provider_success=kw.get("source") == "ai")
        self.local.provenance = None
        if off:
            return out(text=template, source="template", model=None, validated=True, reason="workflow-only mode selected")
        guard = self._exercise_guard(task, user)
        if guard is not None and not guard.allowed:
            return out(text=template, source="template", model=None, validated=True,
                       reason=f"assistance disabled: {guard.reason}")
        if not self.configured:
            return out(text=template, source="template", model=None, validated=True, reason="AI is not configured")
        dep = self.strong if strong else self.fast
        try:
            text = self._chat(dep, system, user)
        except Exception as e:  # network, auth, quota: never block the person
            return out(text=template, source="template", model=None, validated=True, error=type(e).__name__,
                       reason=f"model unavailable ({type(e).__name__})")
        ok = bool(text) and not FORBIDDEN.search(text) and (check(text) if check else True)
        if not ok:
            return out(text=template, source="template", model=dep, validated=False, ai_text=text,
                       reason="model output failed validation")
        return out(text=text, source="ai", model=dep, validated=True, reason=None)

    def source_narrative(self, case_id: str, draft: dict) -> dict:
        """Draft from the authorized form snapshot only; preserve citations and failure."""
        from . import ai_tasks
        labels = [
            f"Form field {field}: {json.dumps(value['value'], sort_keys=True)}"
            for field, value in draft["fields"].items()
            if value["state"] == "confirmed" and field not in (
                "declaration", "signature", "resident_decision", "certification",
                "controlled_approval", "match_budget_approved")
        ]
        sources = {case_id: labels}
        template = "Manual narrative required. Review confirmed source-bound form fields; nothing sent."
        if not labels:
            return dict(text=template, source="template", task="source_bound_narrative",
                        approval="Not reviewed", provider_success=False, assistance_status="disabled",
                        reason="No confirmed permitted form facts", case_id=case_id,
                        input_version=draft["input_version"], source_refs=[], citations=[], citable_facts=[])
        def checked(text):
            _, good, bad, _ = ai_tasks.analyse(text, sources)
            return bool(good) and not bad
        result = self.run("source_bound_narrative",
                         "Draft only from these supplied facts. No approval, signatures or external actions.",
                         json.dumps(labels) + ai_tasks.cite_instruction(sources),
                         template, check=checked, off=ai_tasks.workflow_only())
        clean, citations, bad, _ = ai_tasks.analyse(result["text"], sources)
        return dict(result, text=clean, citations=citations, unresolved_citations=bad,
                    approval="Not reviewed", case_id=case_id, input_version=draft["input_version"],
                    source_refs=[{key: source[key] for key in ("id", "version", "hash")}
                                 for source in draft["sources"].values()],
                    prompt_version=ai_tasks.PROMPT_VERSION, citable_facts=labels)

    def look_at(self, name, data, mime, off=False):
        """Describe an uploaded document. Reads text and images; other types are stored only."""
        system = ("You help a housing association retrofit team file documents. Say what kind of document this is "
                  "(for example EPC, survey, photo of damp, consent form, invoice), list the key facts you can see in at "
                  "most six short bullet points, and flag anything unclear. Do not guess. Plain English.")
        if mime.startswith("image/"):
            content = [{"type": "text", "text": f"File name: {name}"},
                       {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(data).decode()}"}}]
        elif mime.startswith("text/") or mime in ("application/json", "text/csv"):
            content = f"File name: {name}\n\n" + data.decode("utf-8", "replace")[:6000]
        else:
            return dict(text="This file type is stored but not read. Add a short note about what it is.", source="template",
                        model=None, validated=True, task="read_document")
        if off or not self.configured:
            return dict(text="AI reading is not switched on here. The file is stored.", source="template", model=None,
                        validated=True, task="read_document",
                        reason="workflow-only mode selected" if off else "AI is not configured")
        guard = self._exercise_guard("read_document", content, "form_evidence")
        if guard is not None and not guard.allowed:
            return dict(text="Document stored. Use manual evidence review.", source="template", model=None,
                        validated=True, task="read_document", provider_success=False,
                        assistance_status="disabled", reason=guard.reason)
        try:
            text = self._chat(self.strong, system, content, 500)
            return dict(text=text, source="ai", model=self.strong, validated=True, task="read_document")
        except Exception as e:
            return dict(text="The file is stored. AI could not read it just now.", source="template", model=None,
                        validated=True, task="read_document", error=type(e).__name__,
                        reason=f"model unavailable ({type(e).__name__})")
