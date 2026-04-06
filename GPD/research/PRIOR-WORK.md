# Prior Work: Holographic Entropy Cone Inequalities

**Surveyed:** 2026-04-05
**Domain:** Holographic entanglement / quantum information theory / polyhedral geometry
**Confidence:** HIGH (N <= 5 classification), MEDIUM (N = 6 partial results), MEDIUM (non-contraction-map approaches)

## Key Results

| Result | Expression / Value | Conditions | Source | Year | Confidence |
| --- | --- | --- | --- | --- | --- |
| SSA is the only facet for N=2,3 (beyond non-negativity and Araki-Lieb) | S(AB) + S(BC) >= S(B) + S(ABC) | Holographic states; RT formula | Headrick, Takayanagi, arXiv:0704.3719 | 2007 | HIGH |
| MMI is a facet for all N >= 3 | I(A:B:C) := S(AB)+S(AC)+S(BC)-S(A)-S(B)-S(C)-S(ABC) >= 0 | Holographic states; RT formula | Hayden, Headrick, Maloney, arXiv:1107.2940 | 2013 | HIGH |
| SSA + MMI are the complete facets for N <= 4 | No additional independent inequalities | Holographic states; graph models | Bao, Nezami, Ooguri, Stoica, Sully, Walter, arXiv:1505.07839 | 2015 | HIGH |
| HEC is a rational polyhedral cone for each N | Finitely many facets with integer coefficients | RT formula; static bulk geometry | Bao et al., arXiv:1505.07839 | 2015 | HIGH |
| N=5 HEC fully classified: 372 facets, 2267 extreme rays (19 orbits) | 5 new inequality types beyond SSA+MMI (up to symmetry) | RT formula; all proven HEIs for N=5 | Hernandez-Cuenca, arXiv:1903.09148 | 2019 | HIGH |
| Two infinite families of general-N facets (toric + generalized toric) | Proven to be facets by constructing 2^N-2 saturating vectors | RT formula; star graph saturation | Czech, Liu, Yu, arXiv:2401.13029 | 2024 | HIGH |
| N=6 partial: 1877 known facets, 4145 extreme rays (150/156 candidate orbits realized) | 6 "mystery" extreme rays; 3 realized, 3 likely not (implying unknown N=6 inequalities) | RT formula; graph models | Hernandez-Cuenca, Hubeny, Jia, arXiv:2309.06296; Avis, Hernandez-Cuenca, arXiv:2102.07535 | 2023 | MEDIUM |
| Contraction map method is necessary and sufficient for rational HEIs | For all linear HEIs with rational coefficients, validity iff contraction map exists | Rational coefficients only | Bao, Furuya, Naskar, arXiv:2506.18086 | 2025 | HIGH |
| Majorization characterization of the HEC | RT inequalities pass a majorization test; only RT inequalities do | Null-reduced inequalities; perturbative regime | Hubeny et al., arXiv:2508.21823 | 2025 | MEDIUM |

## Foundational Work

### Ryu and Takayanagi (2006) - Holographic Entanglement Entropy

**Key contribution:** Proposed the RT formula: the entanglement entropy of a boundary region A in a holographic CFT equals the area of the minimal surface in the bulk homologous to A, divided by 4G_N. This is the starting point for the entire field.
**Method:** Geometric prescription within AdS/CFT. The minimal surface (RT surface) computes boundary entanglement entropy.
**Limitations:** Static bulk geometries only. Generalized to the covariant HRT formula (Hubeny, Rangamani, Takayanagi, 2007) for time-dependent settings.
**Relevance:** The RT formula is the definition of the entropy we study. All HEC inequalities are constraints on the set of entropy vectors realizable by this formula.

### Headrick and Takayanagi (2007) - Holographic Proof of SSA

**Key contribution:** Proved that strong subadditivity S(AB) + S(BC) >= S(B) + S(ABC) holds for RT entropies using a simple geometric argument involving min-cut surfaces.
**Method:** Geometric/min-cut proof. Given candidate RT surfaces for S(AB) and S(BC), one can cut and re-glue segments to produce candidate surfaces for S(B) and S(ABC), whose total area is no greater.
**Limitations:** Static geometries. The proof method (cut-and-glue) is the prototype for what became the contraction map method.
**Relevance:** Established the proof paradigm that dominates the field. Every subsequent proof method (contraction maps, graph contraction) refines this basic cut-and-glue idea.

### Hayden, Headrick, and Maloney (2013) - Monogamy of Mutual Information (MMI)

**Key contribution:** Proved that holographic mutual information satisfies monogamy: I(A:BC) >= I(A:B) + I(A:C), equivalently I_3(A:B:C) >= 0. This is the first holographic inequality that does NOT hold for general quantum states.
**Method:** Geometric proof analogous to the SSA proof, using min-cut surface rearrangement. The proof is similar in spirit to the Headrick-Takayanagi SSA proof.
**Limitations:** The inequality is specific to holographic states; generic quantum states can violate MMI.
**Relevance:** MMI is the first inequality distinguishing the holographic entropy cone from the quantum entropy cone. It is a facet for all N >= 3, making it the primary benchmark for any proof method.

### Bao, Nezami, Ooguri, Stoica, Sully, and Walter (2015) - The Holographic Entropy Cone

**Key contribution:** Introduced the systematic study of the holographic entropy cone. Proved that for each N, the set of realizable entropy vectors forms a rational polyhedral cone (the HEC). Proved completeness of SSA + MMI as facets for N <= 4. Discovered an infinite family of new inequalities for N >= 5. Introduced the graph model framework: the HEC equals the cone of entropy vectors realizable by weighted graphs (min-cut functions on graphs).
**Method:** (i) Proved that any entropy vector realizable by the RT formula is also realizable by a graph model. (ii) Used the "proof by contraction" method: a valid inequality corresponds to a map on the vertices of the hypercube {0,1}^N that is contracting with respect to the inequality's coefficients. (iii) Enumerated all candidate inequalities for small N and checked validity.
**Limitations:** The contraction map method proves validity but provides no information about whether an inequality is a facet (irredundant) or redundant. The graph model equivalence is proven for static geometries.
**Relevance:** This is the decisive reference. The N <= 4 classification (SSA + MMI are complete) is the benchmark our method must reproduce. The contraction map's inability to detect facet status is the gap our project aims to fill.

### Hernandez-Cuenca (2019) - The Holographic Entropy Cone for Five Regions

**Key contribution:** Completely classified the N=5 HEC. Showed that the cone defined by all known N=5 HEIs has 372 facets (falling into 8 symmetry orbits: 3 "lift" orbits from lower N, plus 5 genuinely new orbits) and 2267 extreme rays (19 symmetry orbits). Proved completeness by constructing explicit graph models realizing every extreme ray.
**Method:** (i) Enumerated all candidate inequalities provable by contraction maps for N=5. (ii) Computed the resulting polyhedral cone (facets and extreme rays). (iii) For each extreme ray orbit, constructed an explicit graph model realizing it. Since every extreme ray is realizable, no additional inequalities can cut them off, proving the cone is complete.
**Limitations:** The completeness proof is indirect: it shows no further inequalities are needed, but does not provide an independent criterion for when an inequality is a facet. The method becomes computationally prohibitive for N >= 6 because the number of candidate inequalities and extreme rays grows combinatorially.
**Relevance:** Provides the ground truth for N=5 that our method should reproduce or at minimum be consistent with. The 5 new inequality types (beyond SSA and MMI lifts) are key test cases.

### He, Headrick, and Hubeny (2019) - Holographic Entropy Relations Repackaged

**Key contribution:** Introduced the K-basis (built from perfect tensor structures) for rewriting entropy quantities. Showed that entropy vectors from perfect tensors are extreme rays of both the HEC and the quantum entropy cone. Identified the "primitive" information quantities that characterize the independent degrees of freedom in holographic entropy.
**Method:** Basis change in the entropy vector space. Information quantities repackaged using the I_n multipartite information measures.
**Limitations:** The K-basis simplification is useful for structural understanding but does not directly prove new inequalities or determine facet status.
**Relevance:** The I_n / K-basis language provides a natural framework for expressing HEC inequalities in information-theoretic terms. Any IT-based proof method should be compatible with this basis.

### Avis and Hernandez-Cuenca (2021/2023) - Foundations and Extremal Structure

**Key contribution:** Developed the HEC from a purely graph-theoretic perspective. Provided self-contained proofs of known results and new results. Developed two systematic approaches for finding facets and extreme rays. Recomputed the N=5 HEC and improved its graph description. Provided partial results for N=6 (150 out of 156 candidate extreme ray orbits realized).
**Method:** Polyhedral geometry and graph theory. Used double description method and exploitation of symmetry group action to compute cones.
**Limitations:** N=6 remains incomplete: 6 "mystery" extreme rays lack graph realizations, suggesting unknown inequalities may exist.
**Relevance:** Provides the computational infrastructure and database for HEC computations. The N=6 partial results define the frontier.

## Recent Developments

| Paper | Authors | Year | Advance | Impact on Our Work |
| --- | --- | --- | --- | --- |
| The holographic entropy cone from marginal independence | Hernandez-Cuenca, Hubeny, Rota | 2022 | HEC can be reconstructed from subadditivity cone extreme rays realizable in holography; introduced "pattern of marginal independence" (PMI) | PMI may provide an information-theoretic criterion related to facet status |
| Holographic Entropy Inequalities and Multipartite Entanglement | Hernandez-Cuenca, Hubeny, Jia | 2024 | Discovered 1800+ novel N=6 inequalities using multipartite information structure; proved no-go for monotonicity under partial trace (superbalance) | Demonstrates power of IT-structural methods for generating candidates; superbalance constraint is relevant |
| Properties of the contraction map for HEE inequalities | Bao, Furuya, Naskar | 2024 | Characterized contraction map properties; established triality between HEIs, contraction maps, and partial cubes | Partial cube perspective may inform IT characterization |
| Two infinite families of facets of the HEC | Czech, Liu, Yu | 2024 | Proved toric and generalized toric inequalities are facets for all N by constructing 2^N-2 saturating vectors | First general-N facet proof beyond MMI; star graph saturation technique is a key method |
| A framework for generalizing toric inequalities | Bao, Furuya, Naskar | 2024 | Extended Czech's toric inequality framework; multi-parameter generalization | Broadens the known general-N facet families |
| Towards a complete classification of HEIs | Bao, Furuya, Naskar | 2025 | Deterministic method to find ALL HEIs with contraction maps; triality with partial cubes and isometric embeddings; argued completeness | If contraction maps are complete, then our IT method must be compatible with this framework |
| On the completeness of contraction map proof method | Bao, Furuya, Naskar | 2025 | Proved contraction map existence is necessary and sufficient for rational HEIs | Establishes that contraction maps fully characterize validity (not facet status); our method's value is in the facet/redundancy distinction |
| Nesting is not Contracting | (multiple authors) | 2025 | Showed proofs by contraction necessarily violate entanglement wedge nesting (EWN); characterized the structure of contraction map proofs | Reveals structural limitations of contraction proofs; EWN violations are a feature, not a bug |
| Exploring the HEC via reinforcement learning | (multiple authors) | 2025/2026 | RL-based discovery of HEC facets; found graph realizations for 3 of 6 mystery N=6 extreme rays | ML methods complement but do not replace analytical understanding |
| A new characterization of the HEC (majorization) | Hubeny et al. | 2025 | RT inequalities pass a majorization test, and only RT inequalities do | Potentially powerful new characterization; could inform or compete with our IT approach |
| Combinatorial properties of HEIs | (multiple authors) | 2026 | Structural combinatorial analysis of holographic entropy inequalities | Further structural understanding of HEI space |
| RG is the Principle behind the HEC | (multiple authors) | 2026 | HEIs enforce and protect holographic RG | Physical interpretation; may inform which properties are IT-fundamental |

## Known Limiting Cases

| Limit | Known Result | Source | Verified By |
| --- | --- | --- | --- |
| N=1 (single region) | Trivial: S(A) >= 0 only | Definition | Universal |
| N=2 (two regions) | Facets: S(A) >= 0, S(B) >= 0, S(AB) >= 0, SSA only (subadditivity + Araki-Lieb) | Bao et al. 2015 | Multiple groups |
| N=3 (three regions) | Facets: non-negativity + SSA + MMI | Bao et al. 2015 | Multiple groups |
| N=4 (four regions) | Facets: non-negativity + SSA + MMI (no new inequalities) | Bao et al. 2015 | Hernandez-Cuenca 2019 (reconfirmed) |
| N=5 (five regions) | Complete: 372 facets = SSA lifts + MMI lifts + 5 new types; 2267 extreme rays | Hernandez-Cuenca 2019 | Avis, Hernandez-Cuenca 2021 (recomputed) |
| All subsystems equal entropy | All HEIs reduce to non-negativity; point is deep interior of cone | Bao et al. 2015 | Trivial check |
| One subsystem has zero entropy (product state with one party) | Reduces to (N-1)-party HEC | Purification / partial trace | Standard |

## Open Questions

1. **Complete N=6 HEC classification** -- 6 mystery extreme rays remain unresolved (3 now realized via RL, 3 suspected to require unknown inequalities). This is the active frontier.
   - Why it matters: Determines whether known HEIs are complete for N=6
   - Current status: 1877 known facets, 150/156 extreme ray orbits realized
   - Key references: arXiv:2102.07535, arXiv:2309.06296, arXiv:2601.19979

2. **General-N facet classification** -- Beyond SSA, MMI, toric, and generalized toric families, are there other infinite families of facets? Is there a finite description of all facets for general N?
   - Why it matters: Central to understanding the structure of the HEC
   - Current status: Two infinite families proven (Czech et al. 2024); systematic search via contraction maps ongoing
   - Key references: arXiv:2401.13029, arXiv:2409.17317

3. **Information-theoretic characterization of facet status** -- No known criterion distinguishes facets from redundant inequalities without computing the full polyhedral cone. This is precisely our research question.
   - Why it matters: This is the core gap our project aims to fill
   - Current status: No published IT-based facet criterion exists
   - Key references: None directly; the marginal independence framework (arXiv:2204.00075) and multipartite information structure (arXiv:2309.06296) are the closest structural analyses

4. **Equivalence of static (RT) and covariant (HRT) entropy cones** -- Conjectured to be equal. The majorization characterization (arXiv:2508.21823) provides new evidence.
   - Why it matters: If equal, static results extend to full generality of holographic spacetimes
   - Current status: Strong evidence but no proof; primitivity of N=5 facet information quantities supports it
   - Key references: arXiv:1903.09148, arXiv:2508.21823, arXiv:2602.04888

5. **Physical interpretation of HEC inequalities** -- Recent work suggests HEIs enforce holographic RG flow. Can this interpretation identify which inequalities are essential (facets)?
   - Why it matters: Could provide the physical insight behind an IT proof method
   - Current status: Preliminary; arXiv:2601.02472 argues RG is the principle
   - Key references: arXiv:2601.02472

## Notation Conventions in the Literature

| Quantity | Standard Symbol(s) | Variations | Our Choice | Reason |
| --- | --- | --- | --- | --- |
| Entanglement entropy of region A | S(A) | S_A, H(A) | S(A) | Standard in holographic literature; H(A) is Shannon/classical convention |
| Mutual information | I(A:B) | I_2(A:B), I(A,B) | I(A:B) | Colon notation standard in QI; subscript 2 when distinguishing from I_n |
| Tripartite information | I_3(A:B:C), -I(A:B:C) | I_3, MMI (when >= 0) | I_3(A:B:C) | Following Bao et al. 2015; note sign convention: I_3 >= 0 is MMI |
| n-partite information | I_n | (-1)^{n+1} times alternating sum | I_n | Following He, Headrick, Hubeny 2019 |
| Holographic entropy cone for N parties | C_N, HEC_N, H_N | Various | C_N | Following Hernandez-Cuenca 2019; C_N for the cone, H_N also common |
| Number of boundary regions (parties) | N, n | k (rare) | N | Capital N for party count; lowercase for other indices |
| Entropy vector | v, s | S-vector | v | Components v_I = S(I) for each nonempty subset I of {1,...,N} |
| Entropy vector space dimension | 2^N - 1 | d | 2^N - 1 | One component per nonempty subsystem |
| Contraction map | f | phi, sigma | f | Following Bao et al. 2015 |
| Graph model | G = (V, E, w) | Weighted graph | G | Vertices include boundary terminals and bulk vertices |

## Relationship Between Key Concepts

### Entropy Cones Hierarchy

The following containment relationships hold for entropy cones:

```
Classical Shannon cone  superset  Quantum entropy cone  superset  Holographic entropy cone (HEC)
```

For N <= 3 parties, the quantum and classical cones coincide (only SA and SSA). For N = 4 parties, they differ: the quantum cone has no known non-Shannon inequalities, but the HEC has MMI. For N >= 5, the HEC is strictly smaller due to additional holographic-specific inequalities.

### Contraction Maps and Facet Status

The contraction map method addresses VALIDITY of an inequality (whether it holds for all holographic states). It does NOT address FACET STATUS (whether the inequality is irredundant given all other valid inequalities).

**Key distinction:**
- **Valid inequality** = holds for all entropy vectors in the HEC. Equivalent to existence of a contraction map (for rational coefficients, proven by Bao, Furuya, Naskar 2025).
- **Facet inequality** = valid AND irredundant (defines a codimension-1 face of the cone). Determined by linear algebra: an inequality is a facet iff 2^N - 2 linearly independent entropy vectors saturate it.
- **Redundant inequality** = valid but implied by other valid inequalities. Does not define a face of the cone.

The contraction map encodes only the "cutting and regluing" argument for why the inequality holds. Two inequalities with identical contraction maps can have different facet status. A contraction map proof for a redundant inequality is just as valid as one for a facet; the proof carries no facet information.

### Proof Methods Taxonomy

| Method | Proves Validity | Determines Facet Status | Scope | References |
| --- | --- | --- | --- | --- |
| Contraction maps | Yes | No | All rational HEIs | Bao et al. 2015; Bao, Furuya, Naskar 2025 |
| Geometric cut-and-glue (Headrick-Takayanagi) | Yes | No | SSA, MMI; prototype for contraction maps | Headrick, Takayanagi 2007; Hayden et al. 2013 |
| Graph model extreme ray enumeration | Indirect (completeness) | Yes (by computing full cone) | Requires full enumeration; feasible for N <= 5 | Hernandez-Cuenca 2019; Avis, Hernandez-Cuenca 2021 |
| Saturating vector construction | No (assumes validity) | Yes | Proving known-valid inequalities are facets | Czech, Liu, Yu 2024 |
| Bit threads | Yes (limited) | No | Small cases; limited generality | Freedman, Headrick 2017; Hubeny 2018 |
| Majorization test | Yes (characterization) | Unknown | All HEIs (conjectured) | Hubeny et al. 2025 |
| Marginal independence / PMI | Structural characterization | Unknown | HEC reconstruction | Hernandez-Cuenca, Hubeny, Rota 2022 |
| Information-theoretic (this project) | Goal: Yes | Goal: Yes | To be determined | --- |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
| --- | --- | --- | --- |
| Framework for entropy vectors | Polyhedral geometry (cone = intersection of half-spaces) | Algebraic geometry / variety approach | HEC is a polyhedral cone, not an algebraic variety; polyhedral methods are exact and well-understood |
| Proof of inequality validity | Contraction maps | Bit threads | Bit threads have limited scope; contraction maps are proven complete for rational HEIs |
| Facet determination | Full cone computation (double description) | Ad hoc checking | Full computation is the only rigorous method known; ad hoc methods miss redundancies |
| Basis for entropy space | Standard subsystem entropies S(I) | K-basis (He, Headrick, Hubeny 2019) | K-basis is useful for structural insight but subsystem entropies are more natural for polyhedral computation |

## Sources

- Ryu, Takayanagi, "Holographic Derivation of Entanglement Entropy from AdS/CFT," PRL 96 (2006) 181602, arXiv:hep-th/0603001 -- Defines the RT formula that generates all entropy vectors we study
- Headrick, Takayanagi, "A holographic proof of the strong subadditivity of entanglement entropy," PRD 76 (2007) 106013, arXiv:0704.3719 -- First geometric proof of SSA for holographic entropy; prototype of contraction map method
- Hayden, Headrick, Maloney, "Holographic mutual information is monogamous," PRD 87 (2013) 046003, arXiv:1107.2940 -- Proved MMI; first inequality distinguishing holographic from quantum entropy cone
- Bao, Nezami, Ooguri, Stoica, Sully, Walter, "The Holographic Entropy Cone," JHEP 09 (2015) 130, arXiv:1505.07839 -- Foundational paper: defined HEC, proved N <= 4 completeness, introduced contraction maps and graph models
- Hernandez-Cuenca, "The Holographic Entropy Cone for Five Regions," PRD 100 (2019) 026004, arXiv:1903.09148 -- Complete N=5 classification: 372 facets, 2267 extreme rays, 19 orbits
- He, Headrick, Hubeny, "Holographic Entropy Relations Repackaged," JHEP 10 (2019) 118, arXiv:1905.06985 -- K-basis and primitive information quantities
- Avis, Hernandez-Cuenca, "On the foundations and extremal structure of the holographic entropy cone," Discrete Applied Mathematics 328 (2023) 16, arXiv:2102.07535 -- Graph-theoretic foundations; recomputed N=5; partial N=6
- Hernandez-Cuenca, Hubeny, Rota, "The holographic entropy cone from marginal independence," JHEP 09 (2022) 190, arXiv:2204.00075 -- PMI-based HEC reconstruction
- Hernandez-Cuenca, Hubeny, Jia, "Holographic Entropy Inequalities and Multipartite Entanglement," JHEP 08 (2024) 238, arXiv:2309.06296 -- 1800+ new N=6 inequalities; multipartite information structure; superbalance no-go
- Czech, Liu, Yu, "Two infinite families of facets of the holographic entropy cone," SciPost Physics (2024), arXiv:2401.13029 -- First general-N facet proof beyond MMI
- Bao, Furuya, Naskar, "Properties of the contraction map for HEE inequalities," JHEP 06 (2024) 039, arXiv:2403.13283 -- Contraction map properties and partial cube triality
- Bao, Furuya, Naskar, "A framework for generalizing toric inequalities," JHEP 10 (2024) 251, arXiv:2408.04741 -- Multi-parameter toric generalization
- Bao, Furuya, Naskar, "Towards a complete classification of holographic entropy inequalities," JHEP 03 (2025) 117, arXiv:2409.17317 -- Deterministic method for finding all contraction-map-provable HEIs; argued completeness
- "Nesting is not Contracting," JHEP 06 (2025) 122, arXiv:2501.17222 -- Structural analysis of contraction proofs via EWN
- Bao, Furuya, Naskar, "On the completeness of contraction map proof method," JHEP 12 (2025) 140, arXiv:2506.18086 -- Proved contraction maps necessary and sufficient for rational HEIs
- Hubeny et al., "A new characterization of the holographic entropy cone," arXiv:2508.21823 -- Majorization characterization
- "Exploring the holographic entropy cone via reinforcement learning," arXiv:2601.19979 -- RL-based facet discovery; resolved 3 of 6 mystery N=6 extreme rays
- GitHub database: https://github.com/SergioHC95/Holographic-Entropy-Cone -- Computational database of HEC extremal elements
