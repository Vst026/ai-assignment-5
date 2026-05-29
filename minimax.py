"""
Task 4 — Bayesian Networks: Modelling, Representation, and Inference
======================================================================
This file:
  1. Defines Bayesian Network theory and key concepts
  2. Implements a BN engine from scratch (CPTs, Variable Elimination)
  3. Models a Medical Diagnosis Network (Flu/Cold/Allergy)
  4. Demonstrates inference with various evidence combinations
  5. Discusses available tools for Bayesian Networks

Run:  python bayesian_network.py
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict
import math
import itertools


# ===========================================================================
# SECTION 1 — Bayesian Network Theory
# ===========================================================================
BAYESIAN_NETWORK_OVERVIEW = """
BAYESIAN NETWORKS — OVERVIEW
==============================

Definition
----------
A Bayesian Network (BN) — also called a Belief Network or Bayes Net — is a
probabilistic graphical model that represents a set of variables and their
conditional dependencies via a Directed Acyclic Graph (DAG).

Structure
---------
- Nodes  : random variables (discrete or continuous)
- Edges  : directed edges A → B mean "A directly influences B"
- CPTs   : each node X has a Conditional Probability Table P(X | Parents(X))
           If X has no parents, the CPT is just a prior P(X).

Key Properties
--------------
1. Markov condition: each node is conditionally independent of its
   non-descendants given its parents.
2. Joint distribution factorises as a product of CPTs:
       P(X1,...,Xn) = Π P(Xi | Parents(Xi))
3. D-separation: a graphical criterion for reading off conditional
   independencies without computing distributions.

Inference
---------
Given evidence E = e (observed values), compute the posterior:
       P(Query | Evidence = e)

Common inference algorithms:
  - Variable Elimination (exact)
  - Belief Propagation / Junction Tree (exact, tree-shaped BNs)
  - MCMC sampling — Gibbs, Metropolis-Hastings (approximate)
  - Likelihood Weighting (approximate, faster for many variables)

Variable Elimination (VE)
--------------------------
VE is an exact inference algorithm that works by:
  1. Representing the joint as a product of factors (CPTs)
  2. Eliminating hidden variables one by one by marginalising them out
  3. Multiplying relevant factors together, then summing over the hidden var

Elimination order affects efficiency (NP-hard to find optimal order,
but good heuristics exist: min-fill, min-degree).
"""


# ===========================================================================
# SECTION 2 — BN Engine (Variable Elimination)
# ===========================================================================
class Factor:
    """
    A factor φ(X1,...,Xk) — a function from variable assignments to
    non-negative reals. The building block of Variable Elimination.
    """

    def __init__(self, variables: List[str], values: Dict[tuple, float]):
        """
        Parameters
        ----------
        variables : ordered list of variable names this factor is over
        values    : dict mapping value-tuples to probabilities
                    e.g. {("T","T"): 0.9, ("T","F"): 0.1, ...}
        """
        self.variables = variables
        self.values    = values

    def get(self, assignment: Dict[str, str]) -> float:
        """Look up the factor value for a specific variable assignment."""
        key = tuple(assignment[v] for v in self.variables)
        return self.values.get(key, 0.0)

    def restrict(self, variable: str, value: str) -> "Factor":
        """
        Restrict: fix one variable to a specific value.
        Returns a new Factor with that variable removed.
        """
        idx      = self.variables.index(variable)
        new_vars = [v for v in self.variables if v != variable]
        new_vals = {}
        for key, prob in self.values.items():
            if key[idx] == value:
                new_key = tuple(k for i, k in enumerate(key) if i != idx)
                new_vals[new_key] = prob
        return Factor(new_vars, new_vals)

    def multiply(self, other: "Factor") -> "Factor":
        """
        Factor product: φ1(X, Y) * φ2(Y, Z) = φ3(X, Y, Z).
        """
        # Union of variables, preserving order
        all_vars = self.variables[:]
        for v in other.variables:
            if v not in all_vars:
                all_vars.append(v)

        # Domains must be inferred from existing keys
        def get_domain(factor, var):
            idx = factor.variables.index(var)
            return list({key[idx] for key in factor.values})

        domains = {v: get_domain(self, v) if v in self.variables
                   else get_domain(other, v)
                   for v in all_vars}

        new_vals = {}
        for combo in itertools.product(*[domains[v] for v in all_vars]):
            assign = dict(zip(all_vars, combo))
            p1 = self.get(assign)  if all(v in self.variables  for v in self.variables)  else 1.0
            p2 = other.get(assign) if all(v in other.variables for v in other.variables) else 1.0
            # Check if all variables needed exist in assignment
            self_key  = tuple(assign[v] for v in self.variables  if v in assign)
            other_key = tuple(assign[v] for v in other.variables if v in assign)
            p1 = self.values.get(self_key,  0.0)
            p2 = other.values.get(other_key, 0.0)
            new_vals[combo] = p1 * p2

        return Factor(all_vars, new_vals)

    def sum_out(self, variable: str) -> "Factor":
        """
        Marginalise out a variable by summing over all its values.
        """
        idx      = self.variables.index(variable)
        new_vars = [v for v in self.variables if v != variable]
        new_vals: Dict[tuple, float] = defaultdict(float)
        for key, prob in self.values.items():
            new_key = tuple(k for i, k in enumerate(key) if i != idx)
            new_vals[new_key] += prob
        return Factor(new_vars, dict(new_vals))

    def normalise(self) -> "Factor":
        """Normalise so that values sum to 1.0."""
        total = sum(self.values.values())
        if total == 0:
            return self
        new_vals = {k: v / total for k, v in self.values.items()}
        return Factor(self.variables, new_vals)

    def __repr__(self):
        return f"Factor({self.variables})"


class BayesianNetwork:
    """
    Discrete Bayesian Network with Variable Elimination inference.
    """

    def __init__(self):
        self._nodes:    List[str]                 = []
        self._parents:  Dict[str, List[str]]      = {}
        self._domains:  Dict[str, List[str]]      = {}
        self._cpts:     Dict[str, Factor]         = {}

    # ------------------------------------------------------------------ #
    # Network construction
    # ------------------------------------------------------------------ #
    def add_variable(self, name: str, domain: List[str], parents: List[str],
                     cpt_values: Dict[tuple, float]):
        """
        Add a variable with its CPT.

        Parameters
        ----------
        name       : variable name
        domain     : possible values e.g. ["T", "F"] or ["flu", "cold", "healthy"]
        parents    : list of parent variable names (empty list for root nodes)
        cpt_values : dict mapping (parent_val, ..., own_val) tuples to probabilities.
                     For a root node, keys are single-element tuples of own values.
        """
        self._nodes.append(name)
        self._parents[name] = parents
        self._domains[name] = domain

        # Build the Factor
        factor_vars = parents + [name]
        self._cpts[name] = Factor(factor_vars, cpt_values)

    # ------------------------------------------------------------------ #
    # Variable Elimination Inference
    # ------------------------------------------------------------------ #
    def query(
        self,
        query_var:  str,
        evidence:   Dict[str, str],
        elim_order: Optional[List[str]] = None,
    ) -> Dict[str, float]:
        """
        Compute P(query_var | evidence) using Variable Elimination.

        Parameters
        ----------
        query_var  : the variable to query
        evidence   : dict of observed variable → value
        elim_order : order in which to eliminate hidden variables
                     (default: topological order minus query and evidence vars)

        Returns
        -------
        dict mapping each value of query_var to its posterior probability
        """
        # Start with all CPT factors
        factors = list(self._cpts.values())

        # 1. Restrict evidence variables
        reduced = []
        for f in factors:
            for var, val in evidence.items():
                if var in f.variables:
                    f = f.restrict(var, val)
            reduced.append(f)
        factors = reduced

        # 2. Determine elimination order (hidden variables = not query, not evidence)
        observed = set(evidence.keys()) | {query_var}
        hidden   = [v for v in self._nodes if v not in observed]

        if elim_order is None:
            elim_order = hidden

        # 3. Eliminate hidden variables
        for var in elim_order:
            # Collect factors that involve this variable
            involving = [f for f in factors if var in f.variables]
            remaining = [f for f in factors if var not in f.variables]

            if not involving:
                factors = remaining
                continue

            # Multiply all involving factors together
            product = involving[0]
            for f in involving[1:]:
                product = product.multiply(f)

            # Sum out the hidden variable
            marginalised = product.sum_out(var)
            factors = remaining + [marginalised]

        # 4. Multiply remaining factors (should involve query_var)
        result_factor = factors[0]
        for f in factors[1:]:
            result_factor = result_factor.multiply(f)

        # 5. Extract and normalise
        query_idx = result_factor.variables.index(query_var)
        result = {}
        for key, prob in result_factor.values.items():
            val = key[query_idx] if isinstance(key, tuple) else key
            result[val] = result.get(val, 0.0) + prob

        total = sum(result.values())
        if total > 0:
            result = {k: v / total for k, v in result.items()}

        return result

    def joint_probability(self, assignment: Dict[str, str]) -> float:
        """
        Compute the joint probability P(X1=x1, ..., Xn=xn).
        """
        prob = 1.0
        for var, cpt in self._cpts.items():
            prob *= cpt.get(assignment)
        return prob


# ===========================================================================
# SECTION 3 — Medical Diagnosis Bayesian Network
# ===========================================================================
def build_medical_bn() -> BayesianNetwork:
    """
    Flu Diagnosis Network
    ----------------------
    Variables: Season, Flu, Cold, Fever, Cough, Fatigue, Headache, Diagnosis

    Structure (edges):
        Season   → Flu
        Season   → Cold
        Flu      → Fever
        Cold     → Fever
        Flu      → Cough
        Cold     → Cough
        Flu      → Fatigue
        Flu      → Headache
        Cold     → Headache
        Fever, Cough, Fatigue, Headache → Diagnosis
    """
    bn = BayesianNetwork()

    # ---- Season (root node) ----
    bn.add_variable(
        name="Season", domain=["spring", "summer", "autumn", "winter"],
        parents=[],
        cpt_values={
            ("spring",): 0.25,
            ("summer",): 0.25,
            ("autumn",): 0.25,
            ("winter",): 0.25,
        }
    )

    # ---- Flu | Season ----
    bn.add_variable(
        name="Flu", domain=["T", "F"],
        parents=["Season"],
        cpt_values={
            ("spring", "T"): 0.15, ("spring", "F"): 0.85,
            ("summer", "T"): 0.05, ("summer", "F"): 0.95,
            ("autumn", "T"): 0.25, ("autumn", "F"): 0.75,
            ("winter", "T"): 0.35, ("winter", "F"): 0.65,
        }
    )

    # ---- Cold | Season ----
    bn.add_variable(
        name="Cold", domain=["T", "F"],
        parents=["Season"],
        cpt_values={
            ("spring", "T"): 0.25, ("spring", "F"): 0.75,
            ("summer", "T"): 0.05, ("summer", "F"): 0.95,
            ("autumn", "T"): 0.15, ("autumn", "F"): 0.85,
            ("winter", "T"): 0.30, ("winter", "F"): 0.70,
        }
    )

    # ---- Fever | Flu, Cold ----
    bn.add_variable(
        name="Fever", domain=["T", "F"],
        parents=["Flu", "Cold"],
        cpt_values={
            ("T", "T", "T"): 0.95, ("T", "T", "F"): 0.05,
            ("T", "F", "T"): 0.90, ("T", "F", "F"): 0.10,
            ("F", "T", "T"): 0.60, ("F", "T", "F"): 0.40,
            ("F", "F", "T"): 0.02, ("F", "F", "F"): 0.98,
        }
    )

    # ---- Cough | Flu, Cold ----
    bn.add_variable(
        name="Cough", domain=["T", "F"],
        parents=["Flu", "Cold"],
        cpt_values={
            ("T", "T", "T"): 0.95, ("T", "T", "F"): 0.05,
            ("T", "F", "T"): 0.80, ("T", "F", "F"): 0.20,
            ("F", "T", "T"): 0.70, ("F", "T", "F"): 0.30,
            ("F", "F", "T"): 0.05, ("F", "F", "F"): 0.95,
        }
    )

    # ---- Fatigue | Flu ----
    bn.add_variable(
        name="Fatigue", domain=["T", "F"],
        parents=["Flu"],
        cpt_values={
            ("T", "T"): 0.85, ("T", "F"): 0.15,
            ("F", "T"): 0.15, ("F", "F"): 0.85,
        }
    )

    # ---- Headache | Flu, Cold ----
    bn.add_variable(
        name="Headache", domain=["T", "F"],
        parents=["Flu", "Cold"],
        cpt_values={
            ("T", "T", "T"): 0.85, ("T", "T", "F"): 0.15,
            ("T", "F", "T"): 0.70, ("T", "F", "F"): 0.30,
            ("F", "T", "T"): 0.45, ("F", "T", "F"): 0.55,
            ("F", "F", "T"): 0.05, ("F", "F", "F"): 0.95,
        }
    )

    # ---- Diagnosis | Fever, Cough, Fatigue, Headache ----
    # 4 binary parents → 16 parent combinations
    diagnoses = ["flu", "cold", "allergy", "healthy"]
    diag_cpt  = {}

    combos = list(itertools.product(["T", "F"], repeat=4))   # Fever, Cough, Fatigue, Headache
    rules = {
        # (Fever, Cough, Fatigue, Headache)
        ("T", "T", "T", "T"): {"flu": 0.75, "cold": 0.15, "allergy": 0.05, "healthy": 0.05},
        ("T", "T", "T", "F"): {"flu": 0.70, "cold": 0.15, "allergy": 0.10, "healthy": 0.05},
        ("T", "T", "F", "T"): {"flu": 0.40, "cold": 0.40, "allergy": 0.10, "healthy": 0.10},
        ("T", "T", "F", "F"): {"flu": 0.30, "cold": 0.45, "allergy": 0.15, "healthy": 0.10},
        ("T", "F", "T", "T"): {"flu": 0.55, "cold": 0.15, "allergy": 0.20, "healthy": 0.10},
        ("T", "F", "T", "F"): {"flu": 0.50, "cold": 0.10, "allergy": 0.30, "healthy": 0.10},
        ("T", "F", "F", "T"): {"flu": 0.25, "cold": 0.30, "allergy": 0.35, "healthy": 0.10},
        ("T", "F", "F", "F"): {"flu": 0.15, "cold": 0.25, "allergy": 0.35, "healthy": 0.25},
        ("F", "T", "T", "T"): {"flu": 0.40, "cold": 0.30, "allergy": 0.20, "healthy": 0.10},
        ("F", "T", "T", "F"): {"flu": 0.35, "cold": 0.25, "allergy": 0.25, "healthy": 0.15},
        ("F", "T", "F", "T"): {"flu": 0.10, "cold": 0.50, "allergy": 0.30, "healthy": 0.10},
        ("F", "T", "F", "F"): {"flu": 0.05, "cold": 0.45, "allergy": 0.40, "healthy": 0.10},
        ("F", "F", "T", "T"): {"flu": 0.30, "cold": 0.10, "allergy": 0.40, "healthy": 0.20},
        ("F", "F", "T", "F"): {"flu": 0.25, "cold": 0.05, "allergy": 0.45, "healthy": 0.25},
        ("F", "F", "F", "T"): {"flu": 0.05, "cold": 0.10, "allergy": 0.50, "healthy": 0.35},
        ("F", "F", "F", "F"): {"flu": 0.02, "cold": 0.03, "allergy": 0.05, "healthy": 0.90},
    }
    for (fever, cough, fatigue, headache) in combos:
        key = (fever, cough, fatigue, headache)
        probs = rules[key]
        for diag in diagnoses:
            diag_cpt[(fever, cough, fatigue, headache, diag)] = probs[diag]

    bn.add_variable(
        name="Diagnosis",
        domain=diagnoses,
        parents=["Fever", "Cough", "Fatigue", "Headache"],
        cpt_values=diag_cpt,
    )

    return bn


# ===========================================================================
# SECTION 4 — Inference Demonstrations
# ===========================================================================
def run_inference_scenarios(bn: BayesianNetwork):
    print("\n" + "=" * 70)
    print("BAYESIAN NETWORK — INFERENCE SCENARIOS")
    print("=" * 70)
    print("Network: Flu Diagnosis")
    print("Query variable: Diagnosis")
    print()

    scenarios = [
        {
            "name":     "No evidence (prior)",
            "evidence": {},
        },
        {
            "name":     "Winter season only",
            "evidence": {"Season": "winter"},
        },
        {
            "name":     "Fever + Cough (classic flu symptoms)",
            "evidence": {"Fever": "T", "Cough": "T"},
        },
        {
            "name":     "Fever + Cough + Fatigue + Headache (all symptoms)",
            "evidence": {"Fever": "T", "Cough": "T", "Fatigue": "T", "Headache": "T"},
        },
        {
            "name":     "Cough only, no fever (could be allergy)",
            "evidence": {"Fever": "F", "Cough": "T"},
        },
        {
            "name":     "No symptoms at all",
            "evidence": {"Fever": "F", "Cough": "F", "Fatigue": "F", "Headache": "F"},
        },
        {
            "name":     "Winter + Fever + Fatigue (likely flu)",
            "evidence": {"Season": "winter", "Fever": "T", "Fatigue": "T"},
        },
        {
            "name":     "Summer + Cough only (likely allergy)",
            "evidence": {"Season": "summer", "Cough": "T"},
        },
    ]

    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        if scenario["evidence"]:
            print(f"  Evidence: {scenario['evidence']}")
        else:
            print(f"  Evidence: (none — prior distribution)")

        result = bn.query("Diagnosis", scenario["evidence"])

        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for diagnosis, prob in sorted_result:
            bar_len = int(prob * 40)
            bar     = "█" * bar_len + "░" * (40 - bar_len)
            print(f"  {diagnosis:<10} {bar}  {prob:.4f} ({prob*100:.1f}%)")

        top_diagnosis = sorted_result[0][0]
        print(f"  Most likely: {top_diagnosis.upper()}")
        print()

    # Also show flu probability given symptoms
    print("=" * 70)
    print("MARGINAL INFERENCE — P(Flu | Evidence)")
    print("=" * 70)
    flu_scenarios = [
        {"name": "No evidence",          "evidence": {}},
        {"name": "Winter",               "evidence": {"Season": "winter"}},
        {"name": "Fever=T",              "evidence": {"Fever": "T"}},
        {"name": "Fever=T, Fatigue=T",   "evidence": {"Fever": "T", "Fatigue": "T"}},
        {"name": "All symptoms=T",       "evidence": {"Fever": "T", "Cough": "T", "Fatigue": "T", "Headache": "T"}},
        {"name": "Summer, no symptoms",  "evidence": {"Season": "summer", "Fever": "F", "Cough": "F"}},
    ]

    print(f"\n  {'Scenario':<35}  P(Flu=T)   P(Flu=F)")
    print(f"  {'-'*60}")
    for sc in flu_scenarios:
        result = bn.query("Flu", sc["evidence"])
        p_t = result.get("T", 0.0)
        p_f = result.get("F", 0.0)
        print(f"  {sc['name']:<35}  {p_t:.4f}     {p_f:.4f}")


# ===========================================================================
# SECTION 5 — BN Tools Comparison
# ===========================================================================
BN_TOOLS = [
    {
        "name":        "pgmpy",
        "language":    "Python",
        "open_source": "Yes (MIT)",
        "inference":   ["Variable Elimination", "Belief Propagation", "MPLP", "Causal Inference"],
        "strengths":   ["Pure Python, easy to integrate", "scikit-learn compatible", "Causal reasoning support"],
        "weaknesses":  ["Slower than compiled tools for large networks"],
        "example":     "from pgmpy.models import BayesianNetwork\nfrom pgmpy.inference import VariableElimination",
    },
    {
        "name":        "Netica",
        "language":    "C/C++ (GUI + API)",
        "open_source": "No (commercial)",
        "inference":   ["Belief propagation", "Junction Tree", "Sensitivity analysis"],
        "strengths":   ["Mature commercial tool", "Excellent GUI", "Very fast inference"],
        "weaknesses":  ["Commercial license", "Limited scripting"],
        "example":     "net = Netica.Streamer()\nnet.ReadNet(\"diagnosis.dne\")",
    },
    {
        "name":        "Hugin Expert",
        "language":    "C++ (GUI + API bindings)",
        "open_source": "No (commercial)",
        "inference":   ["Junction Tree", "LBP", "Sensitivity", "LIMID (decision networks)"],
        "strengths":   ["Industry standard for decision analysis", "Dynamic BNs", "OOBNs"],
        "weaknesses":  ["Expensive", "Steeper learning curve"],
        "example":     "import Hugin\ndomain = Hugin.ParseDomainFromFile(\"net.net\")",
    },
    {
        "name":        "BayesFusion GeNIe",
        "language":    "C++ (GUI) with Python/R API",
        "open_source": "Free academic",
        "inference":   ["Junction Tree", "Forward Sampling", "ArcStrength"],
        "strengths":   ["Excellent GUI for network design", "Free for academics", "Influence diagrams"],
        "weaknesses":  ["Commercial for production", "GUI-centric workflow"],
        "example":     "import pysmile\nnet = pysmile.Network()\nnet.read_file(\"model.xdsl\")",
    },
    {
        "name":        "PyAgrum",
        "language":    "Python (C++ core)",
        "open_source": "Yes (LGPL3)",
        "inference":   ["Variable Elimination", "Belief Propagation", "Gibbs Sampling", "Loopy BP"],
        "strengths":   ["Fast C++ backend", "Jupyter-friendly visualisation", "Active development"],
        "weaknesses":  ["Smaller community than pgmpy"],
        "example":     "import pyAgrum as gum\nbn = gum.BayesNet('Diagnosis')\nbn.add(gum.LabelizedVariable('Flu', '', 2))",
    },
    {
        "name":        "bnlearn (R)",
        "language":    "R",
        "open_source": "Yes (GPL 2+)",
        "inference":   ["Exact inference", "MCMC", "Structure learning"],
        "strengths":   ["Excellent structure learning algorithms", "Deep statistical integration in R"],
        "weaknesses":  ["R-only", "Less friendly for production deployment"],
        "example":     "library(bnlearn)\ndag = model2network('[Flu][Season|Flu][Fever|Flu:Cold]')",
    },
]


def print_tools():
    print("\n" + "=" * 70)
    print("BAYESIAN NETWORK TOOLS COMPARISON")
    print("=" * 70)
    for tool in BN_TOOLS:
        print(f"\n  {tool['name']} ({tool['language']})")
        print(f"  Open Source  : {tool['open_source']}")
        print(f"  Inference    : {', '.join(tool['inference'])}")
        print(f"  Strengths    : {' | '.join(tool['strengths'])}")
        print(f"  Weaknesses   : {' | '.join(tool['weaknesses'])}")
        print(f"  Code sample  :")
        for line in tool["example"].splitlines():
            print(f"    {line}")


# ===========================================================================
# MAIN
# ===========================================================================
if __name__ == "__main__":
    print(BAYESIAN_NETWORK_OVERVIEW)

    print("=" * 70)
    print("BUILDING MEDICAL DIAGNOSIS BAYESIAN NETWORK")
    print("=" * 70)
    print("""
  Network Structure:
    Season
    ├── Flu
    │   ├── Fever ◄────────────────────────────────────────────┐
    │   ├── Cough ◄──────────────────────────────────────────┐ │
    │   ├── Fatigue                                           │ │
    │   └── Headache ◄───────────────────────────────────┐   │ │
    └── Cold ────────────────────────────────────────────►│   │ │
        │                                                 │   │ │
        ├── Fever (also) ─────────────────────────────────────► Diagnosis
        ├── Cough (also) ────────────────────────────────────►
        └── Headache (also) ─────────────────────────────────►
    Fatigue ──────────────────────────────────────────────────►
    """)

    bn = build_medical_bn()
    run_inference_scenarios(bn)
    print_tools()
