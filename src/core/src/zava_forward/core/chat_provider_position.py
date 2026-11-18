"""Model provider data-handling and region position contract (ADR 0004, GitHub #163).

Records and enforces Zava Forward's technical posture for Azure OpenAI / Microsoft
Foundry chat and memory inference without claiming legal or DPO approval:

* Residency posture: primary domestic deployment in ``uksouth`` with regional
  ``Standard`` processing; bounded EU data-zone posture across allowlisted EEA
  regions (``Standard`` or ``DataZoneStandard``) gated on recorded cross-border
  transfer sign-off; ``GlobalStandard`` and non-UK/non-EU regions fail closed.
* Zero model training: customer prompts, completions and opt-in memory are never
  permitted for foundation-model training or improvement; any enabled or unknown
  training flag fails closed.
* Content-filtering and abuse-monitoring disclosure: distinguishes stateless
  synchronous Azure AI Content Safety harm filtering from platform-default
  30-day flagged-sample storage and Microsoft human review unless modified abuse
  monitoring is recorded, keeping UK South reviewer residency marked unverified.
* Cross-border transfer prohibition: processing outside domestic ``uksouth``
  ``Standard`` fails closed unless ``CHAT_TRANSFER_REF`` holds a valid governance
  reference (and rejects synthetic/demo references in ``actual`` data mode).
* Pre-approval retention boundary: no retention period is active before DPO and
  Legal approval references and provider/region checks pass.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any, Final, TypedDict

from zava_forward.core.data_protection import actual_mode

DPO_LEGAL_APPROVED: Final[bool] = False
PROVIDER_DESCRIPTION = (
    "Azure OpenAI through the existing Foundry deployments (ADR 0001 to ADR 0003)"
)
REGION_DECISION = "uksouth (owner decision 2026-10-15)"
PRIMARY_REGION = "uksouth"
EU_DATA_ZONE_REGIONS: tuple[str, ...] = (
    "swedencentral",
    "westeurope",
    "northeurope",
    "francecentral",
    "germanywestcentral",
    "italynorth",
    "polandcentral",
    "spaincentral",
)
APPROVED_RESIDENCY_REGIONS: tuple[str, ...] = (PRIMARY_REGION, *EU_DATA_ZONE_REGIONS)
APPROVED_DEPLOYMENT_TYPES: tuple[str, ...] = ("Standard", "DataZoneStandard")

SYNTHETIC_REF_PREFIXES: tuple[str, ...] = ("synth-", "syn-", "synthetic-")
DEMO_REF_MARKERS: tuple[str, ...] = (
    "chat-demo-storage-approval-",
    "chat-demo-breakglass-disclaimer-",
    "chat-memory-dpia.md",
)
PLACEHOLDER_REF_TOKENS: frozenset[str] = frozenset(
    {
        "yes",
        "no",
        "true",
        "false",
        "1",
        "0",
        "ok",
        "approved",
        "none",
        "null",
        "n/a",
        "unknown",
        "tbd",
        "todo",
    }
)

_DEPLOYMENT_TYPE_MAP: dict[str, str] = {
    "standard": "Standard",
    "datazonestandard": "DataZoneStandard",
}
_DISABLED_TRAINING_VALUES: frozenset[str] = frozenset(
    {"", "false", "0", "no", "off", "disabled", "none"}
)
_FALSE_BOOL_VALUES: frozenset[str] = frozenset({"", "false", "0", "no", "off"})
_TRUE_BOOL_VALUES: frozenset[str] = frozenset({"true", "1", "yes", "on"})

HUMAN_GATE_STATEMENT = (
    "DPO and Legal sign-off is not recorded; environment reference pointers enforce "
    "runtime gates only and never establish legal acceptance."
)


class DocumentedVendorTerms(TypedDict):
    source: str
    source_date: str
    retrieved: str
    status: str
    dpo_accepted: bool
    summary: str


class ContentFilteringDisclosure(TypedDict):
    service: str
    mode: str
    stores_prompts: bool
    trains_models: bool
    summary: str


class AbuseMonitoringDisclosure(TypedDict):
    mode: str
    modified_abuse_monitoring_recorded: bool
    modified_abuse_monitoring_verified: bool
    default_sample_retention_days: int
    human_review_possible: bool
    eea_reviewer_residency_documented: bool
    uk_reviewer_residency_verified: bool
    summary: str


class CrossBorderTransferPolicy(TypedDict):
    prohibited_without_dpo_legal_signoff: bool
    transfer_ref_env: str
    primary_domestic_region: str
    eu_data_zone_requires_transfer_signoff: bool
    global_deployments_permitted: bool
    summary: str


class RetentionApprovalPolicy(TypedDict):
    active_before_dpo_legal_approval: bool
    required_approval_refs: tuple[str, str, str]
    retention_ref_env: str
    retention_days_env: str
    summary: str


class ProviderPositionEvaluation(TypedDict):
    valid: bool
    provider: str
    region: str
    residency_zone: str
    deployment_type: str
    deployment_attested: bool
    primary_region: str
    eu_data_zone_regions: list[str]
    approved_deployment_types: list[str]
    zava_stores_prompts: bool
    foundry_agent_memory: bool
    zero_model_training: bool
    customer_data_training: bool
    content_filtering: ContentFilteringDisclosure
    abuse_monitoring: AbuseMonitoringDisclosure
    cross_border_transfer: bool
    transfer_signoff_required: bool
    transfer_ref_recorded: bool
    cross_border_transfer_policy: CrossBorderTransferPolicy
    retention_policy: RetentionApprovalPolicy
    actual_data_mode: bool
    dpo_legal_approved: bool
    human_gate: str
    documented_terms: DocumentedVendorTerms
    violations: list[str]


DOCUMENTED_VENDOR_TERMS: DocumentedVendorTerms = {
    "source": "https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy",
    "source_date": "2026-06-05",
    "retrieved": "2026-11-01",
    "status": "vendor_documentation_not_dpo_accepted",
    "dpo_accepted": False,
    "summary": (
        "Prompts and completions are not shared with other customers or used to train or "
        "improve models without permission; models are stateless; standard processing stays "
        "in the resource geography, Global and DataZone deployments may process elsewhere; "
        "abuse monitoring may store and human-review flagged samples unless modified "
        "monitoring is approved; processing is governed by the Microsoft Data Protection "
        "Addendum."
    ),
}

CONTENT_FILTERING_DISCLOSURE: ContentFilteringDisclosure = {
    "service": "Azure AI Content Safety",
    "mode": "synchronous_stateless_harm_filtering",
    "stores_prompts": False,
    "trains_models": False,
    "summary": (
        "Prompts and completions pass through synchronous Azure AI Content Safety classifiers "
        "in transit without persisting customer content or training models."
    ),
}

ABUSE_MONITORING_DISCLOSURE: AbuseMonitoringDisclosure = {
    "mode": "platform_default_unverified",
    "modified_abuse_monitoring_recorded": False,
    "modified_abuse_monitoring_verified": False,
    "default_sample_retention_days": 30,
    "human_review_possible": True,
    "eea_reviewer_residency_documented": True,
    "uk_reviewer_residency_verified": False,
    "summary": (
        "Unless Microsoft approves modified abuse monitoring (ContentLogging disabled) and "
        "DPO and Legal verify that subscription state alongside "
        "CHAT_ABUSE_MONITORING_MODIFIED_REF, flagged prompts and completions may be stored "
        "encrypted in the resource geography for up to 30 days and reviewed by authorised "
        "Microsoft personnel; vendor documentation guarantees EEA reviewer location for EEA "
        "resources only, leaving uksouth reviewer location unverified."
    ),
}

CROSS_BORDER_TRANSFER_POLICY: CrossBorderTransferPolicy = {
    "prohibited_without_dpo_legal_signoff": True,
    "transfer_ref_env": "CHAT_TRANSFER_REF",
    "primary_domestic_region": PRIMARY_REGION,
    "eu_data_zone_requires_transfer_signoff": True,
    "global_deployments_permitted": False,
    "summary": (
        "Inference outside domestic uksouth Standard (including EU data-zone regions or "
        "DataZoneStandard) is prohibited unless DPO and Legal transfer sign-off is recorded "
        "in CHAT_TRANSFER_REF; GlobalStandard and non-UK/non-EU regions are always rejected."
    ),
}

RETENTION_APPROVAL_POLICY: RetentionApprovalPolicy = {
    "active_before_dpo_legal_approval": False,
    "required_approval_refs": ("CHAT_DPIA_REF", "CHAT_LAWFUL_BASIS_REF", "CHAT_NOTICE_REF"),
    "retention_ref_env": "CHAT_RETENTION_REF",
    "retention_days_env": "CHAT_RETENTION_DAYS",
    "summary": (
        "No chat or memory retention period is active before DPIA, lawful-basis, staff-notice "
        "and provider/region checks pass alongside CHAT_RETENTION_REF and CHAT_RETENTION_DAYS."
    ),
}

OPEN_ITEMS: tuple[str, str] = (
    "DPO and Legal must accept or reject the documented terms and confirm the deployment type "
    "(Standard, DataZone or Global) and whether modified abuse monitoring is approved; not "
    "verified against the deployment.",
    "International transfer position, if any, stays Unknown until the DPO records it.",
)

MODEL_PROVIDER_CONTRACT: dict[str, Any] = {
    "provider": PROVIDER_DESCRIPTION,
    "region": REGION_DECISION,
    "primary_region": PRIMARY_REGION,
    "eu_data_zone_regions": EU_DATA_ZONE_REGIONS,
    "approved_residency_regions": APPROVED_RESIDENCY_REGIONS,
    "approved_deployment_types": APPROVED_DEPLOYMENT_TYPES,
    "deployment_attested": False,
    "zava_stores_prompts": False,
    "foundry_agent_memory": False,
    "zero_model_training": True,
    "customer_data_training": False,
    "content_filtering": dict(CONTENT_FILTERING_DISCLOSURE),
    "abuse_monitoring": dict(ABUSE_MONITORING_DISCLOSURE),
    "cross_border_transfer_policy": dict(CROSS_BORDER_TRANSFER_POLICY),
    "retention_policy": dict(RETENTION_APPROVAL_POLICY),
    "dpo_legal_approved": DPO_LEGAL_APPROVED,
    "human_gate": HUMAN_GATE_STATEMENT,
    "documented_terms": dict(DOCUMENTED_VENDOR_TERMS),
    "open_items": OPEN_ITEMS,
}


class ProviderPositionError(ValueError):
    """Raised when model provider residency, training, or transfer posture fails closed."""

    def __init__(self, message: str, *, violations: list[str]) -> None:
        super().__init__(message)
        self.violations = list(violations)


def is_demo_or_synthetic_ref(value: str) -> bool:
    """True when a governance reference uses synthetic test prefixes or demo/draft documents."""
    low = str(value or "").strip().lower()
    if not low:
        return False
    if low.startswith(SYNTHETIC_REF_PREFIXES):
        return True
    return any(marker in low for marker in DEMO_REF_MARKERS)


def is_valid_governance_ref(value: str, *, actual: bool = False) -> bool:
    """Validate a governance reference; reject placeholders and actual-mode demo refs."""
    cleaned = str(value or "").strip()
    if not cleaned:
        return False
    if cleaned.lower() in PLACEHOLDER_REF_TOKENS:
        return False
    return not (actual and is_demo_or_synthetic_ref(cleaned))


def evaluate_provider_position(
    env: Mapping[str, str] | None = None,
    *,
    region: str | None = None,
    deployment_type: str | None = None,
    customer_data_training: bool | str | None = None,
    cross_border_transfer: bool | str | None = None,
    transfer_ref: str | None = None,
    abuse_monitoring_modified_ref: str | None = None,
) -> ProviderPositionEvaluation:
    """Evaluate residency, zero-training, disclosure and transfer gates without echoing values."""
    source_env: Mapping[str, str] = os.environ if env is None else env
    is_actual = actual_mode(source_env)
    violations: list[str] = []

    region_explicit = region is not None or "CHAT_PROVIDER_REGION" in source_env
    if region is not None:
        raw_region = str(region).strip().lower()
    elif "CHAT_PROVIDER_REGION" in source_env:
        raw_region = str(source_env.get("CHAT_PROVIDER_REGION") or "").strip().lower()
    elif is_actual:
        raw_region = ""
    else:
        raw_region = PRIMARY_REGION

    if not region_explicit and is_actual:
        residency_zone = "unapproved"
        safe_region = "unapproved"
        violations.append("unattested_region_in_actual_mode")
    elif raw_region == PRIMARY_REGION:
        residency_zone = "uk_south"
        safe_region = PRIMARY_REGION
    elif raw_region in EU_DATA_ZONE_REGIONS:
        residency_zone = "eu_data_zone"
        safe_region = raw_region
    else:
        residency_zone = "unapproved"
        safe_region = "unapproved"
        violations.append("unapproved_region")

    deployment_explicit = deployment_type is not None or "CHAT_DEPLOYMENT_TYPE" in source_env
    if deployment_type is not None:
        raw_deployment = str(deployment_type).strip()
    elif "CHAT_DEPLOYMENT_TYPE" in source_env:
        raw_deployment = str(source_env.get("CHAT_DEPLOYMENT_TYPE") or "").strip()
    elif is_actual:
        raw_deployment = ""
    else:
        raw_deployment = "Standard"

    canonical_deployment = (
        None
        if (not deployment_explicit and is_actual)
        else _DEPLOYMENT_TYPE_MAP.get(raw_deployment.lower())
    )
    if not deployment_explicit and is_actual:
        safe_deployment = "unapproved"
        violations.append("unattested_deployment_in_actual_mode")
    elif canonical_deployment is None:
        safe_deployment = "unapproved"
        violations.append("unapproved_deployment_residency")
    elif canonical_deployment == "DataZoneStandard" and residency_zone != "eu_data_zone":
        safe_deployment = canonical_deployment
        violations.append("unapproved_deployment_residency")
    else:
        safe_deployment = canonical_deployment

    if customer_data_training is not None:
        if isinstance(customer_data_training, bool):
            training_violation = customer_data_training
        else:
            training_violation = (
                str(customer_data_training).strip().lower() not in _DISABLED_TRAINING_VALUES
            )
    else:
        raw_training = str(source_env.get("CHAT_PROVIDER_TRAINING") or "").strip().lower()
        training_violation = raw_training not in _DISABLED_TRAINING_VALUES

    if training_violation:
        violations.append("provider_training_prohibited")

    if cross_border_transfer is not None:
        if isinstance(cross_border_transfer, bool):
            explicit_transfer = cross_border_transfer
        else:
            raw_cb = str(cross_border_transfer).strip().lower()
            if raw_cb in _FALSE_BOOL_VALUES:
                explicit_transfer = False
            elif raw_cb in _TRUE_BOOL_VALUES:
                explicit_transfer = True
            else:
                explicit_transfer = True
                violations.append("invalid_cross_border_flag")
    else:
        raw_cb = str(source_env.get("CHAT_CROSS_BORDER_TRANSFER") or "").strip().lower()
        if raw_cb in _FALSE_BOOL_VALUES:
            explicit_transfer = False
        elif raw_cb in _TRUE_BOOL_VALUES:
            explicit_transfer = True
        else:
            explicit_transfer = True
            violations.append("invalid_cross_border_flag")

    requires_transfer_signoff = (
        residency_zone == "eu_data_zone"
        or (region_explicit and raw_region != PRIMARY_REGION)
        or canonical_deployment == "DataZoneStandard"
        or explicit_transfer
    )

    raw_transfer_ref = str(
        transfer_ref if transfer_ref is not None else (source_env.get("CHAT_TRANSFER_REF") or "")
    ).strip()
    transfer_ref_structural = is_valid_governance_ref(raw_transfer_ref, actual=False)
    transfer_ref_valid = is_valid_governance_ref(raw_transfer_ref, actual=is_actual)

    if requires_transfer_signoff:
        if not transfer_ref_structural:
            violations.append("cross_border_transfer_unapproved")
        elif not transfer_ref_valid:
            violations.append("synthetic_or_demo_transfer_ref_in_actual_mode")

    if is_actual and not DPO_LEGAL_APPROVED:
        violations.append("actual_mode_dpo_legal_unapproved")

    raw_abuse_ref = str(
        abuse_monitoring_modified_ref
        if abuse_monitoring_modified_ref is not None
        else (source_env.get("CHAT_ABUSE_MONITORING_MODIFIED_REF") or "")
    ).strip()
    modified_abuse_ok = False
    if raw_abuse_ref:
        if not is_valid_governance_ref(raw_abuse_ref, actual=False):
            violations.append("invalid_abuse_monitoring_ref")
        elif not is_valid_governance_ref(raw_abuse_ref, actual=is_actual):
            violations.append("synthetic_or_demo_abuse_monitoring_ref_in_actual_mode")
        else:
            modified_abuse_ok = True

    abuse_disclosure: AbuseMonitoringDisclosure = {
        "mode": (
            "modified_recorded_unverified" if modified_abuse_ok else "platform_default_unverified"
        ),
        "modified_abuse_monitoring_recorded": modified_abuse_ok,
        "modified_abuse_monitoring_verified": False,
        "default_sample_retention_days": 30,
        "human_review_possible": True,
        "eea_reviewer_residency_documented": True,
        "uk_reviewer_residency_verified": False,
        "summary": ABUSE_MONITORING_DISCLOSURE["summary"],
    }

    deployment_attested = bool(
        region_explicit
        and deployment_explicit
        and residency_zone != "unapproved"
        and safe_deployment != "unapproved"
        and "unapproved_deployment_residency" not in violations
    )

    return {
        "valid": not violations,
        "provider": PROVIDER_DESCRIPTION,
        "region": safe_region,
        "residency_zone": residency_zone,
        "deployment_type": safe_deployment,
        "deployment_attested": deployment_attested,
        "primary_region": PRIMARY_REGION,
        "eu_data_zone_regions": list(EU_DATA_ZONE_REGIONS),
        "approved_deployment_types": list(APPROVED_DEPLOYMENT_TYPES),
        "zava_stores_prompts": False,
        "foundry_agent_memory": False,
        "zero_model_training": not training_violation,
        "customer_data_training": training_violation,
        "content_filtering": dict(CONTENT_FILTERING_DISCLOSURE),  # type: ignore[typeddict-item]
        "abuse_monitoring": abuse_disclosure,
        "cross_border_transfer": requires_transfer_signoff,
        "transfer_signoff_required": requires_transfer_signoff,
        "transfer_ref_recorded": bool(transfer_ref_valid and (not is_actual or DPO_LEGAL_APPROVED)),
        "cross_border_transfer_policy": dict(CROSS_BORDER_TRANSFER_POLICY),  # type: ignore[typeddict-item]
        "retention_policy": dict(RETENTION_APPROVAL_POLICY),  # type: ignore[typeddict-item]
        "actual_data_mode": is_actual,
        "dpo_legal_approved": DPO_LEGAL_APPROVED,
        "human_gate": HUMAN_GATE_STATEMENT,
        "documented_terms": dict(DOCUMENTED_VENDOR_TERMS),  # type: ignore[typeddict-item]
        "violations": violations,
    }


def require_provider_position(
    env: Mapping[str, str] | None = None,
    *,
    region: str | None = None,
    deployment_type: str | None = None,
    customer_data_training: bool | str | None = None,
    cross_border_transfer: bool | str | None = None,
    transfer_ref: str | None = None,
    abuse_monitoring_modified_ref: str | None = None,
) -> ProviderPositionEvaluation:
    """Return the evaluated provider position or raise ProviderPositionError fail-closed."""
    evaluated = evaluate_provider_position(
        env,
        region=region,
        deployment_type=deployment_type,
        customer_data_training=customer_data_training,
        cross_border_transfer=cross_border_transfer,
        transfer_ref=transfer_ref,
        abuse_monitoring_modified_ref=abuse_monitoring_modified_ref,
    )
    if not evaluated["valid"]:
        joined = ", ".join(evaluated["violations"])
        raise ProviderPositionError(
            f"Model provider data-handling or region position is unapproved: {joined}",
            violations=evaluated["violations"],
        )
    return evaluated


__all__ = [
    "ABUSE_MONITORING_DISCLOSURE",
    "APPROVED_DEPLOYMENT_TYPES",
    "APPROVED_RESIDENCY_REGIONS",
    "CONTENT_FILTERING_DISCLOSURE",
    "CROSS_BORDER_TRANSFER_POLICY",
    "DEMO_REF_MARKERS",
    "DOCUMENTED_VENDOR_TERMS",
    "DPO_LEGAL_APPROVED",
    "EU_DATA_ZONE_REGIONS",
    "HUMAN_GATE_STATEMENT",
    "MODEL_PROVIDER_CONTRACT",
    "OPEN_ITEMS",
    "PLACEHOLDER_REF_TOKENS",
    "PRIMARY_REGION",
    "PROVIDER_DESCRIPTION",
    "ProviderPositionError",
    "ProviderPositionEvaluation",
    "REGION_DECISION",
    "RETENTION_APPROVAL_POLICY",
    "SYNTHETIC_REF_PREFIXES",
    "evaluate_provider_position",
    "is_demo_or_synthetic_ref",
    "is_valid_governance_ref",
    "require_provider_position",
]
