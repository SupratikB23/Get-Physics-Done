# Canonical Schema Discipline

Use the schema and template files already listed in the prompt as the authority. Do not invent hidden fields, extra keys, placeholder fallbacks, flattened shapes, or alternate JSON payloads from prior runs.

If a field is hard-enforced, surface it in model-visible schema text before asking the model to satisfy it. Keep required IDs exact and non-empty.

For project-scoping work, keep `project_contract` literal and preserve cross-referenced IDs, gate state, and approval blockers exactly.

For publication and review artifacts, treat `VERIFICATION.md`, `contract_results`, `comparison_verdicts`, `REVIEW-LEDGER{round_suffix}.json`, `REFEREE-DECISION{round_suffix}.json`, `manuscript_path`, and `manuscript_sha256` as hard contracts. Do not infer fallback review heuristics or a second JSON shape from earlier rounds.
