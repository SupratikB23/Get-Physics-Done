# Methods Research

**Domain:** Holographic entanglement / polyhedral geometry / quantum information theory
**Researched:** 2026-04-05
**Confidence:** HIGH (for established methods), MEDIUM (for novel IT-geometric bridge)

## Scope Boundary

METHODS.md covers analytical and combinatorial PHYSICS methods for proving holographic entropy inequalities and detecting facet status of the holographic entropy cone (HEC). It does NOT cover software tools or libraries -- those belong in COMPUTATIONAL.md. The focus is on the interplay between information-theoretic proof techniques and polyhedral geometry.

---

## Recommended Methods

### Analytical Methods

| Method | Purpose | Why Recommended |
| --- | --- | --- |
| Contraction maps | Prove validity of candidate HEC inequalities | Proven complete for HEIs with rational coefficients (arXiv:2506.18086); the standard and only systematically complete proof method |
| Graph model construction | Prove validity by realizing entropy vectors on weighted graphs via min-cut | Constructive; directly connects to RT formula; essential for extreme ray verification |
| Superbalance / primitivity analysis | Filter candidate inequalities; necessary condition for non-SA HEIs | All non-SA non-redundant HEIs are superbalanced (arXiv:2002.04558); cheap combinatorial filter |
| K-basis decomposition | Re-express inequalities to reveal positivity structure | All HEIs have non-negative K-basis coefficients; makes facet structure more transparent (arXiv:1905.06985) |
| Marginal independence reconstruction | Derive HEC structure from patterns of marginal independence (PMIs) | Reconstructs the entire HEC from combinatorial data about which mutual informations vanish (arXiv:2204.00075) |
| Codimension-1 saturation test | Determine facet vs. redundant status of a valid inequality | The definitive geometric test: construct 2^N - 2 linearly independent saturating entropy vectors |

### Numerical Methods

| Method | Purpose | When to Use |
| --- | --- | --- |
| Vertex/facet enumeration (double description) | Convert between H-representation (inequalities) and V-representation (extreme rays) of cones | Essential for complete cone classification at fixed N; use cdd/lrs/normaliz |
| Linear programming for saturation | Find entropy vectors saturating a given inequality | Testing whether a specific inequality is a facet by maximizing dimension of saturating face |
| Graph model search (exhaustive/heuristic) | Find graph realizations of candidate entropy vectors | Verifying extreme rays of HEC; demonstrating that candidate vectors lie inside the cone |
| Reinforcement learning for graph search | Explore large graph spaces for entropy vector realizations | N >= 6 where exhaustive search is infeasible (arXiv:2601.19979) |

---

## Method Details

### Method 1: Contraction Maps

**What:** A contraction map is a combinatorial map from subsets of boundary regions to subsets, which reassigns pieces of RT surfaces on the "greater-than" side of an inequality to candidate RT surfaces on the "less-than" side. The RT formula then implies the inequality holds because the candidate surfaces have area >= the true minimal surfaces.

**Mathematical basis:** Given a candidate inequality sum_I a_I S(A_I) >= 0, a contraction map f partitions each A_I (with a_I > 0) into segments and reassigns them to form candidate homologous surfaces for each A_J (with a_J < 0). The min-cut property of RT surfaces then implies the inequality.

**Completeness:** Bao, Furuya, and Naskar (arXiv:2506.18086) proved that for all linear HEIs with rational coefficients, a contraction map exists if and only if the inequality is valid. This resolves the long-standing question of completeness of the contraction map method.

**Connection to partial cubes:** The triality established in arXiv:2409.17317 shows that HEIs, contraction maps, and partial cubes (isometric subgraphs of hypercubes) are in one-to-one correspondence. Finding all HEIs is equivalent to finding all partial cubes that are images of contraction maps.

**Known failure modes:**
- Cannot determine facet status. A valid inequality proven by contraction map may be a facet or redundant; the contraction map itself carries no information about which.
- Contraction maps are not unique. Different contraction maps can prove the same inequality (arXiv:2501.17222 "Nesting is not Contracting").
- All contraction map proofs necessarily involve candidate RT surfaces violating entanglement wedge nesting (EWN).

**Relevance to this project:** This is the method we seek to supplement, not replace. The project goal is an IT-based method that carries facet information the contraction map lacks.

**Confidence:** HIGH. Completeness proven; method is mature and well-understood.

**Key references:**
- Bao et al., JHEP 09 (2015) 130, arXiv:1505.07839 (original)
- Bao, Furuya, Naskar, JHEP 03 (2025) 117, arXiv:2409.17317 (classification via partial cubes)
- Bao, Furuya, Naskar, JHEP 12 (2025) 140, arXiv:2506.18086 (completeness proof)
- Czech, Shuai, JHEP 06 (2025) 122, arXiv:2501.17222 (EWN structure of contraction proofs)


### Method 2: Codimension-1 Saturation Test (Facet Detection)

**What:** A valid inequality defines a facet of the HEC if and only if the set of holographic entropy vectors saturating it (achieving equality) spans a hyperplane of codimension 1 in the full entropy vector space (dimension 2^N - 2 after quotienting by purification).

**Mathematical basis:** For an N-party system, the entropy vector space has dimension d = 2^N - 2 (for 2^N - 1 non-empty subsystems minus 1 from the purification constraint S(A) = S(A^c) for pure states). An inequality H(v) >= 0 defines a facet of the cone C if and only if the face F = {v in C : H(v) = 0} has dimension d - 1, i.e., there exist d - 1 linearly independent vectors in F.

**Algorithm:**
1. Enumerate (or search for) holographic entropy vectors v_1, ..., v_k that saturate the inequality
2. Check if rank({v_1, ..., v_k}) = d - 1
3. If yes: inequality is a facet. If rank < d - 1: inequality is NOT a facet (it lies on a proper face of higher codimension, or is redundant).

**How to find saturating vectors:** Construct graph models (star graphs, tree graphs, more complex graphs) whose min-cut entropies exactly saturate the inequality. Czech, Liu, and Yu (arXiv:2401.13029) demonstrated this approach for infinite families, constructing exactly 2^N - 2 linearly independent saturating vectors for each inequality.

**Known failure modes:**
- Requires knowing the full HEC (or at least enough extreme rays) to guarantee completeness
- Finding saturating graph models is itself non-trivial; no systematic algorithm exists for arbitrary inequalities
- Computationally expensive for large N due to the exponential dimension of entropy space

**Relevance to this project:** This is the DEFINITIVE geometric method for facet detection. Any IT-based method must either reproduce this test or provide an alternative criterion that is equivalent to it.

**Confidence:** HIGH. Standard polyhedral geometry; mathematically rigorous.


### Method 3: Superbalance and Primitivity Analysis

**What:** An entropy inequality is "balanced" if UV divergences cancel in the continuum limit (each pair of adjacent regions appears net zero times). It is "superbalanced" if this cancellation persists even after purifying any subset of parties.

**Mathematical basis (informal):** Write the inequality as sum_I c_I S(A_I) >= 0. Balance requires sum_I c_I |A_I intersect {i}| = 0 for each party i. Superbalance strengthens this: the same cancellation holds when any party is replaced by its purifier. Equivalently, every pair of parties {i,j} appears a net zero number of times across all terms.

**Key result (He, Hubeny, Rangamani, JHEP 07 (2020) 245, arXiv:2002.04558):** Every primitive (non-SA, non-redundant) HEI is superbalanced. This is a necessary condition, not sufficient. Superbalance acts as a filter: any candidate inequality that is NOT superbalanced can immediately be rejected as non-primitive.

**Complementary result:** Every HEI is a non-negative integer combination of SA instances and a superbalanced HEI (arXiv:2601.09987). This decomposition is the "primitive decomposition."

**Known failure modes:**
- Superbalance is necessary but not sufficient for being a valid HEI
- Does not distinguish facets from redundant inequalities
- Does not by itself prove an inequality

**Relevance to this project:** Superbalance is a structural property of HEIs that is information-theoretic in character (it concerns cancellation of divergences, which is about the UV structure of entanglement). It is a candidate ingredient for the IT proof method: if we can characterize what ADDITIONAL property beyond superbalance makes an inequality a facet, we may have the desired method.

**Confidence:** HIGH. Proven rigorously; well-established in the literature.


### Method 4: K-Basis and I-Basis Representations

**What:** Two alternative bases for the entropy vector space that make different structural properties of HEIs manifest.

**I-basis (arXiv:2309.06296):** The set of all singleton multipartite information quantities I_n(A_1:...:A_n) forms a basis. In this basis, HEIs have coefficients that alternate in sign with respect to the order n. This is the "information-theoretic" representation.

**K-basis (arXiv:1905.06985, "Holographic Entropy Relations Repackaged"):** Constructed from perfect tensor entropy vectors (which are extreme rays of the HEC). In this basis, ALL HEI coefficients are non-negative. This is a remarkable positivity property unique to holographic inequalities.

**Why K-basis positivity matters for facets:** Since K-basis elements are proportional to extreme rays, and HEIs have non-negative K-basis coefficients, the facet structure of the HEC is intimately connected to which subsets of extreme rays a given inequality "activates" (has zero coefficient for). A facet inequality must have its zero-coefficient K-basis elements spanning a codimension-1 face.

**Relevance to this project:** The K-basis provides a bridge between IT quantities (information measures) and polyhedral geometry (extreme rays, faces). The positivity property in the K-basis is potentially the key structural feature that an IT proof method can exploit. If an inequality's K-basis representation reveals its codimension structure, this could simultaneously prove validity (all coefficients non-negative) and detect facet status (the pattern of zero coefficients).

**Confidence:** MEDIUM-HIGH. The K-basis properties are established, but their connection to facet detection is NOT yet proven -- this is the open research direction.


### Method 5: Marginal Independence Reconstruction

**What:** Hernandez-Cuenca, Rolph, and Sorce (JHEP 09 (2022) 190, arXiv:2204.00075) showed that the HEC can be reconstructed entirely from data about which mutual informations vanish -- the "pattern of marginal independence" (PMI). The PMIs compatible with holography determine the extreme rays, and the cone they generate is the HEC.

**Mathematical basis:** A PMI specifies which pairs (or higher-order collections) of subsystems have zero mutual information. In holography, vanishing mutual information I(A:B) = 0 corresponds to disconnected entanglement wedges. The set of PMIs realizable by graph models defines the extreme ray structure of the HEC.

**Connection to correlation hypergraphs (arXiv:2412.18018):** The correlation hypergraph is a new representation of PMIs that encodes which subsystems share correlations. The graph theoretic structure of correlation hypergraphs provides necessary conditions for holographic realizability.

**Tree graph models (arXiv:2512.24490, arXiv:2512.18702):** Recent work provides necessary and sufficient conditions for entropy vectors to be realized by simple tree graph models, based on a "chordality condition" on the correlation hypergraph's line graph.

**Relevance to this project:** This is potentially the most promising avenue for the IT proof method. The marginal independence approach is inherently information-theoretic (it is about which subsystems are correlated) and simultaneously determines the extreme ray structure (which is the dual description of the facets). A method that characterizes facets through their PMI structure could be exactly what the project seeks.

**Confidence:** MEDIUM. The reconstruction works for known cases (N <= 5), but its capacity to distinguish facets from redundant inequalities has not been demonstrated. This is an open question.


### Method 6: Graph Model Constructions (Extreme Ray Verification)

**What:** To verify that a candidate entropy vector lies in the HEC, construct a weighted graph whose min-cut entropies reproduce the target vector.

**Types of graph models:**
- **Star graphs:** A central vertex connected to N boundary vertices. The simplest models. Star graph entropy vectors are always holographic. Many extreme rays of the HEC are star graph realizable (7 of 19 orbits for N=5, per arXiv:1903.09148).
- **Tree graphs:** Generalization of star graphs to tree topologies. Simple tree graph models are conjectured to provide building blocks for the HEC.
- **General graphs:** Arbitrary weighted graphs. Required for the remaining 12 extreme ray orbits at N=5 that are not star/tree realizable.
- **Perfect tensor states (flower graphs):** Special graph models associated with K-basis elements. Used in facet verification (arXiv:2401.13029).

**Known results for facet verification using graph models:** Czech, Liu, and Yu (arXiv:2401.13029) verified that two infinite families of HEIs (toric and projective inequalities) are facets by constructing 2^N - 2 linearly independent saturating entropy vectors from star graphs and perfect tensor states.

**Confidence:** HIGH for validity testing; MEDIUM for systematic facet detection.


### Method 7: Bit Threads (Max-Flow/Min-Cut Duality)

**What:** Freedman and Headrick (Commun. Math. Phys. 352 (2017) 407, arXiv:1604.00354) reformulated the RT formula using flows: the entanglement entropy S(A) equals the maximum flux of a divergence-free, norm-bounded vector field through the boundary region A.

**Mathematical basis:** By the max-flow/min-cut theorem, max flux = min cut area = S(A). Entropy inequalities correspond to properties of multicommodity flows. For example, strong subadditivity follows from the ability to decompose a max-flow into component flows.

**Advantage for proofs:** Bit thread proofs of entropy inequalities map transparently to information-theoretic meanings. The flow decomposition makes the "reason" for an inequality visible in a way that contraction maps do not.

**Known failure modes:**
- Multicommodity flow problems in continuous settings are technically demanding
- Not all HEIs have known bit thread proofs (the method has not been shown to be complete)
- Extension to quantum corrections (quantum bit threads, arXiv:2105.08063) adds complexity

**Relevance to this project:** Bit threads provide an alternative proof framework that is closer to IT reasoning than contraction maps. The flow decomposition structure might carry facet information. However, there is no known result connecting bit thread structure to facet detection. This is a speculative direction.

**Confidence:** MEDIUM for proving validity; LOW for facet detection (no existing results).


### Method 8: Vertex/Facet Enumeration (Double Description Method)

**What:** Given the H-representation (set of linear inequalities), compute the V-representation (extreme rays) of the HEC, or vice versa. This is the fundamental computational problem for complete cone classification.

**Mathematical basis:** The double description method (Motzkin et al. 1953, revised by Fukuda and Prodon 1996) incrementally constructs extreme rays from inequalities. The reverse search method (Avis and Fukuda) provides an alternative with good parallelization properties.

**Computational complexity:** The vertex/facet enumeration problem is polynomial in |H| + |V| for simple polytopes, but NP-hard for unbounded polyhedra in general. For the HEC specifically:
- N=4: d = 14 (after purification, d = 7). Trivially computable.
- N=5: d = 30 (after purification, d = 15). 372 facets, 2267 extreme rays (19 orbits). Computed by Hernandez-Cuenca (2019).
- N=6: d = 62 (after purification, d = 31). Partial results only. The number of extreme rays and facets is not fully known.

**Symmetry exploitation:** The permutation group S_N acts on the entropy vector space. Exploiting this symmetry (working with orbits rather than individual rays/facets) is essential for N >= 5. Software: PANDA supports symmetry-aware enumeration.

**Confidence:** HIGH. Standard computational geometry; implementations are mature.

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
| --- | --- | --- |
| Contraction maps for validity proof | Bit threads (max-flow) | When seeking IT-transparent proofs; not yet proven complete |
| Codimension-1 saturation for facet test | K-basis coefficient analysis | When seeking an IT criterion that avoids explicit enumeration |
| Double description for enumeration | Reverse search (lrs) | When memory is limiting (lrs has polynomial memory) |
| Graph model construction for extreme rays | Reinforcement learning search | At N >= 6 where exhaustive search is infeasible |
| PMI reconstruction | Direct inequality search | When the extreme ray structure is unknown a priori |

## What NOT to Use

| Avoid | Why | Use Instead |
| --- | --- | --- |
| Shannon-type inequality machinery alone | The HEC is strictly contained in the quantum entropy cone, which is strictly contained in the Shannon cone. Shannon-type methods prove too much (non-holographic inequalities) and miss holographic structure. | Use graph model / contraction map methods specific to holographic states |
| Non-Shannon inequality search (Zhang-Yeung style) | Non-Shannon inequalities arise for classical random variables (n >= 4). The quantum and holographic settings have different structure. The quantum entropy cone is not even polyhedral for n >= 4 (Matus 2007). | Use holographic-specific methods (contraction maps, graph models) |
| Fourier-Motzkin elimination for large N | Doubly exponential blowup in the number of intermediate inequalities. Completely infeasible for N >= 5. | Use double description or reverse search with symmetry exploitation |
| Naive brute-force graph enumeration for N >= 6 | Combinatorial explosion in the number of graphs to test. | Use heuristic search, RL-assisted search, or symmetry reduction |
| Treating the HEC as a polytope (bounded) | The HEC is a cone (unbounded). Methods designed for bounded polytopes may fail or give misleading results. | Always work with cone-specific algorithms |

## Method Selection by Problem Type

**If proving a candidate inequality is valid:**
- Use contraction maps (complete, algorithmic). The partial cube characterization (arXiv:2409.17317) provides a systematic search procedure.
- Fallback: construct graph models saturating the inequality to verify it holds on all holographic states.

**If determining whether a valid inequality is a facet:**
- Primary: codimension-1 saturation test. Construct 2^N - 2 linearly independent saturating holographic entropy vectors.
- Speculative alternative: K-basis coefficient analysis. Investigate whether the pattern of zero K-basis coefficients characterizes facets.
- Speculative alternative: PMI characterization. Investigate whether the pattern of marginal independences on the saturating face characterizes facets.

**If classifying the complete HEC at fixed N:**
- Compute all extreme rays via double description (with symmetry exploitation)
- Verify each extreme ray is holographic by constructing graph models
- The dual (H-representation) gives all facets
- Verify facet status via saturation test

**If exploring the HEC at large N (N >= 6):**
- Use the partial cube / contraction map search algorithm of arXiv:2409.17317 to find candidate inequalities
- Use RL-assisted graph model search (arXiv:2601.19979) to verify extreme rays
- Exploit infinite families of known facets (toric and projective, arXiv:2401.13029) as structural scaffolding

## Validation Strategy by Method

| Method | Validation Approach | Key Benchmarks |
| --- | --- | --- |
| Contraction map proof | Verify map is well-defined (every region piece reassigned exactly once); check inequality on explicit graph models | Reproduce SA, SSA, MMI proofs; match N=4 HEC (Bao et al. 2015) |
| Facet detection (saturation) | Verify linear independence of saturating vectors; check rank computation numerically and symbolically | Reproduce N=4 facets (SA + MMI); reproduce N=5 facets (372 facets, Hernandez-Cuenca 2019) |
| K-basis decomposition | Verify all coefficients non-negative; cross-check against known inequalities in S-basis | Match known K-basis decompositions for MMI, toric/projective families |
| Graph model construction | Verify min-cuts match target entropy vector; check all 2^N - 1 cuts | Match known extreme rays for N <= 5 |
| Double description enumeration | Run both H-to-V and V-to-H; verify mutual consistency; check against known results | Reproduce N=4 (SSA+MMI gives 8 extreme ray orbits); reproduce N=5 (372 facets, 2267 extreme rays in 19 orbits) |

---

## Critical Methodological Gaps Relevant to This Project

### Gap 1: No IT criterion for facet status exists

**Status:** OPEN. The central research question of this project.

No information-theoretic property is currently known that distinguishes facet inequalities from redundant ones. Superbalance is necessary for non-SA HEIs but does not distinguish facets. K-basis positivity holds for all valid HEIs, not just facets. The codimension-1 saturation test is purely geometric, not information-theoretic.

**Promising direction:** The K-basis provides the tightest known bridge between IT structure and polyhedral geometry. Since K-basis elements are extreme rays (perfect tensor states), the K-basis decomposition of an inequality encodes which extreme rays it "sees." A facet must be saturated by a codimension-1 set of extreme rays. The K-basis coefficient pattern might encode this.

**Alternative promising direction:** The marginal independence (PMI) reconstruction shows that IT data (which mutual informations vanish) determines the cone. Facets might correspond to specific PMI patterns on their saturating faces.

### Gap 2: Contraction maps are complete but "blind" to facet structure

**Status:** RESOLVED as a theoretical result, but creates the practical problem this project addresses.

The completeness proof (arXiv:2506.18086) shows contraction maps are necessary and sufficient for validity. But the non-uniqueness of contraction maps (arXiv:2501.17222) and their violation of entanglement wedge nesting mean they carry structural information about the proof, not about the inequality's geometric role in the cone.

### Gap 3: Computational barrier at N=6

**Status:** OPEN. The enumeration problem becomes genuinely hard.

The entropy vector space at N=6 has dimension 31 (after purification). Complete extreme ray enumeration is at the boundary of computational feasibility. New methods (RL search, symmetry exploitation, infinite families) are needed.

---

## Connection Between IT Structure and Polyhedral Structure

This section synthesizes the key insight relevant to the project's central question.

### What is known

1. **Validity = contraction map existence** (complete, arXiv:2506.18086). This is a combinatorial/graph-theoretic criterion.

2. **Facet = codimension-1 saturation** (standard polyhedral geometry). This is a geometric criterion.

3. **Superbalance = necessary for primitive HEIs** (arXiv:2002.04558). This is an IT-flavored structural property.

4. **K-basis positivity = necessary and sufficient for HEI validity** (arXiv:1905.06985, assuming the K-basis spans the extreme rays). This is an IT-geometric bridge: the K-basis is information-theoretic (built from multipartite information quantities) and geometric (its elements are extreme rays).

5. **PMI reconstruction = IT data determines the cone** (arXiv:2204.00075). The pattern of vanishing mutual informations determines which entropy vectors are holographic.

### What is not known (and constitutes the project's research frontier)

6. **What IT property, beyond validity, characterizes facets?** The K-basis coefficients of a facet inequality versus a redundant inequality must differ in a way that encodes the codimension of the saturating face. Characterizing this difference is the project goal.

7. **Can the PMI structure of the saturating face of an inequality distinguish facets?** A facet's saturating face has maximal dimension. The PMIs realized on this face might have a distinctive IT character.

8. **Does the contraction map's violation of EWN encode facet information?** Czech and Shuai (arXiv:2501.17222) showed that EWN violations are structured. Whether this structure correlates with facet status is unknown.

---

## Sources

### Foundational
- Bao, Nezami, Ooguri, Stoica, Sully, Walter, "The Holographic Entropy Cone," JHEP 09 (2015) 130, arXiv:1505.07839 [HIGH confidence]
- Hernandez-Cuenca, "The Holographic Entropy Cone for Five Regions," Phys. Rev. D 100 (2019) 026004, arXiv:1903.09148 [HIGH confidence]

### Contraction Maps and Completeness
- Bao, Furuya, Naskar, "Towards a complete classification of holographic entropy inequalities," JHEP 03 (2025) 117, arXiv:2409.17317 [HIGH confidence]
- Bao, Furuya, Naskar, "On the completeness of contraction map proof method for holographic entropy inequalities," JHEP 12 (2025) 140, arXiv:2506.18086 [HIGH confidence]
- Czech, Shuai, "Nesting is not Contracting," JHEP 06 (2025) 122, arXiv:2501.17222 [HIGH confidence]

### Information-Theoretic Structure
- He, Hubeny, Rangamani, "Superbalance of Holographic Entropy Inequalities," JHEP 07 (2020) 245, arXiv:2002.04558 [HIGH confidence]
- He, Hubeny, Rota, "Holographic Entropy Relations Repackaged," JHEP 10 (2019) 118, arXiv:1905.06985 [HIGH confidence]
- Czech, Liu, Yu, "Two infinite families of facets of the holographic entropy cone," SciPost Phys., arXiv:2401.13029 [HIGH confidence]

### Marginal Independence and Correlation Hypergraphs
- Hernandez-Cuenca, Rolph, Sorce, "The holographic entropy cone from marginal independence," JHEP 09 (2022) 190, arXiv:2204.00075 [HIGH confidence]
- Hernandez-Cuenca, Li, Rolph, "Correlation hypergraph: a new representation of a quantum marginal independence pattern," JHEP 09 (2025) 080, arXiv:2412.18018 [HIGH confidence]
- Hernandez-Cuenca, Li, Rolph, "Necessary and sufficient conditions for entropy vector realizability by holographic simple tree graph models," arXiv:2512.24490 [MEDIUM-HIGH confidence]

### Bit Threads
- Freedman, Headrick, "Bit threads and holographic entanglement," Commun. Math. Phys. 352 (2017) 407, arXiv:1604.00354 [HIGH confidence]

### Graphical Proof Framework
- "A graphical framework for proving holographic entanglement entropy inequalities in multipartite systems," arXiv:2512.18726 [MEDIUM confidence]

### Combinatorial Properties
- "Combinatorial properties of holographic entropy inequalities," arXiv:2601.09987 [MEDIUM confidence]
- "Holographic entropy inequalities pass the majorization test," arXiv:2601.09989 [MEDIUM confidence]

### Computational Methods for Polyhedral Geometry
- Fukuda, Prodon, "Double Description Method Revisited," Springer, 1996 [HIGH confidence]
- Avis, Fukuda, "A pivoting algorithm for convex hulls and vertex enumeration of arrangements and polyhedra," Discrete Comput. Geom. 8 (1992) 295 [HIGH confidence]
- Assarf et al., "Computing convex hulls and counting integer points with polymake," Math. Prog. Comp. 9 (2017) 1 [HIGH confidence]

### Novel Directions
- Grimaldi, Headrick, Hubeny, "A new characterization of the holographic entropy cone," arXiv:2508.21823 [MEDIUM confidence -- preprint, very recent]
- Bousso, Kaya, "Holographic Entropy Cone Beyond AdS/CFT," arXiv:2502.03516 [MEDIUM confidence]
- "Exploring the holographic entropy cone via reinforcement learning," arXiv:2601.19979 [MEDIUM confidence]
- "Renormalization Group is the Principle behind the Holographic Entropy Cone," arXiv:2601.02472 [MEDIUM confidence]

---

_Methods research for: Holographic entropy cone proof methods and facet detection_
_Researched: 2026-04-05_
