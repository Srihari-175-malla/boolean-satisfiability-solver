import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cdcl_solver import CDCLSatSolver

class TestCDCLSatSolver(unittest.TestCase):
    def test_satisfiable_cnf(self):
        dimacs = """
        p cnf 3 3
        1 2 0
        -1 3 0
        -2 -3 0
        """
        solver = CDCLSatSolver.from_dimacs(dimacs)
        sat, model = solver.solve()
        self.assertTrue(sat)
        self.assertIn(1, model)

    def test_unsatisfiable_cnf(self):
        dimacs = """
        p cnf 1 2
        1 0
        -1 0
        """
        solver = CDCLSatSolver.from_dimacs(dimacs)
        sat, model = solver.solve()
        self.assertFalse(sat)

if __name__ == '__main__':
    unittest.main()
