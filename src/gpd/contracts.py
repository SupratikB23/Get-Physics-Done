"""GPD contracts -- shared data types for conventions, planning, and verification."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator

__all__ = [
    "ConventionLock",
    "VerificationEvidence",
    "ContractEvidenceStatus",
    "ContractEvidenceEntry",
    "ContractResultEntry",
    "ContractReferenceActionStatus",
    "ContractReferenceUsage",
    "ContractForbiddenProxyStatus",
    "ContractForbiddenProxyResult",
    "ContractResults",
    "SuggestedContractCheck",
    "ComparisonVerdict",
    "PROJECT_CONTRACT_MAPPING_LIST_FIELDS",
    "PROJECT_CONTRACT_TOP_LEVEL_LIST_FIELDS",
    "PROJECT_CONTRACT_COLLECTION_LIST_FIELDS",
    "ContractScope",
    "ContractContextIntake",
    "ContractApproachPolicy",
    "ContractObservable",
    "ContractClaim",
    "ContractDeliverable",
    "ContractAcceptanceTest",
    "ContractReference",
    "ContractForbiddenProxy",
    "ContractLink",
    "ContractUncertaintyMarkers",
    "ResearchContract",
    "collect_plan_contract_integrity_errors",
    "contract_has_explicit_context_intake",
    "ProjectContractParseResult",
    "parse_project_contract_data_strict",
    "parse_project_contract_data_salvage",
    "collect_contract_integrity_errors",
    "contract_from_data",
    "contract_from_data_salvage",
]

def _normalize_optional_str(value: object) -> object:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return value


def _normalize_non_empty_optional_str(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("must be a non-empty string")
        return stripped
    return value


def _normalize_required_str(value: object) -> object:
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("value must not be blank")
        return stripped
    return value


def _normalize_string_list(value: object) -> object:
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return [stripped]
    if not isinstance(value, list):
        return value
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str):
            normalized.append(item)
            continue
        stripped = item.strip()
        if not stripped or stripped in seen:
            continue
        seen.add(stripped)
        normalized.append(stripped)
    return normalized


PROJECT_CONTRACT_MAPPING_LIST_FIELDS: dict[str, tuple[str, ...]] = {
    "scope": ("in_scope", "out_of_scope", "unresolved_questions"),
    "context_intake": (
        "must_read_refs",
        "must_include_prior_outputs",
        "user_asserted_anchors",
        "known_good_baselines",
        "context_gaps",
        "crucial_inputs",
    ),
    "approach_policy": (
        "formulations",
        "allowed_estimator_families",
        "forbidden_estimator_families",
        "allowed_fit_families",
        "forbidden_fit_families",
        "stop_and_rethink_conditions",
    ),
    "uncertainty_markers": (
        "weakest_anchors",
        "unvalidated_assumptions",
        "competing_explanations",
        "disconfirming_observations",
    ),
}
PROJECT_CONTRACT_TOP_LEVEL_LIST_FIELDS: tuple[str, ...] = (
    "observables",
    "claims",
    "deliverables",
    "acceptance_tests",
    "references",
    "forbidden_proxies",
    "links",
)
PROJECT_CONTRACT_COLLECTION_LIST_FIELDS: dict[str, tuple[str, ...]] = {
    "claims": ("observables", "deliverables", "acceptance_tests", "references"),
    "deliverables": ("must_contain",),
    "acceptance_tests": ("evidence_required",),
    "references": ("aliases", "applies_to", "carry_forward_to", "required_actions"),
    "links": ("verified_by",),
}


def _collect_project_contract_list_member_errors(data: object) -> list[str]:
    """Reject blank or duplicate list members before model normalization."""

    if not isinstance(data, dict):
        return []

    errors: list[str] = []

    def _check_string_list(value: object, *, path: str) -> None:
        if not isinstance(value, list):
            return
        seen: set[str] = set()
        for index, item in enumerate(value):
            if not isinstance(item, str):
                continue
            stripped = item.strip()
            if not stripped:
                errors.append(f"{path}.{index} must not be blank")
                continue
            if stripped in seen:
                errors.append(f"{path}.{index} is a duplicate")
                continue
            seen.add(stripped)

    def _check_mapping_lists(mapping: object, *, path_prefix: str, field_names: tuple[str, ...]) -> None:
        if not isinstance(mapping, dict):
            return
        for field_name in field_names:
            if field_name in mapping:
                _check_string_list(mapping[field_name], path=f"{path_prefix}.{field_name}")

    def _check_collection_item_lists(collection_name: str, field_names: tuple[str, ...]) -> None:
        raw_collection = data.get(collection_name)
        if not isinstance(raw_collection, list):
            return
        for index, item in enumerate(raw_collection):
            if isinstance(item, dict):
                _check_mapping_lists(item, path_prefix=f"{collection_name}.{index}", field_names=field_names)

    for section_name, field_names in PROJECT_CONTRACT_MAPPING_LIST_FIELDS.items():
        _check_mapping_lists(data.get(section_name), path_prefix=section_name, field_names=field_names)
    for collection_name, field_names in PROJECT_CONTRACT_COLLECTION_LIST_FIELDS.items():
        _check_collection_item_lists(collection_name, field_names)

    return errors


class _StrictContractResultsInput(dict[str, object]):
    """Marker mapping for strict contract-results validation contexts."""


_STRICT_CONTRACT_RESULTS_STRING_LIST_FIELDS: dict[str, tuple[str, ...]] = {
    "claims": ("linked_ids",),
    "deliverables": ("linked_ids",),
    "acceptance_tests": ("linked_ids",),
    "references": ("completed_actions", "missing_actions"),
}


def _normalize_literal_choice(value: object, choices: tuple[str, ...]) -> object:
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return stripped
        for choice in choices:
            if stripped.casefold() == choice.casefold():
                return choice
        return stripped
    return value


def _normalize_literal_choice_list(value: object, choices: tuple[str, ...]) -> object:
    normalized = _normalize_string_list(value)
    if not isinstance(normalized, list):
        return normalized

    canonicalized: list[object] = []
    seen: set[str] = set()
    for item in normalized:
        if not isinstance(item, str):
            canonicalized.append(item)
            continue
        choice = _normalize_literal_choice(item, choices)
        if not isinstance(choice, str):
            canonicalized.append(choice)
            continue
        if choice in seen:
            continue
        seen.add(choice)
        canonicalized.append(choice)
    return canonicalized


def normalize_contract_results_input(value: object, *, strict: bool = True) -> object:
    """Preserve contract-results shape before strict ``ContractResults`` validation.

    Legacy permissive normalization is intentionally unsupported. All live
    contract-results entry points validate strict contract-backed ledgers, so
    this helper now rejects ``strict=False`` rather than silently reintroducing
    coercive compatibility behavior.
    """
    if not isinstance(value, dict):
        return value

    if strict is not True:
        raise ValueError("normalize_contract_results_input only supports strict=True")

    return _StrictContractResultsInput(dict(value))


def _collect_strict_contract_results_errors(value: _StrictContractResultsInput) -> list[str]:
    """Return strict contract-results shape errors before Pydantic defaults apply."""

    errors: list[str] = []

    for section_name in ("claims", "deliverables", "acceptance_tests", "references", "forbidden_proxies"):
        section = value.get(section_name)
        if not isinstance(section, dict):
            continue
        for entry_id, entry in section.items():
            if isinstance(entry, dict) and "status" not in entry:
                errors.append(
                    f"{section_name}.{entry_id}.status must be explicit in contract-backed contract_results"
                )

    for section_name, field_names in _STRICT_CONTRACT_RESULTS_STRING_LIST_FIELDS.items():
        section = value.get(section_name)
        if not isinstance(section, dict):
            continue
        for entry_id, entry in section.items():
            if not isinstance(entry, dict):
                continue
            for field_name in field_names:
                if isinstance(entry.get(field_name), str):
                    errors.append(f"{section_name}.{entry_id}.{field_name} must be a list, not str")

    markers = value.get("uncertainty_markers")
    if isinstance(markers, dict):
        for field_name in (
            "weakest_anchors",
            "unvalidated_assumptions",
            "competing_explanations",
            "disconfirming_observations",
        ):
            if isinstance(markers.get(field_name), str):
                errors.append(f"uncertainty_markers.{field_name} must be a list, not str")
        if not markers.get("weakest_anchors"):
            errors.append(
                "uncertainty_markers.weakest_anchors must be non-empty in contract-backed contract_results"
            )
        if not markers.get("disconfirming_observations"):
            errors.append(
                "uncertainty_markers.disconfirming_observations must be non-empty in contract-backed contract_results"
            )

    return errors


class ConventionLock(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    metric_signature: str | None = None
    fourier_convention: str | None = None
    natural_units: str | None = None
    gauge_choice: str | None = None
    regularization_scheme: str | None = None
    renormalization_scheme: str | None = None
    coordinate_system: str | None = None
    spin_basis: str | None = None
    state_normalization: str | None = None
    coupling_convention: str | None = None
    index_positioning: str | None = None
    time_ordering: str | None = None
    commutation_convention: str | None = None
    levi_civita_sign: str | None = None
    generator_normalization: str | None = None
    covariant_derivative_sign: str | None = None
    gamma_matrix_convention: str | None = None
    creation_annihilation_order: str | None = None
    custom_conventions: dict[str, str] = Field(default_factory=dict)


class VerificationEvidence(BaseModel):
    """Structured provenance for a verification event attached to a result."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    verified_at: str | None = None
    verifier: str | None = None
    method: str = "manual"
    confidence: Literal["high", "medium", "low", "unreliable"] = "medium"
    evidence_path: str | None = None
    trace_id: str | None = None
    commit_sha: str | None = None
    notes: str | None = None
    claim_id: str | None = None
    deliverable_id: str | None = None
    acceptance_test_id: str | None = None
    reference_id: str | None = None
    forbidden_proxy_id: str | None = None

    @field_validator(
        "claim_id",
        "deliverable_id",
        "acceptance_test_id",
        "reference_id",
        "forbidden_proxy_id",
        mode="before",
    )
    @classmethod
    def _normalize_optional_contract_id(cls, value: object) -> object:
        return _normalize_optional_str(value)

    @field_validator("confidence", mode="before")
    @classmethod
    def _normalize_confidence(cls, value: object) -> object:
        return _normalize_literal_choice(value, ("high", "medium", "low", "unreliable"))


ContractEvidenceStatus = Literal["passed", "partial", "failed", "blocked", "not_attempted"]
ContractReferenceAction = Literal["read", "use", "compare", "cite", "avoid"]


class ContractEvidenceEntry(BaseModel):
    """Structured evidence item tied back to contract IDs."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    summary: str | None = None
    evidence: list[VerificationEvidence] = Field(default_factory=list)
    notes: str | None = None


class ContractResultEntry(ContractEvidenceEntry):
    """Execution or verification outcome for a contract subject."""

    status: ContractEvidenceStatus = "not_attempted"
    linked_ids: list[str] = Field(default_factory=list)
    path: str | None = None

    @field_validator("linked_ids", mode="before")
    @classmethod
    def _normalize_linked_ids(cls, value: object) -> object:
        return _normalize_string_list(value)

    @field_validator("status", mode="before")
    @classmethod
    def _normalize_status(cls, value: object) -> object:
        return _normalize_literal_choice(value, ("passed", "partial", "failed", "blocked", "not_attempted"))


ContractReferenceActionStatus = Literal["completed", "missing", "not_applicable"]


class ContractReferenceUsage(BaseModel):
    """Status for required actions on a contract reference anchor."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    status: ContractReferenceActionStatus = "missing"
    completed_actions: list[ContractReferenceAction] = Field(default_factory=list)
    missing_actions: list[ContractReferenceAction] = Field(default_factory=list)
    summary: str | None = None
    evidence: list[VerificationEvidence] = Field(default_factory=list)

    @field_validator("completed_actions", "missing_actions", mode="before")
    @classmethod
    def _normalize_action_lists(cls, value: object) -> object:
        return _normalize_literal_choice_list(value, ("read", "use", "compare", "cite", "avoid"))

    @field_validator("status", mode="before")
    @classmethod
    def _normalize_status(cls, value: object) -> object:
        return _normalize_literal_choice(value, ("completed", "missing", "not_applicable"))

    @model_validator(mode="after")
    def _validate_action_status(self) -> ContractReferenceUsage:
        completed = set(self.completed_actions)
        missing = set(self.missing_actions)
        overlap = sorted(completed.intersection(missing))

        if overlap:
            raise ValueError(
                "completed_actions and missing_actions must not overlap: " + ", ".join(overlap)
            )
        if self.status == "completed":
            if not self.completed_actions:
                raise ValueError("status=completed requires completed_actions")
            if self.missing_actions:
                raise ValueError("status=completed requires missing_actions to be empty")
        elif self.status == "missing":
            if not self.missing_actions:
                raise ValueError("status=missing requires missing_actions")
        elif self.completed_actions or self.missing_actions:
            raise ValueError("status=not_applicable requires completed_actions and missing_actions to be empty")

        return self


ContractForbiddenProxyStatus = Literal["rejected", "violated", "unresolved", "not_applicable"]


class ContractForbiddenProxyResult(BaseModel):
    """Status for a forbidden-proxy guardrail."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    status: ContractForbiddenProxyStatus = "unresolved"
    notes: str | None = None
    evidence: list[VerificationEvidence] = Field(default_factory=list)

    @field_validator("status", mode="before")
    @classmethod
    def _normalize_status(cls, value: object) -> object:
        return _normalize_literal_choice(value, ("rejected", "violated", "unresolved", "not_applicable"))


class ContractResults(BaseModel):
    """Execution-facing outcome ledger keyed to canonical contract IDs."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    claims: dict[str, ContractResultEntry] = Field(default_factory=dict)
    deliverables: dict[str, ContractResultEntry] = Field(default_factory=dict)
    acceptance_tests: dict[str, ContractResultEntry] = Field(default_factory=dict)
    references: dict[str, ContractReferenceUsage] = Field(default_factory=dict)
    forbidden_proxies: dict[str, ContractForbiddenProxyResult] = Field(default_factory=dict)
    uncertainty_markers: ContractUncertaintyMarkers = Field(default_factory=lambda: ContractUncertaintyMarkers())

    @model_validator(mode="before")
    @classmethod
    def _validate_strict_contract_results(cls, value: object) -> object:
        if isinstance(value, _StrictContractResultsInput):
            errors = _collect_strict_contract_results_errors(value)
            if "uncertainty_markers" not in value:
                errors.append("uncertainty_markers must be explicit in contract-backed contract_results")
            if errors:
                raise ValueError("; ".join(errors))
        return value

    @field_validator(
        "claims",
        "deliverables",
        "acceptance_tests",
        "references",
        "forbidden_proxies",
        mode="before",
    )
    @classmethod
    def _normalize_mapping_sections(cls, value: object) -> object:
        return value


class SuggestedContractCheck(BaseModel):
    """Structured gap to add when the contract is missing decisive verification."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    check: str
    reason: str
    suggested_subject_kind: Literal["claim", "deliverable", "acceptance_test", "reference"] | None = None
    suggested_subject_id: str | None = None
    evidence_path: str | None = None

    @field_validator("check", "reason", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("suggested_subject_kind", mode="before")
    @classmethod
    def _normalize_optional_kind(cls, value: object) -> object:
        return _normalize_literal_choice(
            _normalize_optional_str(value),
            ("claim", "deliverable", "acceptance_test", "reference"),
        )

    @field_validator("suggested_subject_id", "evidence_path", mode="before")
    @classmethod
    def _normalize_optional_fields(cls, value: object) -> object:
        return _normalize_optional_str(value)


class ComparisonVerdict(BaseModel):
    """Machine-readable verdict for an internal or external comparison."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    subject_id: str
    subject_kind: Literal["claim", "deliverable", "acceptance_test", "reference"]
    subject_role: Literal["decisive", "supporting", "supplemental", "other"]
    reference_id: str | None = None
    comparison_kind: Literal["benchmark", "prior_work", "experiment", "cross_method", "baseline", "other"] = "other"
    metric: str | None = None
    threshold: str | None = None
    verdict: Literal["pass", "tension", "fail", "inconclusive"] = "inconclusive"
    recommended_action: str | None = None
    notes: str | None = None

    @field_validator("subject_id", mode="before")
    @classmethod
    def _normalize_subject_id(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("subject_kind", "subject_role", "comparison_kind", "verdict", mode="before")
    @classmethod
    def _normalize_required_literals(cls, value: object, info: ValidationInfo) -> object:
        normalized = _normalize_required_str(value)
        field_choices = {
            "subject_kind": ("claim", "deliverable", "acceptance_test", "reference"),
            "subject_role": ("decisive", "supporting", "supplemental", "other"),
            "comparison_kind": ("benchmark", "prior_work", "experiment", "cross_method", "baseline", "other"),
            "verdict": ("pass", "tension", "fail", "inconclusive"),
        }
        return _normalize_literal_choice(normalized, field_choices[info.field_name])

    @field_validator("reference_id", "metric", "threshold", "recommended_action", "notes", mode="before")
    @classmethod
    def _normalize_optional_fields(cls, value: object) -> object:
        return _normalize_optional_str(value)

    def anchored_reference_ids(self, known_reference_ids: set[str] | None = None) -> set[str]:
        """Return contract reference anchors named by this verdict.

        ``reference_id`` is the explicit anchor field. ``subject_kind: reference``
        also anchors the verdict directly to the referenced contract node.
        """

        anchors: set[str] = set()
        if self.reference_id is not None:
            anchors.add(self.reference_id)
        if self.subject_kind == "reference":
            anchors.add(self.subject_id)
        if known_reference_ids is None:
            return anchors
        return anchors.intersection(known_reference_ids)


class ContractScope(BaseModel):
    """High-level problem boundary for a project or phase."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    question: str
    in_scope: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)

    @field_validator("question", mode="before")
    @classmethod
    def _normalize_question(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("in_scope", "out_of_scope", "unresolved_questions", mode="before")
    @classmethod
    def _normalize_scope_lists(cls, value: object) -> object:
        return _normalize_string_list(value)


class ContractContextIntake(BaseModel):
    """Inputs the user says must stay visible during execution."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    must_read_refs: list[str] = Field(default_factory=list)
    must_include_prior_outputs: list[str] = Field(default_factory=list)
    user_asserted_anchors: list[str] = Field(default_factory=list)
    known_good_baselines: list[str] = Field(default_factory=list)
    context_gaps: list[str] = Field(default_factory=list)
    crucial_inputs: list[str] = Field(default_factory=list)

    @field_validator(
        "must_read_refs",
        "must_include_prior_outputs",
        "user_asserted_anchors",
        "known_good_baselines",
        "context_gaps",
        "crucial_inputs",
        mode="before",
    )
    @classmethod
    def _normalize_intake_lists(cls, value: object) -> object:
        return _normalize_string_list(value)


class ContractApproachPolicy(BaseModel):
    """Representation, estimator, and rethink guardrails that must survive downstream."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    formulations: list[str] = Field(default_factory=list)
    allowed_estimator_families: list[str] = Field(default_factory=list)
    forbidden_estimator_families: list[str] = Field(default_factory=list)
    allowed_fit_families: list[str] = Field(default_factory=list)
    forbidden_fit_families: list[str] = Field(default_factory=list)
    stop_and_rethink_conditions: list[str] = Field(default_factory=list)

    @field_validator(
        "formulations",
        "allowed_estimator_families",
        "forbidden_estimator_families",
        "allowed_fit_families",
        "forbidden_fit_families",
        "stop_and_rethink_conditions",
        mode="before",
    )
    @classmethod
    def _normalize_policy_lists(cls, value: object) -> object:
        return _normalize_string_list(value)


class ContractObservable(BaseModel):
    """A target quantity or behavior the work needs to establish."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    id: str
    name: str
    kind: Literal["scalar", "curve", "map", "classification", "proof_obligation", "other"] = "other"
    definition: str
    regime: str | None = None
    units: str | None = None

    @field_validator("id", "name", "definition", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("regime", "units", mode="before")
    @classmethod
    def _normalize_optional_fields(cls, value: object) -> object:
        return _normalize_non_empty_optional_str(value)

    @field_validator("kind", mode="before")
    @classmethod
    def _normalize_kind(cls, value: object) -> object:
        return _normalize_literal_choice(
            _normalize_required_str(value),
            ("scalar", "curve", "map", "classification", "proof_obligation", "other"),
        )


class ContractClaim(BaseModel):
    """A statement the phase must establish."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    id: str
    statement: str
    observables: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    acceptance_tests: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)

    @field_validator("id", "statement", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("observables", "deliverables", "acceptance_tests", "references", mode="before")
    @classmethod
    def _normalize_id_lists(cls, value: object) -> object:
        return _normalize_string_list(value)


class ContractDeliverable(BaseModel):
    """An artifact the phase must produce."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    id: str
    kind: Literal["figure", "table", "dataset", "data", "derivation", "code", "note", "report", "other"] = "other"
    path: str | None = None
    description: str
    must_contain: list[str] = Field(default_factory=list)

    @field_validator("id", "description", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("kind", mode="before")
    @classmethod
    def _normalize_kind(cls, value: object) -> object:
        return _normalize_literal_choice(
            _normalize_required_str(value),
            ("figure", "table", "dataset", "data", "derivation", "code", "note", "report", "other"),
        )

    @field_validator("path", mode="before")
    @classmethod
    def _normalize_optional_path(cls, value: object) -> object:
        return _normalize_optional_str(value)

    @field_validator("must_contain", mode="before")
    @classmethod
    def _normalize_must_contain(cls, value: object) -> object:
        return _normalize_string_list(value)


class ContractAcceptanceTest(BaseModel):
    """A concrete check proving whether a claim or deliverable succeeded."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    id: str
    subject: str
    kind: Literal[
        "existence",
        "schema",
        "benchmark",
        "consistency",
        "cross_method",
        "limiting_case",
        "symmetry",
        "dimensional_analysis",
        "convergence",
        "oracle",
        "proxy",
        "reproducibility",
        "human_review",
        "other",
    ] = "other"
    procedure: str
    pass_condition: str
    evidence_required: list[str] = Field(default_factory=list)
    automation: Literal["automated", "hybrid", "human"] = "hybrid"

    @field_validator("id", "subject", "procedure", "pass_condition", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("kind", mode="before")
    @classmethod
    def _normalize_kind(cls, value: object) -> object:
        return _normalize_literal_choice(
            _normalize_required_str(value),
            (
                "existence",
                "schema",
                "benchmark",
                "consistency",
                "cross_method",
                "limiting_case",
                "symmetry",
                "dimensional_analysis",
                "convergence",
                "oracle",
                "proxy",
                "reproducibility",
                "human_review",
                "other",
            ),
        )

    @field_validator("automation", mode="before")
    @classmethod
    def _normalize_automation(cls, value: object) -> object:
        return _normalize_literal_choice(_normalize_required_str(value), ("automated", "hybrid", "human"))

    @field_validator("evidence_required", mode="before")
    @classmethod
    def _normalize_evidence_required(cls, value: object) -> object:
        return _normalize_string_list(value)


class ContractReference(BaseModel):
    """A literature, dataset, or artifact anchor the workflow must respect."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    id: str
    kind: Literal["paper", "dataset", "prior_artifact", "spec", "user_anchor", "other"] = "other"
    locator: str
    aliases: list[str] = Field(default_factory=list)
    role: Literal["definition", "benchmark", "method", "must_consider", "background", "other"] = "other"
    why_it_matters: str
    applies_to: list[str] = Field(default_factory=list)
    carry_forward_to: list[str] = Field(default_factory=list)
    must_surface: bool = False
    required_actions: list[ContractReferenceAction] = Field(default_factory=list)

    @field_validator("id", "locator", "why_it_matters", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("kind", "role", mode="before")
    @classmethod
    def _normalize_literal_fields(cls, value: object, info: ValidationInfo) -> object:
        normalized = _normalize_required_str(value)
        if info.field_name == "kind":
            return _normalize_literal_choice(
                normalized,
                ("paper", "dataset", "prior_artifact", "spec", "user_anchor", "other"),
            )
        return _normalize_literal_choice(
            normalized,
            ("definition", "benchmark", "method", "must_consider", "background", "other"),
        )

    @field_validator("aliases", "applies_to", "carry_forward_to", mode="before")
    @classmethod
    def _normalize_reference_lists(cls, value: object) -> object:
        return _normalize_string_list(value)

    @field_validator("required_actions", mode="before")
    @classmethod
    def _normalize_required_actions(cls, value: object) -> object:
        return _normalize_literal_choice_list(value, ("read", "use", "compare", "cite", "avoid"))


class ContractForbiddenProxy(BaseModel):
    """A proxy or shortcut that should not be accepted as success."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    id: str
    subject: str
    proxy: str
    reason: str

    @field_validator("id", "subject", "proxy", "reason", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)


class ContractLink(BaseModel):
    """A machine-readable dependency from one contract node to another."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    id: str
    source: str
    target: str
    relation: Literal["supports", "computes", "visualizes", "benchmarks", "depends_on", "evaluated_by", "other"] = "other"
    verified_by: list[str] = Field(default_factory=list)

    @field_validator("id", "source", "target", mode="before")
    @classmethod
    def _normalize_required_fields(cls, value: object) -> object:
        return _normalize_required_str(value)

    @field_validator("relation", mode="before")
    @classmethod
    def _normalize_relation(cls, value: object) -> object:
        return _normalize_literal_choice(
            _normalize_required_str(value),
            ("supports", "computes", "visualizes", "benchmarks", "depends_on", "evaluated_by", "other"),
        )

    @field_validator("verified_by", mode="before")
    @classmethod
    def _normalize_verified_by(cls, value: object) -> object:
        return _normalize_string_list(value)


class ContractUncertaintyMarkers(BaseModel):
    """Structured skepticism markers carried alongside the contract."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    weakest_anchors: list[str] = Field(default_factory=list)
    unvalidated_assumptions: list[str] = Field(default_factory=list)
    competing_explanations: list[str] = Field(default_factory=list)
    disconfirming_observations: list[str] = Field(default_factory=list)

    @field_validator(
        "weakest_anchors",
        "unvalidated_assumptions",
        "competing_explanations",
        "disconfirming_observations",
        mode="before",
    )
    @classmethod
    def _normalize_uncertainty_lists(cls, value: object) -> object:
        return _normalize_string_list(value)


class ResearchContract(BaseModel):
    """Canonical contract shared across planning, execution, and verification."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    schema_version: Literal[1] = 1
    scope: ContractScope
    context_intake: ContractContextIntake = Field(default_factory=ContractContextIntake)
    approach_policy: ContractApproachPolicy = Field(default_factory=ContractApproachPolicy)
    observables: list[ContractObservable] = Field(default_factory=list)
    claims: list[ContractClaim] = Field(default_factory=list)
    deliverables: list[ContractDeliverable] = Field(default_factory=list)
    acceptance_tests: list[ContractAcceptanceTest] = Field(default_factory=list)
    references: list[ContractReference] = Field(default_factory=list)
    forbidden_proxies: list[ContractForbiddenProxy] = Field(default_factory=list)
    links: list[ContractLink] = Field(default_factory=list)
    uncertainty_markers: ContractUncertaintyMarkers = Field(default_factory=lambda: ContractUncertaintyMarkers())


_CONTRACT_ID_GROUPS: tuple[tuple[str, str], ...] = (
    ("observable", "observables"),
    ("claim", "claims"),
    ("deliverable", "deliverables"),
    ("acceptance test", "acceptance_tests"),
    ("reference", "references"),
    ("forbidden proxy", "forbidden_proxies"),
    ("link", "links"),
)
_AMBIGUOUS_TARGET_ID_KINDS: tuple[str, ...] = ("claim", "deliverable", "acceptance test", "reference")


def _contract_ids_by_kind(contract: ResearchContract) -> dict[str, set[str]]:
    return {
        kind: {item.id for item in getattr(contract, field_name)}
        for kind, field_name in _CONTRACT_ID_GROUPS
    }


def collect_contract_integrity_errors(contract: ResearchContract) -> list[str]:
    """Return semantic integrity errors that require a cross-contract view."""

    ids_by_kind = _contract_ids_by_kind(contract)
    owners_by_id: dict[str, list[str]] = defaultdict(list)
    errors: list[str] = []

    for kind, field_name in _CONTRACT_ID_GROUPS:
        counts: dict[str, int] = defaultdict(int)
        for item in getattr(contract, field_name):
            counts[item.id] += 1
        for item_id, count in sorted(counts.items()):
            if count > 1:
                errors.append(f"duplicate {kind} id {item_id}")

    for kind in _AMBIGUOUS_TARGET_ID_KINDS:
        for item_id in ids_by_kind[kind]:
            owners_by_id[item_id].append(kind)

    for item_id, owner_kinds in sorted(owners_by_id.items()):
        unique_kinds = tuple(dict.fromkeys(owner_kinds))
        if len(unique_kinds) < 2:
            continue
        kinds_text = ", ".join(unique_kinds)
        errors.append(f"contract id {item_id} is reused across {kinds_text}; target resolution is ambiguous")

    declared_contract_ids = {
        item_id
        for ids in ids_by_kind.values()
        for item_id in ids
    }
    for reference in contract.references:
        for target in reference.carry_forward_to:
            if target in declared_contract_ids:
                errors.append(
                    f"reference {reference.id} carry_forward_to must name workflow scope, not contract id {target}"
                )

    return errors


def _has_contract_grounding_context(contract: ResearchContract) -> bool:
    """Return whether the contract carries explicit grounding outside references."""

    return any(
        (
            contract.context_intake.must_include_prior_outputs,
            contract.context_intake.user_asserted_anchors,
            contract.context_intake.known_good_baselines,
            contract.context_intake.crucial_inputs,
            contract.approach_policy.formulations,
            contract.approach_policy.stop_and_rethink_conditions,
        )
    )


def contract_has_explicit_context_intake(contract: ResearchContract) -> bool:
    """Return whether ``context_intake`` carries any explicit non-empty field."""

    return any(
        (
            contract.context_intake.must_read_refs,
            contract.context_intake.must_include_prior_outputs,
            contract.context_intake.user_asserted_anchors,
            contract.context_intake.known_good_baselines,
            contract.context_intake.context_gaps,
            contract.context_intake.crucial_inputs,
        )
    )


def _is_scoping_contract(contract: ResearchContract) -> bool:
    """Return whether the contract is still framing the work rather than proving it."""

    return (
        not contract.claims
        and not contract.acceptance_tests
        and (
            bool(contract.observables)
            or bool(contract.deliverables)
            or bool(contract.scope.unresolved_questions)
            or _has_contract_grounding_context(contract)
        )
    )


def _is_exploratory_contract(contract: ResearchContract) -> bool:
    """Return whether the contract semantics describe setup/exploratory work."""

    exploratory_test_kinds = {
        "existence",
        "schema",
        "human_review",
        "consistency",
        "limiting_case",
        "symmetry",
        "dimensional_analysis",
        "convergence",
        "other",
    }
    exploratory_deliverable_kinds = {"code", "note", "report", "derivation", "figure", "table", "dataset", "data", "other"}

    return (
        not _is_scoping_contract(contract)
        and (bool(contract.acceptance_tests) or _has_contract_grounding_context(contract))
        and all(test.kind in exploratory_test_kinds for test in contract.acceptance_tests)
        and all(deliverable.kind in exploratory_deliverable_kinds for deliverable in contract.deliverables)
    )


def collect_plan_contract_integrity_errors(contract: ResearchContract) -> list[str]:
    """Return the full semantic integrity error set for plan-style contracts."""

    issues = list(collect_contract_integrity_errors(contract))
    scoping_contract = _is_scoping_contract(contract)
    exploratory_contract = _is_exploratory_contract(contract)

    if not contract.claims and not scoping_contract:
        issues.append("missing claims")
    if not contract.deliverables and not scoping_contract:
        issues.append("missing deliverables")
    if not contract.acceptance_tests and not scoping_contract:
        issues.append("missing acceptance_tests")
    if not contract.references and not (_has_contract_grounding_context(contract) or exploratory_contract or scoping_contract):
        issues.append("missing references or explicit grounding context")
    if not contract.forbidden_proxies and not (exploratory_contract or scoping_contract):
        issues.append("missing forbidden_proxies")
    if not contract.uncertainty_markers.weakest_anchors:
        issues.append("missing uncertainty_markers.weakest_anchors")
    if not contract.uncertainty_markers.disconfirming_observations:
        issues.append("missing uncertainty_markers.disconfirming_observations")
    if scoping_contract and not (
        contract.observables
        or contract.deliverables
        or contract.scope.unresolved_questions
        or _has_contract_grounding_context(contract)
    ):
        issues.append("scoping contracts must preserve at least one target, open question, or carry-forward input")

    observable_ids = {observable.id for observable in contract.observables}
    claim_ids = {claim.id for claim in contract.claims}
    deliverable_ids = {deliverable.id for deliverable in contract.deliverables}
    acceptance_test_ids = {test.id for test in contract.acceptance_tests}
    reference_ids = {reference.id for reference in contract.references}
    known_ids = claim_ids | deliverable_ids | acceptance_test_ids | reference_ids

    if contract.references and not any(reference.must_surface for reference in contract.references):
        issues.append("references must include at least one must_surface=true anchor")
    for must_read_ref in contract.context_intake.must_read_refs:
        if must_read_ref not in reference_ids:
            issues.append(f"context_intake.must_read_refs references unknown reference {must_read_ref}")

    for claim in contract.claims:
        if not claim.deliverables:
            issues.append(f"claim {claim.id} missing deliverables")
        if not claim.acceptance_tests:
            issues.append(f"claim {claim.id} missing acceptance_tests")
        for observable_id in claim.observables:
            if observable_id not in observable_ids:
                issues.append(f"claim {claim.id} references unknown observable {observable_id}")
        for deliverable_id in claim.deliverables:
            if deliverable_id not in deliverable_ids:
                issues.append(f"claim {claim.id} references unknown deliverable {deliverable_id}")
        for test_id in claim.acceptance_tests:
            if test_id not in acceptance_test_ids:
                issues.append(f"claim {claim.id} references unknown acceptance test {test_id}")
        for reference_id in claim.references:
            if reference_id not in reference_ids:
                issues.append(f"claim {claim.id} references unknown reference {reference_id}")

    for test in contract.acceptance_tests:
        if test.subject not in claim_ids and test.subject not in deliverable_ids:
            issues.append(f"acceptance test {test.id} targets unknown subject {test.subject}")
        for evidence_id in test.evidence_required:
            if evidence_id not in known_ids:
                issues.append(f"acceptance test {test.id} references unknown evidence {evidence_id}")

    for reference in contract.references:
        if reference.must_surface and not reference.required_actions:
            issues.append(f"reference {reference.id} is must_surface but missing required_actions")
        if reference.must_surface and not reference.applies_to:
            issues.append(f"reference {reference.id} is must_surface but missing applies_to")
        for applies_to_id in reference.applies_to:
            if applies_to_id not in claim_ids and applies_to_id not in deliverable_ids:
                issues.append(f"reference {reference.id} applies_to unknown target {applies_to_id}")

    for forbidden_proxy in contract.forbidden_proxies:
        if forbidden_proxy.subject not in claim_ids and forbidden_proxy.subject not in deliverable_ids:
            issues.append(
                f"forbidden proxy {forbidden_proxy.id} targets unknown subject {forbidden_proxy.subject}"
            )

    for link in contract.links:
        if link.source not in known_ids:
            issues.append(f"link {link.id} references unknown source {link.source}")
        if link.target not in known_ids:
            issues.append(f"link {link.id} references unknown target {link.target}")
        for verification_id in link.verified_by:
            if verification_id not in acceptance_test_ids:
                issues.append(f"link {link.id} references unknown acceptance test {verification_id}")

    return issues


class ProjectContractParseResult(BaseModel):
    """Structured result for project-contract payload parsing boundaries."""

    model_config = ConfigDict(frozen=True)

    contract: ResearchContract | None = None
    blocking_errors: list[str] = Field(default_factory=list)
    recoverable_errors: list[str] = Field(default_factory=list)

    @property
    def errors(self) -> list[str]:
        return [*self.blocking_errors, *self.recoverable_errors]

    @property
    def warnings(self) -> list[str]:
        return list(self.recoverable_errors)


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def _project_contract_parse_result(
    *,
    contract: ResearchContract | None = None,
    blocking_errors: list[str] | None = None,
    recoverable_errors: list[str] | None = None,
) -> ProjectContractParseResult:
    return ProjectContractParseResult(
        contract=contract,
        blocking_errors=_dedupe_preserve_order(list(blocking_errors or [])),
        recoverable_errors=_dedupe_preserve_order(list(recoverable_errors or [])),
    )


def _parse_project_contract_data(
    data: object,
    *,
    strict: bool,
) -> ProjectContractParseResult:
    if not isinstance(data, dict):
        return _project_contract_parse_result(blocking_errors=["project contract must be a JSON object"])

    from gpd.core.contract_validation import _collect_list_shape_drift_errors, salvage_project_contract

    contract, schema_findings = salvage_project_contract(data)
    list_shape_drift_errors = _collect_list_shape_drift_errors(data)
    if strict:
        from gpd.core.contract_validation import _split_project_contract_schema_findings

        schema_warnings, schema_errors = _split_project_contract_schema_findings(
            schema_findings,
            allow_singleton_defaults=False,
        )
        blocking_errors = [
            *schema_errors,
            *schema_warnings,
            *list_shape_drift_errors,
            *_collect_project_contract_list_member_errors(data),
        ]
        if contract is None:
            if not blocking_errors and schema_findings:
                blocking_errors = list(schema_findings)
            if not blocking_errors:
                blocking_errors = ["project contract could not be normalized"]
            return _project_contract_parse_result(blocking_errors=blocking_errors)
        integrity_errors = collect_contract_integrity_errors(contract)
        blocking_errors.extend(integrity_errors)
        if blocking_errors:
            return _project_contract_parse_result(blocking_errors=blocking_errors)
        return _project_contract_parse_result(contract=contract)

    from gpd.core.contract_validation import _split_project_contract_schema_findings

    schema_warnings, schema_errors = _split_project_contract_schema_findings(
        schema_findings,
        allow_singleton_defaults=True,
    )
    recoverable_errors = [*schema_warnings, *list_shape_drift_errors, *_collect_project_contract_list_member_errors(data)]
    if contract is None:
        blocking_errors = [*schema_errors]
        if not blocking_errors and schema_findings:
            blocking_errors = list(schema_findings)
        if not blocking_errors:
            blocking_errors = ["project contract could not be normalized"]
        return _project_contract_parse_result(
            blocking_errors=blocking_errors,
            recoverable_errors=recoverable_errors,
        )

    integrity_errors = collect_contract_integrity_errors(contract)
    if integrity_errors:
        return _project_contract_parse_result(
            blocking_errors=integrity_errors,
            recoverable_errors=recoverable_errors,
        )
    return _project_contract_parse_result(contract=contract, recoverable_errors=recoverable_errors)


def parse_project_contract_data_strict(data: object) -> ProjectContractParseResult:
    """Strictly parse an authored project-contract payload.

    This entrypoint is for model-facing or authoring boundaries where recoverable
    salvage is undesirable. Inputs that would require schema normalization
    (singleton list drift, extra keys, defaulted singleton sections, coercive
    scalars) are rejected explicitly instead of being silently canonicalized.
    Read/repair flows should continue to use ``contract_from_data_salvage()``
    or the lower-level salvage helpers.
    """

    return _parse_project_contract_data(data, strict=True)


def parse_project_contract_data_salvage(data: object) -> ProjectContractParseResult:
    """Salvage a project-contract payload while still surfacing recoverable findings."""

    return _parse_project_contract_data(data, strict=False)


def contract_from_data(
    data: object,
    *,
    allow_recoverable_warnings: bool = False,
    require_draft_validity: bool = False,
    project_root: Path | None = None,
) -> ResearchContract | None:
    """Return a validated :class:`ResearchContract` when *data* is a mapping.

    This entrypoint is strict by default and fails closed on recoverable
    schema drift. Callers that need repair-oriented salvage should use
    :func:`contract_from_data_salvage` explicitly. Callers that preserve
    contracts back into state can additionally require draft-level scoping
    validity.
    """

    if not isinstance(data, dict):
        return None
    if allow_recoverable_warnings:
        return contract_from_data_salvage(
            data,
            require_draft_validity=require_draft_validity,
            project_root=project_root,
        )

    strict_result = parse_project_contract_data_strict(data)
    if strict_result.contract is None or strict_result.errors:
        return None
    if require_draft_validity:
        from gpd.core.contract_validation import validate_project_contract

        draft_validation = validate_project_contract(strict_result.contract, mode="draft", project_root=project_root)
        if not draft_validation.valid:
            return None
    return strict_result.contract


def contract_from_data_salvage(
    data: object,
    *,
    require_draft_validity: bool = False,
    project_root: Path | None = None,
) -> ResearchContract | None:
    """Return a salvaged :class:`ResearchContract` for repair/migration callers."""

    if not isinstance(data, dict):
        return None
    from gpd.core.contract_validation import validate_project_contract

    salvage_result = parse_project_contract_data_salvage(data)
    if salvage_result.contract is None or salvage_result.blocking_errors:
        return None
    if require_draft_validity:
        draft_validation = validate_project_contract(salvage_result.contract, mode="draft", project_root=project_root)
        if not draft_validation.valid:
            return None
    return salvage_result.contract
