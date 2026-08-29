#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_PATH = ROOT / "data" / "ontologia" / "bmen_v1.json"
EVIDENCE_PATH = ROOT / "data" / "ontologia" / "evidencias_fontes.json"
MATRIX_PATH = ROOT / "data" / "ontologia" / "matriz_condicao_dominio_intervencao.csv"
MANIFEST_PATH = ROOT / "data" / "ontologia" / "datasets_manifest.json"
CONCEPTS_PATH = ROOT / "concepts.json"
ALIASES_PATH = ROOT / "aliases.json"
ONTOLOGY_DIR = ROOT / "ontology"
DIFFERENTIALS_DIR = ROOT / "differentials"

SNAKE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
EVIDENCE_ID_RE = re.compile(r"^ev_[a-z0-9]+(?:_[a-z0-9]+)*$")
SOURCE_ID_RE = re.compile(r"^src_[a-z0-9]+(?:_[a-z0-9]+)*$")
CONCEPT_ID_RE = re.compile(r"^[A-Z]+_[A-Z0-9]+_[A-Z]+_[0-9]{3}$")
CONCEPT_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
CRITERION_RE = re.compile(r"^[A-E][0-9]*$")
CONCEPT_CONDITIONS = {"TEA", "TDAH", "LINGUAGEM", "ANSIEDADE", "SENSORIAL"}
CONCEPT_ALLOWED_KEYS = {
    "id", "concept", "label", "condition", "criterion", "domain", "domain_id",
    "weight", "description", "age_relevant", "created_at", "updated_at",
}
CONCEPT_REQUIRED_KEYS = ["id", "concept", "label", "condition", "criterion", "domain", "weight", "description"]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check(condition, message, errors):
    if not condition:
        errors.append(message)


def check_required(obj, fields, where, errors):
    for field in fields:
        check(field in obj, f"{where}: campo obrigatório ausente '{field}'", errors)


def validate_ontology(ontology, errors):
    check_required(
        ontology,
        ["meta", "domains", "conditions", "signs", "assessments", "interventions", "relations"],
        "bmen_v1",
        errors,
    )
    if errors:
        return

    meta = ontology["meta"]
    check_required(
        meta,
        ["ontology_id", "name", "version", "language", "created_at", "namespaces", "scope"],
        "bmen_v1.meta",
        errors,
    )
    if "ontology_id" in meta:
        check(bool(SNAKE_RE.fullmatch(meta["ontology_id"])), "bmen_v1.meta.ontology_id deve ser snake_case", errors)
    if "version" in meta:
        check(bool(SEMVER_RE.fullmatch(meta["version"])), "bmen_v1.meta.version deve seguir semver (x.y.z)", errors)
    if "namespaces" in meta and isinstance(meta["namespaces"], dict):
        check("bmen" in meta["namespaces"], "bmen_v1.meta.namespaces deve conter prefixo 'bmen'", errors)

    domains = ontology.get("domains", [])
    domain_ids = set()
    for i, domain in enumerate(domains):
        where = f"bmen_v1.domains[{i}]"
        check_required(domain, ["id", "label", "description"], where, errors)
        domain_id = domain.get("id")
        if isinstance(domain_id, str):
            check(bool(SNAKE_RE.fullmatch(domain_id)), f"{where}.id deve ser snake_case", errors)
            check(domain_id not in domain_ids, f"{where}.id duplicado: {domain_id}", errors)
            domain_ids.add(domain_id)

    condition_ids = set()
    for i, condition in enumerate(ontology.get("conditions", [])):
        where = f"bmen_v1.conditions[{i}]"
        check_required(condition, ["id", "label", "aliases", "category", "affects_domains", "source_ids"], where, errors)
        cond_id = condition.get("id")
        if isinstance(cond_id, str):
            check(bool(SNAKE_RE.fullmatch(cond_id)), f"{where}.id deve ser snake_case", errors)
            check(cond_id not in condition_ids, f"{where}.id duplicado: {cond_id}", errors)
            condition_ids.add(cond_id)
        for domain_id in condition.get("affects_domains", []):
            check(domain_id in domain_ids, f"{where}.affects_domains referencia dominio inexistente: {domain_id}", errors)
        for source_id in condition.get("source_ids", []):
            check(bool(SOURCE_ID_RE.fullmatch(source_id)), f"{where}.source_ids inválido: {source_id}", errors)

    sign_ids = set()
    for i, sign in enumerate(ontology.get("signs", [])):
        where = f"bmen_v1.signs[{i}]"
        check_required(sign, ["id", "label", "related_domains"], where, errors)
        sign_id = sign.get("id")
        if isinstance(sign_id, str):
            check(bool(SNAKE_RE.fullmatch(sign_id)), f"{where}.id deve ser snake_case", errors)
            check(sign_id not in sign_ids, f"{where}.id duplicado: {sign_id}", errors)
            sign_ids.add(sign_id)
        for domain_id in sign.get("related_domains", []):
            check(domain_id in domain_ids, f"{where}.related_domains referencia dominio inexistente: {domain_id}", errors)

    assessment_ids = set()
    for i, assessment in enumerate(ontology.get("assessments", [])):
        where = f"bmen_v1.assessments[{i}]"
        check_required(assessment, ["id", "label", "type", "target_domains", "source_ids"], where, errors)
        assessment_id = assessment.get("id")
        if isinstance(assessment_id, str):
            check(bool(SNAKE_RE.fullmatch(assessment_id)), f"{where}.id deve ser snake_case", errors)
            check(assessment_id not in assessment_ids, f"{where}.id duplicado: {assessment_id}", errors)
            assessment_ids.add(assessment_id)
        for domain_id in assessment.get("target_domains", []):
            check(domain_id in domain_ids, f"{where}.target_domains referencia dominio inexistente: {domain_id}", errors)
        for source_id in assessment.get("source_ids", []):
            check(bool(SOURCE_ID_RE.fullmatch(source_id)), f"{where}.source_ids inválido: {source_id}", errors)

    intervention_ids = set()
    allowed_indication_ids = condition_ids | sign_ids
    for i, intervention in enumerate(ontology.get("interventions", [])):
        where = f"bmen_v1.interventions[{i}]"
        check_required(
            intervention,
            ["id", "label", "type", "target_domains", "indications", "evidence_ids", "source_ids"],
            where,
            errors,
        )
        intervention_id = intervention.get("id")
        if isinstance(intervention_id, str):
            check(bool(SNAKE_RE.fullmatch(intervention_id)), f"{where}.id deve ser snake_case", errors)
            check(intervention_id not in intervention_ids, f"{where}.id duplicado: {intervention_id}", errors)
            intervention_ids.add(intervention_id)
        for domain_id in intervention.get("target_domains", []):
            check(domain_id in domain_ids, f"{where}.target_domains referencia dominio inexistente: {domain_id}", errors)
        for indication_id in intervention.get("indications", []):
            check(indication_id in allowed_indication_ids, f"{where}.indications referencia entidade inexistente: {indication_id}", errors)
        for evidence_id in intervention.get("evidence_ids", []):
            check(bool(EVIDENCE_ID_RE.fullmatch(evidence_id)), f"{where}.evidence_ids inválido: {evidence_id}", errors)
        for source_id in intervention.get("source_ids", []):
            check(bool(SOURCE_ID_RE.fullmatch(source_id)), f"{where}.source_ids inválido: {source_id}", errors)


def validate_evidence(evidence_data, intervention_ids, errors):
    check_required(evidence_data, ["meta", "evidences", "sources"], "evidencias_fontes", errors)
    if errors:
        return

    meta = evidence_data["meta"]
    check_required(meta, ["name", "version", "language", "created_at"], "evidencias_fontes.meta", errors)
    if "version" in meta:
        check(bool(SEMVER_RE.fullmatch(meta["version"])), "evidencias_fontes.meta.version deve seguir semver (x.y.z)", errors)

    source_ids = set()
    for i, source in enumerate(evidence_data.get("sources", [])):
        where = f"evidencias_fontes.sources[{i}]"
        check_required(source, ["id", "title", "authors", "year", "url_or_doi", "notes"], where, errors)
        source_id = source.get("id")
        if isinstance(source_id, str):
            check(bool(SOURCE_ID_RE.fullmatch(source_id)), f"{where}.id inválido: {source_id}", errors)
            check(source_id not in source_ids, f"{where}.id duplicado: {source_id}", errors)
            source_ids.add(source_id)

    evidence_ids = set()
    for i, evidence in enumerate(evidence_data.get("evidences", [])):
        where = f"evidencias_fontes.evidences[{i}]"
        check_required(evidence, ["id", "statement", "level", "supports_interventions", "source_ids"], where, errors)
        evidence_id = evidence.get("id")
        if isinstance(evidence_id, str):
            check(bool(EVIDENCE_ID_RE.fullmatch(evidence_id)), f"{where}.id inválido: {evidence_id}", errors)
            check(evidence_id not in evidence_ids, f"{where}.id duplicado: {evidence_id}", errors)
            evidence_ids.add(evidence_id)

        for intervention_id in evidence.get("supports_interventions", []):
            check(intervention_id in intervention_ids, f"{where}.supports_interventions referencia intervenção inexistente: {intervention_id}", errors)
        for source_id in evidence.get("source_ids", []):
            check(source_id in source_ids, f"{where}.source_ids referencia fonte inexistente: {source_id}", errors)


def validate_matrix(intervention_ids, condition_ids, domain_ids, errors):
    required_columns = {
        "condition_id",
        "condition_label",
        "domain_id",
        "domain_label",
        "intervention_id",
        "intervention_label",
        "intervention_type",
        "priority",
        "notes",
    }

    with MATRIX_PATH.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = set(reader.fieldnames or [])
        missing = required_columns - columns
        check(not missing, f"matriz_condicao_dominio_intervencao.csv: colunas ausentes {sorted(missing)}", errors)

        for index, row in enumerate(reader, start=2):
            condition_id = row.get("condition_id", "")
            domain_id = row.get("domain_id", "")
            intervention_id = row.get("intervention_id", "")
            check(condition_id in condition_ids, f"CSV linha {index}: condition_id inexistente '{condition_id}'", errors)
            check(domain_id in domain_ids, f"CSV linha {index}: domain_id inexistente '{domain_id}'", errors)
            check(intervention_id in intervention_ids, f"CSV linha {index}: intervention_id inexistente '{intervention_id}'", errors)


def validate_manifest(errors):
    manifest = load_json(MANIFEST_PATH)
    check_required(manifest, ["dataset_release", "generated_at", "datasets"], "datasets_manifest", errors)
    for i, dataset in enumerate(manifest.get("datasets", [])):
        where = f"datasets_manifest.datasets[{i}]"
        check_required(dataset, ["id", "file", "format", "schema", "version", "description", "contains_sensitive_data"], where, errors)
        file_name = dataset.get("file")
        if isinstance(file_name, str):
            dataset_file = MANIFEST_PATH.parent / file_name
            check(dataset_file.exists(), f"{where}.file referencia arquivo inexistente: {file_name}", errors)


def validate_concepts(domain_ids, errors):
    concepts = load_json(CONCEPTS_PATH)
    check(isinstance(concepts, list) and len(concepts) > 0, "concepts.json deve ser uma lista não vazia", errors)
    concept_ids = set()
    concept_names = set()
    concept_index = {}
    if not isinstance(concepts, list):
        return concept_ids, concept_names, concept_index

    for i, concept in enumerate(concepts):
        where = f"concepts.json[{i}]"
        if not isinstance(concept, dict):
            errors.append(f"{where}: deve ser um objeto")
            continue
        check_required(concept, CONCEPT_REQUIRED_KEYS, where, errors)
        extra_keys = set(concept.keys()) - CONCEPT_ALLOWED_KEYS
        check(not extra_keys, f"{where}: campos não permitidos {sorted(extra_keys)}", errors)

        concept_id = concept.get("id")
        if isinstance(concept_id, str):
            check(bool(CONCEPT_ID_RE.fullmatch(concept_id)), f"{where}.id deve seguir o padrão CONDICAO_CRITERIO_DOMINIO_NUM", errors)
            check(concept_id not in concept_ids, f"{where}.id duplicado: {concept_id}", errors)
            concept_ids.add(concept_id)

        concept_name = concept.get("concept")
        if isinstance(concept_name, str):
            check(bool(CONCEPT_NAME_RE.fullmatch(concept_name)), f"{where}.concept deve ser snake_case", errors)
            concept_names.add(concept_name)

        condition = concept.get("condition")
        check(condition in CONCEPT_CONDITIONS, f"{where}.condition inválida: {condition}", errors)

        criterion = concept.get("criterion")
        if isinstance(criterion, str):
            check(bool(CRITERION_RE.fullmatch(criterion)), f"{where}.criterion inválido: {criterion}", errors)

        weight = concept.get("weight")
        check(isinstance(weight, int) and not isinstance(weight, bool) and 1 <= weight <= 10, f"{where}.weight deve ser inteiro entre 1 e 10", errors)

        description = concept.get("description")
        check(isinstance(description, str) and len(description) >= 20, f"{where}.description deve ter ao menos 20 caracteres", errors)

        domain_id = concept.get("domain_id")
        if domain_id is not None:
            check(domain_id in domain_ids, f"{where}.domain_id referencia domínio inexistente em bmen_v1: {domain_id}", errors)

        if isinstance(condition, str) and isinstance(criterion, str) and isinstance(concept_id, str):
            concept_index.setdefault((condition, criterion), []).append(concept_id)

    return concept_ids, concept_names, concept_index


def validate_aliases(concept_names, errors):
    try:
        with ALIASES_PATH.open("r", encoding="utf-8") as f:
            content = f.read().strip()
        aliases = json.loads(content) if content else None
    except json.JSONDecodeError:
        errors.append("aliases.json: JSON inválido")
        return

    check(isinstance(aliases, list) and len(aliases) > 0, "aliases.json deve ser uma lista não vazia", errors)
    if not isinstance(aliases, list):
        return

    covered = set()
    for i, entry in enumerate(aliases):
        where = f"aliases.json[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{where}: deve ser um objeto")
            continue
        check_required(entry, ["concept", "condition", "criterion", "aliases"], where, errors)
        concept_name = entry.get("concept")
        check(concept_name in concept_names, f"{where}.concept referencia conceito inexistente em concepts.json: {concept_name}", errors)
        alias_list = entry.get("aliases")
        check(isinstance(alias_list, list) and len(alias_list) > 0, f"{where}.aliases deve ser lista não vazia", errors)
        if isinstance(concept_name, str):
            covered.add(concept_name)

    missing = concept_names - covered
    check(not missing, f"aliases.json: conceitos de concepts.json sem aliases cadastrados: {sorted(missing)}", errors)


def validate_dsm_ontology_files(concept_ids, concept_index, errors):
    for condition_key, filename in [("TEA", "tea.json"), ("TDAH", "tdah.json")]:
        path = ONTOLOGY_DIR / filename
        where = f"ontology/{filename}"
        if not path.exists():
            errors.append(f"{where}: arquivo ausente")
            continue
        data = load_json(path)
        check_required(data, ["id", "label", "version", "description", "criteria"], where, errors)
        if not bool(SEMVER_RE.fullmatch(str(data.get("version", "")))):
            errors.append(f"{where}.version deve seguir semver (x.y.z)")

        linked = set()
        for crit_key, crit in data.get("criteria", {}).items():
            groups = crit.get("subcriteria") or crit.get("presentations") or {}
            for sub_key, sub in groups.items():
                sub_concepts = sub.get("concepts", [])
                for concept_id in sub_concepts:
                    check(
                        concept_id in concept_ids,
                        f"{where}.criteria.{crit_key}.{sub_key}.concepts referencia conceito inexistente: {concept_id}",
                        errors,
                    )
                    linked.add(concept_id)
                for concept_id in concept_index.get((condition_key, sub_key), []):
                    check(
                        concept_id in sub_concepts,
                        f"{where}.criteria.{crit_key}.{sub_key}: concepts.json define {concept_id} mas ele não está vinculado neste arquivo",
                        errors,
                    )


def validate_free_ontology_files(errors):
    for filename in ["ansiedade.json", "linguagem.json", "sensorial.json"]:
        path = ONTOLOGY_DIR / filename
        where = f"ontology/{filename}"
        check(path.exists(), f"{where}: arquivo ausente", errors)
        if not path.exists():
            continue
        data = load_json(path)
        check_required(data, ["id", "label", "version", "description"], where, errors)
        version = data.get("version", "")
        check(bool(SEMVER_RE.fullmatch(str(version))), f"{where}.version deve seguir semver (x.y.z)", errors)


def validate_differentials(errors):
    path = DIFFERENTIALS_DIR / "tea-vs-tdah.json"
    where = "differentials/tea-vs-tdah.json"
    check(path.exists(), f"{where}: arquivo ausente", errors)
    if not path.exists():
        return
    data = load_json(path)
    check_required(data, ["id", "title", "version", "key_distinctions"], where, errors)
    key_distinctions = data.get("key_distinctions", [])
    check(isinstance(key_distinctions, list) and len(key_distinctions) > 0, f"{where}.key_distinctions deve ser lista não vazia", errors)
    for i, item in enumerate(key_distinctions):
        check_required(item, ["domain", "tea", "tdah"], f"{where}.key_distinctions[{i}]", errors)


def main():
    errors = []

    ontology = load_json(ONTOLOGY_PATH)
    validate_ontology(ontology, errors)

    condition_ids = {item["id"] for item in ontology.get("conditions", []) if isinstance(item, dict) and "id" in item}
    domain_ids = {item["id"] for item in ontology.get("domains", []) if isinstance(item, dict) and "id" in item}
    intervention_ids = {item["id"] for item in ontology.get("interventions", []) if isinstance(item, dict) and "id" in item}

    evidence_data = load_json(EVIDENCE_PATH)
    validate_evidence(evidence_data, intervention_ids, errors)

    evidence_ids = {item["id"] for item in evidence_data.get("evidences", []) if isinstance(item, dict) and "id" in item}
    for i, intervention in enumerate(ontology.get("interventions", [])):
        where = f"bmen_v1.interventions[{i}]"
        for evidence_id in intervention.get("evidence_ids", []):
            check(evidence_id in evidence_ids, f"{where}.evidence_ids referencia evidencia inexistente: {evidence_id}", errors)

    source_ids = {item["id"] for item in evidence_data.get("sources", []) if isinstance(item, dict) and "id" in item}
    for group_name in ["conditions", "assessments", "interventions"]:
        for i, entity in enumerate(ontology.get(group_name, [])):
            where = f"bmen_v1.{group_name}[{i}]"
            for source_id in entity.get("source_ids", []):
                check(source_id in source_ids, f"{where}.source_ids referencia fonte inexistente: {source_id}", errors)

    validate_matrix(intervention_ids, condition_ids, domain_ids, errors)
    validate_manifest(errors)

    concept_ids, concept_names, concept_index = validate_concepts(domain_ids, errors)
    validate_aliases(concept_names, errors)
    validate_dsm_ontology_files(concept_ids, concept_index, errors)
    validate_free_ontology_files(errors)
    validate_differentials(errors)

    if errors:
        print("Falhas de validação detectadas:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("Validação concluída com sucesso.")


if __name__ == "__main__":
    main()
