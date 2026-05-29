================================================================================
  AI PROGRAMMING ASSIGNMENT — SUBMISSION README
================================================================================

Submission date : 29 May 2026
Language        : Python 3.11+
Dependencies    : Standard library only (math, random, itertools, collections,
                  json, time, copy) — no pip install required.

--------------------------------------------------------------------------------
DIRECTORY STRUCTURE
--------------------------------------------------------------------------------

assignment/
├── README.txt                               ← this file
│
├── task1_search_algorithms/
│   ├── minimax.py                           ← Task 1a: Minimax
│   ├── alpha_beta.py                        ← Task 1b: Alpha-Beta Pruning
│   ├── heuristic_alpha_beta.py              ← Task 1c: Heuristic Alpha-Beta
│   ├── mcts.py                              ← Task 1d: Monte-Carlo Tree Search
│   └── test_cases.py                        ← Comparison table: all 4 algorithms
│
├── task2_travel_planner/
│   ├── knowledge_base.py                    ← Task 2a: Knowledge bases (KB)
│   └── travel_planner.py                    ← Task 2b: Reasoning / planning engine
│
├── task3_knowledge_graphs/
│   ├── knowledge_graphs.py                  ← Task 3: KG engine + travel domain KG
│   ├── knowledge_graphs_description.txt     ← Written description & tool comparison
│   └── travel_kg_export.json                ← JSON export of the travel KG
│
└── task4_bayesian_networks/
    ├── bayesian_network.py                  ← Task 4: BN engine + medical diagnosis
    └── bayesian_networks_description.txt    ← Written description & tool comparison


--------------------------------------------------------------------------------
HOW TO RUN EACH FILE
--------------------------------------------------------------------------------

Run all files with:  python3 <filename>.py
(All files must be run from their own subdirectory, not from the project root.)

TASK 1 — Search Algorithms
---------------------------
  cd assignment/task1_search_algorithms

  python3 minimax.py
    → Runs 5 Tic-Tac-Toe test cases with Minimax, then enters interactive mode
      (you play as O, AI plays as X).

  python3 alpha_beta.py
    → Runs the same 5 cases with Alpha-Beta, printing nodes explored vs. Minimax,
      then enters interactive mode.

  python3 heuristic_alpha_beta.py
    → Tests Heuristic Alpha-Beta at depths 1, 2, 4, 9, then interactive mode.

  python3 mcts.py
    → Runs MCTS at 200 and 1 000 simulations, then prompts for simulation count
      and enters interactive mode.

  python3 test_cases.py
    → Side-by-side comparison table of all four algorithms on 8 board states.

TASK 2 — AI Travel Planner
---------------------------
  cd assignment/task2_travel_planner

  python3 knowledge_base.py
    → Demonstrates the three knowledge bases: wines, destinations, cuisines.
      Runs several sample queries (beach destinations, vegan cuisines, etc.).

  python3 travel_planner.py
    → Runs four example travel plans with different preferences (budget, cuisine
      restriction, travel type) and prints day-by-day itineraries.

TASK 3 — Knowledge Graphs
--------------------------
  cd assignment/task3_knowledge_graphs

  python3 knowledge_graphs.py
    → Prints the written KG overview, builds the travel domain KG, runs
      SPARQL-like queries, prints tool comparison, and exports travel_kg_export.json.

  (See knowledge_graphs_description.txt for the full written description.)

TASK 4 — Bayesian Networks
---------------------------
  cd assignment/task4_bayesian_networks

  python3 bayesian_network.py
    → Prints the BN overview, builds the Medical Diagnosis network, runs 8
      inference scenarios using Variable Elimination, and prints tool comparison.

  (See bayesian_networks_description.txt for the full written description.)


--------------------------------------------------------------------------------
DESIGN DECISIONS
--------------------------------------------------------------------------------

Task 1
  • All four algorithms share the same TicTacToe board class (defined in
    minimax.py and imported by the other files) to ensure identical game logic.
  • Minimax uses +10/−10/0 terminal scores; Heuristic AB uses ±1000 for
    terminals and a positional evaluation function for non-terminals.
  • MCTS uses UCB1 exploration with coefficient √2; rollouts are random
    (uniform policy).

Task 2
  • Knowledge bases are plain Python dicts/lists — no external ontology library.
  • The reasoning engine implements forward chaining: it iterates over KB entries
    checking conditions, firing rules that match, and accumulating derived facts.
  • Cost model is per-person per-day, broken into accommodation / meals /
    activities / transport bands.

Task 3
  • An in-memory Property Graph (adjacency list) is implemented from scratch.
  • SPARQL-like queries use Python lambda predicates rather than a parser.
  • The JSON export (travel_kg_export.json) follows a standard
    nodes/edges schema for interoperability.

Task 4
  • Variable Elimination is implemented from scratch with a Factor class that
    supports restrict, multiply, marginalise (sum-out), and normalise.
  • The Medical Diagnosis BN has 8 variables and 8 CPTs defined as nested dicts.
  • Inference order follows a simple heuristic: hidden variables with fewest
    remaining states are eliminated first.

================================================================================
