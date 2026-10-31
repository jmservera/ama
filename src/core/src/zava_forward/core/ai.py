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
import uuid
from dataclasses import replace
from . import ai_consumption, ai_prompts, export_fields

SCOPE = "https://cognitiveservices.azure.com"
FORBIDDEN = re.compile(r"\b(i have sent|has been sent|we have sent|i've sent|email sent|message sent)\b", re.I)


class ModelMismatch(ValueError):
    def __init__(self, model):
        super().__init__("Returned model differs from the released model version.")
        self.model = ai_consumption.bounded_model(model)


class Ai:
    def __init__(self):
        self.endpoint = os.environ.get("AI_ENDPOINT", "").rstrip("/")
        self.fast = os.environ.get("AI_DEPLOYMENT", "standard")
        self.strong = os.environ.get("AI_DEPLOYMENT_STRONG", "capable")
        self.model_version = os.environ.get("AI_MODEL_VERSION", "unattested")
        self.model_version_strong = os.environ.get("AI_MODEL_VERSION_STRONG", self.model_version)
        self.token = None
        self.expires = 0
        self.gate = None  # (task, deployment) -> reason the task is suspended, or None
        self.release = None  # Per-invocation selected record; never mutable shared request state.
        self.consumption = None

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

    def configuration(self, deployment, temperature, max_tokens):
        model = self.model_version_strong if deployment == self.strong else self.model_version
        return ai_consumption.reference(json.dumps(dict(
            endpoint=self.endpoint, deployment=deployment, model=model,
            api_version="2024-10-21", temperature=temperature, max_tokens=max_tokens,
        ), sort_keys=True))

    def _request(self, deployment, system, user, max_tokens, timeout, temperature, receipt):
        body = json.dumps({"messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                           "max_tokens": max_tokens, "temperature": temperature}, ensure_ascii=True).encode("ascii")
        if self.consumption is None:
            raise ai_consumption.DispatchHeld("financial-meter-unavailable")
        model = self.model_version_strong if deployment == self.strong else self.model_version
        context = ai_consumption.CURRENT.get()
        if context is None:
            context = ai_consumption.CallContext(
                ai_consumption.reference(uuid.uuid4().hex), ai_consumption.reference(uuid.uuid4().hex),
                "evidence", "retrofit-case", self.configuration(deployment, temperature, max_tokens),
                ai_consumption.reference(system),
            )
        context = replace(context, configuration=self.configuration(deployment, temperature, max_tokens))
        bound = len(body) if isinstance(user, str) else None
        parsed_endpoint = urllib.parse.urlparse(self.endpoint)
        nonbillable_loopback = parsed_endpoint.scheme == "http" and parsed_endpoint.hostname in ("127.0.0.1", "localhost", "::1")
        rid = self.consumption.reserve(context, model, bound, max_tokens, live=not nonbillable_loopback)
        receipt.update(meter_id=rid, meter_root=context.root,
                       configuration=context.configuration, prompt_hash=context.prompt, usage=None)
        try:
            req = urllib.request.Request(f"{self.endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-10-21",
                                         data=body, headers={"Authorization": f"Bearer {self._token()}", "Content-Type": "application/json"})
            self.consumption.dispatch_check(rid)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read(256001)
                if len(raw) > 256000:
                    raise ValueError("Oversized provider envelope.")
                result = json.loads(raw)
            receipt.update(usage=ai_consumption.usage(result.get("usage")),
                           returned_model=ai_consumption.bounded_model(result.get("model")))
            self.consumption.complete(rid, result.get("usage"), result.get("model"), "returned")
        except Exception as error:
            self.consumption.complete(rid, None, None, "timeout" if isinstance(error, TimeoutError) else "provider-unavailable")
            raise
        if model != "unattested" and result.get("model") != model:
            raise ModelMismatch(result.get("model"))
        return result

    def _chat(self, deployment, system, user, max_tokens=700, receipt=None):
        receipt = {} if receipt is None else receipt
        result = self._request(deployment, system, user, max_tokens, 40, 0.3, receipt)
        return result["choices"][0]["message"]["content"].strip()

    def evidence(self, system, user, max_tokens=600, timeout=20):
        """No fallback, raw output or exception text in the durable usage envelope."""
        envelope = dict(provider="azure-openai", deployment=self.fast, model=None,
                        usage=None, outcome="disabled", source="unverified", text=None)
        if not self.configured:
            return envelope
        try:
            result = self._request(self.fast, system, user, max_tokens, timeout, 0, envelope)
            envelope.update(model=result.get("model"), outcome="returned", source="ai",
                            text=result["choices"][0]["message"]["content"])
        except ModelMismatch as error:
            envelope.update(model=error.model, outcome="model-mismatch")
        except ai_consumption.DispatchHeld as error:
            envelope.update(outcome="financial-held", reason=str(error))
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
        selected = None
        receipt = {}

        def out(**kw):
            return dict(kw, **receipt, task=task, release=selected,
                        prompt_version=ai_prompts.version(task) if task in ai_prompts.PROMPTS else None,
                        latency_ms=round((time.perf_counter() - t0) * 1000, 1))
        if off:
            return out(text=template, source="template", model=None, validated=True, reason="workflow-only mode selected")
        dep = self.strong if strong else self.fast
        held = self.gate(task, dep) if self.gate else None
        if held:
            return out(text=template, source="template", model=None, validated=True, reason=held)
        if not self.configured:
            return out(text=template, source="template", model=None, validated=True, reason="AI is not configured")
        selected = self.release(task, dep) if self.release else None
        if self.release and selected is None:
            return out(text=template, source="template", model=None, validated=True,
                       reason="Release changed before dispatch; use the manual route.")
        try:
            if ai_consumption.CURRENT.get() is None:
                root = ai_consumption.reference(uuid.uuid4().hex)
                context = ai_consumption.CallContext(root, root, task.replace("_", "-"), "retrofit-case",
                                                     self.configuration(dep, 0.3, 700),
                                                     ai_consumption.reference(ai_prompts.version(task)) if task in ai_prompts.PROMPTS else ai_consumption.reference(system))
                with ai_consumption.call_context(context):
                    text = self._chat(dep, system, user, receipt=receipt)
            else:
                text = self._chat(dep, system, user, receipt=receipt)
        except Exception as e:  # network, auth, quota: never block the person
            return out(text=template, source="template", model=None, validated=True, error=type(e).__name__,
                       reason=f"model unavailable ({type(e).__name__})")
        ok = bool(text) and not FORBIDDEN.search(text) and (check(text) if check else True)
        if not ok:
            return out(text=template, source="template", model=dep, validated=False, ai_text=text,
                       reason="model output failed validation")
        held = self.gate(task, dep) if self.gate else None
        if self.release and selected != self.release(task, dep):
            held = "activation release changed; use the manual route"
        if held:  # completion recheck: suspension or revocation during the call discards the text
            return out(text=template, source="template", model=None, validated=True, quarantined=True,
                       reason=f"result discarded: {held}")
        return out(text=text, source="ai", model=dep, validated=True, reason=None)

    def look_at(self, name, data, mime, off=False):
        """Describe an uploaded document. Reads text and images; other types are stored only."""
        export_fields.scalars(dict(name=name, mime=mime), ("name", "mime"))
        system, instruction = ai_prompts.render("read_document", name=name)
        if mime.startswith("image/"):
            content = [{"type": "text", "text": instruction},
                       {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(data).decode()}"}}]
        elif mime.startswith("text/") or mime in ("application/json", "text/csv"):
            content = instruction + "\n\n" + data.decode("utf-8", "replace")[:6000]
        else:
            return dict(text="This file type is stored but not read. Add a short note about what it is.", source="template",
                        model=None, validated=True, task="read_document")
        held = self.gate("read_document", self.strong) if self.gate else None
        if held:
            return dict(text="The file is stored. AI reading is suspended; add a short note about what it is.", source="template",
                        model=None, validated=True, task="read_document", reason=held)
        if off or not self.configured:
            return dict(text="AI reading is not switched on here. The file is stored.", source="template", model=None,
                        validated=True, task="read_document",
                        reason="workflow-only mode selected" if off else "AI is not configured")
        selected = None
        receipt = {}
        try:
            selected = self.release("read_document", self.strong) if self.release else None
            if self.release and selected is None:
                return dict(text="The file is stored. Add a short note about what it is.",
                            source="template", model=None, validated=True, task="read_document",
                            reason="Release changed before dispatch; use the manual route.")
            if ai_consumption.CURRENT.get() is None:
                root = ai_consumption.reference(uuid.uuid4().hex)
                context = ai_consumption.CallContext(root, root, "read-document", "document",
                                                     self.configuration(self.strong, 0.3, 500),
                                                     ai_consumption.reference(ai_prompts.version("read_document")))
                with ai_consumption.call_context(context):
                    text = self._chat(self.strong, system, content, 500, receipt=receipt)
            else:
                text = self._chat(self.strong, system, content, 500, receipt=receipt)
            held = self.gate("read_document", self.strong) if self.gate else None
            if self.release and selected != self.release("read_document", self.strong):
                held = "activation release changed; use the manual route"
            if held:
                return dict(text="The file is stored. AI reading is suspended; add a short note about what it is.",
                            source="template", model=None, validated=True, task="read_document", quarantined=True,
                            release=selected, **receipt, reason=f"result discarded: {held}")
            return dict(text=text, source="ai", model=self.strong, validated=True, task="read_document",
                        release=selected, **receipt, prompt_version=ai_prompts.version("read_document"))
        except Exception as e:
            return dict(text="The file is stored. AI could not read it just now.", source="template", model=None,
                        validated=True, task="read_document", release=selected, **receipt, error=type(e).__name__,
                        reason=f"model unavailable ({type(e).__name__})")
