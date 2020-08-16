import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from cell import Cell

class TestCell(unittest.TestCase):

    def init(self):
        self.cell = Cell()

    def test_setup(self):
        self.init()
        res = self.cell.setup(setup_type="")
        self.assertFalse(res, "Empty Setup Type: Should be False")

        res = self.cell.setup(setup_type="Array")
        self.assertFalse(res, "Empty Array; Should be False")

        res = self.cell.setup(setup_type="Impulse")
        self.assertFalse(res, "Empty Tuple; Should be False")

        regime = [[0, 1000, 25]]
        res = self.cell.setup(setup_type="Array", regime=regime)
        self.assertTrue(res, "Valid Array: Should be True")

        res = self.cell.setup(setup_type="Impulse", impulse=(1000, 25))
        self.assertTrue(res, "Valid Impulse: Should be True")

        res = self.cell.setup(setup_type="Blah")
        self.assertFalse(res, "Invalid Setup Type: Should be False")

    def test_iterate(self):
        # NOTE: we don't actually check to see if iterate is providing good
        # results, just that it does provide results.
        self.init()
        # deps
        self.test_model()

        env = (1000, 25)
        self.assertTrue(self.cell.setup(setup_type="Impulse", impulse=env), "Bad setup")
        self.assertIsNotNone(self.cell.iterate(0), "Result is not None")

    def test_model(self):
        # NOTE: we don't actually check to see if model is providing good
        # results, just that it does provide results.
        self.init()
        env = (1000, 25)
        self.assertTrue(self.cell.setup(setup_type="Impulse", impulse=env), "Bad setup")
        self.assertIsNotNone(self.cell.model(0), "Result is not None")

    def test_get_cell_IV(self):
        self.init()
        # deps
        self.test_iterate()

        env = (1000, 25)
        self.assertTrue(self.cell.setup(setup_type="Impulse", impulse=env), "Bad setup")
        self.assertIsNotNone(self.cell.get_cell_IV(), "Result is not None")

    def test_get_cell_gmpp(self):
        # NOTE: we don't actually check to see if get_cell_gmpp is providing
        # good results, just that it does provide results.
        self.init()
        # deps
        self.test_get_cell_IV()

        env = (1000, 25)
        self.assertTrue(self.cell.setup(setup_type="Impulse", impulse=env), "Bad setup")
        self.assertIsNotNone(self.cell.get_cell_gmpp(), "Result is not None")

    def test_get_env_conditions(self):
        self.init()
        # deps
        self.test_iterate()
        self.test_increment_cycle()

        env = (1000, 25)
        self.assertTrue(self.cell.setup(setup_type="Impulse", impulse=env), "Bad setup")
        self.assertEqual(self.cell.get_env_conditions(), (1000, 25, 0), "Impulse Env does not match up")

        regime = [[0, 1000, 25], [1, 700, 50]]
        self.assertTrue(self.cell.setup(setup_type="Array", regime=regime), "Bad setup")
        self.assertEqual(self.cell.get_env_conditions(), (1000, 25, 0), "Array Env does not match up")
        
        # update env variable
        self.cell.increment_cycle()
        self.cell.iterate(0)
        self.assertEqual(self.cell.get_env_conditions(), (700, 50, 0), "Array Env does not match up")

    def test_get_model_type(self):
        self.init()
        cell = Cell()
        self.assertEqual(cell.get_model_type(), "Nonideal", "Should Nonideal")
        cell = Cell("Ideal")
        self.assertEqual(cell.get_model_type(), "Ideal", "Should be Ideal")
        cell = Cell("Nonideal")
        self.assertEqual(cell.get_model_type(), "Nonideal", "Should be Nonideal")

    def test_set_current_cycle(self):
        self.init()
        self.assertEqual(self.cell.cycle, 0, "Cycle does not match 0")
        self.cell.set_current_cycle(5)
        self.assertEqual(self.cell.cycle, 5, "Cycle does not match 5")

    def test_increment_cycle(self):
        self.init()
        self.assertEqual(self.cell.cycle, 0, "Cycle does not match 0")
        self.cell.increment_cycle()
        self.assertEqual(self.cell.cycle, 1, "Cycle does not match 1")

if __name__ == '__main__':
    unittest.main()