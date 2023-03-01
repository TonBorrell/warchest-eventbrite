import unittest

from code.unit import Archer, ControlZone, Crossbowman

class TestUnit(unittest.TestCase):
    def setUp(self) -> None:
        self.archer = Archer((2,3), "archer")
        self.crossbowman = Crossbowman((2,3), "crossbowman")

    def test_is_close_non_diagonal(self):
        response = self.archer.is_close((2,4), diagonal=False)
        expected_output = True

        self.assertEqual(response, expected_output)

    def test_is_close_diagonal(self):
        response = self.archer.is_close((3,4), diagonal=True)
        expected_output = True

        self.assertEqual(response, expected_output)

    def test_is_close_non_diagonal_non_close(self):
        response = self.archer.is_close((3,4), diagonal=False)
        expected_output = False

        self.assertEqual(response, expected_output)

    def test_archer_attack_correct(self):
        response = self.archer.attack((4, 5))
        expected_output = True

        self.assertEqual(response, expected_output)

    def test_archer_attack_incorrect(self):
        response = self.archer.attack((5, 5))
        expected_output = False

        self.assertEqual(response, expected_output)

    def test_crossbowman_attack_correct(self):
        response = self.crossbowman.attack((4, 3))
        expected_output = True

        self.assertEqual(response, expected_output)

    def test_crossbowman_attack_incorrect(self):
        response = self.crossbowman.attack((4, 5))
        expected_output = False

        self.assertEqual(response, expected_output)

