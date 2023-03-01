import unittest

from code.board import Board
from code.unit import Archer, ControlZone


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.pieces = {
            "Test": [ControlZone((2, 0), "control"), Archer((3, 4), "archer")]
        }

        self.board.pieces = self.pieces

    def test_is_pos_active_for_occuped_control_zone(self):
        response = self.board.is_pos_active((2, 0))
        expected_output = "T"

        self.assertEqual(response, expected_output)

    def test_is_pos_active_for_non_occuped_control_zone(self):
        response = self.board.is_pos_active((2, 4))
        expected_output = "@"

        self.assertEqual(response, expected_output)

    def test_is_non_pos_active(self):
        response = self.board.is_pos_active((2, 5))
        expected_output = "."

        self.assertEqual(response, expected_output)

    def test_is_pos_active_for_archer(self):
        response = self.board.is_pos_active((3, 4))
        expected_output = "A"

        self.assertEqual(response, expected_output)
