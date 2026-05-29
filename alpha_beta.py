================================================================================
  TASK 4 — BAYESIAN NETWORKS: MODELLING AND INFERENCE
================================================================================


1. WHAT IS A BAYESIAN NETWORK?
--------------------------------

A Bayesian Network (BN) — also called a Belief Network, Bayes Net, or
Probabilistic Directed Graphical Model — is a compact representation of a
joint probability distribution over a set of random variables. It combines
probability theory with graph theory to model uncertainty and causal
relationships in a domain.

A Bayesian Network consists of two components:

  a) Structure — a Directed Acyclic Graph (DAG):
       • Nodes  represent random variables (discrete or continuous)
       • Directed edges  A → B  encode "A directly influences B"
       • The graph is acyclic (no feedback loops), guaranteeing a consistent
         probabilistic interpretation

  b) Parameters — a set of Conditional Probability Tables (CPTs):
       • Each node X has one CPT: P(X | Parents(X))
       • If X has no parents, its CPT is just a prior distribution P(X)
       • CPT entries must sum to 1 for each combination of parent values

The full joint probability distribution decomposes as a product of CPTs:

    P(X₁, X₂, ..., Xₙ) = Π  P(Xᵢ | Parents(Xᵢ))
                          i=1

This factorisation is the key advantage of BNs: a full joint distribution
over n binary variables requires 2ⁿ − 1 parameters, but a BN typically
requires far fewer (exponential in the maximum number of parents, not n).


2. KEY PROBABILISTIC CONCEPTS
-------------------------------

2.1  Conditional Independence and the Markov Condition
  Every node Xᵢ is conditionally independent of its non-descendants given
  its parents:

    Xᵢ ⊥⊥ NonDescendants(Xᵢ) | Parents(Xᵢ)

  This is the local Markov condition and is the formal justification for
  the factorisation above.

2.2  D-Separation
  D-separation is a graphical criterion for determining whether two sets of
  variables A and B are conditionally independent given a third set C,
  directly from the graph structure (without computing probabilities).

  Three fundamental structures:
    • Chain:       A → B → C     (B blocks A — C if observed)
    • Fork:        A ← B → C     (B blocks A — C if observed)
    • Collider:    A → B ← C     (B opens A — C if B or a descendant observed)

  Knowing these patterns allows experts to read independencies from a BN
  diagram and design efficient inference algorithms.

2.3  Bayes' Theorem
  The foundation of BN inference. For evidence E = e and query variable Q:

    P(Q | E = e) = P(E = e | Q) × P(Q)
                   ─────────────────────
                         P(E = e)

  In practice, the denominator is computed by marginalisation (summing over
  all values of Q), and Variable Elimination automates this process.


3. BAYESIAN NETWORK INFERENCE
-------------------------------

Given a BN, inference answers queries of the form:
    "What is P(Query = q | Evidence = e)?"

where Evidence is a subset of observed variables and Query is an unobserved
variable of interest. Variables that are neither query nor evidence are
called hidden (nuisance) variables and must be marginalised out.

3.1  Exact Inference Algorithms

  Variable Elimination (VE)
    The most fundamental exact algorithm. Works by:
      1. Representing the joint as a product of factor tables (CPTs restricted
         to observed evidence values)
      2. Choosing an elimination ordering for hidden variables
      3. For each hidden variable: multiplying all factors that mention it,
         then summing (marginalising) it out of the product factor
      4. Multiplying remaining factors and normalising to get the posterior

    Complexity: exponential in the treewidth of the graph, polynomial for
    polytrees (singly-connected networks). Optimal elimination ordering is
    NP-hard in general, but good heuristics (min-fill, min-degree) work well.

  Junction Tree (Clique Tree) Algorithm
    Converts the DAG into a cluster tree (junction tree) of maximal cliques,
    then passes messages between cliques. After two message-passing rounds
    (collect + distribute evidence), all marginals can be read off.
    More efficient than VE when multiple queries are needed over the same
    evidence, as the tree only needs to be compiled once.

  Belief Propagation (BP)
    An exact algorithm for polytrees (singly-connected DAGs), also used as an
    approximate algorithm for general graphs (Loopy BP). Messages are passed
    from leaves inward (π messages) and from root outward (λ messages).
    Exact in polytrees; converges to good approximations in many loopy graphs.

3.2  Approximate Inference Algorithms

  Monte-Carlo Sampling — Forward Sampling
    Samples from P(X₁, ..., Xₙ) by sampling root nodes first, then children.
    Simple but inefficient when evidence has low prior probability.

  Likelihood Weighting
    A weighted form of forward sampling. Fixes observed variables to their
    evidence values and weights each sample by the likelihood of the evidence.
    Much more efficient than rejection sampling for rare evidence.

  Gibbs Sampling (MCMC)
    Initialises all non-evidence variables randomly, then iteratively
    re-samples each variable conditioned on the current values of all others.
    Produces a Markov chain whose stationary distribution is the posterior.
    Excellent for large networks where exact methods are intractable.

  Variational Inference
    Approximates the true posterior with a simpler distribution (e.g. mean
    field) by minimising KL divergence. Used in large-scale ML models
    (Variational Autoencoders, LDA topic models).


4. BUILDING A BAYESIAN NETWORK — METHODOLOGY
----------------------------------------------

Step 1: Identify Variables
  Choose a set of relevant discrete or continuous random variables.
  For medical diagnosis: Season, Flu, Cold, Fever, Cough, Fatigue,
  Headache, Diagnosis.

Step 2: Define the DAG Structure
  Draw directed edges from causes to effects, encoding domain knowledge
  (causal or associative). Aim for sparse graphs (few parents per node)
  to keep CPTs manageable and inference tractable.
  
  Guideline: each node should have at most 3–4 parents in practice.

Step 3: Elicit / Estimate CPTs
  For each node, specify the conditional probability of each value given
  every combination of parent values. Sources:
    • Expert elicitation (domain experts specify probabilities)
    • Learning from data (MLE, Bayesian parameter estimation)
    • Noisy-OR / Noisy-AND models to reduce parameter count

Step 4: Validate
  Check that CPT rows sum to 1. Perform prior-predictive checks — does
  the network produce sensible prior distributions over key variables?

Step 5: Inference
  Apply an algorithm (VE, Junction Tree, MCMC) to answer queries.
  Sensitivity analysis: how much does P(Query | Evidence) change as
  individual CPT entries vary? High sensitivity indicates important variables.


5. THE MEDICAL DIAGNOSIS NETWORK (THIS IMPLEMENTATION)
--------------------------------------------------------

The network in bayesian_network.py models influenza and cold diagnosis
with 8 variables:

  Variable     Values                     Parents
  -----------  -------------------------  ----------------------------
  Season       winter, spring, summer,    (none — prior)
               autumn
  Flu          true, false                Season
  Cold         true, false                Season
  Fever        true, false                Flu, Cold
  Cough        true, false                Flu, Cold
  Fatigue      true, false                Flu
  Headache     true, false                Flu, Cold
  Diagnosis    healthy, flu, cold,        Fever, Cough, Fatigue,
               allergy                    Headache

DAG structure:
  Season → Flu  → Fever, Cough, Fatigue, Headache
  Season → Cold → Fever, Cough, Headache
  Fever, Cough, Fatigue, Headache → Diagnosis

Eight inference scenarios are demonstrated:
  1. Prior distribution (no evidence)
  2. High fever only
  3. Winter season, fever + cough
  4. Fever + cough + fatigue (classic flu pattern)
  5. Mild cough only
  6. All symptoms present (worst case)
  7. Summer season, mild cough
  8. Headache + fatigue, no fever

The implementation uses Variable Elimination with a Factor class that
implements: restrict (fix evidence), multiply (factor product), sum_out
(marginalise), and normalise.


6. BAYESIAN NETWORK TOOLS — COMPARISON
-----------------------------------------

6.1  pgmpy (Python)
  Type        : Open-source Python library
  Model       : Discrete / Gaussian BNs, Markov Networks, Dynamic BNs
  Algorithms  : Variable Elimination, Belief Propagation, MPLP, Causal
                inference (do-calculus), structure learning (Hill Climb,
                PC algorithm, Tabu search), parameter learning (MLE, Bayes)
  Strengths   : Pure Python; NumPy/SciPy backed; integrates with pandas;
                extensive structure and parameter learning; active development;
                good documentation with Jupyter notebook examples.
  Weaknesses  : Slower than commercial tools for very large networks;
                approximate inference less mature than exact.
  Best for    : Research, teaching, rapid prototyping in Python.
  Licence     : MIT (open source)

6.2  Netica (Norsys)
  Type        : Desktop application + C/Java API
  Model       : Discrete BNs, Influence Diagrams (decision networks)
  Algorithms  : Exact (Junction Tree), approximate (stochastic simulation)
  Strengths   : Mature, widely used in risk analysis and environmental
                modelling; intuitive drag-and-drop GUI; good sensitivity
                analysis; influence diagram support for decision making;
                API for embedding in other applications.
  Weaknesses  : Proprietary; Windows-centric GUI; API licensing costs.
  Best for    : Risk analysis, decision support, environmental and ecological
                modelling; consultancy work requiring a polished GUI.
  Licence     : Commercial (free limited version available)

6.3  Hugin Expert
  Type        : Commercial BN platform (desktop + server)
  Model       : Discrete BNs, Gaussian BNs, hybrid, Influence Diagrams,
                Object-Oriented BNs (OOBNs), Dynamic BNs (DBNs)
  Algorithms  : Junction Tree (exact); adaptive importance sampling
                (approximate); LIMID for decision graphs
  Strengths   : Industry benchmark for exact inference performance; OOBNs
                allow modular, reusable network components; strong support
                for temporal models (DBNs); used in medical devices and
                real-time monitoring systems; APIs for C, Java, Python, .NET.
  Weaknesses  : Expensive commercial licence; steeper learning curve.
  Best for    : Medical decision support, fault diagnosis in engineering
                systems, real-time monitoring, safety-critical applications.
  Licence     : Commercial (academic licences available)

6.4  GeNIe Modeler (BayesFusion)
  Type        : Desktop modeller + SMILE inference engine
  Model       : Discrete BNs, Gaussian BNs, hybrid, Influence Diagrams,
                Dynamic BNs, Decision Trees
  Algorithms  : Exact (Junction Tree, Variable Elimination); approximate
                (Importance Sampling, Forward Sampling); EM learning
  Strengths   : Free academic licence; polished GUI with extensive
                visualisation; SMILE engine available as a C++/Java/Python
                library; good sensitivity analysis and case fitting tools.
  Weaknesses  : Full commercial licence required for production use;
                SMILE library somewhat dated in Python ecosystem.
  Best for    : Academic research and teaching; industrial applications
                requiring a GUI for model inspection and presentation.
  Licence     : GeNIe academic: free; SMILE library: commercial

6.5  PyAgrum (LIP6, Sorbonne)
  Type        : Open-source Python library with C++ core
  Model       : Discrete BNs, Credal Networks, Markov Networks, Influence
                Diagrams, Dynamic BNs
  Algorithms  : Variable Elimination, Loopy BP, Importance Sampling;
                structure learning, parameter learning
  Strengths   : Python-friendly wrapping of fast C++ engine; rich
                visualisation (SVG network diagrams in Jupyter); good
                support for credal networks (imprecise probabilities);
                Jupyter notebook integration excellent for teaching.
  Weaknesses  : Smaller community than pgmpy; documentation primarily
                in English/French; fewer tutorials.
  Best for    : Academic research especially in France; teaching BNs
                interactively in Jupyter notebooks; credal network research.
  Licence     : LGPL (open source)

6.6  bnlearn (R)
  Type        : R package for BN structure and parameter learning
  Model       : Discrete, Gaussian, and mixed (conditional linear Gaussian)
  Algorithms  : Score-based learning (HC, Tabu), constraint-based (PC,
                GS, MMPC), hybrid (RSMAX2, MMHC); exact and approximate
                inference; bootstrap aggregation for network averaging
  Strengths   : Gold standard for BN learning in R; comprehensive set of
                learning algorithms with unified interface; built-in network
                comparison and hypothesis testing; good visualisation with
                Rgraphviz; extensive documentation and vignettes.
  Weaknesses  : R ecosystem only; slower than commercial tools for inference
                on large networks; not ideal for real-time applications.
  Best for    : Statistical analysis of observational data; epidemiology;
                bioinformatics; any task where BN structure must be learned
                from data rather than specified by experts.
  Licence     : GPL-2 (open source)


7. TOOL SELECTION GUIDE
--------------------------

  Need                                    Recommended Tool
  --------------------------------------  ----------------------
  Python rapid prototyping / research     pgmpy
  R data-driven structure learning        bnlearn
  Industrial / real-time deployment       Hugin Expert
  Academic teaching with GUI              GeNIe Modeler (free)
  Commercial risk / decision analysis     Netica
  Python + fast C++ + Jupyter teaching    PyAgrum
  Full Python implementation from scratch bayesian_network.py (this file)


8. THIS IMPLEMENTATION
------------------------

The file bayesian_network.py implements everything from scratch using only
the Python standard library:

  a) Written conceptual overview of BNs (printed to stdout)

  b) Factor class:
       • restrict(variable, value)    — fix evidence, reduce table
       • multiply(other)              — pointwise factor product
       • sum_out(variable)            — marginalise out a variable
       • normalise()                  — divide by partition function Z

  c) BayesianNetwork class:
       • add_variable(name, values, parents, cpt) — build network
       • variable_elimination(query, evidence)    — exact posterior
       • _build_factors(evidence)                 — apply evidence
       • _elimination_order(query, evidence)      — heuristic ordering

  d) Medical Diagnosis BN:
       8 variables, 8 CPTs, built and validated

  e) 8 inference scenarios with bar-chart visualisation (text-based)

  f) Tool comparison table (Section 6 above, also printed at runtime)

================================================================================
