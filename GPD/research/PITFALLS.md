# Known Pitfalls Research

**Domain:** Holographic entropy cone classification, entropy inequality proofs, polyhedral geometry
**Researched:** 2026-04-05
**Confidence:** HIGH (for critical/moderate pitfalls); MEDIUM (for IT-method-specific pitfalls, since the IT proof method is novel and untested)

---

## Critical Pitfalls

Mistakes that invalidate results or waste months of computation.

### Pitfall 1: Confusing HEC Validity with Facet Status

**What goes wrong:**
A contraction map proof (or any proof) establishes that an inequality is *valid* for all holographic states, but the researcher concludes it is therefore a *facet* of the HEC. Validity and facet status are logically independent properties: a valid inequality can be redundant (implied by other facets). The contraction map method, by construction, proves validity but is blind to whether the inequality is irredundant. This is the single most important conceptual distinction in the project.

**Why it happens:**
The literature often presents new holographic entropy inequalities without immediately determining their facet status, and many papers use "new HEC inequality" loosely when they mean "new valid inequality." The facet check requires a separate, independent computation: one must show that the inequality defines a codimension-1 face of the cone, i.e., that a sufficient number of linearly independent extreme rays saturate it. This step is often deferred or omitted entirely.

**How to avoid:**
Always maintain a strict two-column classification: (1) is the inequality valid? (2) is it a facet? For any new inequality, perform both checks independently. The facet check requires constructing a maximal set of linearly independent holographic entropy vectors that saturate the inequality and verifying that this set spans a codimension-1 subspace. Czech, Liu, and Yu (arXiv:2401.13029) give explicit examples of the required saturation constructions using star graphs and perfect tensors.

**Warning signs:**
- Claiming a new "facet" based only on a contraction map proof
- Inability to exhibit saturating extreme rays
- No explicit dimension count of the saturating face

**Phase to address:**
Phase 1 (foundations and benchmarking) -- the N=4 benchmark must separately verify both validity and facet status for every inequality tested.

**References:**
- Bao et al., arXiv:1505.07839 (original HEC paper, establishes the distinction)
- Czech, Liu, Yu, arXiv:2401.13029 (explicit facet verification via saturation)
- Avis and Hernandez-Cuenca, arXiv:2102.07535 (systematic facet/extreme ray computation)

---

### Pitfall 2: Assuming the IT Method Must Reproduce Contraction Map Structure

**What goes wrong:**
The researcher designs the information-theoretic proof method to mimic the structure of contraction maps (bit-string assignments, graph embeddings) and then "discovers" that the IT method reduces to contraction maps. The result is tautological: the method provides no new capability because it was built to replicate the old one.

**Why it happens:**
Contraction maps are the only established proof technique for HEC inequalities, so they naturally dominate the researcher's mental model. Bao, Furuya, and Naskar (arXiv:2506.18086) proved that contraction maps are both sufficient and necessary for all linear HEC inequalities with rational coefficients. This completeness result means any alternative proof method for validity alone is logically equivalent to finding a contraction map. Therefore, the IT method's value cannot lie in proving validity differently -- it must lie in extracting *additional information* (facet vs. redundant) that contraction maps do not provide.

**How to avoid:**
The IT method must be designed from the start to produce a structural invariant or certificate that distinguishes facets from redundant inequalities. This means the method must access information beyond what a contraction map encodes -- for example, the dimension of the saturation locus, the structure of the set of saturating graphs, or an information-theoretic characterization of when an inequality is "tight" in a maximal sense. Do not optimize the IT method for validity proofs; optimize it for the facet/redundant distinction.

**Warning signs:**
- The IT proof reduces to checking existence of a contraction map
- No structural difference observed between IT proofs of facets vs. redundant inequalities
- The method works for validity but adds nothing to facet classification

**Phase to address:**
Phase 2 (method development) -- the method design must explicitly target the facet/redundant distinction from day one, not as an afterthought.

**References:**
- Bao, Furuya, Naskar, arXiv:2506.18086 (completeness of contraction maps)
- Bao, Furuya, Naskar, arXiv:2409.17317 (triality: HEIs, contraction maps, partial cubes)

---

### Pitfall 3: The 2^N Dimensional Explosion

**What goes wrong:**
The entropy vector space for N parties has dimension 2^N - 1 (one component S(A) for each non-empty subset A). At N=4 this is 15 dimensions; at N=5 it is 31 dimensions. Polyhedral computations (vertex enumeration, facet enumeration, linear programming over the cone) scale extremely poorly with this ambient dimension. Researchers underestimate the computational cost and attempt brute-force enumeration that is feasible at N=4 but completely intractable at N=5.

**Why it happens:**
N=4 is deceptively easy. The HEC at N=4 has only 2 facet orbits (SSA and MMI under permutations) and a manageable number of extreme rays. N=5 already has at least 7 orbits of facets (the 5 new inequalities beyond SSA and MMI reported in Hernandez-Cuenca arXiv:1903.09148, plus the known ones), and the number of extreme ray orbits grows substantially. The double exponential growth in the number of candidate inequalities makes exhaustive enumeration impractical.

**How to avoid:**
(a) Exploit symmetry aggressively: the permutation group S_N acts on the entropy vector space and reduces the effective dimension. Work with orbits under S_N, not individual inequalities/rays. (b) Use exact rational arithmetic, not floating-point, for all polyhedral computations -- degeneracy detection is impossible with floating-point. (c) Use mature polyhedral computation libraries (cddlib, lrs, polymake) that handle degeneracy correctly. (d) Set explicit computational budgets and bail-out criteria before starting enumeration at N=5.

**Warning signs:**
- Enumeration at N=5 running for days without convergence
- Memory usage growing exponentially during double-description iterations
- Intermediate cone representations orders of magnitude larger than the final result (a known pathology of the DD method sensitive to insertion order)

**Phase to address:**
Phase 3 (N=5 application) -- computational feasibility must be assessed before committing to a brute-force strategy. Phase 1 should establish the computational pipeline on N=4 first.

**References:**
- Avis and Hernandez-Cuenca, arXiv:2102.07535 (computational methods for HEC)
- Hernandez-Cuenca, arXiv:1903.09148 (N=5 HEC)
- Fukuda, "Frequently Asked Questions in Polyhedral Computation" (cddlib documentation on DD method pathologies)

---

### Pitfall 4: Mistaking Necessary Conditions for Sufficient Conditions in Inequality Proofs

**What goes wrong:**
The researcher proves that a candidate inequality is satisfied by all graph models tested (necessary condition for being a valid HEI), and concludes the inequality is valid for all holographic states (sufficient condition). This confuses empirical evidence with proof. Conversely, showing that an inequality *can* be saturated by some holographic state does not make it a facet -- it could still be redundant.

**Why it happens:**
Testing an inequality against a finite (even large) set of graph models is computationally straightforward and psychologically satisfying. But the HEC is defined by validity on *all* holographic states, which form a continuum. A finite sample can miss violations. The correct standard is: (a) for validity, either a contraction map proof or the IT equivalent; (b) for facet status, a codimension-1 saturation argument with linearly independent saturating vectors.

**How to avoid:**
Maintain a strict hierarchy of evidence:
1. **Conjecture:** Inequality tested numerically on sample graphs, no violations found
2. **Proven valid:** Contraction map or equivalent proof exists
3. **Proven facet:** Codimension-1 saturation demonstrated

Never promote a result from level 1 to level 2 or 3 without the corresponding proof. Label all results with their evidence level explicitly.

**Warning signs:**
- Claims of "new facets" supported only by numerical testing
- No explicit proof construction (contraction map, IT proof, or saturation argument)
- Treating a large Monte Carlo search over graph models as a proof

**Phase to address:**
All phases -- this is a discipline issue that must be enforced from the start.

**References:**
- Bao et al., arXiv:1505.07839 (establishes proof standards for HEC)
- Bao, Furuya, Naskar, arXiv:2506.18086 (completeness theorem clarifying what constitutes a proof)

---

### Pitfall 5: Forgetting Purification and the Purifier Subsystem

**What goes wrong:**
In the holographic setting, the total system is pure (the boundary CFT state on the full boundary is pure), so S(A) = S(A^c) for any subsystem A and its complement A^c. This purification constraint halves the independent components of the entropy vector. Researchers sometimes write entropy inequalities in 2^N - 1 independent variables without imposing purification, producing inequalities that are not in the correct form for the HEC, or missing that purification makes some apparently distinct inequalities equivalent.

**Why it happens:**
When working abstractly with Shannon/von Neumann entropy, the natural setting is a mixed state with 2^N - 1 independent entropies. The holographic setting requires purity of the total state, reducing the independent entropies to 2^(N-1) - 1. Switching between these two conventions (with and without purification) is a common source of errors, especially when importing results from the quantum information literature (which typically does not assume purity).

**How to avoid:**
Fix notation at the outset: specify whether the N-party system includes or excludes the purifier. In the Bao et al. convention, the N "parties" are boundary subregions, and the purifier O is an additional implicit party satisfying S(A) = S(A^c O) where A^c O is the complement including the purifier. Every inequality must be written in a form consistent with this constraint. When comparing with quantum information results (which may not assume purity), explicitly impose purification and check whether the inequality reduces or becomes trivial.

**Warning signs:**
- The entropy vector has 2^N - 1 independent components instead of 2^(N-1) - 1
- An inequality that should be non-trivial becomes 0 >= 0 after imposing purification
- Two apparently different inequalities become identical after using S(A) = S(A^c)

**Phase to address:**
Phase 1 (foundations) -- the notation and convention for purification must be locked before any derivations begin.

**References:**
- Bao et al., arXiv:1505.07839 (Section 2: conventions on purification)
- Hernandez-Cuenca, arXiv:1903.09148 (explicit treatment of purification in N=5)

---

## Moderate Pitfalls

### Pitfall 6: The IT Method Works for N=4 But Fails to Generalize

**What goes wrong:**
The IT proof method successfully classifies all N=4 facets (SSA and MMI) but does so by exploiting structural features specific to N=4 (small number of subsystems, simple symmetry structure, only two facet orbits). When applied to N=5, the method either (a) fails to produce a facet/redundant classification, (b) produces wrong classifications, or (c) becomes computationally more expensive than contraction maps.

**Why it happens:**
N=4 is the first non-trivial case and has very special properties: subadditivity and MMI together completely characterize the cone, and the symmetry group is small enough that exhaustive analysis is feasible. Any method that handles two facet orbits and a 15-dimensional space may appear powerful but be relying on the simplicity of this case. The project's scoping contract explicitly flags this as a "false progress to reject."

**How to avoid:**
Design the method with generalization in mind from the start. Before declaring N=4 success, test whether the structural features the method uses are present at N=5. Specifically: (a) does the method produce a classification for all known N=5 inequalities? (b) does the computational cost scale reasonably? (c) does the method identify the same facets as the saturation-based approach?

**Warning signs:**
- The IT method uses case-by-case analysis that does not generalize
- The proof for MMI uses a different argument structure than the proof for N=5 inequalities
- Computational cost at N=5 is orders of magnitude worse than at N=4

**Phase to address:**
Phase 2 (method development) -- scalability testing should be integrated into the development cycle, not deferred to Phase 3.

**References:**
- PROJECT.md scoping contract: "false progress to reject: method works only for N<=4"

---

### Pitfall 7: Conflating the Holographic Entropy Cone with the Quantum Entropy Cone

**What goes wrong:**
The researcher assumes that a property proven for holographic states (those with smooth geometric bulk duals via RT) holds for all quantum states, or conversely, that a quantum information-theoretic result applies directly in the holographic setting without modification. The HEC is strictly contained within the quantum entropy cone (QEC), and neither cone's structure trivially determines the other's.

**Why it happens:**
The boundary between holographic and quantum results is subtle. Some inequalities (like strong subadditivity) hold for both. Others (like monogamy of mutual information) hold holographically but are violated by certain quantum states (e.g., the GHZ state). The "holographic" qualifier is easy to forget when working with information-theoretic tools, which naturally apply to all quantum states.

**How to avoid:**
Every result must carry an explicit label: "holographic" (proven via RT/graph models/contraction maps) or "quantum" (proven for all quantum states). When the IT method proves an inequality, it must be clear whether the proof uses holographic-specific structure (graph models, min-cut) or purely quantum information-theoretic tools. If the latter, the result may hold for the QEC, not just the HEC -- which is interesting but may not help with facet classification of the HEC specifically.

**Warning signs:**
- Proving an inequality using only subadditivity and strong subadditivity (these hold for all quantum states, so the result is about the QEC, not the HEC)
- Using holographic results to draw conclusions about quantum states in general
- Not checking whether the GHZ state or other known HEC-violating states are handled correctly

**Phase to address:**
Phase 1 (foundations) and Phase 2 (method development) -- the method must be clear about which cone it characterizes.

**References:**
- Bao et al., arXiv:1505.07839 (HEC strictly inside QEC)
- Cadney, Linden, Winter, arXiv:1107.2940 (monogamy of mutual information: holographic but not quantum)
- Czech, Dong, arXiv:2306.00199 (tip of the quantum entropy cone -- illustrates the gap)

---

### Pitfall 8: Incorrect Symmetry Reduction Leading to Missing or Duplicate Orbits

**What goes wrong:**
The permutation group S_N acts on the entropy vector space by permuting the N parties. Inequalities and extreme rays that are related by permutations form orbits, and one should classify orbits, not individual objects. Errors in the symmetry reduction (incorrect orbit representatives, missing orbits, double-counting) propagate into wrong facet counts.

**Why it happens:**
At N=5, S_5 has 120 elements, and the action on 2^5 - 1 = 31 subset-entropies is non-trivial. Computing orbit representatives requires careful group-theoretic bookkeeping. The purification constraint S(A) = S(A^c) introduces additional equivalences. Mistakes include: not accounting for the purifier when computing symmetries, using the wrong group action (permuting individual parties vs. permuting subsets), and missing stabilizer subgroups that make an orbit smaller than expected.

**How to avoid:**
Use computational algebra systems (GAP, SageMath) to compute orbits explicitly. Verify orbit counts against published results. For N=4, there should be 2 facet orbits (SSA and MMI). For N=5, the known result is approximately 7 facet orbits (SSA, MMI, plus 5 new orbits from Hernandez-Cuenca arXiv:1903.09148). Cross-check by computing |orbit| = |S_N| / |stabilizer| for each representative.

**Warning signs:**
- Facet or extreme ray counts that disagree with published values
- Orbits whose sizes do not divide |S_N| = N!
- Two "distinct" inequalities that are related by a permutation

**Phase to address:**
Phase 1 (foundations) -- the symmetry reduction pipeline must be validated on N=4 before being applied to N=5.

**References:**
- Hernandez-Cuenca, arXiv:1903.09148 (orbit classification for N=5)
- Avis and Hernandez-Cuenca, arXiv:2102.07535 (systematic symmetry reduction)

---

### Pitfall 9: Floating-Point Arithmetic in Polyhedral Computations

**What goes wrong:**
Using floating-point arithmetic for vertex/facet enumeration of the HEC produces incorrect results due to degeneracy. The HEC is highly degenerate (many extreme rays lie on the intersection of multiple facets), and floating-point perturbation can merge or split degenerate faces, creating phantom extreme rays or missing real ones.

**Why it happens:**
The entropy vectors in the HEC have rational entries (they come from min-cuts on weighted graphs with rational weights), and the cone itself is defined by rational linear inequalities. The H-representation to V-representation conversion involves solving systems of linear equations that are highly degenerate -- many more rays are "near" a hyperplane than exactly on it. Floating-point tolerance decisions (is this ray on the hyperplane or not?) inevitably produce errors.

**How to avoid:**
Use exact rational arithmetic exclusively. cddlib supports exact rational arithmetic via GMP. lrs (by David Avis, one of the authors of arXiv:2102.07535) uses exact arithmetic by default. Never use numpy/scipy floating-point linear algebra for the polyhedral computation step. Floating-point is acceptable only for non-critical tasks like visualization or rough feasibility checks.

**Warning signs:**
- Different results from H-to-V and V-to-H conversions (should be inverses)
- Extreme ray counts that change when numerical tolerance is varied
- Rays that are "almost" on a facet but not exactly

**Phase to address:**
Phase 1 (computational setup) -- the polyhedral computation pipeline must use exact arithmetic from the start.

**References:**
- Avis and Hernandez-Cuenca, arXiv:2102.07535 (uses lrs with exact arithmetic)
- Fukuda, "Frequently Asked Questions in Polyhedral Computation" (discusses floating-point pitfalls in DD method)

---

### Pitfall 10: The Contraction Map Completeness Result Constrains Alternative Approaches

**What goes wrong:**
The researcher develops an "alternative" proof method that is in fact logically equivalent to finding a contraction map, just expressed in different language. The completeness result of Bao, Furuya, and Naskar (arXiv:2506.18086) -- that contraction maps are both necessary and sufficient for all linear HEC inequalities with rational coefficients -- means that any alternative validity proof must be equivalent to a contraction map at some level. The researcher wastes effort on what amounts to a reformulation.

**Why it happens:**
The completeness theorem is recent (June 2025, published December 2025) and may not have been fully internalized. It establishes a strong equivalence: an inequality is a valid HEI if and only if it has a contraction map. This means the space for "alternative proofs of validity" is zero -- any such proof implicitly constructs a contraction map.

**How to avoid:**
Accept the completeness result and do not try to prove validity by a fundamentally different route. Instead, focus the IT method on what contraction maps *cannot* do: distinguish facets from redundant inequalities. The IT method's value proposition is not "prove validity differently" but "extract structural information (facet status) that contraction maps don't provide."

**Warning signs:**
- The IT method proves validity but does not address facet status
- The IT proof is translatable step-by-step into a contraction map argument
- No additional information beyond validity is extracted

**Phase to address:**
Phase 2 (method development) -- the method must be explicitly designed to go beyond validity.

**References:**
- Bao, Furuya, Naskar, arXiv:2506.18086 (completeness theorem)

---

## Minor Pitfalls

### Pitfall 11: Sign and Coefficient Errors in Multi-Term Inequalities

**What goes wrong:**
Holographic entropy inequalities for N >= 5 involve many terms (sums of entropies of various subsystems with integer coefficients that can be positive or negative). A sign error in one coefficient -- e.g., writing +S(ABC) instead of -S(ABC) -- produces an inequality that may still "look reasonable" but is either not valid or is a different inequality entirely.

**How to avoid:**
Use machine-readable representations of inequalities (coefficient vectors indexed by subsets). Never manipulate inequalities only in human-readable form. Verify every inequality by checking it against published coefficient vectors. Implement automated sign-checking by evaluating both sides on known extreme rays.

**Warning signs:**
- An inequality that should be tight on specific graph models is violated instead
- Coefficient vector that does not match published form after permutation

**Phase to address:**
All phases -- automated coefficient tracking should be standard infrastructure.

---

### Pitfall 12: Assuming SSA Is a Facet of the HEC

**What goes wrong:**
Strong subadditivity (SSA), S(AB) + S(BC) >= S(B) + S(ABC), is often listed as a "facet" of the HEC because it is a facet of the quantum entropy cone. However, in the holographic cone, SSA can be *implied* by other inequalities (subadditivity + MMI). Whether SSA is a facet of the HEC depends on the number of parties N and the specific formulation. The researcher must check irredundancy rather than assuming SSA is always a facet.

**How to avoid:**
Explicitly check whether each inequality is redundant by solving the linear program: can the inequality be written as a non-negative linear combination of other inequalities in the set? If yes, it is redundant. Do this for SSA in the specific formulation being used.

**Warning signs:**
- Facet count that disagrees with published values by the number of SSA instances
- Treating SSA and MMI as independently essential without checking

**Phase to address:**
Phase 1 (N=4 benchmark) -- the benchmark must correctly identify which inequalities are facets and which are redundant.

**References:**
- Bao et al., arXiv:1505.07839 (discusses the relationship between SSA and MMI in the HEC)
- Hernandez-Cuenca, arXiv:2204.00075 (marginal independence perspective clarifies redundancy)

---

### Pitfall 13: Ignoring the Superbalance Property

**What goes wrong:**
Holographic entropy inequalities satisfy a property called "superbalance": for every party i, the sum of coefficients of all terms containing i on the LHS equals the sum on the RHS. Superbalance is a necessary condition for an inequality to be holographic. Candidate inequalities that violate superbalance are not HEIs and should be immediately discarded. Failing to check superbalance wastes effort investigating non-holographic candidates.

**Why it happens:**
Superbalance is a non-obvious structural property. In a brute-force search for new inequalities, the candidate space is vast, and without the superbalance filter, most candidates are not holographic.

**How to avoid:**
Implement a superbalance check as the first filter on any candidate inequality. This is a simple linear condition on the coefficient vector and costs O(N * 2^N) to verify.

**Warning signs:**
- Large numbers of candidate inequalities passing initial tests but failing contraction map search
- Candidates that are valid quantum inequalities but not holographic

**Phase to address:**
Phase 1 (computational infrastructure) -- superbalance checking should be in the core toolbox.

**References:**
- Czech, Soni, "Superbalance of holographic entropy inequalities," arXiv:2307.13457

---

## Approximation Shortcuts

Shortcuts that seem reasonable but introduce systematic errors.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
| --- | --- | --- | --- |
| Testing on random graph models instead of proving formally | Quick empirical feedback on candidate inequalities | Can never promote a conjecture to a theorem; may miss rare violations | Acceptable for initial screening only; must be followed by formal proof |
| Working with floating-point instead of exact arithmetic for polyhedral geometry | 10-100x faster computation | Silent errors in degeneracy detection; phantom or missing extreme rays | Never acceptable for final facet/extreme ray enumeration |
| Ignoring purification (treating as mixed-state entropy cone) | Doubles the independent variables, simplifies some algebra | Wrong cone; inequalities may be trivially satisfied or have wrong dimension | Never acceptable for final results; useful only for preliminary intuition |
| Restricting to "simple" graph models (e.g., trees only) | Smaller search space for extreme rays | Misses non-tree extreme rays; incomplete cone description | Acceptable as a starting point; recent work (arXiv:2512.24490) characterizes tree-realizable vectors explicitly |
| Using known N=5 facet list without re-deriving | Saves time | If the list has errors or omissions, all downstream results are wrong | Acceptable if cross-checked against multiple published sources |

## Convention Traps

Common mistakes when converting between different conventions or comparing with literature.

| Convention Issue | Common Mistake | Correct Approach |
| --- | --- | --- |
| Purifier inclusion | Treating the N-party system as the entire Hilbert space (no purifier) when the holographic setting requires a pure state on N+1 parties | Always specify whether N counts boundary regions only or includes the purifier O. In the Bao et al. convention, N counts boundary regions and the purifier is implicit. |
| Entropy vector indexing | Inconsistent ordering of subsets in the entropy vector (e.g., lexicographic vs. size-first ordering) | Fix a canonical ordering at the start. Use the same ordering as the comparison literature (Bao et al. use a specific convention). Document the ordering explicitly in code. |
| Inequality normalization | Comparing inequalities with different overall normalizations (e.g., one source writes 2S(A) >= ... while another writes S(A) >= .../2) | Normalize all inequalities to have coprime integer coefficients with positive leading term before comparing. |
| Permutation action | Applying S_N to party labels vs. applying S_N to subset labels (these generate different groups on the entropy vector space) | S_N acts on party labels {1, ..., N}. This induces an action on subsets (and hence on entropy vector components). Implement the induced action, do not permute components directly. |
| "Region" vs. "party" | Conflating the number of boundary regions with the number of independent subsystems when purification is imposed | With purification, an N-region system has 2^(N-1) - 1 independent entropy components, not 2^N - 1. |

## Numerical Traps

Patterns that work for simple cases but fail for realistic calculations.

| Trap | Symptoms | Prevention | When It Breaks |
| --- | --- | --- | --- |
| DD method insertion-order sensitivity | Intermediate cone has exponentially more extreme rays than the final cone; computation exhausts memory | Use lexicographic or random ordering; use lrs (reverse search) instead of DD for large problems | N >= 5, highly degenerate cones |
| Naive LP for redundancy checking | Linear program returns "feasible" with floating-point tolerance, but the inequality is actually tight (degenerate) | Use exact arithmetic LP (e.g., QSopt_ex, lrs); avoid simplex with floating-point pivoting for degeneracy-sensitive questions | Any redundancy check, especially near-degenerate cases |
| Brute-force contraction map search | Exponential search space for bit-string assignments; backtracking explosion | Use the triality framework (arXiv:2409.17317) to reduce to graph isomorphism; exploit structure of partial cubes | N >= 5, inequalities with many terms |
| Memory explosion in extreme ray enumeration | Process killed by OOM for N >= 6; swap thrashing for N=5 | Compute orbits under S_N first, enumerate representatives only; use output-sensitive algorithms (lrs) | Ambient dimension >= 31 (N >= 5) |

## Interpretation Mistakes

Domain-specific errors in interpreting results beyond computational bugs.

| Mistake | Risk | Prevention |
| --- | --- | --- |
| Interpreting an IT proof as providing holographic insight when it uses only quantum (non-holographic) properties | The method works for the QEC, not the HEC; facet classification is for the wrong cone | Check whether the proof uses any holographic-specific structure (graph models, RT, min-cut). If not, the result may be about the QEC. |
| Claiming a new facet when the inequality is known but written in a different basis or convention | Apparent "discovery" is actually a permutation or relabeling of a known inequality | Before announcing a new facet, check all S_N images and purification equivalences against the known list. |
| Assuming that computational intractability at N=6 means the method is useless | The method may be valuable even if it does not scale to all N, as long as it provides insight at N=5 | Evaluate the method's contribution at each N separately; N=5 progress alone is valuable. |
| Conflating "IT proof exists" with "the inequality has an IT interpretation" | An IT proof might be purely technical (algebraic manipulation) without providing physical intuition about the inequality's role | Demand that the IT proof provides a structural reason for facet status, not just a verification. |

## Publication Pitfalls

Common mistakes specific to writing up and presenting physics results.

| Pitfall | Impact | Better Approach |
| --- | --- | --- |
| Not comparing with the Bao-Furuya-Naskar triality framework (arXiv:2409.17317) | Referee will immediately ask how the method relates to the completeness result | Explicitly state how the IT method relates to, differs from, or goes beyond the contraction map / partial cube framework |
| Claiming the method "classifies" the N=5 HEC without complete facet enumeration | Overclaim; the N=5 HEC is already characterized by Hernandez-Cuenca (arXiv:1903.09148) | State precisely which new information the IT method provides (e.g., facet/redundant distinctions, structural insights) rather than claiming full classification |
| Presenting only positive results (cases where the method works) without discussing failure modes or limitations | Reduced credibility and reproducibility | Document cases where the method fails or gives ambiguous results; these are scientifically informative |

## "Looks Correct But Is Not" Checklist

Things that appear right but are missing critical pieces.

- [ ] **Inequality validity proof:** Often missing the final step of verifying the proof applies to *all* holographic states (not just tested graph models) -- verify that a contraction map or equivalent formal proof exists
- [ ] **Facet claim:** Often missing the dimension count -- verify that the set of saturating entropy vectors spans a codimension-1 subspace of the cone
- [ ] **Orbit classification:** Often missing the purification equivalences -- verify that S(A) = S(A^c) has been applied before counting distinct orbits
- [ ] **Extreme ray construction:** Often missing the check that the ray is actually holographic (realizable by a graph model or bulk geometry) -- verify that a graph model is exhibited
- [ ] **IT proof structure:** Often claimed to "distinguish facets from redundant" but actually only provides a different proof of validity -- verify that the proof produces different output (or fails) for known redundant inequalities
- [ ] **Computational pipeline:** Often tested only on N=4 -- verify that the pipeline handles the 31-dimensional N=5 entropy space without memory or time blowup
- [ ] **Superbalance:** Often not checked for candidate inequalities -- verify that every candidate passes the superbalance filter before investing effort in contraction map search

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
| --- | --- | --- |
| Floating-point errors in polyhedral computation | MEDIUM | Rerun all polyhedral computations with exact rational arithmetic; compare results; discard any extreme rays or facets that differ |
| IT method reduces to contraction maps | HIGH | Redesign from scratch with facet-detection as the primary objective; consider whether the method can be augmented with saturation analysis |
| Wrong orbit count from symmetry errors | LOW | Recompute orbits using a trusted computational algebra system (GAP/SageMath); verify against published orbit counts |
| Purification not imposed | MEDIUM | Re-derive all results with purification imposed; check which inequalities become trivial or equivalent |
| Method works at N=4 but fails at N=5 | HIGH | Analyze *why* it fails: is it computational (scaling) or structural (N=5 has features N=4 lacks)? If structural, the method may need fundamental revision |
| Necessary/sufficient confusion | LOW | Re-label all results with correct evidence levels; identify which claims need upgrading from "conjecture" to "proven" |

## Pitfall-to-Phase Mapping

How research phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
| --- | --- | --- |
| Confusing validity with facet status (1) | Phase 1: Foundations | N=4 benchmark separately verifies both properties for SSA and MMI |
| IT method mimics contraction maps (2) | Phase 2: Method development | Check whether IT proof output differs structurally for facets vs. redundant inequalities |
| 2^N dimensional explosion (3) | Phase 1: Computational setup | Polyhedral pipeline tested on N=4 with timing; extrapolated to N=5 |
| Necessary vs. sufficient (4) | All phases | Every result carries an explicit evidence level label |
| Purification errors (5) | Phase 1: Foundations | Convention document specifies purification treatment; N=4 benchmark verifies |
| N=4-only success (6) | Phase 2-3 | Method tested on at least one known N=5 inequality during Phase 2 |
| HEC/QEC confusion (7) | Phase 1-2 | Each result labeled "holographic" or "quantum" |
| Symmetry reduction errors (8) | Phase 1 | Orbit counts verified against published values for N=4 and N=5 |
| Floating-point errors (9) | Phase 1: Setup | Exact arithmetic mandated for all polyhedral computations |
| Completeness constrains alternatives (10) | Phase 2 | Method explicitly designed to go beyond validity proofs |
| Sign/coefficient errors (11) | All phases | Machine-readable inequality representations; automated checking |
| SSA facet assumption (12) | Phase 1 | Redundancy LP for every inequality in the candidate set |
| Superbalance ignored (13) | Phase 1 | Superbalance filter implemented as first-pass candidate screen |

## Sources

- Bao, Nezami, Ooguri, Stoica, Sully, Walter, "The Holographic Entropy Cone," arXiv:1505.07839
- Hernandez-Cuenca, "The Holographic Entropy Cone for Five Regions," arXiv:1903.09148
- Avis, Hernandez-Cuenca, "On the foundations and extremal structure of the holographic entropy cone," arXiv:2102.07535
- Hernandez-Cuenca, "The holographic entropy cone from marginal independence," arXiv:2204.00075
- Czech, Liu, Yu, "Two infinite families of facets of the holographic entropy cone," arXiv:2401.13029
- Bao, Furuya, Naskar, "Properties of the contraction map for holographic entanglement entropy inequalities," arXiv:2403.13283
- Bao, Furuya, Naskar, "Towards a complete classification of holographic entropy inequalities," arXiv:2409.17317
- Bao, Furuya, Naskar, "On the completeness of contraction map proof method for holographic entropy inequalities," arXiv:2506.18086
- Czech, Soni, "Superbalance of holographic entropy inequalities," arXiv:2307.13457
- Cadney, Linden, Winter, "Holographic mutual information is monogamous," arXiv:1107.2940
- Czech, Dong, "Tip of the Quantum Entropy Cone," arXiv:2306.00199
- Fukuda, "Frequently Asked Questions in Polyhedral Computation," cddlib documentation

---

_Known pitfalls research for: Holographic entropy cone classification and IT proof methods_
_Researched: 2026-04-05_
