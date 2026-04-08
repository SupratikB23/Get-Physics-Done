---
reference_version: 1
---

# Bibliography Advanced Search Protocols

Load this reference only when the bibliography task requires more than ordinary citation verification or manuscript auditing. Typical triggers:

- frontier literature mapping
- structured INSPIRE/arXiv lookups for incomplete metadata
- citation-network analysis
- related-work section generation

For routine `.bib` maintenance, hallucination checks, retraction checks, and citation-completeness audits, stay on the core bibliographer prompt instead of loading this pack.

## INSPIRE-HEP Quick Protocol

Use INSPIRE for particle, nuclear, gravity, and mathematical-physics references when a structured match is available.

Preferred lookup order:

1. arXiv ID
2. DOI
3. INSPIRE texkey
4. author + title fragment query

Typical queries:

```text
https://inspirehep.net/api/arxiv/<arxiv-id>
https://inspirehep.net/api/doi/<doi>
https://inspirehep.net/api/literature?q=texkeys:<texkey>
https://inspirehep.net/api/literature?sort=mostrecent&size=5&q=find a <author> and t <title-fragment>
```

When available, prefer INSPIRE's BibTeX export over hand-built entries:

```text
https://inspirehep.net/api/literature?q=texkeys:<texkey>&format=bibtex
```

Never guess an INSPIRE texkey.

## arXiv Category Routing

Use the narrowest category set that matches the domain before broadening:

| Domain | Primary categories | Secondary categories |
| --- | --- | --- |
| QFT / HEP | `hep-th`, `hep-ph` | `hep-lat`, `math-ph` |
| Condensed matter | `cond-mat.str-el`, `cond-mat.stat-mech` | `cond-mat.supr-con`, `cond-mat.mtrl-sci` |
| Quantum information | `quant-ph` | `cond-mat.str-el`, `cs.IT` |
| Nuclear physics | `nucl-th`, `nucl-ex` | `hep-ph`, `hep-lat` |
| Gravity / cosmology | `gr-qc`, `astro-ph.CO` | `hep-th` |
| Astrophysics | `astro-ph.HE`, `astro-ph.SR`, `astro-ph.CO` | `gr-qc`, `hep-ph` |
| AMO | `physics.atom-ph`, `quant-ph` | `physics.optics` |
| Mathematical physics | `math-ph` | `hep-th`, `math.QA` |

For cross-disciplinary work, search all relevant primary categories before expanding further.

## Citation-Network Triage

Use network analysis only for literature-review or manuscript-context work.

Core passes:

1. Forward citations: who cites the key paper?
2. Backward citations: what foundational papers does it rely on?
3. Cluster the field into:
   - foundational papers
   - same-method same-system papers
   - competing approaches
   - reconciliation / comparison papers
   - recent frontier papers

When prioritizing a limited bibliography, include in this order:

1. original derivations used directly
2. exact comparison targets
3. most-cited field-defining papers
4. same-method same-system papers
5. fair representation of competing results
6. recent directly relevant work
7. software/code papers actually used

## Related-Work Generation

For a related-work section:

1. Identify the contribution space:
   - method axis
   - system axis
2. Map the closest prior work first:
   - same method + same system
   - same system + different method
   - same method + different system
3. Organize by intellectual proximity, not chronology.
4. Verify the section includes:
   - directly comparable work
   - competing approaches
   - the most-cited foundational paper
   - recent frontier work when relevant

## When Not To Load This Pack

Do not load this reference for:

- simple key resolution from known metadata
- ordinary `.bib` deduplication or normalization
- manuscript `\cite{}` key audits
- routine hallucination or retraction checks
