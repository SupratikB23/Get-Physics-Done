Shared manuscript-root publication preflight.

For any resumed manuscript, strict preflight reads `ARTIFACT-MANIFEST.json`, `BIBLIOGRAPHY-AUDIT.json`, and `reproducibility-manifest.json` from the resolved manuscript directory itself. Resolve the active manuscript entry point only from `paper/`, `manuscript/`, or `draft/`, using `ARTIFACT-MANIFEST.json` first and `PAPER-CONFIG.json` second. Do not use ad hoc wildcard discovery or first-match filename scans.

Keep all manuscript-local support artifacts rooted at the same explicit manuscript directory. Treat `gpd paper-build` as the authoritative step that regenerates `BIBLIOGRAPHY-AUDIT.json` for the resolved manuscript root. In strict mode, `bibliography_audit_clean` and `reproducibility_ready` must pass before review or packaging proceeds.
