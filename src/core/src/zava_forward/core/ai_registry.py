"""Versioned registry of every AI-assisted task, and the unapproved proposal envelope.

The registry covers the five proposal-only assistants and the retained
briefing, message, summary, priority, funding and document-reading paths.
Everything here is constructed offline scaffolding: no accountable individual,
delegation or approval is recorded, so no task is approved for live reliance.
An unknown owner stays unknown and can never authorize activation. A task that
is not registered gets no model call.
"""
import hashlib
import json
from . import ai_prompts, rai_release, ranking

from .assistants import REGISTRY as ASSISTANTS, VERSION as ASSISTANT_VERSION

REGISTRY_VERSION = "2026-10-15.1"
UNKNOWN = "unknown"
UNAPPROVED = "unapproved"
PROVIDER = "azure-openai"
CHAT_TASK = "chat-case-conversation"
PROHIBITED_PURPOSES = (
    "tenant social scoring",
    "inferring refusal or vulnerability from silence or missing sensors",
    "consent manipulation",
    "staff performance or emotion assessment without approval",
    "changing, ranking, approving, signing or sending anything for a person",
)
APPROVAL_EVIDENCE = (
    "task owner personal validation of own authority",
    "Assurance delegate personal validation",
    "Safety delegate personal validation",
    "DPO and Legal delegate personal validation",
    "dated qualified UK and conditional EU intended-use, actor-role, influence and currentness review",
)
# Recorded separately; none is granted by constructed fixtures or role-agent output.
AUTHORITY_STATES = ("owner_report_acceptance", "prd_acceptance", "task_control_acceptance", "operational_release")

LEGACY = {
    "briefing": dict(route="fast", purpose="Draft a morning briefing for a housing officer", roles=("Retrofit Coordinator", "Resident Liaison Officer"),
                     categories=("stage", "waiting", "safety"), influence="Draft text a person reads; no ranking input",
                     affected=("staff", "residents"), reviewer="Retrofit Programme Manager"),
    "message": dict(route="fast", purpose="Draft a resident visit or update message", roles=("Retrofit Coordinator", "Resident Liaison Officer"),
                    categories=("stage", "preferences", "adjustments"), influence="Draft text; a person edits and sends outside the product",
                    affected=("residents", "staff"), reviewer="Retrofit Programme Manager"),
    "summary": dict(route="fast", purpose="Catch-me-up summary for a colleague taking over a case", roles=("Retrofit Coordinator", "Resident Liaison Officer"),
                    categories=("stage", "history", "contacts"), influence="Reading aid; cited bullets only",
                    affected=("staff", "residents"), reviewer="Retrofit Programme Manager"),
    "priority": dict(route="strong", purpose="Explain a suggested order of work for a person to accept or reject", roles=("Retrofit Coordinator", "Retrofit Programme Manager"),
                     categories=("stage", "safety", "ranking"), influence="Advisory; ranking and queue membership unchanged",
                     affected=("residents", "staff"), reviewer="Retrofit Programme Manager"),
    "funding_draft": dict(route="strong", purpose="Draft funding application wording", roles=("Grants and Evidence Officer", "Retrofit Programme Manager"),
                          categories=("measures", "funding"), influence="Draft wording; no submission or eligibility decision",
                          affected=("residents", "funders"), reviewer="Grants and Evidence Officer"),
    "read_document": dict(route="strong", purpose="Describe an uploaded document", roles=("Retrofit Coordinator", "Grants and Evidence Officer", "Quality Inspector"),
                          categories=("documents",), influence="Filing note; no extraction into the case",
                          affected=("staff", "providers"), reviewer="Retrofit Programme Manager"),
}


LEGACY_SCHEMA = "legacy-text-v1"
LEGACY_PROMPT = "legacy-prompts-2026-10-15"
LEGACY_POLICY = "legacy-forbidden-output-filter-v1"
LEGACY_PROVENANCE = "constructed-synthetic-demo-labelled"


def legacy_deployment(task, ai):
    """Current registered route, independent of a retained output's historical alias."""
    return getattr(ai, LEGACY[task]["route"])


def legacy_binding(task, ai, deployment):
    """What a retained legacy task would dispatch with; a release must match every field, including the deployment actually called."""
    spec = LEGACY[task]
    policy = f"{LEGACY_POLICY}:{ranking.policy_hash(ranking.CURRENT)}" if task == "priority" else LEGACY_POLICY
    return dict(registry_version=REGISTRY_VERSION, schema_version=LEGACY_SCHEMA, provider=PROVIDER,
                endpoint=getattr(ai, "endpoint", "") or "", deployment=deployment or "",
                prompt_version=ai_prompts.version(task), policy_version=policy,
                data_version=digest([LEGACY_SCHEMA, spec["categories"]])[:16], provenance_version=LEGACY_PROVENANCE,
                permission_version=digest([spec["roles"], spec["affected"]])[:16],
                model_version=(getattr(ai, "model_version_strong", getattr(ai, "model_version", "unattested"))
                               if deployment == getattr(ai, "strong", None) else getattr(ai, "model_version", "unattested")),
                task_contract_version=digest(get(task)), evaluation_version=rai_release.EVALUATION_VERSION)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _entry(task_id, kind, version, purpose, roles, categories, influence, affected, reviewer):
    return dict(
        id=task_id, kind=kind, version=version, purpose=purpose,
        scope="constructed synthetic exercise only; no live resident, safety or financial processing",
        permitted_capability="draft or propose text for a person to review; no write, send, approve or rank",
        intended_use=purpose, prohibited_uses=list(PROHIBITED_PURPOSES), influence=influence,
        affected=list(affected), roles=list(roles), source_permissions=list(categories),
        accountable_function=reviewer, accountable_individual=UNKNOWN, delegation=UNKNOWN,
        approval_state=UNAPPROVED, activation="denied for live use; constructed offline scaffolding permitted",
        impact_record=dict(status="not assessed", residual_risk=UNKNOWN,
                           note="Impact and residual-risk record is an open owner and qualified-reviewer item."),
        required_approval_evidence=list(APPROVAL_EVIDENCE),
        authority={k: UNKNOWN for k in AUTHORITY_STATES},
        reliance_review="dated qualified UK and conditional EU review required before affected operational reliance; "
                        "housing or hosting location alone does not decide applicability",
        manual_route="Use the ordinary case controls and the named function; no model call.",
    )


def tasks():
    out = {}
    for k, v in ASSISTANTS.items():
        out[k] = _entry(k, "assistant", ASSISTANT_VERSION, v["purpose"], v["roles"], v["categories"],
                        "Proposal only; a person verifies and accepts", ("residents", "staff", "providers"), v["roles"][-1])
    for k, v in LEGACY.items():
        out[k] = _entry(k, "retained-path", REGISTRY_VERSION, v["purpose"], v["roles"], v["categories"], v["influence"],
                        v["affected"], v["reviewer"])
    out[CHAT_TASK] = chat_entry()
    return out


def chat_entry():
    """Case conversation task: registered but disabled; thresholds are proposals, never approved here."""
    e = _entry(CHAT_TASK, "chat", REGISTRY_VERSION, "Answer questions about a case with cited sources; refuse approve, decide, consent, diagnose and resident-contact asks",
               ("Retrofit Coordinator", "Retrofit Programme Manager"), ("home", "survey", "measures", "stage"),
               "Cited reading aid; no write, approval or decision", ("staff", "residents"), "Retrofit Programme Manager")
    e.update(enabled=False, state="disabled",
             activation="disabled; enabling needs approved thresholds, a named accountable individual and the evidence in required_enablement_evidence",
             thresholds=dict(status="proposed", approved_by=None, approved_on=None,
                             proposed=dict(critical_failures=0, open_critical_gaps=0,
                                           memory_poisoning_pass_rate=1.0, prompt_injection_pass_rate=1.0,
                                           permission_pass_rate=1.0, out_of_scope_refusal_rate=1.0)),
             required_enablement_evidence=["approved thresholds", "accountable individual", "independently labelled held-out set",
                                           "actual-model evaluation within a finite authorisation", "authorised human exercises"],
             manual_route="Use the ordinary case controls and the named function; the panel answers nothing without a model.")
    return e


def registry():
    t = tasks()
    return dict(version=REGISTRY_VERSION, tasks=list(t.values()), registry_hash=digest(t),
                note="Constructed offline scaffolding. Unknown individuals or delegations cannot authorize activation.")


def get(task_id):
    return tasks().get(task_id)


def authorizes_live(task_id):
    """Always false until every authority is a recorded, personally validated person: none is."""
    t = get(task_id)
    return bool(t) and t["accountable_individual"] != UNKNOWN and t["delegation"] != UNKNOWN and \
        t["approval_state"] != UNAPPROVED and all(v != UNKNOWN for v in t["authority"].values())


def envelope(task_id, case_ids, source_versions, result, case_version=None):
    """Unapproved proposal envelope: task, case and source versions plus provider, deployment and model."""
    t = get(task_id)
    source = result.get("source")
    abstained = source != "ai"
    return dict(
        task=task_id, task_version=t["version"] if t else None, registered=bool(t),
        registry_version=REGISTRY_VERSION, prompt_version=result.get("prompt_version"),
        case_ids=list(case_ids), case_version=case_version, source_versions=dict(source_versions),
        provider=PROVIDER if source == "ai" else None,
        deployment=result.get("model") if source == "ai" else None,
        model=result.get("model") if source == "ai" else None,
        outcome="abstained-or-failed" if abstained else "proposed",
        failure=result.get("reason") if abstained else None,
        approval="Not reviewed", approved=False, reviewer_function=t["accountable_function"] if t else None,
        release=result.get("release"),
        usage=result.get("usage"), meter_id=result.get("meter_id"),
        meter_root=result.get("meter_root"), configuration=result.get("configuration"),
        prompt_hash=result.get("prompt_hash"),
    )
