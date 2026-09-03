#!/usr/bin/env python3
"""Validate the control catalog schema and repository-level invariants."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover - exercised before tests load
    raise SystemExit(
        "PyYAML is required; run: "
        "python3 -m pip install -r controls/requirements.txt"
    ) from exc


class CatalogValidator:
    """Validate the intentionally small JSON Schema subset used by the catalog."""

    def __init__(
        self,
        *,
        catalog_path: Path,
        schema_path: Path,
        repository_root: Path,
    ) -> None:
        self.catalog_path = catalog_path
        self.schema_path = schema_path
        self.repository_root = repository_root.resolve()
        self.errors: list[str] = []

    def validate(self) -> list[str]:
        self.errors = []
        catalog = self._load_yaml(self.catalog_path)
        schema = self._load_json(self.schema_path)
        if catalog is None or schema is None:
            return self.errors

        self._validate_schema(catalog, schema, schema, "$")
        if not self.errors:
            self._validate_semantics(catalog)
        return self.errors

    def _load_yaml(self, path: Path) -> Any | None:
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            self.errors.append(f"{path}: cannot load YAML: {exc}")
            return None

    def _load_json(self, path: Path) -> Any | None:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.errors.append(f"{path}: cannot load JSON Schema: {exc}")
            return None

    def _validate_schema(
        self,
        value: Any,
        schema: dict[str, Any],
        root_schema: dict[str, Any],
        path: str,
    ) -> None:
        if "$ref" in schema:
            target = self._resolve_reference(root_schema, schema["$ref"])
            if target is None:
                self.errors.append(
                    f"{path}: unsupported schema reference {schema['$ref']}"
                )
                return
            self._validate_schema(value, target, root_schema, path)
            return

        if "const" in schema and value != schema["const"]:
            self.errors.append(f"{path}: must equal {schema['const']!r}")
        if "enum" in schema and value not in schema["enum"]:
            self.errors.append(f"{path}: must be one of {schema['enum']!r}")

        if "type" in schema and not self._type_matches(value, schema["type"]):
            expected = schema["type"]
            expected_types = expected if isinstance(expected, list) else [expected]
            self.errors.append(f"{path}: expected type {' or '.join(expected_types)}")
            return

        if isinstance(value, dict):
            self._validate_object(value, schema, root_schema, path)
        elif isinstance(value, list):
            self._validate_array(value, schema, root_schema, path)
        elif isinstance(value, str):
            self._validate_string(value, schema, path)

    def _resolve_reference(
        self, root_schema: dict[str, Any], reference: str
    ) -> dict[str, Any] | None:
        if not reference.startswith("#/"):
            return None

        node: Any = root_schema
        for token in reference.removeprefix("#/").split("/"):
            if not isinstance(node, dict):
                return None
            token = token.replace("~1", "/").replace("~0", "~")
            node = node.get(token)
        return node if isinstance(node, dict) else None

    @staticmethod
    def _type_matches(value: Any, expected: str | list[str]) -> bool:
        expected_types = expected if isinstance(expected, list) else [expected]
        matchers = {
            "array": lambda item: isinstance(item, list),
            "integer": lambda item: isinstance(item, int)
            and not isinstance(item, bool),
            "null": lambda item: item is None,
            "object": lambda item: isinstance(item, dict),
            "string": lambda item: isinstance(item, str),
        }
        return any(
            expected_type in matchers and matchers[expected_type](value)
            for expected_type in expected_types
        )

    def _validate_object(
        self,
        value: dict[str, Any],
        schema: dict[str, Any],
        root_schema: dict[str, Any],
        path: str,
    ) -> None:
        for key in schema.get("required", []):
            if key not in value:
                self.errors.append(f"{path}: missing required property {key}")

        properties = schema.get("properties", {})
        for key, child in value.items():
            child_schema = properties.get(key)
            if child_schema is not None:
                self._validate_schema(child, child_schema, root_schema, f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                self.errors.append(f"{path}: unexpected property {key}")

    def _validate_array(
        self,
        value: list[Any],
        schema: dict[str, Any],
        root_schema: dict[str, Any],
        path: str,
    ) -> None:
        minimum = schema.get("minItems")
        if minimum is not None and len(value) < minimum:
            self.errors.append(f"{path}: must contain at least {minimum} item(s)")

        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(set(serialized)) != len(serialized):
                self.errors.append(f"{path}: items must be unique")

        item_schema = schema.get("items")
        if item_schema is None:
            return
        for index, child in enumerate(value):
            self._validate_schema(
                child, item_schema, root_schema, f"{path}[{index}]"
            )

    def _validate_string(
        self, value: str, schema: dict[str, Any], path: str
    ) -> None:
        minimum = schema.get("minLength")
        if minimum is not None and len(value) < minimum:
            self.errors.append(
                f"{path}: must contain at least {minimum} character(s)"
            )

        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            self.errors.append(f"{path}: does not match {pattern}")

        if schema.get("format") == "date":
            try:
                date.fromisoformat(value)
            except ValueError:
                self.errors.append(f"{path}: must be an ISO 8601 date")

    def _validate_semantics(self, catalog: dict[str, Any]) -> None:
        metadata = catalog["catalog"]
        requirements = catalog["requirements"]
        self._validate_source_registration(
            metadata["source_key"],
            metadata["source_status"],
            "$.catalog",
        )
        self._validate_unique_ids(requirements)

        for index, requirement in enumerate(requirements):
            path = f"$.requirements[{index}]"
            self._validate_identifier_consistency(
                requirement, metadata["source_version"], path
            )
            self._validate_source_snapshot(requirement, metadata, path)
            self._validate_repository_reference(
                requirement["control_ref"], f"{path}.control_ref"
            )
            self._validate_control_document_metadata(requirement, metadata, path)
            for reference_index, reference in enumerate(
                requirement["mapping_assessment_refs"]
            ):
                self._validate_repository_reference(
                    reference,
                    f"{path}.mapping_assessment_refs[{reference_index}]",
                )
            self._validate_threat_mappings(requirement, path)
            self._validate_review_gate(requirement, path)

    def _validate_source_registration(
        self, source_key: str, source_status: str, path: str
    ) -> None:
        registry_path = self.repository_root / "sources/registry.yaml"
        if not registry_path.is_file():
            return

        registry = self._load_yaml(registry_path)
        if registry is None:
            return

        registered_source = registry.get("sources", {}).get(source_key)
        if registered_source is None:
            self.errors.append(
                f"{path}.source_key: {source_key!r} is absent from "
                "sources/registry.yaml"
            )
            return

        registered_status = registered_source.get("status")
        if source_status != registered_status:
            self.errors.append(
                f"{path}.source_status: {source_status!r} does not match "
                f"sources/registry.yaml status {registered_status!r}"
            )

    def _validate_unique_ids(self, requirements: list[dict[str, Any]]) -> None:
        counts: dict[str, int] = {}
        for requirement in requirements:
            versioned_id = requirement["versioned_id"]
            counts[versioned_id] = counts.get(versioned_id, 0) + 1
        for versioned_id, count in counts.items():
            if count > 1:
                self.errors.append(
                    f"$.requirements: duplicate versioned_id {versioned_id}"
                )

    def _validate_identifier_consistency(
        self, requirement: dict[str, Any], source_version: str, path: str
    ) -> None:
        requirement_id = requirement["requirement_id"]
        expected = f"v{source_version}-{requirement_id}"
        if requirement["versioned_id"] != expected:
            self.errors.append(
                f"{path}.versioned_id: expected {expected} "
                "from source_version and requirement_id"
            )

        match = re.fullmatch(r"(C\d+)\.(\d+)\.\d+", requirement_id)
        if match is None:
            return

        expected_family = match.group(1)
        expected_section = f"{match.group(1)}.{match.group(2)}"
        if requirement["family"]["id"] != expected_family:
            self.errors.append(f"{path}.family.id: expected {expected_family}")
        if requirement["section"]["id"] != expected_section:
            self.errors.append(f"{path}.section.id: expected {expected_section}")

    def _validate_source_snapshot(
        self,
        requirement: dict[str, Any],
        metadata: dict[str, Any],
        path: str,
    ) -> None:
        if metadata["source_key"] != "owasp-aisvs":
            return

        revision = metadata["upstream_revision"]
        urls = {
            "upstream_url": requirement["upstream_url"],
            "research_source.url": requirement["research_source"]["url"],
        }
        for field, url in urls.items():
            if f"/blob/{revision}/" not in url:
                self.errors.append(
                    f"{path}.{field}: must pin catalog upstream_revision {revision}"
                )

    def _validate_threat_mappings(
        self, requirement: dict[str, Any], path: str
    ) -> None:
        identities: set[tuple[str, str, str]] = set()

        for index, mapping in enumerate(requirement["threat_mappings"]):
            mapping_path = f"{path}.threat_mappings[{index}]"
            self._validate_source_registration(
                mapping["source_key"],
                mapping["source_status"],
                mapping_path,
            )

            revision = mapping["upstream_revision"]
            if revision not in mapping["source_url"]:
                self.errors.append(
                    f"{mapping_path}.source_url: must pin mapping "
                    f"upstream_revision {revision}"
                )

            relationship_is_context = mapping["relationship"] == "context"
            strength_is_context = mapping["strength"] == "context"
            if relationship_is_context != strength_is_context:
                self.errors.append(
                    f"{mapping_path}: relationship and strength must both be "
                    "context, or neither may be context"
                )

            identity = (
                mapping["source_key"],
                mapping["source_version"],
                mapping["identifier"],
            )
            if identity in identities:
                self.errors.append(
                    f"{mapping_path}: duplicate threat mapping "
                    f"{mapping['source_key']}:{mapping['source_version']}:"
                    f"{mapping['identifier']}"
                )
            identities.add(identity)

    def _validate_repository_reference(
        self, reference: str | None, path: str
    ) -> None:
        if reference is None:
            return

        relative_path = reference.split("#", 1)[0]
        resolved = (self.repository_root / relative_path).resolve()
        if not resolved.is_relative_to(self.repository_root):
            self.errors.append(f"{path}: reference escapes the repository root")
            return
        if not resolved.is_file():
            self.errors.append(f"{path}: dangling reference {reference}")

    def _validate_control_document_metadata(
        self,
        requirement: dict[str, Any],
        catalog_metadata: dict[str, Any],
        path: str,
    ) -> None:
        reference = requirement["control_ref"]
        if reference is None:
            return

        document_path = (self.repository_root / reference).resolve()
        if (
            not document_path.is_relative_to(self.repository_root)
            or not document_path.is_file()
        ):
            return

        try:
            lines = document_path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            self.errors.append(f"{path}.control_ref: cannot read front matter: {exc}")
            return

        if not lines or lines[0] != "---":
            self.errors.append(
                f"{path}.control_ref: control document must start with YAML "
                "front matter"
            )
            return

        try:
            closing_delimiter = lines.index("---", 1)
        except ValueError:
            self.errors.append(
                f"{path}.control_ref: control document front matter is not closed"
            )
            return

        try:
            front_matter = yaml.safe_load("\n".join(lines[1:closing_delimiter]))
        except yaml.YAMLError as exc:
            self.errors.append(
                f"{path}.control_ref: cannot parse control document front matter: {exc}"
            )
            return

        if not isinstance(front_matter, dict):
            self.errors.append(
                f"{path}.control_ref: control document front matter must be an object"
            )
            return

        expected_metadata = {
            "versioned_id": requirement["versioned_id"],
            "source_key": catalog_metadata["source_key"],
            "source_version": catalog_metadata["source_version"],
            "source_status": catalog_metadata["source_status"],
            "upstream_revision": catalog_metadata["upstream_revision"],
            "upstream_url": requirement["upstream_url"],
            "research_url": requirement["research_source"]["url"],
            "maturity": requirement["maturity"],
            "review_status": requirement["review_status"],
            "last_reviewed": requirement["last_reviewed"],
            "reviewed_by": requirement["reviewed_by"],
            "review_scope": requirement["review_scope"],
            "review_evidence": requirement["review_evidence"],
            "mapping_assessment_refs": requirement["mapping_assessment_refs"],
        }

        for field, expected in expected_metadata.items():
            actual = front_matter.get(field)
            if actual != expected:
                self.errors.append(
                    f"{path}.control_ref front matter {field}: expected "
                    f"{expected!r}, found {actual!r}"
                )

    def _validate_review_gate(
        self, requirement: dict[str, Any], path: str
    ) -> None:
        if (
            requirement["maturity"] == "verifiable"
            and requirement["control_ref"] is None
        ):
            self.errors.append(f"{path}: verifiable maturity requires control_ref")

        if requirement["review_status"] != "reviewed":
            return

        review_fields = {
            "last_reviewed": requirement["last_reviewed"],
            "reviewed_by": requirement["reviewed_by"],
            "review_scope": requirement["review_scope"],
            "review_evidence": requirement["review_evidence"],
        }
        for field, value in review_fields.items():
            if value is None or value == "" or value == []:
                self.errors.append(
                    f"{path}.{field}: required when review_status is reviewed"
                )

        for index, mapping in enumerate(requirement["threat_mappings"]):
            if mapping["status"] != "validated":
                self.errors.append(
                    f"{path}.threat_mappings[{index}].status: must be validated "
                    "when review_status is reviewed"
                )


def main(argv: list[str]) -> int:
    repository_root = Path(__file__).resolve().parents[2]
    catalog_path = (
        Path(argv[1])
        if len(argv) > 1
        else repository_root / "controls/catalog.yaml"
    )
    schema_path = (
        Path(argv[2])
        if len(argv) > 2
        else repository_root / "controls/schema/control-catalog.schema.json"
    )
    validator = CatalogValidator(
        catalog_path=catalog_path,
        schema_path=schema_path,
        repository_root=repository_root,
    )
    errors = validator.validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {catalog_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
