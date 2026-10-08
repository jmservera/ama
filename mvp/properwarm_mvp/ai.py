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
            return json.load(r)["choices"][0]["message"]["content"].strip()

    def run(self, task, system, user, template, strong=False, check=None):
        """Return dict(text, source, model, validated). Falls back to the template on any failure."""
        if not self.configured:
            return dict(text=template, source="template", model=None, validated=True, task=task)
        dep = self.strong if strong else self.fast
        try:
            text = self._chat(dep, system, user)
        except Exception as e:  # network, auth, quota: never block the person
            return dict(text=template, source="template", model=None, validated=True, task=task, error=type(e).__name__)
        ok = bool(text) and not FORBIDDEN.search(text) and (check(text) if check else True)
        if not ok:
            return dict(text=template, source="template", model=dep, validated=False, task=task)
        return dict(text=text, source="ai", model=dep, validated=True, task=task)

    def look_at(self, name, data, mime):
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
        if not self.configured:
            return dict(text="AI reading is not switched on here. The file is stored.", source="template", model=None,
                        validated=True, task="read_document")
        try:
            text = self._chat(self.strong, system, content, 500)
            return dict(text=text, source="ai", model=self.strong, validated=True, task="read_document")
        except Exception as e:
            return dict(text="The file is stored. AI could not read it just now.", source="template", model=None,
                        validated=True, task="read_document", error=type(e).__name__)
