"""AI assistance, bounded by design.

The model only drafts text for a person to read, change and use. It cannot
change a case, send anything or decide anything. Each request carries only the
fields it needs, output is checked before it is shown, every run is recorded in
the audit log, and a plain template is used if the model is unavailable.
"""
import base64
import contextlib
import contextvars
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections.abc import Mapping
from dataclasses import replace
from . import ai_consumption, ai_prompts, ai_transport, data_protection, export_fields, task_contracts, telemetry

SCOPE = "https://cognitiveservices.azure.com"
_ACTIONS = (r"sent|approved|authori[sz]ed|signed off|rejected|declined|updated|changed|amended|edited|"
            r"modified|re-?ranked|ranked|recorded|submitted|released|closed|reopened|assigned|escalated|"
            r"booked|cancelled|canceled|deleted|saved|published|awarded|paid|committed")
# Claims that the assistant, or an unnamed actor, has just approved, sent or changed something.
# Plain past-tense status of an already recorded field ("was approved on 3 March") is not matched.
FORBIDDEN = re.compile(
    r"\b(?:email sent|message sent"
    rf"|(?:i|we)(?:\s+have|\s+had|'ve|\s+just|\s+now)(?:\s+(?:just|now|already|successfully))*\s+(?:{_ACTIONS})"
    rf"|(?:has|have)(?:\s+(?:now|just|already|successfully))*\s+been\s+(?:{_ACTIONS}))\b",
    re.I,
)


class DispatchDenied(RuntimeError):
    pass


DEMO_SENSOR_DISPATCH_ENV = "ZF_DEMO_SENSOR_MODEL_DISPATCH"
DEMO_SENSOR_DISPATCH_VALUE = "synthetic-demo-only"


def demo_sensor_dispatch(env: "Mapping[str, str] | None" = None) -> bool:
    """Demo-only opt-in: a real Ai client may carry captured retained readings.

    Retained readings are synthetic by construction. The deployment must run the demo profile and set
    the exact value; every other deployment keeps the fail-closed ban. Per-attempt consent, release and
    epoch checks still run before dispatch."""
    env = os.environ if env is None else env
    return (
        env.get(DEMO_SENSOR_DISPATCH_ENV) == DEMO_SENSOR_DISPATCH_VALUE
        and env.get("ZF_DEPLOYMENT_PROFILE") == "demo"
    )


def may_carry_captured_readings(carrier: object, env: "Mapping[str, str] | None" = None) -> bool:
    """Captured IoT readings may only reach a carrier that is not a real Ai client and declares that it
    sends no bytes, or a real Ai client in the explicitly opted-in synthetic demo deployment. This is a
    composition declaration about the sink, not data provenance."""
    if isinstance(carrier, Ai):
        return demo_sensor_dispatch(env)
    return getattr(carrier, "sends_no_bytes", False) is True


MAX_TEXT_BYTES = 128 * 1024
MAX_IMAGE_BYTES = 4 * 1024 * 1024
MAX_PARTS = 8
IMAGE_TYPES = ("image/png", "image/jpeg")


class InputRefused(ValueError):
    """The request is outside the approved input bounds; no provider call is made."""


def _utf8_size(text):
    try:
        return len(text.encode("utf-8"))
    except UnicodeEncodeError:
        raise InputRefused("input-type-not-approved") from None


def approved_payload(system, user):
    """Type and size allowlist at the one boundary every provider family shares; raises InputRefused."""
    if not isinstance(system, str):
        raise InputRefused("input-type-not-approved")
    text = 0
    images = 0
    if isinstance(user, str):
        user = [{"type": "text", "text": user}]
    if not isinstance(user, list) or not user:
        raise InputRefused("input-type-not-approved")
    if len(user) > MAX_PARTS:
        raise InputRefused("input-too-many-parts")
    for part in user:
        if not isinstance(part, dict):
            raise InputRefused("input-type-not-approved")
        if part.keys() == {"type", "text"} and part["type"] == "text" and isinstance(part["text"], str):
            text += _utf8_size(part["text"])
            continue
        image = part.get("image_url")
        url = image.get("url") if isinstance(image, dict) and image.keys() == {"url"} else None
        if part.keys() != {"type", "image_url"} or part["type"] != "image_url" or not isinstance(url, str):
            raise InputRefused("input-type-not-approved")
        head, _, data = url.partition(";base64,")
        if not head.startswith("data:") or head.removeprefix("data:") not in IMAGE_TYPES:
            raise InputRefused("input-type-not-approved")
        try:
            base64.b64decode(data, validate=True)
        except ValueError:
            raise InputRefused("input-type-not-approved") from None
        images += len(data) * 3 // 4
        if images > MAX_IMAGE_BYTES:
            raise InputRefused("input-image-too-large")
    if text + _utf8_size(system) > MAX_TEXT_BYTES:
        raise InputRefused("input-too-large")


class DispatchWitness:
    """Core-written record of one `Ai.evidence` invocation's transport hand-offs.

    Only this module changes it. `attempts` counts requests handed to the transport (a send-fence
    withdrawal inside the opener or a redirect inside `urlopen` is not counted separately).
    """

    def __init__(self):
        self.witnessed = False
        self.attempts = 0
        self.closed = False


DISPATCH = contextvars.ContextVar("ai_dispatch_witness", default=None)


@contextlib.contextmanager
def count_dispatches():
    """Open one witness for the invocations the caller makes inside this scope on this context."""
    witness = DispatchWitness()
    token = DISPATCH.set(witness)
    try:
        yield witness
    finally:
        witness.closed = True
        DISPATCH.reset(token)


class ModelMismatch(ValueError):
    def __init__(self, model):
        super().__init__("Returned model differs from the released model version.")
        self.model = ai_consumption.bounded_model(model)


class Ai:
    # No transport here can establish an atomic suspend-and-send guarantee against a real provider,
    # so the sealed simulation route is unavailable. Only labelled scripted test doubles set this.
    send_fence_supported = False

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
        self.simulation_verifier = None  # set only by trusted composition: (seal, body bytes) -> raises SimulationRefused
        self.synthetic_price_capabilities = frozenset()  # demo-only: capabilities whose synthetic price may admit a live call

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

    @staticmethod
    def provider_body(system, user, max_tokens, temperature):
        """The only serializer of the provider request body; the sealed simulation lane uses it too."""
        return json.dumps({"messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                           "max_tokens": max_tokens, "temperature": temperature}, ensure_ascii=True).encode("ascii")

    def is_live(self, capability):
        endpoint = urllib.parse.urlparse(self.endpoint)
        nonbillable = endpoint.scheme == "http" and endpoint.hostname in ("127.0.0.1", "localhost", "::1")
        return not nonbillable and capability not in self.synthetic_price_capabilities

    def request_plan(self, system, user, deployment, temperature, max_tokens):
        """The exact request facts a permit binds: final body digest, model, configuration and bounds."""
        body = self.provider_body(system, user, max_tokens, temperature)
        return dict(body_sha256=hashlib.sha256(body).hexdigest(),
                    model=self.model_version_strong if deployment == self.strong else self.model_version,
                    deployment=deployment, temperature=temperature, max_tokens=max_tokens,
                    configuration=self.configuration(deployment, temperature, max_tokens),
                    input_bound=len(body) if isinstance(user, str) else None)

    def _request(self, deployment, system, user, max_tokens, timeout, temperature, receipt):
        with telemetry.operation("chat") as observation:
            try:
                return self._request_body(deployment, system, user, max_tokens, timeout, temperature, receipt)
            finally:
                if usage := receipt.get("usage"):
                    observation.usage(usage["prompt_tokens"], usage["completion_tokens"])

    def _request_body(self, deployment, system, user, max_tokens, timeout, temperature, receipt):
        approved_payload(system, user)
        seal = ai_consumption.SIMULATION_SEAL.get()
        if ai_consumption.CAPTURED_READINGS.get() and seal is None:
            raise ai_consumption.DispatchWithdrawn("captured-readings-transmission-unavailable")
        body = self.provider_body(system, user, max_tokens, temperature)
        if seal is not None:
            if not self.send_fence_supported:
                raise ai_consumption.SimulationRefused("real-provider-route-unavailable")
            # Verified against the bytes serialized here, before the data hold, meter, token or socket.
            verifier = self.simulation_verifier
            if verifier is None:
                raise ai_consumption.SimulationRefused("verifier-unavailable")
            verifier(seal, body)
        protected = data_protection.dispatch_hold("prompt_output", os.environ)
        if protected:
            raise DispatchDenied(protected)
        if isinstance(user, str) and len(body) > MAX_TEXT_BYTES:
            raise InputRefused("input-too-large")
        if self.consumption is None:
            raise ai_consumption.DispatchHeld("financial-meter-unavailable")
        fence = ai_consumption.SEND_FENCE.get()
        if fence is not None:
            fence()  # a late caller creates no financial reservation, credential or socket
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
        rid = self.consumption.reserve(context, model, bound, max_tokens, live=self.is_live(context.capability))
        receipt.update(meter_id=rid, meter_root=context.root,
                       configuration=context.configuration, prompt_hash=context.prompt, usage=None)
        try:
            req = urllib.request.Request(f"{self.endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-10-21",
                                         data=body, headers={"Authorization": f"Bearer {self._token()}", "Content-Type": "application/json"})
            self.consumption.dispatch_check(rid)
            open_request = urllib.request.urlopen if fence is None else ai_transport.opener(fence, timeout).open
            witness = DISPATCH.get()
            if witness is not None and not witness.closed:
                witness.attempts += 1  # the provider request is handed to the transport here and only here
            with open_request(req, timeout=timeout) as response:
                raw = response.read(256001)
                if len(raw) > 256000:
                    raise ValueError("Oversized provider envelope.")
                result = json.loads(raw)
            self.consumption.complete(rid, result.get("usage"), result.get("model"), "returned")
            # Usage is reported only after the ledger settled it, so a result never states tokens the ledger lacks.
            receipt.update(usage=ai_consumption.usage(result.get("usage")),
                           returned_model=ai_consumption.bounded_model(result.get("model")))
        except Exception as error:
            if isinstance(error, urllib.error.HTTPError):
                error.close()  # releases the absolute deadline that owns the connection
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
        envelope = dict(provider="azure-openai", deployment=ai_consumption.safe_identity(self.fast), model=None,
                        usage=None, outcome="disabled", source="unverified", text=None)
        witness = DISPATCH.get()
        if witness is not None and not witness.closed:
            witness.witnessed = True
        if not self.configured:
            return envelope
        try:
            result = self._request(self.fast, system, user, max_tokens, timeout, 0, envelope)
            envelope.update(model=ai_consumption.bounded_model(result.get("model")), outcome="returned", source="ai",
                            text=result["choices"][0]["message"]["content"])
        except InputRefused as error:
            envelope.update(outcome="input-refused", reason=str(error))
        except ModelMismatch as error:
            envelope.update(model=error.model, outcome="model-mismatch")
        except ai_consumption.SimulationRefused as error:
            envelope.update(outcome="simulation-refused", reason=error.code, usage=None)
        except ai_consumption.DispatchWithdrawn:
            envelope.update(outcome="suspended-before-dispatch", usage=None)
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
            kw["model"] = ai_consumption.bounded_model(kw.get("model"))
            return dict(kw, **receipt, task=task, release=selected,
                        prompt_version=ai_prompts.version(task) if task in ai_prompts.PROMPTS else None,
                        latency_ms=round((time.perf_counter() - t0) * 1000, 1))
        from . import ai_registry
        if not ai_registry.is_registered(task):
            return out(text=template, source="template", model=None, validated=True, registered=False,
                       reason="AI feature is not registered; use the manual route")
        if not ai_registry.is_dispatch_enabled(task):
            return out(text=template, source="template", model=None, validated=True, enabled=False,
                       reason="AI feature is disabled; use the manual route")
        if off:
            return out(text=template, source="template", model=None, validated=True, reason="workflow-only mode selected")
        label = task_contracts.prohibited_in(task, system, user)
        if label:
            return out(text=template, source="template", model=None, validated=True,
                       reason=f"Prompt holds prohibited content ({label}); it is not sent to AI. Use the manual route.")
        dep = self.strong if strong else self.fast
        held = self.gate(task, dep) if self.gate else None
        if held:
            return out(text=template, source="template", model=None, validated=True, reason=held)
        protected = data_protection.dispatch_hold("prompt_output", os.environ)
        if protected:
            return out(text=template, source="template", model=None, validated=True, reason=protected)
        if not self.configured:
            return out(text=template, source="template", model=None, validated=True, reason="AI is not configured")
        selected = self.release(task, dep) if self.release else None
        if self.release and selected is None:
            return out(text=template, source="template", model=None, validated=True,
                       reason="Release changed before dispatch; use the manual route.")
        try:
            if ai_consumption.CURRENT.get() is None:
                root = ai_consumption.reference(uuid.uuid4().hex)
                context = ai_consumption.CallContext(root, root, ai_registry.consumption_capability(task), "retrofit-case",
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

    def look_at(self, name, data, mime, off=False, *, derivative=None, necessity_exception=None,
                case_id=None, doc_id=None, resident_consent=None, doc=None):
        """Describe an uploaded document. Reads text and images; other types are stored only."""
        export_fields.scalars(dict(name=name, mime=mime), ("name", "mime"))
        from . import ai_registry
        if not ai_registry.is_registered("read_document"):
            return dict(text="The file is stored. AI reading is not registered; add a short note about what it is.",
                        source="template", model=None, validated=True, registered=False, task="read_document",
                        reason="AI feature is not registered; use the manual route")
        if not ai_registry.is_dispatch_enabled("read_document"):
            return dict(text="The file is stored. AI reading is disabled; add a short note about what it is.",
                        source="template", model=None, validated=True, enabled=False, task="read_document",
                        reason="AI feature is disabled; use the manual route")
        system, instruction = ai_prompts.render("read_document", name=name)
        if mime.startswith("image/"):
            if mime not in IMAGE_TYPES or len(data) > MAX_IMAGE_BYTES:
                return dict(text="The file is stored but too large or not a type that AI reads. Add a short note about what it is.",
                            source="template", model=None, validated=True, task="read_document",
                            reason="input outside approved bounds; use the manual route")
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
        protected = data_protection.document_model_hold(
            doc, os.environ, case_id=case_id, doc_id=doc_id,
            derivative=derivative, necessity_exception=necessity_exception,
            resident_consent=resident_consent)
        if protected:
            return dict(text="The file is stored. It is not sent to AI; add a short note about what it is.", source="template",
                        model=None, validated=True, task="read_document", reason=protected)
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
                context = ai_consumption.CallContext(root, root, ai_registry.consumption_capability("read_document"), "document",
                                                     self.configuration(self.strong, 0.3, 500),
                                                     ai_consumption.reference(ai_prompts.version("read_document")))
                with ai_consumption.call_context(context):
                    text = self._chat(self.strong, system, content, 500, receipt=receipt)
            else:
                text = self._chat(self.strong, system, content, 500, receipt=receipt)
            if not text or FORBIDDEN.search(text):
                return dict(text="The file is stored. Add a short note about what it is.",
                            source="template", model=self.strong, validated=False, ai_text=text,
                            task="read_document", release=selected, **receipt,
                            reason="model output failed validation")
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
