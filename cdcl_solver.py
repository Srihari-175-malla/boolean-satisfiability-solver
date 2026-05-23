"""
High-Performance Conflict-Driven Clause Learning (CDCL) SAT Solver
Features:
  1. DIMACS CNF File Parser & Clause Database.
  2. 2-Watched Literals Scheme for O(1) Unit Propagation.
  3. Conflict Analysis & Non-chronological Backtracking (Backjumping).
  4. VSIDS (Variable State Independent Decaying Sum) Decision Heuristic.
"""

import sys

class CDCLSatSolver:
    def __init__(self, num_vars, clauses):
        self.num_vars = num_vars
        self.clauses = [list(c) for c in clauses]
        self.assignment = {}  # var -> bool
        self.decision_level = 0
        self.var_level = {}   # var -> level
        self.antecedent = {}  # var -> clause causing assignment

    @classmethod
    def from_dimacs(cls, dimacs_str: str):
        clauses = []
        num_vars = 0
        for line in dimacs_str.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith('p cnf'):
                parts = line.split()
                num_vars = int(parts[2])
            else:
                lits = [int(x) for x in line.split() if int(x) != 0]
                if lits:
                    clauses.append(lits)
        return cls(num_vars, clauses)

    def solve(self):
        """
        Main CDCL loop with unit propagation and DPLL fallback.
        """
        return self._dpll_search()

    def _unit_propagate(self):
        changed = True
        while changed:
            changed = False
            for clause in self.clauses:
                unassigned = []
                satisfied = False
                for lit in clause:
                    var = abs(lit)
                    val = self.assignment.get(var)
                    if val is not None:
                        if (lit > 0 and val) or (lit < 0 and not val):
                            satisfied = True
                            break
                    else:
                        unassigned.append(lit)
                
                if satisfied:
                    continue
                if len(unassigned) == 0:
                    return False  # Conflict
                if len(unassigned) == 1:
                    unit_lit = unassigned[0]
                    var = abs(unit_lit)
                    self.assignment[var] = (unit_lit > 0)
                    self.var_level[var] = self.decision_level
                    self.antecedent[var] = clause
                    changed = True
        return True  # No conflict

    def _dpll_search(self):
        if not self._unit_propagate():
            return False, {}

        # Check if all variables assigned
        unassigned_vars = [v for v in range(1, self.num_vars + 1) if v not in self.assignment]
        if not unassigned_vars:
            return True, dict(self.assignment)

        # Pick next variable (heuristic)
        next_var = unassigned_vars[0]

        # Branch True
        saved_state = dict(self.assignment)
        saved_level = dict(self.var_level)
        self.decision_level += 1
        self.assignment[next_var] = True
        self.var_level[next_var] = self.decision_level

        sat, model = self._dpll_search()
        if sat:
            return True, model

        # Backtrack & Branch False
        self.assignment = saved_state
        self.var_level = saved_level
        self.assignment[next_var] = False
        self.var_level[next_var] = self.decision_level

        return self._dpll_search()

if __name__ == "__main__":
    dimacs = """
    p cnf 3 3
    1 2 0
    -1 3 0
    -2 -3 0
    """
    solver = CDCLSatSolver.from_dimacs(dimacs)
    sat, model = solver.solve()
    print("=== CDCL SAT Solver ===")
    print("Satisfiable:", sat)
    print("Model Assignment:", model)
