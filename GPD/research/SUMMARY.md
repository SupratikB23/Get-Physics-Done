# Research Summary

**Project:** Alternative Proof Methods for Holographic Entropy Cone Inequalities
**Domain:** Holographic entanglement / quantum information theory / polyhedral geometry
**Researched:** 2026-04-05
**Confidence:** MEDIUM-HIGH

## Unified Notation

| Symbol | Quantity | Units/Dimensions | Convention Notes |
|--------|----------|------------------|------------------|
| N | Number of boundary regions (parties) | Dimensionless integer | Does NOT include the purifier; the total system has N+1 parties with purity imposed |
| S(A) | Entanglement entropy of boundary region A | Dimensionless (bits or nats) | Computed via RT formula: S(A) = Area(gamma_A) / 4G_N; we work in units where 4G_N = 1 |
| v | Entropy vector | R^{2^N - 1} | Components v_I = S(I) for each nonempty subset I of {1,...,N}; purification reduces independent components to 2^{N-1} - 1 |
| C_N | Holographic entropy cone for N parties | Polyhedral cone in R^{2^N - 1} | Following Hernandez-Cuenca (2019); defined as closure of entropy vectors realizable by RT |
| I(A:B) | Mutual information | Dimensionless | I(A:B) = S(A) + S(B) - S(AB); colon notation standard |
| I_3(A:B:C) | Tripartite information | Dimensionless | I_3 = S(A)+S(B)+S(C)-S(AB)-S(AC)-S(BC)+S(ABC); MMI is I_3 >= 0 |
| I_n | n-partite information | Dimensionless | Alternating sum following He, Headrick, Hubeny (2019); I_n = sum_{k=1}^{n} (-1)^{k+1} sum_{|J|=k} S(J) |
| f | Contraction map | Map: 2^{[N]} -> 2^{[N]} | Following Bao et al. (2015); reassigns surface segments from LHS to RHS of inequality |
| G = (V, E, w) | Weighted graph model | Vertices, edges, positive rational weights | Boundary terminals + bulk vertices; S(A) = min-cut separating A from complement |
| K-basis | Basis of entropy space from perfect tensor structures | Vectors in R^{2^N - 1} | Elements are extreme rays of HEC; all HEI coefficients non-negative in this basis |
| PMI | Pattern of marginal independence | Combinatorial data | Specifies which mutual informations I(A:B) vanish; determines extreme ray structure |
| d | Effective dimension of entropy cone | 2^{N-1} - 1 after purification | N=4: d=7; N=5: d=15; N=6: d=31 |

**Key convention choices:**

- Purification is always imposed: S(A) = S(A^c) where A^c is the complement including the purifier O. This halves the independent entropy components.
- Inequalities are written with coprime integer coefficients, positive leading term.
- The permutation group S_N acts on party labels {1,...,N}, inducing an action on subsets and hence on entropy vector components. Orbits under S_N are the natural equivalence classes.
- "Facet" means irredundant inequality defining a codimension-1 face of C_N. "Valid" means the inequality holds for all entropy vectors in C_N. Every facet is valid; not every valid inequality is a facet.

## Executive Summary

The holographic entropy cone (HEC) captures all linear constraints on entanglement entropies of boundary subregions in holographic CFTs with classical bulk duals. For N <= 4 parties, the cone is fully characterized by strong subadditivity (SSA) and monogamy of mutual information (MMI). For N = 5, Hernandez-Cuenca (2019) completely classified the cone: 372 facets falling into 8 symmetry orbits (3 inherited from lower N, 5 genuinely new) and 2267 extreme rays in 19 orbits. Two infinite families of general-N facets -- toric and generalized toric -- were proven by Czech, Liu, and Yu (2024) via explicit saturation constructions. The contraction map method, the only systematic proof technique for validity of holographic entropy inequalities, was recently proven complete for all rational HEIs (Bao, Furuya, Naskar 2025). However, contraction maps are fundamentally blind to whether a valid inequality is a facet or redundant.

This project seeks an information-theoretic proof method that bridges the gap between validity (which contraction maps handle) and facet status (which currently requires brute-force polyhedral enumeration). The two most promising theoretical bridges are: (1) the K-basis representation, where all HEI coefficients are non-negative and the pattern of zero coefficients may encode codimension structure; and (2) the marginal independence (PMI) reconstruction, which shows that purely information-theoretic data -- which mutual informations vanish -- determines the entire cone. Neither approach has yet been shown to distinguish facets from redundant inequalities, making this the central open question. The N = 5 HEC provides the ideal testbed: it is fully classified (ground truth exists) and contains 5 genuinely new facet types that any method must reproduce.

The principal risk is that facet status is a purely combinatorial property of the polyhedral cone with no clean information-theoretic characterization -- the "competing explanation" identified in the scoping contract. Mitigation requires designing the IT method to target the facet/redundant distinction from the outset (not as an afterthought to validity proofs), and testing against the full N = 5 classification at every stage. A secondary risk is that a method working at N = 4 exploits the special simplicity of that case (only 2 facet orbits) and fails to generalize. The mandatory stop condition is: if the method scales worse than contraction maps or works only for N <= 4, it should be abandoned.

## Key Findings

### Computational Approaches

The computational backbone is polyhedral cone enumeration: converting between H-representation (inequalities/facets) and V-representation (extreme rays). **lrslib** is the recommended primary tool for N >= 5, due to its O(n*d) memory per vertex (versus cddlib's O(v*d) which stores all vertices, risking memory blowup). **pycddlib** serves as a rapid-prototyping secondary tool for N = 4 and for LP-based redundancy removal. **psitip** handles Shannon-type inequality verification. Graph model entropy computation uses **NetworkX** max-flow routines on small weighted graphs. All polyhedral computations must use exact rational arithmetic -- floating-point is forbidden for facet/extreme-ray enumeration due to degeneracy sensitivity (Pitfall 9). [CONFIDENCE: HIGH]

**Core approach:**

- **lrslib (reverse search):** Vertex/facet enumeration for high-dimensional cones -- low memory, parallelizable via mplrs, used in the original N=5 computation
- **pycddlib (double description):** Python-native LP and redundancy removal -- convenient for small problems and rapid prototyping
- **psitip:** Information-theoretic inequality verification -- scriptable, supports constrained inequalities essential for testing IT method
- **NetworkX max-flow:** Graph model entropy computation -- small graph sizes make this instantaneous

### Prior Work Landscape

The field has a clear hierarchy of established results with decreasing confidence as N increases. [CONFIDENCE: HIGH for N <= 5; MEDIUM for N = 6]

**Must reproduce (benchmarks):**

- N = 4 HEC: SSA + MMI are the complete facets (Bao et al. 2015) -- the non-negotiable validation checkpoint
- N = 5 HEC: 372 facets in 8 orbits, 2267 extreme rays in 19 orbits (Hernandez-Cuenca 2019; reconfirmed by Avis & Hernandez-Cuenca 2021) -- the ground truth for the IT method
- MMI is a facet for all N >= 3 (Hayden, Headrick, Maloney 2013) -- any general-N method must confirm this
- Toric and generalized toric inequalities are facets for all N (Czech, Liu, Yu 2024) -- the only known infinite families beyond MMI

**Novel predictions (contributions):**

- IT criterion that classifies N = 5 inequalities as facet or redundant -- the core deliverable
- Structural characterization of what makes an inequality a facet versus redundant -- the theoretical insight

**Defer (future work):**

- N = 6 classification (1877 known facets, 6 mystery extreme rays, 3 now resolved via RL) -- computationally at the frontier, out of project scope
- Complete general-N facet catalogue beyond toric/generalized toric families
- Connection to majorization characterization (Hubeny et al. 2025) -- promising but too recent to build on

### Methods and Tools

Eight methods span the toolkit from established to speculative. Contraction maps (complete for validity, blind to facets) and codimension-1 saturation (definitive for facets but requires brute-force enumeration) anchor the established end. Superbalance analysis provides a cheap necessary filter for non-SA HEIs. The K-basis and PMI reconstruction are the most promising IT-geometric bridges for the novel facet criterion. Bit threads offer IT-transparent validity proofs but have no known connection to facet detection.

**Major components:**

1. **Contraction maps** -- prove validity of candidate HEIs; complete for rational coefficients; the baseline method to compare against [CONFIDENCE: HIGH]
2. **Codimension-1 saturation test** -- definitive geometric facet detection; requires 2^{N-1} - 1 linearly independent saturating vectors [CONFIDENCE: HIGH]
3. **K-basis decomposition** -- all HEI coefficients non-negative; zero-coefficient pattern may encode codimension structure [CONFIDENCE: MEDIUM-HIGH for properties; LOW for facet detection -- unproven]
4. **PMI reconstruction** -- IT data determines the cone; facets may correspond to specific PMI patterns on saturating faces [CONFIDENCE: MEDIUM for reconstruction; LOW for facet detection -- unproven]
5. **Superbalance filter** -- necessary condition for primitive (non-SA) HEIs; cheap combinatorial first-pass screen [CONFIDENCE: HIGH]

### Critical Pitfalls

13 pitfalls identified, with clear severity ranking. The top 5 are:

1. **Confusing validity with facet status (Pitfall 1, CRITICAL)** -- A contraction map proves an inequality holds, not that it is irredundant. The N=4 benchmark must separately verify both properties. Prevention: maintain strict two-column classification (valid? / facet?) for every inequality.

2. **IT method mimics contraction maps (Pitfall 2, CRITICAL)** -- The completeness result (arXiv:2506.18086) means any alternative validity proof is logically equivalent to a contraction map. The IT method must extract facet information that contraction maps cannot. Prevention: design for the facet/redundant distinction from day one; reject any method that reduces to contraction map existence.

3. **2^N dimensional explosion (Pitfall 3, CRITICAL)** -- Entropy vector space dimension doubles with each party. N=4 is deceptively easy; N=5 requires careful algorithmic choices. Prevention: exploit S_N symmetry; use lrslib (not cddlib) for N >= 5; set computational budgets.

4. **N=4-only success (Pitfall 6, MODERATE)** -- N=4 has only 2 facet orbits; any method handling these may rely on simplicity absent at N=5. Prevention: test on at least one N=5 inequality during method development, before declaring N=4 success.

5. **Floating-point errors (Pitfall 9, MODERATE)** -- Polyhedral computations on degenerate cones require exact rational arithmetic. Prevention: mandate exact arithmetic (lrslib/cddlib with GMP) for all cone computations; floating-point only for visualization.

## Approximation Landscape

| Method | Valid Regime | Breaks Down When | Controlled? | Complements |
|--------|-------------|------------------|-------------|-------------|
| Contraction maps | All rational HEIs (proven complete) | Cannot distinguish facets from redundant | Yes (exact combinatorial method) | Saturation test for facet detection |
| Codimension-1 saturation | Any valid inequality, any N | Computational cost exponential in N; finding saturating vectors is hard | Yes (exact linear algebra) | Contraction maps for validity |
| Double description (cddlib) | N <= 4 (d <= 15) | Memory blowup from intermediate swell at N >= 5 | Yes (exact arithmetic) | Reverse search (lrslib) for larger N |
| Reverse search (lrslib) | N <= 5 (d <= 31); partial at N = 6 | Computationally infeasible for full enumeration at N >= 7 | Yes (exact arithmetic) | RL-assisted search for N >= 6 |
| K-basis coefficient analysis | Any HEI (coefficients always non-negative) | Facet detection capability UNPROVEN | Unknown (research frontier) | PMI reconstruction |
| PMI reconstruction | N <= 5 (reconstruction demonstrated) | Scalability to N >= 6 untested | Unknown (research frontier) | K-basis analysis |
| Superbalance filter | All candidate HEIs | Necessary but not sufficient; does not distinguish facets | Yes (exact linear check) | Must be combined with other methods |

**Coverage gaps:** No method currently provides an IT criterion for facet status. The codimension-1 saturation test is definitive but purely geometric (not information-theoretic) and requires brute-force enumeration. The K-basis and PMI approaches are promising but unproven for facet detection. This gap is precisely the target of the project.

## Theoretical Connections

### K-Basis as IT-Polyhedral Bridge (ESTABLISHED, partially)

The K-basis (He, Headrick, Hubeny 2019) is constructed from perfect tensor entropy vectors, which are extreme rays of the HEC. All valid HEIs have non-negative K-basis coefficients. This establishes a direct bridge: the K-basis is information-theoretic in origin (built from multipartite information quantities I_n) and geometric in effect (its elements are extreme rays). The zero-coefficient pattern of an HEI in the K-basis determines which extreme rays it "sees" -- and a facet must have its zero set spanning a codimension-1 face. Whether this zero-coefficient pattern suffices to distinguish facets from redundant inequalities is the open question.

### PMI as Dual IT Characterization (ESTABLISHED for reconstruction; CONJECTURED for facets)

The marginal independence reconstruction (Hernandez-Cuenca, Hubeny, Rota 2022) shows that purely IT data -- which mutual informations vanish -- determines the extreme ray structure and hence the entire HEC. This provides a second IT-polyhedral bridge, dual to the K-basis: where the K-basis connects IT quantities to the inequality (H-representation) side, the PMI connects IT data to the extreme ray (V-representation) side. Recent work on correlation hypergraphs (arXiv:2412.18018) and tree graph models (arXiv:2512.24490) further develops the combinatorial structure of PMIs. Whether the PMI structure on a facet's saturating face has a distinctive IT character is unknown.

### Contraction Map Triality (ESTABLISHED)

Bao, Furuya, and Naskar (arXiv:2409.17317) established a triality between HEIs, contraction maps, and partial cubes (isometric subgraphs of hypercubes). This provides a complete combinatorial characterization of the validity question. The triality is exact and proven, but it encodes validity information only -- no facet information. The EWN (entanglement wedge nesting) violation structure of contraction proofs (arXiv:2501.17222) is structured but its correlation with facet status is unknown.

### Superbalance as UV Structure (ESTABLISHED)

Every primitive (non-SA, non-redundant) HEI is superbalanced (He, Hubeny, Rangamani 2020). Superbalance concerns cancellation of UV divergences in the continuum limit. This is an IT-flavored structural property that acts as a necessary filter. Combined with the decomposition result (arXiv:2601.09987) -- every HEI is a non-negative integer combination of SA instances and a superbalanced HEI -- this provides a structural decomposition of the HEC inequality space.

### RG Interpretation (SPECULATIVE)

Recent work (arXiv:2601.02472) argues that HEIs enforce and protect holographic RG flow. If this physical interpretation is correct, it could inform which inequalities are "essential" (facets) versus "derived" (redundant). This is too preliminary to build on but may provide future physical intuition.

### Cross-Validation Opportunities

| | Contraction Maps | Saturation Test | K-Basis Analysis | PMI Reconstruction | Superbalance |
|---|:---:|:---:|:---:|:---:|:---:|
| **Contraction Maps** | -- | Both classify all N=5 inequalities | K-basis coefficients computable for any contraction-map-proven HEI | PMI extreme rays define the cone contraction maps constrain | Superbalance is necessary for non-SA contraction-map-provable HEIs |
| **Saturation Test** | Saturation uses graph models that contraction maps also use | -- | K-basis zero pattern on saturating face determines codimension | Saturating vectors have specific PMIs | N/A (saturation is about facets, not superbalance) |
| **K-Basis Analysis** | Every valid HEI has non-negative K-coefficients | Zero-coefficient pattern encodes face structure | -- | K-basis elements are extreme rays; PMIs determine which are realized | Superbalanced HEIs may have distinctive K-basis patterns |
| **IT Method (new)** | Must be compatible with completeness result | Must agree with saturation test on facet/redundant | Likely works through K-basis or PMI structure | Likely works through PMI structure | Should respect superbalance as necessary condition |

### Critical Claim Verification

| # | Claim | Source | Verification | Result |
|---|-------|--------|--------------|--------|
| 1 | Contraction maps are necessary and sufficient for all rational HEIs | METHODS.md | WebSearch: "Bao Furuya Naskar completeness contraction map 2025" | CONFIRMED -- Published JHEP 12 (2025) 140 |
| 2 | N=5 HEC has 372 facets in 8 orbits, 2267 extreme rays in 19 orbits | PRIOR-WORK.md | WebSearch: "Hernandez-Cuenca holographic entropy cone five regions 372 facets" | CONFIRMED -- Published Phys. Rev. D 100 (2019) 026004 |
| 3 | Toric and generalized toric are facets for all N | METHODS.md | WebSearch: "Czech Liu Yu two infinite families facets 2024" | CONFIRMED -- Published SciPost Physics 17 (2024) 084 |
| 4 | PMI reconstruction recovers the HEC from marginal independence data | METHODS.md | WebSearch: "Hernandez-Cuenca Hubeny Rota marginal independence 2022" | CONFIRMED -- Published JHEP 09 (2022) 190 |
| 5 | K-basis coefficients of all HEIs are non-negative | METHODS.md | WebSearch: "He Headrick Hubeny K-basis holographic entropy repackaged 2019" | CONFIRMED -- Published JHEP 10 (2019) 118 |
| 6 | N=5 HEC: 5 new inequality types are genuinely new (not lifts from lower N) | PRIOR-WORK.md | Verified via claim 2; Hernandez-Cuenca (2019) proves 8 orbits = 3 lifts + 5 new | CONFIRMED |
| 7 | Superbalance is necessary for primitive HEIs | METHODS.md | Cited as He, Hubeny, Rangamani (2020), arXiv:2002.04558; well-cited | CONFIRMED (based on publication record) |

### Input Quality -> Roadmap Impact

| Input File | Quality | Affected Recommendations | Impact if Wrong |
|------------|---------|------------------------|-----------------|
| METHODS.md | GOOD | Method selection, phase ordering, IT-bridge identification | Phases 2-3 may target wrong structural property |
| PRIOR-WORK.md | GOOD | Benchmark values, success criteria, literature completeness | Phases may validate against wrong ground truth |
| COMPUTATIONAL.md | GOOD | Tool selection, resource estimates, computational pipeline | Tool substitution needed; timing estimates off |
| PITFALLS.md | GOOD | Risk mitigation in all phases, design constraints on IT method | Blind spots in method development |

## Implications for Roadmap

### Suggested Phase Structure

### Phase 1: Foundations and N=4 Benchmark

**Rationale:** All downstream work depends on a validated computational pipeline and correct reproduction of the known N=4 classification. The notation conventions, purification treatment, and symmetry reduction must be locked before any novel work begins. N=4 is the non-negotiable checkpoint (d=7, only 2 facet orbits -- trivially computable, but must be gotten right).

**Delivers:** (a) Validated polyhedral computation pipeline (lrslib + pycddlib). (b) Verified N=4 HEC: extreme rays, facets, redundancy classification. (c) Superbalance filter implementation. (d) Graph model entropy computation (NetworkX max-flow). (e) K-basis and PMI computation infrastructure.

**Methods:** Double description (pycddlib for N=4), LP redundancy removal, max-flow for graph models, psitip for IT inequality verification.

**Validates:** N=4 facets (SSA + MMI), N=4 extreme rays, orbit counts under S_4.

**Avoids:** Pitfalls 1 (validity vs. facet), 5 (purification), 8 (symmetry), 9 (floating-point), 11 (sign errors), 12 (SSA facet assumption), 13 (superbalance).

**Success criteria:** 100% agreement with Bao et al. (2015) N=4 classification; both validity and facet status independently verified for every inequality.

### Phase 2: IT Method Development

**Rationale:** With the computational infrastructure validated, the core intellectual work begins: developing an information-theoretic criterion that distinguishes facets from redundant inequalities. The two candidate bridges -- K-basis coefficient patterns and PMI structure on saturating faces -- should be investigated in parallel. The method must be designed to go beyond validity proofs (Pitfall 2) and must be tested on at least one N=5 inequality during development (Pitfall 6).

**Delivers:** (a) IT criterion or structural invariant that differentiates facets from redundant inequalities. (b) Proof or strong evidence that the criterion works for N=4. (c) Preliminary test on at least one known N=5 facet and one known N=5 redundant inequality.

**Methods:** K-basis decomposition, PMI analysis, codimension-1 saturation test (as validation oracle), superbalance analysis.

**Builds on:** Phase 1 computational pipeline and N=4 benchmark data.

**Avoids:** Pitfalls 2 (mimicking contraction maps), 4 (necessary vs. sufficient), 6 (N=4-only success), 7 (HEC vs. QEC confusion), 10 (completeness constrains alternatives).

**Success criteria:** The IT method produces different outputs (or different structural signatures) for known facets versus known redundant inequalities at N=4. At least one N=5 test case confirms the method generalizes.

**Risk:** HIGH -- this is the central open question. The competing explanation (facet status has no clean IT characterization) cannot be ruled out a priori.

### Phase 3: N=5 Classification and Validation

**Rationale:** The N=5 HEC is the primary proving ground. With 372 facets in 8 orbits (including 5 genuinely new types), the ground truth is complete and the test is non-trivial. The IT method must reproduce the known facet/redundant classification for all N=5 candidate inequalities. Computational scaling from N=4 (d=7) to N=5 (d=15) tests whether the method is practical.

**Delivers:** (a) IT-based facet/redundant classification of all known N=5 HEIs. (b) Cross-validation against the LP-based classification (which uses the full polyhedral cone computation). (c) Assessment of computational scaling. (d) Structural insights into why the 5 new N=5 facet types are facets.

**Methods:** IT proof method (from Phase 2), lrslib extreme ray enumeration, LP redundancy removal, K-basis analysis, PMI reconstruction.

**Builds on:** Phase 2 IT method, Phase 1 computational pipeline.

**Avoids:** Pitfalls 3 (2^N explosion -- use lrslib and S_5 symmetry), 6 (N=4-only success -- this is the definitive test).

**Success criteria:** IT classification agrees with polyhedral classification on all N=5 inequalities tested. Computational cost is comparable to or better than full cone enumeration. The method provides structural insight (not just a yes/no answer).

### Phase 4: Synthesis and General-N Analysis

**Rationale:** If the IT method succeeds at N=5, explore its implications for general N. Test against the known infinite families (toric, generalized toric) to see if the method explains why they are facets. Assess whether the method provides a path toward N=6 or general-N classification without full enumeration.

**Delivers:** (a) IT analysis of toric and generalized toric families. (b) Assessment of whether the IT criterion extends to general N. (c) Working notes documenting the method, its validation, and its scope. (d) Identification of the method's limitations and failure modes.

**Methods:** IT proof method, saturation constructions (Czech, Liu, Yu 2024 approach), superbalance analysis.

**Builds on:** Phase 3 N=5 results.

**Success criteria:** The IT method correctly identifies toric and generalized toric inequalities as facets for tested values of N. Working notes are complete with method statement, N=4 validation, N=5 application, and general-N discussion.

**Risk:** MEDIUM -- the method may work case-by-case at N=5 but not yield a general-N criterion.

### Phase Ordering Rationale

- **Phase 1 before Phase 2:** You cannot develop a new method without a validated computational baseline to test against. The pipeline and benchmarks are prerequisites.
- **Phase 2 before Phase 3:** The IT method must exist (even in preliminary form) before it can be applied to the full N=5 dataset. Testing one N=5 case during Phase 2 provides an early generalization check.
- **Phase 3 before Phase 4:** General-N analysis without N=5 validation is premature. The N=5 results determine whether generalization is worth pursuing.
- **Phases are strictly sequential:** Each phase's deliverables are prerequisites for the next. No parallelization across phases.

### Phases Requiring Deep Investigation

Phases likely needing additional theoretical or computational exploration:

- **Phase 2:** Novel derivation needed -- no literature precedent for an IT-based facet criterion. This is genuinely open research. Consider running `gpd:research-phase` before execution to survey K-basis coefficient patterns and PMI structures on known facets.

Phases with established methodology (straightforward execution):

- **Phase 1:** Well-documented techniques; multiple references available for every step. Polyhedral computation, graph models, and symmetry reduction are mature.
- **Phase 3:** Execution is straightforward IF Phase 2 succeeds -- it is applying a developed method to known data.

## Confidence Assessment

| Area | Confidence | Notes |
|------|-----------|-------|
| Computational Approaches | HIGH | Mature tools (lrslib, cddlib, psitip); exact arithmetic; validated on N=5 by multiple groups |
| Prior Work | HIGH | N <= 5 classification is complete and independently confirmed; N=6 partial results are well-documented |
| Methods | MEDIUM-HIGH | Established methods (contraction maps, saturation) are HIGH; novel IT bridges (K-basis, PMI for facets) are LOW-MEDIUM (unproven) |
| Pitfalls | HIGH | 13 pitfalls identified covering conceptual, computational, and methodological failure modes; phase mapping is complete |

**Overall confidence:** MEDIUM-HIGH. The established landscape is well-understood with HIGH confidence. The novel research direction (IT-based facet detection) is inherently LOW confidence because it addresses an open question with no existing solution. The project is well-designed to mitigate this: the N=5 ground truth provides a definitive test, and the stop conditions are clear.

### Gaps to Address

- **No existing IT facet criterion:** The central gap. No published work demonstrates an information-theoretic property that distinguishes facets from redundant inequalities. Phase 2 must address this from scratch.
- **K-basis zero-coefficient pattern analysis not yet performed:** While K-basis positivity is proven, no systematic study of zero-coefficient patterns across facets vs. redundant inequalities has been published. This is a concrete Phase 2 investigation.
- **PMI structure on saturating faces not characterized:** The PMIs of extreme rays are studied, but the PMI structure restricted to the saturating face of a given inequality is unexplored territory.
- **Majorization characterization's relation to facets unknown:** Hubeny et al. (2025) provide a new HEC characterization via majorization, but its connection to facet status is unstudied. This could become relevant but is too recent to rely on.
- **N=6 incomplete:** 3 of 6 mystery extreme rays remain unrealized, suggesting unknown N=6 inequalities. Out of scope but relevant context.

## Open Questions

1. **(HIGH PRIORITY, blocks Phase 2)** What information-theoretic property distinguishes HEC facets from redundant inequalities? -- The core research question. No existing answer.

2. **(HIGH PRIORITY, blocks Phase 2)** Does the K-basis zero-coefficient pattern of an HEI encode its codimension in the cone? -- If yes, this directly yields a facet criterion (codimension 1 = facet).

3. **(HIGH PRIORITY, blocks Phase 2)** Does the PMI structure on the saturating face of an inequality have a distinctive character for facets versus redundant inequalities? -- The dual approach to Question 2.

4. **(MEDIUM PRIORITY, informs Phase 4)** Do the toric and generalized toric infinite families have a common IT structural feature that marks them as facets? -- Would provide evidence for a general-N criterion.

5. **(MEDIUM PRIORITY, informs Phase 4)** Does the contraction map's EWN violation structure correlate with facet status? -- Speculative but could connect the contraction map framework to facet detection.

6. **(LOW PRIORITY, future work)** Is the majorization characterization of the HEC (Hubeny et al. 2025) related to facet status? -- Too recent to assess; note for future investigation.

7. **(LOW PRIORITY, out of scope)** Does the complete N=6 HEC require unknown inequalities? -- 3 unrealized mystery extreme rays suggest yes; out of project scope.

## Sources

### Primary (HIGH)

- Bao, Nezami, Ooguri, Stoica, Sully, Walter, "The Holographic Entropy Cone," JHEP 09 (2015) 130, [arXiv:1505.07839](https://arxiv.org/abs/1505.07839) -- Foundational: defined HEC, proved N <= 4 completeness, introduced contraction maps and graph models
- Hernandez-Cuenca, "Holographic entropy cone for five regions," Phys. Rev. D 100 (2019) 026004, [arXiv:1903.09148](https://arxiv.org/abs/1903.09148) -- Complete N=5 classification: 372 facets, 2267 extreme rays
- Bao, Furuya, Naskar, "On the completeness of contraction map proof method," JHEP 12 (2025) 140, [arXiv:2506.18086](https://arxiv.org/abs/2506.18086) -- Contraction maps necessary and sufficient for rational HEIs
- Czech, Liu, Yu, "Two infinite families of facets of the holographic entropy cone," SciPost Phys. 17 (2024) 084, [arXiv:2401.13029](https://arxiv.org/abs/2401.13029) -- First general-N facet proof beyond MMI; star graph saturation technique
- He, Headrick, Hubeny, "Holographic Entropy Relations Repackaged," JHEP 10 (2019) 118, [arXiv:1905.06985](https://arxiv.org/abs/1905.06985) -- K-basis construction; HEI coefficients non-negative in K-basis
- Hernandez-Cuenca, Hubeny, Rota, "The holographic entropy cone from marginal independence," JHEP 09 (2022) 190, [arXiv:2204.00075](https://arxiv.org/abs/2204.00075) -- PMI-based HEC reconstruction
- Avis, Hernandez-Cuenca, "On the foundations and extremal structure of the holographic entropy cone," Discrete Applied Mathematics 328 (2023) 16, [arXiv:2102.07535](https://arxiv.org/abs/2102.07535) -- Graph-theoretic foundations; recomputed N=5; partial N=6
- Hayden, Headrick, Maloney, "Holographic mutual information is monogamous," PRD 87 (2013) 046003, [arXiv:1107.2940](https://arxiv.org/abs/1107.2940) -- Proved MMI

### Secondary (MEDIUM)

- Bao, Furuya, Naskar, "Towards a complete classification of holographic entropy inequalities," JHEP 03 (2025) 117, [arXiv:2409.17317](https://arxiv.org/abs/2409.17317) -- Partial cube triality; deterministic contraction map search
- He, Hubeny, Rangamani, "Superbalance of holographic entropy inequalities," JHEP 07 (2020) 245, [arXiv:2002.04558](https://arxiv.org/abs/2002.04558) -- Superbalance necessary condition
- Hernandez-Cuenca, Hubeny, Jia, "Holographic Entropy Inequalities and Multipartite Entanglement," JHEP 08 (2024) 238, [arXiv:2309.06296](https://arxiv.org/abs/2309.06296) -- 1800+ new N=6 inequalities; superbalance no-go
- Czech, Shuai, "Nesting is not Contracting," JHEP 06 (2025) 122, [arXiv:2501.17222](https://arxiv.org/abs/2501.17222) -- EWN structure of contraction proofs
- Hernandez-Cuenca, Li, Rolph, "Correlation hypergraph," JHEP 09 (2025) 080, [arXiv:2412.18018](https://arxiv.org/abs/2412.18018) -- Correlation hypergraph representation of PMIs
- Bao, Furuya, Naskar, "A framework for generalizing toric inequalities," JHEP 10 (2024) 251, [arXiv:2408.04741](https://arxiv.org/abs/2408.04741) -- Multi-parameter toric generalization
- Freedman, Headrick, "Bit threads and holographic entanglement," Commun. Math. Phys. 352 (2017) 407, [arXiv:1604.00354](https://arxiv.org/abs/1604.00354) -- Bit thread framework

### Tertiary (LOW)

- Hubeny et al., "A new characterization of the holographic entropy cone," [arXiv:2508.21823](https://arxiv.org/abs/2508.21823) -- Majorization characterization; recent preprint, needs independent verification
- "Exploring the holographic entropy cone via reinforcement learning," [arXiv:2601.19979](https://arxiv.org/abs/2601.19979) -- RL-based facet discovery; resolved 3 of 6 mystery N=6 extreme rays
- "Renormalization Group is the Principle behind the Holographic Entropy Cone," [arXiv:2601.02472](https://arxiv.org/abs/2601.02472) -- RG interpretation of HEIs; speculative
- "Combinatorial properties of holographic entropy inequalities," [arXiv:2601.09987](https://arxiv.org/abs/2601.09987) -- Structural decomposition: every HEI = SA combination + superbalanced part

### Computational Tools

- lrslib: [http://cgm.cs.mcgill.ca/~avis/C/lrs.html](http://cgm.cs.mcgill.ca/~avis/C/lrs.html)
- pycddlib: [https://pypi.org/project/pycddlib/](https://pypi.org/project/pycddlib/)
- psitip: [https://github.com/cheuktingli/psitip](https://github.com/cheuktingli/psitip)
- Holographic-Entropy-Cone database: [https://github.com/SergioHC95/Holographic-Entropy-Cone](https://github.com/SergioHC95/Holographic-Entropy-Cone)

---

_Research analysis completed: 2026-04-05_
_Ready for research plan: yes_

```yaml
# --- ROADMAP INPUT (machine-readable, consumed by gpd-roadmapper) ---
synthesis_meta:
  project_title: "Alternative Proof Methods for Holographic Entropy Cone Inequalities"
  synthesis_date: "2026-04-05"
  input_files: [METHODS.md, PRIOR-WORK.md, COMPUTATIONAL.md, PITFALLS.md]
  input_quality: {METHODS: good, PRIOR-WORK: good, COMPUTATIONAL: good, PITFALLS: good}

conventions:
  unit_system: "natural"
  metric_signature: "N/A (combinatorial/information-theoretic setting)"
  fourier_convention: "N/A"
  coupling_convention: "N/A"
  renormalization_scheme: "N/A"
  entropy_convention: "S(A) = min-cut in graph model; dimensionless; purification imposed S(A)=S(A^c)"
  symmetry_group: "S_N acting on party labels {1,...,N}"

methods_ranked:
  - name: "K-basis coefficient analysis"
    regime: "Any valid HEI; most promising for facet detection"
    confidence: MEDIUM
    cost: "O(2^N) per inequality (basis change)"
    complements: "PMI reconstruction (dual V-rep perspective)"
  - name: "PMI reconstruction / marginal independence analysis"
    regime: "Any HEI; reconstruction proven for N <= 5"
    confidence: MEDIUM
    cost: "O(2^N) per extreme ray characterization"
    complements: "K-basis analysis (dual H-rep perspective)"
  - name: "Contraction maps"
    regime: "All rational HEIs (proven complete for validity)"
    confidence: HIGH
    cost: "Polynomial via partial cube characterization"
    complements: "Saturation test (covers facet detection where contraction maps are blind)"
  - name: "Codimension-1 saturation test"
    regime: "Any valid inequality, any N"
    confidence: HIGH
    cost: "O(2^N) saturating vectors needed; finding them is the hard part"
    complements: "Contraction maps (covers validity where saturation addresses facets)"
  - name: "Superbalance filter"
    regime: "All candidate HEIs; necessary condition for non-SA primitives"
    confidence: HIGH
    cost: "O(N * 2^N) per inequality"
    complements: "All other methods (cheap first-pass filter)"
  - name: "lrslib vertex/facet enumeration"
    regime: "N <= 5 (full enumeration); N = 6 (partial)"
    confidence: HIGH
    cost: "Output-sensitive; hours for N=5, days-weeks for N=6 partial"
    complements: "pycddlib for small problems; Normaliz for lattice structure"

phase_suggestions:
  - name: "Foundations and N=4 Benchmark"
    goal: "Validate computational pipeline and reproduce known N=4 HEC classification"
    methods: ["Contraction maps", "Codimension-1 saturation test", "lrslib vertex/facet enumeration", "Superbalance filter"]
    depends_on: []
    needs_research: false
    risk: LOW
    pitfalls: ["validity-facet-confusion", "purification-errors", "symmetry-reduction-errors", "floating-point-errors", "sign-coefficient-errors", "SSA-facet-assumption", "superbalance-ignored"]

  - name: "IT Method Development"
    goal: "Develop information-theoretic criterion distinguishing HEC facets from redundant inequalities"
    methods: ["K-basis coefficient analysis", "PMI reconstruction / marginal independence analysis", "Codimension-1 saturation test", "Superbalance filter"]
    depends_on: ["Foundations and N=4 Benchmark"]
    needs_research: true
    risk: HIGH
    pitfalls: ["IT-mimics-contraction-maps", "necessary-vs-sufficient", "N4-only-success", "HEC-QEC-confusion", "completeness-constrains-alternatives"]

  - name: "N=5 Classification and Validation"
    goal: "Apply IT method to full N=5 HEC and cross-validate against known classification"
    methods: ["K-basis coefficient analysis", "PMI reconstruction / marginal independence analysis", "lrslib vertex/facet enumeration", "Codimension-1 saturation test"]
    depends_on: ["IT Method Development"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["2N-dimensional-explosion", "N4-only-success"]

  - name: "Synthesis and General-N Analysis"
    goal: "Test IT method on infinite families and assess general-N applicability"
    methods: ["K-basis coefficient analysis", "PMI reconstruction / marginal independence analysis", "Contraction maps"]
    depends_on: ["N=5 Classification and Validation"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["N4-only-success"]

critical_benchmarks:
  - quantity: "N=4 HEC facet orbits"
    value: "2 (SSA and MMI)"
    source: "Bao et al. (2015), arXiv:1505.07839"
    confidence: HIGH
  - quantity: "N=5 HEC facet count"
    value: "372 facets in 8 symmetry orbits"
    source: "Hernandez-Cuenca (2019), arXiv:1903.09148"
    confidence: HIGH
  - quantity: "N=5 HEC extreme ray count"
    value: "2267 extreme rays in 19 symmetry orbits"
    source: "Hernandez-Cuenca (2019), arXiv:1903.09148"
    confidence: HIGH
  - quantity: "N=5 genuinely new facet types"
    value: "5 new orbits beyond SSA and MMI lifts"
    source: "Hernandez-Cuenca (2019), arXiv:1903.09148"
    confidence: HIGH
  - quantity: "Effective entropy space dimension at N=5 (after purification)"
    value: "15"
    source: "Standard: 2^(N-1) - 1 = 2^4 - 1 = 15"
    confidence: HIGH

open_questions:
  - question: "What IT property distinguishes HEC facets from redundant inequalities?"
    priority: HIGH
    blocks_phase: "IT Method Development"
  - question: "Does the K-basis zero-coefficient pattern encode codimension in the cone?"
    priority: HIGH
    blocks_phase: "IT Method Development"
  - question: "Does the PMI structure on a facet's saturating face have distinctive IT character?"
    priority: HIGH
    blocks_phase: "IT Method Development"
  - question: "Do toric/generalized toric families share an IT structural feature marking them as facets?"
    priority: MEDIUM
    blocks_phase: "Synthesis and General-N Analysis"
  - question: "Does the contraction map EWN violation structure correlate with facet status?"
    priority: MEDIUM
    blocks_phase: "none"
  - question: "Is the majorization characterization related to facet status?"
    priority: LOW
    blocks_phase: "none"
  - question: "Does the complete N=6 HEC require unknown inequalities?"
    priority: LOW
    blocks_phase: "none"

contradictions_unresolved: []
```
