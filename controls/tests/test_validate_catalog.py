"""Regression tests for the control catalog validator."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from controls.scripts.validate_catalog import CatalogValidator  # noqa: E402


class CatalogValidatorTest(unittest.TestCase):
    catalog_path = REPOSITORY_ROOT / "controls/catalog.yaml"
    schema_path = (
        REPOSITORY_ROOT / "controls/schema/control-catalog.schema.json"
    )

    def test_repository_catalog_is_valid(self) -> None:
        self.assertEqual(
            [],
            self._validator(self.catalog_path, REPOSITORY_ROOT).validate(),
        )

    def test_rejects_duplicate_versioned_ids(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"].append(
                copy.deepcopy(catalog["requirements"][0])
            )
        )
        self.assertTrue(
            any("duplicate versioned_id v1.0-C5.2.5" in error for error in errors)
        )

    def test_rejects_invalid_maturity(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                maturity="documented"
            )
        )
        self.assertTrue(any("must be one of" in error for error in errors))

    def test_rejects_inconsistent_versioned_identifier(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                versioned_id="v1.0-C5.2.6"
            )
        )
        self.assertTrue(any("expected v1.0-C5.2.5" in error for error in errors))

    def test_rejects_source_url_that_does_not_pin_catalog_revision(self) -> None:
        def change_research_url(catalog: dict[str, Any]) -> None:
            catalog["requirements"][0]["research_source"]["url"] = (
                "https://github.com/OWASP/AISVS/blob/main/1.0/research/README.md"
            )

        errors = self._validate_modified_catalog(change_research_url)
        self.assertTrue(
            any("must pin catalog upstream_revision" in error for error in errors)
        )

    def test_rejects_dangling_control_reference(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                control_ref=(
                    "controls/control-records/c05-access-control-and-identity/"
                    "v1.0-c5.2.5-missing.md"
                )
            )
        )
        self.assertTrue(any("dangling reference" in error for error in errors))

    def test_rejects_control_reference_in_wrong_family_directory(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                control_ref=(
                    "controls/control-records/c06-model-supply-chain/"
                    "v1.0-c5.2.5-missing.md"
                )
            )
        )
        self.assertTrue(
            any("family directory must start with c05-" in error for error in errors)
        )

    def test_rejects_control_filename_with_wrong_requirement_id(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                control_ref=(
                    "controls/control-records/c05-access-control-and-identity/"
                    "v1.0-c5.2.6-missing.md"
                )
            )
        )
        self.assertTrue(
            any("filename must start with v1.0-c5.2.5-" in error for error in errors)
        )

    def test_rejects_dangling_mapping_assessment_reference(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                mapping_assessment_refs=["mappings/missing.yaml"]
            )
        )
        self.assertTrue(any("dangling reference" in error for error in errors))

    def test_rejects_control_document_metadata_drift(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                review_scope="Catalog-only review scope"
            )
        )
        self.assertTrue(
            any("front matter review_scope" in error for error in errors)
        )

    def test_verifiable_control_requires_control_document(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                maturity="verifiable", control_ref=None
            )
        )
        self.assertTrue(
            any("verifiable maturity requires control_ref" in error for error in errors)
        )

    def test_rejects_unregistered_threat_source(self) -> None:
        def change_source(catalog: dict[str, Any]) -> None:
            catalog["requirements"][0]["threat_mappings"][0]["source_key"] = (
                "unknown-source"
            )

        errors = self._validate_modified_catalog(change_source)
        self.assertTrue(
            any("absent from sources/registry.yaml" in error for error in errors)
        )

    def test_rejects_threat_source_status_mismatch(self) -> None:
        def change_status(catalog: dict[str, Any]) -> None:
            catalog["requirements"][0]["threat_mappings"][0]["source_status"] = (
                "stable"
            )

        errors = self._validate_modified_catalog(change_status)
        self.assertTrue(
            any(
                "does not match sources/registry.yaml status" in error
                for error in errors
            )
        )

    def test_rejects_threat_url_without_mapping_revision(self) -> None:
        def change_source_url(catalog: dict[str, Any]) -> None:
            catalog["requirements"][0]["threat_mappings"][0]["source_url"] = (
                "https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/"
                "ATLAS-2026.08.yaml"
            )

        errors = self._validate_modified_catalog(change_source_url)
        self.assertTrue(
            any("must pin mapping upstream_revision" in error for error in errors)
        )

    def test_rejects_context_relationship_with_mitigation_strength(self) -> None:
        def change_strength(catalog: dict[str, Any]) -> None:
            catalog["requirements"][0]["threat_mappings"][1]["strength"] = (
                "partial"
            )

        errors = self._validate_modified_catalog(change_strength)
        self.assertTrue(
            any(
                "relationship and strength must both be context" in error
                for error in errors
            )
        )

    def test_rejects_duplicate_threat_mapping_identity(self) -> None:
        def duplicate_mapping(catalog: dict[str, Any]) -> None:
            catalog["requirements"][0]["threat_mappings"].append(
                copy.deepcopy(catalog["requirements"][0]["threat_mappings"][0])
            )

        errors = self._validate_modified_catalog(duplicate_mapping)
        self.assertTrue(any("duplicate threat mapping" in error for error in errors))

    def test_reviewed_control_requires_human_review_metadata(self) -> None:
        errors = self._validate_modified_catalog(
            lambda catalog: catalog["requirements"][0].update(
                review_status="reviewed"
            )
        )
        for field in (
            "last_reviewed",
            "reviewed_by",
            "review_scope",
            "review_evidence",
        ):
            self.assertTrue(
                any(f"{field}: required" in error for error in errors),
                field,
            )

    def test_reviewed_control_requires_validated_threat_mappings(self) -> None:
        def mark_reviewed(catalog: dict[str, Any]) -> None:
            requirement = catalog["requirements"][0]
            requirement.update(
                review_status="reviewed",
                last_reviewed="2026-09-03",
                reviewed_by=["human-reviewer"],
                review_scope="Complete Golden Control",
                review_evidence="https://example.invalid/reviews/1",
            )

        errors = self._validate_modified_catalog(mark_reviewed)
        self.assertTrue(
            any(
                "must be validated when review_status is reviewed" in error
                for error in errors
            )
        )

    def _validator(
        self, catalog_path: Path, repository_root: Path
    ) -> CatalogValidator:
        return CatalogValidator(
            catalog_path=catalog_path,
            schema_path=self.schema_path,
            repository_root=repository_root,
        )

    def _validate_modified_catalog(
        self, mutate: Callable[[dict[str, Any]], None]
    ) -> list[str]:
        catalog = yaml.safe_load(self.catalog_path.read_text(encoding="utf-8"))
        mutate(catalog)

        with tempfile.TemporaryDirectory(prefix="control-catalog-test-") as directory:
            repository_root = Path(directory)
            temporary_catalog = repository_root / "controls/catalog.yaml"
            temporary_catalog.parent.mkdir(parents=True)
            temporary_catalog.write_text(
                yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8"
            )

            source_registry = repository_root / "sources/registry.yaml"
            source_registry.parent.mkdir(parents=True)
            source_registry.write_text(
                (REPOSITORY_ROOT / "sources/registry.yaml").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )

            control_ref = catalog["requirements"][0]["control_ref"]
            if control_ref is not None:
                temporary_control = repository_root / control_ref
                original_control = REPOSITORY_ROOT / control_ref
                if original_control.is_file():
                    temporary_control.parent.mkdir(parents=True)
                    temporary_control.write_text(
                        original_control.read_text(encoding="utf-8"),
                        encoding="utf-8",
                    )
            return self._validator(temporary_catalog, repository_root).validate()


if __name__ == "__main__":
    unittest.main()
