# Computational Approaches: Holographic Entropy Cone Analysis

**Surveyed:** 2026-04-05
**Domain:** Polyhedral geometry / quantum information / holographic entanglement
**Confidence:** HIGH

## Recommended Stack

The computational backbone of this project is polyhedral cone computation: converting between H-representations (inequalities/facets) and V-representations (extreme rays/vertices) of the holographic entropy cone (HEC). The recommended primary stack is **lrslib** for vertex/facet enumeration (exact arithmetic, low memory, handles high dimensions), supplemented by **pycddlib** for rapid prototyping and redundancy removal in Python, and **SageMath** as a unifying interface that wraps both cddlib and Normaliz backends. For information-theoretic inequality verification, **psitip** (Python Symbolic Information Theoretic Inequality Prover) is the right tool. For graph-model entropy computation (min-cut on weighted graphs), a custom Python implementation using **NetworkX** max-flow routines is the correct approach -- no off-the-shelf HEC-specific library exists for this beyond the existing database at github.com/SergioHC95/Holographic-Entropy-Cone.

The key computational bottleneck is the vertex-facet enumeration problem, which is inherently hard (output-sensitive, worst-case exponential in input+output size). For N=4 (entropy vector dimension 15), this is trivial. For N=5 (dimension 31), it is feasible but requires hours. For N=6 (dimension 63), it is at the frontier of what is computable and requires careful algorithmic choices.

## Numerical Algorithms

| Algorithm | Problem | Convergence | Cost per Step | Memory | Key Reference |
|-----------|---------|-------------|---------------|--------|---------------|
| Double Description (DD) | H-rep to V-rep conversion | Incremental (one inequality at a time) | O(v * d) per inequality, v = current vertices | O(v * d) -- stores all vertices | Fukuda & Prodon (1996) |
| Reverse Search (RS) | H-rep to V-rep or V-rep to H-rep | Enumerates vertices via pivot graph | O(n * d) per vertex for simple polytopes | O(n * d) -- constant per vertex | Avis & Fukuda (1992) |
| Fourier-Motzkin Elimination | Projection of polyhedra | Eliminates one variable per step | Intermediate size can blow up doubly-exponential | Stores all intermediate inequalities | Ziegler (1995), Lectures on Polytopes |
| Max-flow/Min-cut (Ford-Fulkerson/BFS) | Entropy of subsystem from graph model | Exact for integer/rational weights | O(V * E) per cut query | O(V + E) | Cormen et al., CLRS |
| LP (simplex or interior point) | Redundancy removal, feasibility | Simplex: finite pivots; IP: polynomial | Simplex: exponential worst case, fast practice; IP: O(n^3.5) | O(n * m) | Schrijver (1998) |

### Convergence Properties

**Double Description Method (cddlib):**
- **Convergence criterion:** All inequalities processed; final vertex set is complete
- **Expected rate:** Incremental; total time depends on intermediate vertex count, which can be exponentially larger than final count
- **Known failure modes:** Intermediate swell -- when processing inequality k of n, the intermediate vertex count can blow up even if the final count is small. Highly degenerate inputs (many inequalities meeting at one vertex) cause severe performance degradation.

**Reverse Search (lrslib):**
- **Convergence criterion:** All vertices in the reverse search tree have been visited
- **Expected rate:** O(n * d) work per vertex; total time proportional to output size for non-degenerate inputs
- **Known failure modes:** Degeneracy (multiple bases per vertex) can cause redundant work; handled by lexicographic pivoting but with increased constant factor. Does not store all vertices simultaneously, so post-processing requires a second pass.

**Max-flow for entropy vectors:**
- **Convergence criterion:** Augmenting path search finds no further path (max-flow = min-cut by max-flow/min-cut theorem)
- **Expected rate:** Exact in finite steps for rational weights
- **Known failure modes:** None for exact arithmetic on rational weights. For the HEC application, graph sizes are small enough (tens of vertices) that max-flow is instantaneous.

## Software Ecosystem

### Primary Tools

| Tool | Version | Purpose | License | Maturity |
|------|---------|---------|---------|----------|
| lrslib | 7.3+ | Vertex/facet enumeration for high-dimensional cones | GPL v2 | Stable (30+ years) |
| pycddlib | 3.0.2 | Python interface to cddlib for DD method, redundancy removal, LP | GPL v2 | Stable |
| SageMath | 10.x | Unifying interface for polyhedral geometry (wraps cddlib, Normaliz, lrslib) | GPL v2+ | Stable |
| psitip | latest | Shannon-type entropy inequality verification | MIT | Active development |
| NetworkX | 3.x | Graph algorithms including max-flow/min-cut for graph models | BSD | Stable |
| Python | 3.10+ | Scripting, data manipulation, orchestration | PSF | Stable |

### Supporting Tools

| Tool | Version | Purpose | When Needed |
|------|---------|---------|-------------|
| Normaliz / PyNormaliz | 3.10+ / latest | Hilbert basis computation, extreme ray enumeration for lattice cones | When Hilbert basis or lattice point enumeration is needed beyond extreme rays |
| polymake | 4.x | Cross-validation of polyhedral computations, alternative backend | Verification of lrslib/cddlib results; exploration via Perl/Julia interface |
| PORTA (XPORTA.jl) | legacy / Julia wrapper | Historical tool for polyhedral analysis; facet-inducing property checks | Only if Julia-based workflow is preferred; generally superseded by lrslib+cddlib |
| NumPy / SciPy | latest | Matrix operations, sparse linear algebra, LP solver (scipy.optimize.linprog) | Rapid prototyping of LP-based redundancy checks; numerical linear algebra |
| SymPy | latest | Symbolic manipulation of entropy expressions | When deriving IT identities symbolically before numerical verification |
| GLPK / HiGHS | latest | LP solvers for large-scale redundancy removal | When scipy LP solver is insufficient for large N |

### HEC-Specific Resources

| Resource | Type | Purpose | Reference |
|----------|------|---------|-----------|
| Holographic-Entropy-Cone database | GitHub repo | Database of extreme rays and facets for N=5, partial N=6 | github.com/SergioHC95/Holographic-Entropy-Cone |
| Avis & Hernandez-Cuenca (2022) code | Supplementary | lrslib-based computation of HEC on 5 terminals | arXiv:2102.07535 |
| Bao et al. (2015) supplementary | Tables | N=4 HEC facets (SSA + MMI) and extreme rays | arXiv:1505.07839 |

### Information-Theoretic Inequality Provers

| Tool | Language | Purpose | Interface |
|------|----------|---------|-----------|
| psitip | Python | Prove/disprove Shannon-type entropy inequalities; constrained/unconstrained | Python library, scriptable |
| AITIP | Web/MATLAB | Online inequality prover with human-readable proofs | Web interface at aitip.org |
| minitip | C | Lightweight ITIP variant with simplified syntax | Command-line |
| Xitip / oXitip | C / Web | C-based LP solver variant of ITIP | Command-line / web |

**Recommendation:** Use **psitip** because it is Python-native, scriptable, supports constrained inequalities (essential for testing whether an inequality is implied by a set of known facets), and integrates naturally with the rest of the Python stack. Fall back to AITIP for quick manual checks.

## Data Flow

```
Candidate HEC inequality (linear in entropies)
  -> Step 1: Express as inequality on entropy vector space (R^{2^N - 1})
  -> Step 2: Verify Shannon-type validity via psitip/LP
  -> Step 3: Check holographic validity via contraction map search
     OR via graph model extreme ray enumeration
  -> Step 4: Determine facet vs. redundant status
     -> 4a: LP-based: check if removing inequality changes the cone (LP feasibility)
     -> 4b: IT-based: apply new proof method (project deliverable)
  -> Step 5: Cross-validate against known results (N=4 benchmark)
  -> Final output: facet/redundant classification with proof certificate
```

### Graph Model Entropy Computation Pipeline

```
Weighted graph G = (V, E, w)
  -> For each subsystem A subset of boundary vertices:
     -> Compute min-cut separating A from complement
     -> S(A) = min-cut value
  -> Collect all 2^N - 1 entropies into entropy vector v
  -> v is a point in the HEC (or on its boundary)
```

## Computation Order and Dependencies

| Step | Depends On | Produces | Can Parallelize? |
|------|-----------|----------|-----------------|
| Enumerate N=4 HEC extreme rays | N=4 facet inequalities (known: SSA + MMI) | V-representation of C_4 | No (single computation) |
| Verify N=4 facets via IT method | IT proof method (project deliverable) + C_4 data | Validation of method against benchmark | Yes (per inequality) |
| Enumerate N=5 HEC extreme rays | N=5 candidate facets (from literature) | V-representation of C_5 | No (single computation, but can use parallel lrs) |
| Redundancy check for N=5 candidates | C_5 extreme rays OR facet list | Facet vs. redundant classification | Yes (per inequality via LP) |
| Apply IT method to N=5 | IT proof method + N=5 inequalities | Novel facet classification | Yes (per inequality) |
| Cross-validate IT vs. LP classification | Both classification results | Consistency check | Yes |

## Resource Estimates

| Computation | Time (estimate) | Memory | Storage | Hardware |
|-------------|-----------------|--------|---------|----------|
| N=4 HEC full enumeration (both directions) | < 1 second | < 10 MB | Negligible | Any laptop CPU |
| N=4 IT method validation (all facets) | < 1 minute | < 100 MB | Negligible | Any laptop CPU |
| N=5 extreme ray enumeration (lrslib) | Minutes to hours | < 1 GB (lrs is memory-efficient) | ~10 MB output | Single CPU core; mplrs for parallel |
| N=5 facet enumeration from rays (lrslib) | Hours | < 1 GB | ~10 MB output | Single CPU core; mplrs for parallel |
| N=5 redundancy removal (LP per inequality) | Seconds per inequality, minutes total | < 100 MB | Negligible | Any CPU |
| N=5 IT method application | Depends on method -- budget hours | < 1 GB | Negligible | Any CPU |
| N=6 extreme ray enumeration (partial) | Days to weeks | < 10 GB with lrslib | ~100 MB+ output | Multi-core recommended (mplrs) |
| N=6 full facet enumeration | Likely infeasible with current methods | Unknown | Unknown | HPC cluster if attempted |
| Max-flow per graph model (N=5) | Microseconds per cut; milliseconds per full entropy vector | < 1 MB | Negligible | Any CPU |
| psitip inequality check | Seconds per inequality | < 100 MB | Negligible | Any CPU |

### Scaling Analysis

The entropy vector space has dimension d = 2^N - 1 (excluding the empty set):
- N=3: d = 7
- N=4: d = 15
- N=5: d = 31
- N=6: d = 63

After quotienting by the S_N permutation symmetry on parties, the effective dimension is reduced, but the underlying polyhedral computation operates in the full d-dimensional space. The number of extreme ray orbits and facet orbits grows rapidly:
- N=4: Small number of extreme ray orbits under S_4; 2 facet orbit types (SSA, MMI)
- N=5: Hundreds of extreme ray orbits under S_5; known facet list from contraction maps
- N=6: Thousands of extreme ray orbits (>4122 reported in Avis & Hernandez-Cuenca 2022); facet list incomplete

The vertex-facet enumeration problem has output-sensitive complexity: for a cone with f facets and v extreme rays in d dimensions, converting between representations takes time at least O(f * v * d) and in the worst case is much harder (the decision problem is co-NP-complete in general). However, the HEC has special structure (symmetry, rationality, low-dimensional faces) that makes practical computation feasible through N=5.

## Algorithm Comparison: Vertex/Facet Enumeration

| Criterion | lrslib (Reverse Search) | cddlib (Double Description) | Normaliz | polymake |
|-----------|------------------------|---------------------------|----------|----------|
| Algorithm | Reverse search pivoting | Incremental DD method | Primal decomposition + DD | Wraps lrs, cdd, Normaliz |
| Arithmetic | Exact (GMP or fixed) | Exact (GMP) or floating | Exact (GMP) | Backend-dependent |
| Memory | O(n*d) -- constant per vertex | O(v*d) -- stores ALL vertices | O(v*d) | Backend-dependent |
| Parallelism | mplrs (MPI-based) | No native parallel | OpenMP parallel | No native parallel |
| Degeneracy handling | Lexicographic perturbation | Good for highly degenerate | Good | Backend-dependent |
| Best for | High-dimensional, many vertices, memory-limited | Moderate dimension, need all vertices in memory | Lattice problems, Hilbert basis | Exploratory computation |
| Python interface | None (command-line) | pycddlib | PyNormaliz | Polymake.jl (Julia) |
| **Recommendation for HEC** | **PRIMARY for N>=5** | **Secondary for N<=4 and redundancy removal** | Niche (lattice structure) | Cross-validation only |

**Rationale for lrslib as primary:** The HEC at N=5 has dimension 31 with hundreds of extreme ray orbits. lrslib's O(n*d) memory footprint per vertex is critical -- cddlib must store all intermediate vertices, which can cause memory blowup for intermediate steps even when the final answer is manageable. lrslib also supports parallelization via mplrs, which is essential if N=6 computations are attempted. The HEC computation at N=5 in Avis & Hernandez-Cuenca (2022) used lrslib.

**Rationale for pycddlib as secondary:** For N=4 (d=15, trivial size), cddlib via pycddlib provides the most convenient Python-native workflow. Its LP solver is useful for redundancy removal (checking if each inequality is implied by the others). For rapid prototyping and small-scale tests, pycddlib is faster to set up than calling lrslib from the command line.

## Open Questions

| Question | Why Open | Impact on Project | Approaches Being Tried |
|----------|---------|-------------------|----------------------|
| Is the contraction map method complete? | Recently argued yes (He et al. 2024, Czech et al. 2025), but subtle assumptions remain | If complete, the IT method must reproduce all contraction-map-provable inequalities to be valid | Polynomial-time algorithm via partial cube characterization (arXiv:2409.17317) |
| Can IT methods detect facet status without full cone enumeration? | The LP approach requires the full V- or H-representation; an IT shortcut would be a major advance | Central to the project -- this IS the deliverable | Novel IT proof method under development |
| What is the complete N=6 HEC? | Combinatorial explosion: >4122 extreme ray orbits, unknown number of facets | Out of scope, but computational infrastructure should not preclude future extension | Partial enumeration + RL-based search (arXiv:2601.19979) |
| Do unknown N=6 inequalities exist? | 3 of 6 "mystery" extreme rays at N=6 lack graph realizations (arXiv:2601.19979) | Implies the known inequality list is incomplete for N=6 | RL exploration of entropy vector space |

## Anti-Approaches

| Anti-Approach | Why Avoid | What to Do Instead |
|---------------|-----------|-------------------|
| Floating-point arithmetic for polyhedral computation | Convex cone facet enumeration is numerically fragile; floating-point errors produce wrong combinatorial types (missing or spurious facets) | Use exact rational arithmetic exclusively (lrslib, cddlib with GMP, Normaliz) |
| Fourier-Motzkin elimination for projection | Doubly-exponential intermediate blowup; unusable for d > 10 | Use vertex enumeration (lrslib) followed by projection of the vertex set |
| Brute-force contraction map search for large N | Exponential search space in graph size; known to be intractable beyond small cases without structural pruning | Use the partial-cube characterization algorithm (arXiv:2409.17317) or the IT method being developed |
| Full N=6 cone enumeration as a project target | Likely infeasible within project timeline; would consume all computational effort with uncertain payoff | Validate method at N=4 and N=5 first; defer N=6 to future work or use partial/sampling approaches |
| Using polymake as the primary computation engine | Overhead of Perl/Julia wrapper; slower than direct lrslib/cddlib calls for the specific operations needed | Use polymake only for cross-validation and exploratory analysis |
| Symbolic computation (SymPy) for polyhedral geometry | SymPy has no competitive polyhedral geometry backend; orders of magnitude slower than dedicated tools | Use SymPy only for entropy expression manipulation, not for cone computation |

## Logical Dependencies

```
Known N=4 facets (SSA + MMI) -> lrslib enumeration -> N=4 extreme rays (VALIDATION CHECKPOINT)
Known N=4 facets -> IT proof method -> facet/redundant classification -> compare with known answer

Known N=5 candidate inequalities -> lrslib enumeration -> N=5 extreme rays
N=5 extreme rays -> LP redundancy check -> N=5 facet classification (GROUND TRUTH for comparison)
Known N=5 candidate inequalities -> IT proof method -> IT-based classification -> compare with LP classification

IT method validated at N=4 -> apply to N=5 -> novel results
N=5 LP classification + N=5 IT classification -> consistency check -> confidence in method
```

## Recommended Investigation Scope

Prioritize:
1. **N=4 full reproduction** -- enumerate extreme rays and facets using lrslib/pycddlib; verify against Bao et al. (2015). This is the non-negotiable computational validation checkpoint.
2. **N=5 extreme ray and facet enumeration** -- use lrslib to reproduce the results of Avis & Hernandez-Cuenca (2022). This provides ground truth for the IT method.
3. **IT method computational implementation** -- build the infrastructure to test the new proof method against both N=4 and N=5 data.

Defer:
- **N=6 computation:** requires HPC resources and is out of project scope. The computational infrastructure should be designed to scale, but N=6 is not a deliverable.
- **RL-based exploration (arXiv:2601.19979):** interesting but tangential to the IT proof method; note as future direction.

## Validation Strategy

| Result | Validation Method | Benchmark | Source |
|--------|------------------|-----------|--------|
| N=4 extreme rays | Enumerate from known facets (SSA + MMI) | Known orbit count under S_4 | Bao et al. (2015), arXiv:1505.07839 |
| N=4 facets | Enumerate from extreme rays, check irredundancy | SSA and MMI are the only facets | Bao et al. (2015) |
| N=5 extreme rays | Enumerate from known candidate facets | Compare against Holographic-Entropy-Cone database | Avis & Hernandez-Cuenca (2022), arXiv:2102.07535 |
| N=5 facet classification | LP-based redundancy removal | Compare against results in Hernandez-Cuenca (2019), arXiv:1903.09148 | Hernandez-Cuenca (2019) |
| IT method at N=4 | Must reproduce: SSA = facet, MMI = facet, SA = redundant | 100% agreement with known classification | Bao et al. (2015) |
| IT method at N=5 | Must agree with LP classification on all tested inequalities | Consistency with polyhedral computation | Cross-validation |
| Graph model entropy vectors | Compute min-cuts; verify against known entropy vectors | Known extreme ray coordinates from database | Holographic-Entropy-Cone database |
| psitip inequality checks | Verify Shannon-type inequalities hold | Known Shannon inequalities as positive controls | Yeung (2002), Information Theory and Network Coding |

## Installation / Setup

```bash
# Python environment (use project venv)
pip install pycddlib numpy scipy networkx sympy matplotlib

# psitip for information-theoretic inequality proving
pip install psitip

# lrslib -- must be installed separately (not pip-installable)
# On macOS with Homebrew:
brew install lrs

# On Ubuntu/Debian:
# sudo apt-get install lrslib

# For parallel lrslib (mplrs), need MPI:
# brew install open-mpi  (then compile mplrs from source)

# SageMath (optional, for unifying interface):
# Install via conda or system package manager
# conda install -c conda-forge sage

# Normaliz / PyNormaliz (optional, for Hilbert basis):
pip install PyNormaliz
# Or via SageMath: sage -i pynormaliz

# polymake (optional, for cross-validation):
# Install via system package manager or from polymake.org
```

## Sources

- Avis, D. & Fukuda, K. "A pivoting algorithm for convex hulls and vertex enumeration of arrangements and polyhedra." Discrete & Computational Geometry 8 (1992): 295-313. -- Reverse search algorithm (lrslib foundation)
- Fukuda, K. & Prodon, A. "Double description method revisited." Combinatorics and Computer Science, LNCS 1120 (1996): 91-111. -- Double description method (cddlib foundation)
- Avis, D. & Hernandez-Cuenca, S. "On the foundations and extremal structure of the holographic entropy cone." Discrete Applied Mathematics 328 (2023): 26-43. arXiv:2102.07535 -- Computational methods for HEC, lrslib application to N=5
- Bao, N. et al. "The Holographic Entropy Cone." JHEP 09 (2015) 130. arXiv:1505.07839 -- Foundational HEC paper, N=4 complete classification
- Hernandez-Cuenca, S. "Holographic entropy cone for five regions." Phys. Rev. D 100 (2019) 026004. arXiv:1903.09148 -- N=5 HEC complete construction
- He, T. et al. "Towards a complete classification of holographic entropy inequalities." JHEP 03 (2025) 117. arXiv:2409.17317 -- Algorithmic contraction map search, partial-cube characterization
- Czech, B. et al. "Properties of the contraction map for holographic entanglement entropy inequalities." arXiv:2403.13283 -- Contraction map properties, exponential speedup
- Czech, B. et al. "On the completeness of contraction map proof method for holographic entropy inequalities." JHEP 12 (2025) 140. arXiv:2506.18086 -- Completeness argument
- Bao, N. et al. "Exploring the holographic entropy cone via reinforcement learning." arXiv:2601.19979 (2026) -- RL approach to graph model discovery, N=6 mystery rays
- Li, C.T. "psitip: Python Symbolic Information Theoretic Inequality Prover." GitHub, 2020. -- IT inequality verification tool
- Fukuda, K. "Frequently Asked Questions in Polyhedral Computation." ETH Zurich, 2015 (updated). -- Comprehensive survey of polyhedral computation methods and tools
- Schrijver, A. "Theory of Linear and Integer Programming." Wiley, 1998. -- LP theory and algorithms
- Bruns, W. et al. "Normaliz: Algorithms for affine monoids and rational cones." J. Algebra 324 (2010): 1098-1113. -- Normaliz algorithms
