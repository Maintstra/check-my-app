#!/usr/bin/env python3
"""Validate a Check My App report without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION_LEGACY = "check-my-app-report@1.0.0"
SCHEMA_VERSION_CURRENT = "check-my-app-report@1.1.0"
SCHEMA_VERSIONS = {SCHEMA_VERSION_LEGACY, SCHEMA_VERSION_CURRENT}
MODES_LEGACY = {"Audit", "Fix & Retest", "Release Gate"}
MODES_CURRENT = MODES_LEGACY | {"Delivery Closure"}
VERDICTS = {"Not ready", "Pilot ready", "Delivery ready"}
SEVERITIES = {"Blocking", "Must fix", "Improve", "Polish"}
FINDING_STATUSES = {"open", "resolved", "reopened"}
EFFORTS = {"S", "M", "L"}
CLAIM_STATUSES = {"confirmed", "inference", "untested"}
EVIDENCE_TYPES = {
    "screenshot",
    "interaction-trace",
    "log",
    "read-back",
    "deterministic-test",
    "code-inspection",
    "document",
    "other",
}
ARTIFACT_KINDS = {
    "source",
    "development-server",
    "packaged-app",
    "packaged-installer",
    "hosted-release",
    "other",
}
DELIVERY_ARTIFACT_KINDS = {"packaged-app", "packaged-installer", "hosted-release"}
SENSITIVE_KEYS = {
    "apikey",
    "accesstoken",
    "refreshtoken",
    "password",
    "clientsecret",
    "secret",
    "cookie",
    "sessioncookie",
    "authorization",
    "privatekey",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:sk|shpat|shpss)_[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
)
REPORT_FIELDS_LEGACY = {
    "schemaVersion",
    "mode",
    "product",
    "scope",
    "verdict",
    "claims",
    "evidence",
    "findings",
    "limitations",
    "untestedAreas",
    "externalEffects",
    "release",
}
REPORT_FIELDS_CURRENT = REPORT_FIELDS_LEGACY | {"closure"}
CLOSURE_BOUNDARY_DIMENSIONS = {
    "capabilities",
    "roles",
    "surfaces",
    "personas",
    "configurations",
    "lifecycleStages",
    "safetyBoundaries",
}
SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")


class ValidationError(Exception):
    def __init__(self, code: str, path: str, message: str):
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


def _normalise_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.casefold())


def _walk_sensitive(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if _normalise_key(str(key)) in SENSITIVE_KEYS:
                raise ValidationError("SENSITIVE_KEY", child_path, "sensitive field names are forbidden")
            _walk_sensitive(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_sensitive(child, f"{path}[{index}]")
    elif isinstance(value, str):
        if any(pattern.search(value) for pattern in SECRET_PATTERNS):
            raise ValidationError("SENSITIVE_VALUE", path, "secret-shaped values are forbidden")


def _require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("TYPE_OBJECT_REQUIRED", path, "must be an object")
    return value


def _require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError("TYPE_ARRAY_REQUIRED", path, "must be an array")
    return value


def _require_text(value: Any, path: str, minimum: int = 1) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise ValidationError("TEXT_REQUIRED", path, f"must contain at least {minimum} characters")
    return value.strip()


def _require_bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        raise ValidationError("TYPE_BOOLEAN_REQUIRED", path, "must be boolean")
    return value


def _require_nonnegative_int(value: Any, path: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValidationError("TYPE_NONNEGATIVE_INTEGER_REQUIRED", path, "must be a non-negative integer")
    return value


def _require_fields(value: dict[str, Any], fields: set[str], path: str, code: str) -> None:
    missing = sorted(fields.difference(value))
    if missing:
        raise ValidationError(code, path, "missing required fields: " + ", ".join(missing))


def _reject_unknown_fields(value: dict[str, Any], fields: set[str], path: str, code: str) -> None:
    unknown = sorted(set(value).difference(fields))
    if unknown:
        raise ValidationError(code, path, "unknown fields: " + ", ".join(unknown))


def _unique_ids(items: list[Any], path: str) -> set[str]:
    identifiers: set[str] = set()
    for index, raw in enumerate(items):
        item = _require_object(raw, f"{path}[{index}]")
        identifier = _require_text(item.get("id"), f"{path}[{index}].id")
        if identifier in identifiers:
            raise ValidationError("DUPLICATE_ID", f"{path}[{index}].id", "identifier must be unique")
        identifiers.add(identifier)
    return identifiers


def _validate_product(report: dict[str, Any], schema_version: str) -> dict[str, Any]:
    product = _require_object(report.get("product"), "$.product")
    product_fields = {"name", "type", "artifact"}
    _require_fields(product, product_fields, "$.product", "PRODUCT_REQUIRED_FIELD")
    if schema_version == SCHEMA_VERSION_CURRENT:
        _reject_unknown_fields(product, product_fields, "$.product", "PRODUCT_UNKNOWN_FIELD")
    _require_text(product["name"], "$.product.name")
    _require_text(product["type"], "$.product.type")
    artifact = _require_object(product["artifact"], "$.product.artifact")
    _require_fields(artifact, {"kind", "identity", "platform"}, "$.product.artifact", "ARTIFACT_REQUIRED_FIELD")
    if schema_version == SCHEMA_VERSION_CURRENT:
        _reject_unknown_fields(
            artifact,
            {"kind", "identity", "platform", "version", "commit", "sha256", "signatureState"},
            "$.product.artifact",
            "ARTIFACT_UNKNOWN_FIELD",
        )
    if artifact["kind"] not in ARTIFACT_KINDS:
        raise ValidationError("ARTIFACT_KIND_INVALID", "$.product.artifact.kind", "unsupported artifact kind")
    _require_text(artifact["identity"], "$.product.artifact.identity")
    _require_text(artifact["platform"], "$.product.artifact.platform")
    if "sha256" in artifact and (
        not isinstance(artifact["sha256"], str) or not SHA256_PATTERN.fullmatch(artifact["sha256"])
    ):
        raise ValidationError("ARTIFACT_SHA256_INVALID", "$.product.artifact.sha256", "must be a 64-character hexadecimal SHA-256")
    return artifact


def _validate_scope(
    report: dict[str, Any],
    claim_ids: set[str],
    schema_version: str,
) -> tuple[set[str], dict[str, str]]:
    scope = _require_object(report.get("scope"), "$.scope")
    _require_fields(
        scope,
        {"persona", "journeys", "permittedActions", "prohibitedExternalEffects"},
        "$.scope",
        "SCOPE_REQUIRED_FIELD",
    )
    if schema_version == SCHEMA_VERSION_CURRENT:
        _reject_unknown_fields(
            scope,
            {"persona", "journeys", "permittedActions", "prohibitedExternalEffects"},
            "$.scope",
            "SCOPE_UNKNOWN_FIELD",
        )
    _require_text(scope["persona"], "$.scope.persona")
    _require_list(scope["permittedActions"], "$.scope.permittedActions")
    _require_list(scope["prohibitedExternalEffects"], "$.scope.prohibitedExternalEffects")
    journeys = _require_list(scope["journeys"], "$.scope.journeys")
    if schema_version == SCHEMA_VERSION_CURRENT and not journeys:
        raise ValidationError("JOURNEY_REQUIRED", "$.scope.journeys", "version 1.1 reports require at least one journey")
    if report["mode"] == "Delivery Closure" and len(journeys) < 2:
        raise ValidationError("CLOSURE_JOURNEY_MATRIX_REQUIRED", "$.scope.journeys", "Delivery Closure requires at least two distinct journeys")
    journey_ids = _unique_ids(journeys, "$.scope.journeys")
    required_journey_ids: set[str] = set()
    journey_results: dict[str, str] = {}
    for index, raw in enumerate(journeys):
        journey = _require_object(raw, f"$.scope.journeys[{index}]")
        journey_fields = {"id", "name", "required", "result", "claimId"}
        _require_fields(journey, journey_fields, f"$.scope.journeys[{index}]", "JOURNEY_REQUIRED_FIELD")
        if schema_version == SCHEMA_VERSION_CURRENT:
            _reject_unknown_fields(journey, journey_fields, f"$.scope.journeys[{index}]", "JOURNEY_UNKNOWN_FIELD")
        if not isinstance(journey["required"], bool):
            raise ValidationError("JOURNEY_REQUIRED_FLAG_INVALID", f"$.scope.journeys[{index}].required", "must be boolean")
        if journey["result"] not in {"passed", "failed", "blocked", "untested"}:
            raise ValidationError("JOURNEY_RESULT_INVALID", f"$.scope.journeys[{index}].result", "unsupported journey result")
        if journey["claimId"] not in claim_ids:
            raise ValidationError("CLAIM_REFERENCE_UNKNOWN", f"$.scope.journeys[{index}].claimId", "journey claim does not exist")
        journey_results[journey["id"]] = journey["result"]
        if journey["required"]:
            required_journey_ids.add(journey["id"])
    if report["mode"] == "Delivery Closure" and len(required_journey_ids) < 2:
        raise ValidationError("CLOSURE_JOURNEY_MATRIX_REQUIRED", "$.scope.journeys", "Delivery Closure requires at least two distinct required journeys")
    return required_journey_ids, journey_results


def _validate_claims(report: dict[str, Any], evidence_ids: dict[str, str], schema_version: str) -> set[str]:
    claims = _require_list(report.get("claims"), "$.claims")
    claim_ids = _unique_ids(claims, "$.claims")
    for index, raw in enumerate(claims):
        claim = _require_object(raw, f"$.claims[{index}]")
        claim_fields = {"id", "status", "statement", "evidenceIds"}
        _require_fields(claim, claim_fields, f"$.claims[{index}]", "CLAIM_REQUIRED_FIELD")
        if schema_version == SCHEMA_VERSION_CURRENT:
            _reject_unknown_fields(claim, claim_fields, f"$.claims[{index}]", "CLAIM_UNKNOWN_FIELD")
        if claim["status"] not in CLAIM_STATUSES:
            raise ValidationError("CLAIM_STATUS_INVALID", f"$.claims[{index}].status", "unsupported claim status")
        _require_text(claim["statement"], f"$.claims[{index}].statement")
        references = _require_list(claim["evidenceIds"], f"$.claims[{index}].evidenceIds")
        if claim["status"] == "confirmed" and not references:
            raise ValidationError("CONFIRMED_CLAIM_EVIDENCE_REQUIRED", f"$.claims[{index}]", "confirmed claims require evidence")
        for reference in references:
            if reference not in evidence_ids:
                raise ValidationError("EVIDENCE_REFERENCE_UNKNOWN", f"$.claims[{index}].evidenceIds", "referenced evidence does not exist")
    return claim_ids


def _validate_evidence(report: dict[str, Any], schema_version: str) -> dict[str, str]:
    evidence = _require_list(report.get("evidence"), "$.evidence")
    evidence_ids = _unique_ids(evidence, "$.evidence")
    for index, raw in enumerate(evidence):
        item = _require_object(raw, f"$.evidence[{index}]")
        evidence_fields = {"id", "type", "source", "summary", "redacted"}
        _require_fields(item, evidence_fields, f"$.evidence[{index}]", "EVIDENCE_REQUIRED_FIELD")
        if schema_version == SCHEMA_VERSION_CURRENT:
            _reject_unknown_fields(item, evidence_fields, f"$.evidence[{index}]", "EVIDENCE_UNKNOWN_FIELD")
        if item["type"] not in EVIDENCE_TYPES:
            raise ValidationError("EVIDENCE_TYPE_INVALID", f"$.evidence[{index}].type", "unsupported evidence type")
        _require_text(item["source"], f"$.evidence[{index}].source")
        _require_text(item["summary"], f"$.evidence[{index}].summary")
        if not isinstance(item["redacted"], bool):
            raise ValidationError("EVIDENCE_REDACTION_FLAG_REQUIRED", f"$.evidence[{index}].redacted", "must be boolean")
    return {
        item["id"]: item["source"]
        for item in evidence
    }


def _validate_findings(
    report: dict[str, Any],
    claim_ids: set[str],
    evidence_ids: dict[str, str],
    schema_version: str,
) -> dict[str, dict[str, str]]:
    findings = _require_list(report.get("findings"), "$.findings")
    _unique_ids(findings, "$.findings")
    finding_records: dict[str, dict[str, str]] = {}
    required = {
        "id",
        "title",
        "severity",
        "effort",
        "claimIds",
        "evidenceIds",
        "userImpact",
        "rootCause",
        "recommendation",
        "retest",
    }
    if schema_version == SCHEMA_VERSION_CURRENT:
        required.add("status")
    recommendation_fields = {"location", "recommendedChange", "alternative", "tradeoffs"}
    for index, raw in enumerate(findings):
        path = f"$.findings[{index}]"
        finding = _require_object(raw, path)
        _require_fields(finding, required, path, "FINDING_REQUIRED_FIELD")
        if schema_version == SCHEMA_VERSION_CURRENT:
            _reject_unknown_fields(finding, required, path, "FINDING_UNKNOWN_FIELD")
        if finding["severity"] not in SEVERITIES:
            raise ValidationError("FINDING_SEVERITY_INVALID", f"{path}.severity", "unsupported severity")
        status = finding.get("status", "open")
        if schema_version == SCHEMA_VERSION_CURRENT and status not in FINDING_STATUSES:
            raise ValidationError("FINDING_STATUS_INVALID", f"{path}.status", "unsupported finding status")
        finding_records[finding["id"]] = {"severity": finding["severity"], "status": status}
        if finding["effort"] not in EFFORTS:
            raise ValidationError("FINDING_EFFORT_INVALID", f"{path}.effort", "unsupported effort")
        _require_text(finding["userImpact"], f"{path}.userImpact", 20)
        _require_text(finding["rootCause"], f"{path}.rootCause", 20)
        _require_text(finding["retest"], f"{path}.retest", 25)
        recommendation = _require_object(finding["recommendation"], f"{path}.recommendation")
        _require_fields(recommendation, recommendation_fields, f"{path}.recommendation", "FINDING_RECOMMENDATION_REQUIRED_FIELD")
        if schema_version == SCHEMA_VERSION_CURRENT:
            _reject_unknown_fields(recommendation, recommendation_fields, f"{path}.recommendation", "FINDING_RECOMMENDATION_UNKNOWN_FIELD")
        _require_text(recommendation["location"], f"{path}.recommendation.location", 5)
        recommended_change = _require_text(recommendation["recommendedChange"], f"{path}.recommendation.recommendedChange")
        _require_text(recommendation["alternative"], f"{path}.recommendation.alternative", 20)
        _require_text(recommendation["tradeoffs"], f"{path}.recommendation.tradeoffs", 20)
        if len(recommended_change) < 40 or recommended_change.casefold().strip(" .") in {
            "simplify the ui",
            "improve the ui",
            "make it clearer",
            "fix the layout",
            "make it better",
        }:
            raise ValidationError("FINDING_RECOMMENDATION_TOO_VAGUE", f"{path}.recommendation.recommendedChange", "name an exact component, state, copy, layout, rule, or test change")
        for reference in _require_list(finding["claimIds"], f"{path}.claimIds"):
            if reference not in claim_ids:
                raise ValidationError("CLAIM_REFERENCE_UNKNOWN", f"{path}.claimIds", "referenced claim does not exist")
        for reference in _require_list(finding["evidenceIds"], f"{path}.evidenceIds"):
            if reference not in evidence_ids:
                raise ValidationError("EVIDENCE_REFERENCE_UNKNOWN", f"{path}.evidenceIds", "referenced evidence does not exist")
    return finding_records


def _validate_closure(
    report: dict[str, Any],
    artifact: dict[str, Any],
    required_journey_ids: set[str],
    journey_results: dict[str, str],
    findings: dict[str, dict[str, str]],
    evidence_ids: dict[str, str],
) -> None:
    closure = report.get("closure")
    if report["mode"] != "Delivery Closure":
        if closure is not None:
            raise ValidationError("CLOSURE_MODE_CONFLICT", "$.closure", "closure must be null outside Delivery Closure mode")
        return

    closure = _require_object(closure, "$.closure")
    closure_fields = {"boundary", "passes", "cleanPassCount"}
    _require_fields(closure, closure_fields, "$.closure", "CLOSURE_REQUIRED_FIELD")
    _reject_unknown_fields(closure, closure_fields, "$.closure", "CLOSURE_UNKNOWN_FIELD")
    boundary = _require_object(closure["boundary"], "$.closure.boundary")
    _require_fields(boundary, CLOSURE_BOUNDARY_DIMENSIONS, "$.closure.boundary", "CLOSURE_BOUNDARY_REQUIRED")
    _reject_unknown_fields(boundary, CLOSURE_BOUNDARY_DIMENSIONS, "$.closure.boundary", "CLOSURE_BOUNDARY_UNKNOWN_FIELD")
    journey_ids = set(journey_results)

    for dimension in sorted(CLOSURE_BOUNDARY_DIMENSIONS):
        items = _require_list(boundary[dimension], f"$.closure.boundary.{dimension}")
        if not items:
            raise ValidationError("CLOSURE_BOUNDARY_REQUIRED", f"$.closure.boundary.{dimension}", "must contain at least one coverage item")
        _unique_ids(items, f"$.closure.boundary.{dimension}")
        required_coverage_found = False
        for index, raw in enumerate(items):
            path = f"$.closure.boundary.{dimension}[{index}]"
            item = _require_object(raw, path)
            item_fields = {"id", "name", "disposition", "journeyIds", "rationale"}
            _require_fields(item, item_fields, path, "CLOSURE_BOUNDARY_ITEM_REQUIRED")
            _reject_unknown_fields(item, item_fields, path, "CLOSURE_BOUNDARY_ITEM_UNKNOWN_FIELD")
            _require_text(item["name"], f"{path}.name")
            _require_text(item["rationale"], f"{path}.rationale")
            if item["disposition"] not in {"required", "excluded", "untested"}:
                raise ValidationError("CLOSURE_BOUNDARY_DISPOSITION_INVALID", f"{path}.disposition", "unsupported coverage disposition")
            references = _require_list(item["journeyIds"], f"{path}.journeyIds")
            if item["disposition"] == "required" and not references:
                raise ValidationError("CLOSURE_BOUNDARY_MAPPING_REQUIRED", f"{path}.journeyIds", "required coverage must map to a journey")
            if len(references) != len(set(references)):
                raise ValidationError("DUPLICATE_ID", f"{path}.journeyIds", "journey references must be unique")
            for reference in references:
                if reference not in journey_ids:
                    raise ValidationError("JOURNEY_REFERENCE_UNKNOWN", f"{path}.journeyIds", "coverage references an unknown journey")
                if item["disposition"] == "required" and reference not in required_journey_ids:
                    raise ValidationError("CLOSURE_BOUNDARY_REQUIRED_JOURNEY", f"{path}.journeyIds", "required coverage must map only to required journeys")
            required_coverage_found = required_coverage_found or item["disposition"] == "required"
        if not required_coverage_found:
            raise ValidationError("CLOSURE_BOUNDARY_REQUIRED_COVERAGE", f"$.closure.boundary.{dimension}", "Delivery Closure requires at least one required coverage item in every dimension")

    passes = _require_list(closure["passes"], "$.closure.passes")
    if not passes:
        raise ValidationError("CLOSURE_PASS_REQUIRED", "$.closure.passes", "must contain at least one pass")
    _unique_ids(passes, "$.closure.passes")
    clean_pass_count = _require_nonnegative_int(closure["cleanPassCount"], "$.closure.cleanPassCount")
    if clean_pass_count > len(passes):
        raise ValidationError("CLOSURE_CLEAN_PASS_COUNT_INVALID", "$.closure.cleanPassCount", "cannot exceed recorded pass count")

    validated_passes: list[dict[str, Any]] = []
    pass_fields = {
        "id",
        "artifactIdentity",
        "artifactSha256",
        "fullMatrix",
        "journeyResults",
        "newFindingIds",
        "reopenedFindingIds",
        "evidenceIds",
    }
    for index, raw in enumerate(passes):
        path = f"$.closure.passes[{index}]"
        closure_pass = _require_object(raw, path)
        _require_fields(closure_pass, pass_fields, path, "CLOSURE_PASS_REQUIRED_FIELD")
        _reject_unknown_fields(closure_pass, pass_fields, path, "CLOSURE_PASS_UNKNOWN_FIELD")
        _require_text(closure_pass["artifactIdentity"], f"{path}.artifactIdentity")
        artifact_sha256 = _require_text(closure_pass["artifactSha256"], f"{path}.artifactSha256")
        if not SHA256_PATTERN.fullmatch(artifact_sha256):
            raise ValidationError("ARTIFACT_SHA256_INVALID", f"{path}.artifactSha256", "must be a 64-character hexadecimal SHA-256")
        _require_bool(closure_pass["fullMatrix"], f"{path}.fullMatrix")

        pass_results: dict[str, str] = {}
        for result_index, raw_result in enumerate(_require_list(closure_pass["journeyResults"], f"{path}.journeyResults")):
            result_path = f"{path}.journeyResults[{result_index}]"
            result = _require_object(raw_result, result_path)
            result_fields = {"journeyId", "result"}
            _require_fields(result, result_fields, result_path, "CLOSURE_PASS_JOURNEY_REQUIRED_FIELD")
            _reject_unknown_fields(result, result_fields, result_path, "CLOSURE_PASS_JOURNEY_UNKNOWN_FIELD")
            journey_id = _require_text(result["journeyId"], f"{result_path}.journeyId")
            if journey_id in pass_results:
                raise ValidationError("DUPLICATE_ID", f"{result_path}.journeyId", "journey result must be unique within a pass")
            if journey_id not in journey_ids:
                raise ValidationError("JOURNEY_REFERENCE_UNKNOWN", f"{result_path}.journeyId", "pass references an unknown journey")
            if result["result"] not in {"passed", "failed", "blocked", "untested"}:
                raise ValidationError("JOURNEY_RESULT_INVALID", f"{result_path}.result", "unsupported journey result")
            pass_results[journey_id] = result["result"]

        for field in ("newFindingIds", "reopenedFindingIds"):
            for reference in _require_list(closure_pass[field], f"{path}.{field}"):
                if reference not in findings:
                    raise ValidationError("FINDING_REFERENCE_UNKNOWN", f"{path}.{field}", "pass references an unknown finding")
        pass_evidence = _require_list(closure_pass["evidenceIds"], f"{path}.evidenceIds")
        if not pass_evidence:
            raise ValidationError("CLOSURE_PASS_EVIDENCE_REQUIRED", f"{path}.evidenceIds", "each pass requires evidence")
        for reference in pass_evidence:
            if reference not in evidence_ids:
                raise ValidationError("EVIDENCE_REFERENCE_UNKNOWN", f"{path}.evidenceIds", "pass evidence does not exist")
        validated_passes.append({"record": closure_pass, "journeyResults": pass_results, "path": path})

    if report["verdict"] != "Delivery ready":
        return
    if clean_pass_count < 2 or len(validated_passes) < 2:
        raise ValidationError("CLOSURE_CLEAN_PASSES_REQUIRED", "$.closure", "Delivery ready requires two recorded clean full passes")
    artifact_sha256 = artifact.get("sha256")
    if not isinstance(artifact_sha256, str) or not SHA256_PATTERN.fullmatch(artifact_sha256):
        raise ValidationError("CLOSURE_ARTIFACT_SHA256_REQUIRED", "$.product.artifact.sha256", "Delivery ready closure requires a final artifact SHA-256")
    final_passes = validated_passes[-2:]
    first_evidence = set(final_passes[0]["record"]["evidenceIds"])
    second_evidence = set(final_passes[1]["record"]["evidenceIds"])
    first_sources = {evidence_ids[evidence_id] for evidence_id in first_evidence}
    second_sources = {evidence_ids[evidence_id] for evidence_id in second_evidence}
    if first_evidence.intersection(second_evidence) or first_sources.intersection(second_sources):
        raise ValidationError("CLOSURE_PASS_EVIDENCE_REUSED", "$.closure.passes", "the final two clean passes require independent evidence")
    for item in final_passes:
        closure_pass = item["record"]
        path = item["path"]
        if not closure_pass["fullMatrix"]:
            raise ValidationError("CLOSURE_FULL_MATRIX_REQUIRED", f"{path}.fullMatrix", "clean closure passes must cover the full matrix")
        if closure_pass["artifactIdentity"] != artifact["identity"]:
            raise ValidationError("CLOSURE_ARTIFACT_MISMATCH", f"{path}.artifactIdentity", "clean pass must use the exact final artifact")
        if closure_pass["artifactSha256"].casefold() != artifact_sha256.casefold():
            raise ValidationError("CLOSURE_ARTIFACT_MISMATCH", f"{path}.artifactSha256", "clean pass must use the exact final artifact SHA-256")
        missing = sorted(required_journey_ids.difference(item["journeyResults"]))
        if missing:
            raise ValidationError("CLOSURE_REQUIRED_JOURNEY_MISSING", f"{path}.journeyResults", "missing required journeys: " + ", ".join(missing))
        failed = sorted(
            journey_id
            for journey_id in required_journey_ids
            if item["journeyResults"][journey_id] != "passed"
        )
        if failed:
            raise ValidationError("CLOSURE_REQUIRED_JOURNEY_FAILED", f"{path}.journeyResults", "required journeys did not pass: " + ", ".join(failed))
        material = [
            finding_id
            for finding_id in closure_pass["newFindingIds"] + closure_pass["reopenedFindingIds"]
            if findings[finding_id]["severity"] in {"Blocking", "Must fix"}
        ]
        if material:
            raise ValidationError("CLOSURE_MATERIAL_FINDING_DISCOVERED", path, "clean pass contains new or reopened material findings: " + ", ".join(material))


def _validate_delivery(
    report: dict[str, Any],
    artifact: dict[str, Any],
    findings: dict[str, dict[str, str]],
    required_journey_ids: set[str],
    journey_results: dict[str, str],
    schema_version: str,
) -> None:
    if report["verdict"] != "Delivery ready":
        return
    unresolved = {
        finding_id: finding
        for finding_id, finding in findings.items()
        if finding["status"] != "resolved"
    }
    if any(finding["severity"] == "Blocking" for finding in unresolved.values()):
        raise ValidationError("VERDICT_BLOCKING_CONFLICT", "$.verdict", "blocking findings force Not ready")
    if schema_version == SCHEMA_VERSION_CURRENT and any(
        finding["severity"] == "Must fix" for finding in unresolved.values()
    ):
        raise ValidationError("VERDICT_MUST_FIX_CONFLICT", "$.verdict", "open Must fix findings prevent Delivery ready")
    allowed_modes = {"Release Gate"}
    if schema_version == SCHEMA_VERSION_CURRENT:
        allowed_modes.add("Delivery Closure")
    if report["mode"] not in allowed_modes or artifact["kind"] not in DELIVERY_ARTIFACT_KINDS:
        raise ValidationError("DELIVERY_EXACT_ARTIFACT_REQUIRED", "$.product.artifact", "Delivery ready requires an exact final artifact in Release Gate or Delivery Closure mode")
    if schema_version == SCHEMA_VERSION_CURRENT:
        failed_required = sorted(
            journey_id
            for journey_id in required_journey_ids
            if journey_results.get(journey_id) != "passed"
        )
        if failed_required:
            raise ValidationError("DELIVERY_REQUIRED_JOURNEY_FAILED", "$.scope.journeys", "required journeys did not pass: " + ", ".join(failed_required))
    release = _require_object(report.get("release"), "$.release")
    if not release.get("packagedJourneyTested"):
        raise ValidationError("DELIVERY_PACKAGED_JOURNEY_REQUIRED", "$.release.packagedJourneyTested", "critical packaged journey was not tested")
    if not release.get("cleanMachineTested"):
        raise ValidationError("DELIVERY_CLEAN_MACHINE_REQUIRED", "$.release.cleanMachineTested", "clean-machine evidence is required")
    if not release.get("installTested") or not release.get("restartTested"):
        raise ValidationError("DELIVERY_LIFECYCLE_REQUIRED", "$.release", "install and restart lifecycle evidence is required")


def validate(report: Any) -> str:
    report = _require_object(report, "$")
    _walk_sensitive(report)
    schema_version = report.get("schemaVersion")
    if schema_version not in SCHEMA_VERSIONS:
        raise ValidationError("SCHEMA_VERSION_UNSUPPORTED", "$.schemaVersion", "unsupported report schema")
    report_fields = (
        REPORT_FIELDS_CURRENT
        if schema_version == SCHEMA_VERSION_CURRENT
        else REPORT_FIELDS_LEGACY
    )
    _require_fields(report, report_fields, "$", "REPORT_REQUIRED_FIELD")
    unknown_fields = sorted(set(report).difference(report_fields))
    if unknown_fields:
        raise ValidationError("REPORT_UNKNOWN_FIELD", "$", "unknown fields: " + ", ".join(unknown_fields))
    modes = MODES_CURRENT if schema_version == SCHEMA_VERSION_CURRENT else MODES_LEGACY
    if not isinstance(report["mode"], str) or report["mode"] not in modes:
        raise ValidationError("MODE_INVALID", "$.mode", "unsupported audit mode")
    if not isinstance(report["verdict"], str) or report["verdict"] not in VERDICTS:
        raise ValidationError("VERDICT_INVALID", "$.verdict", "unsupported readiness verdict")
    artifact = _validate_product(report, schema_version)
    evidence_ids = _validate_evidence(report, schema_version)
    claim_ids = _validate_claims(report, evidence_ids, schema_version)
    required_journey_ids, journey_results = _validate_scope(report, claim_ids, schema_version)
    findings = _validate_findings(report, claim_ids, evidence_ids, schema_version)
    _require_list(report["limitations"], "$.limitations")
    _require_list(report["untestedAreas"], "$.untestedAreas")
    external_effects = _require_object(report["externalEffects"], "$.externalEffects")
    external_effect_fields = {"observed", "prohibited"}
    _require_fields(external_effects, external_effect_fields, "$.externalEffects", "EXTERNAL_EFFECTS_REQUIRED_FIELD")
    if schema_version == SCHEMA_VERSION_CURRENT:
        _reject_unknown_fields(external_effects, external_effect_fields, "$.externalEffects", "EXTERNAL_EFFECTS_UNKNOWN_FIELD")
    _require_list(external_effects["observed"], "$.externalEffects.observed")
    _require_list(external_effects["prohibited"], "$.externalEffects.prohibited")
    if schema_version == SCHEMA_VERSION_CURRENT and report.get("release") is not None:
        release = _require_object(report["release"], "$.release")
        _reject_unknown_fields(
            release,
            {
                "packagedJourneyTested",
                "cleanMachineTested",
                "installTested",
                "restartTested",
                "uninstallTested",
                "updateTested",
                "rollbackTested",
            },
            "$.release",
            "RELEASE_UNKNOWN_FIELD",
        )
    if schema_version == SCHEMA_VERSION_CURRENT:
        _validate_closure(
            report,
            artifact,
            required_journey_ids,
            journey_results,
            findings,
            evidence_ids,
        )
    _validate_delivery(
        report,
        artifact,
        findings,
        required_journey_ids,
        journey_results,
        schema_version,
    )
    return schema_version


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("USAGE: validate_report.py <report.json>", file=sys.stderr)
        return 2
    try:
        report = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        schema_version = validate(report)
    except (OSError, json.JSONDecodeError):
        print("REPORT_JSON_INVALID: report could not be read as UTF-8 JSON", file=sys.stderr)
        return 1
    except ValidationError as error:
        print(f"{error.code} at {error.path}: {error.message}", file=sys.stderr)
        return 1
    except (KeyError, TypeError):
        print("REPORT_STRUCTURE_INVALID: report contains an invalid field type or shape", file=sys.stderr)
        return 1
    print(f"VALID {schema_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
