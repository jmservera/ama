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
import urllib.parse
import urllib.request

SCOPE = "https://cognitiveservices.azure.com"
FORBIDDEN = re.compile(r"\b(i have sent|has been sent|we have sent|i've sent|email sent|message sent)\b", re.I)


class Ai:
    def __init__(self):
        self.endpoint = os.environ.get("AI_ENDPOINT", "").rstrip("/")
        self.fast = os.environ.get("AI_DEPLOYMENT", "standard")
        self.strong = os.environ.get("AI_DEPLOYMENT_STRONG", "capable")
        self.token = None
        self.expires = 0

    @property
    def configured(self):
        return bool(self.endpoint)

    def _token(self):
        import time
        if self.token and time.time() < self.expires - 120:
            return self.token
        ep, hdr = os.environ.get("IDENTITY_ENDPOINT"), os.environ.get("IDENTITY_HEADER")
        parameters = {"resource": SCOPE, "api-version": "2019-08-01" if ep else "2018-02-01"}
        client_id = os.environ.get("AZURE_CLIENT_ID")
        if client_id:
            parameters["client_id"] = client_id
        query = urllib.parse.urlencode(parameters)
        if ep:
            req = urllib.request.Request(f"{ep}?{query}", headers={"X-IDENTITY-HEADER": hdr})
        else:
            req = urllib.request.Request(f"http://169.254.169.254/metadata/identity/oauth2/token?{query}",
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
            return json.load(r)["choices"][0]["message"]["content"].strip()

    def evidence(self, system, user, max_tokens=600, timeout=20):
        """No fallback, raw output or exception text in the durable usage envelope."""
        envelope = dict(provider="azure-openai", deployment=self.fast, model=None,
                        usage=None, outcome="disabled", source="unverified", text=None)
        if not self.configured:
            return envelope
        body = json.dumps({"messages": [{"role": "system", "content": system},
                                       {"role": "user", "content": user}],
                           "max_tokens": max_tokens, "temperature": 0}).encode()
        try:
            req = urllib.request.Request(
                f"{self.endpoint}/openai/deployments/{self.fast}/chat/completions?api-version=2024-10-21",
                data=body, headers={"Authorization": f"Bearer {self._token()}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read(256001)
                if len(raw) > 256000:
                    raise ValueError("Oversized provider envelope")
                result = json.loads(raw)
            usage = result.get("usage")
            if isinstance(usage, dict) and all(type(usage.get(k)) is int and usage[k] >= 0
                                              for k in ("prompt_tokens", "completion_tokens", "total_tokens")) and (
                    usage["prompt_tokens"] > 0 and usage["total_tokens"] == usage["prompt_tokens"] + usage["completion_tokens"]):
                envelope["usage"] = {k: usage[k] for k in ("prompt_tokens", "completion_tokens", "total_tokens")}
            envelope.update(model=result.get("model"), outcome="returned", source="ai",
                            text=result["choices"][0]["message"]["content"])
        except TimeoutError:
            envelope["outcome"] = "timeout"
        except Exception:
            envelope["outcome"] = "provider-unavailable"
        return envelope

    def run(self, task, system, user, template, strong=False, check=None, off=False):
        """Return dict(text, source, model, validated, reason, latency_ms). Falls back to the template on any failure.

        off=True is the explicit workflow-only mode: the model is not called.
        """
        t0 = time.perf_counter()

        def out(**kw):
            return dict(kw, task=task, latency_ms=round((time.perf_counter() - t0) * 1000, 1))
        if off:
            return out(text=template, source="template", model=None, validated=True, reason="workflow-only mode selected")
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
        try:
            text = self._chat(self.strong, system, content, 500)
            return dict(text=text, source="ai", model=self.strong, validated=True, task="read_document")
        except Exception as e:
            return dict(text="The file is stored. AI could not read it just now.", source="template", model=None,
                        validated=True, task="read_document", error=type(e).__name__,
                        reason=f"model unavailable ({type(e).__name__})")
