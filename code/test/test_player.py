import unittest
from unittest.mock import patch

from code.player import Player
from code.unit import Royal, Archer, ControlZone
from code.board import Board


class PlayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.name = "Test"
        self.name2 = "Rest"
        self.units = [ControlZone((2, 4), "control")]
        self.units2 = [ControlZone((2, 0), "control"), Archer((2,2), "archer")]
        self.bag = {"archer": 3, "royal": 1}
        self.units_dict = {"archer": Archer, "royal": Royal}
        self.board = Board()
        self.player = Player(
            self.name, self.units, self.bag, self.units_dict, self.board
        )
        self.player2 = Player(
            self.name2, self.units2, self.bag, self.units_dict, self.board
        )
        self.player.other_player = self.player2

    def test_create_hand(self):
        expected_result = ["royal", "archer", "archer"]

        self.player.create_hand()

        self.assertEqual(self.player.hand, expected_result)

    @patch("builtins.input", side_effect=["archer", "2,3"])
    def test_place(self, mock_input):
        self.player.hand = ["archer", "archer", "archer"]
        self.player.place()

        for unit in self.player.units:
            if unit.name == 'archer':
                self.archer = unit

        self.assertEqual(self.player.hand, ["archer", "archer"])
        self.assertEqual(len(self.player.units), 2)
        self.assertEqual(self.player.discard_pile, ["archer"])
        self.assertEqual(self.archer.pos, (2, 3))

    @patch("builtins.input", side_effect=["archer", "2,3", "2,3", "archer", "1,3"])
    def test_move(self, mock_input):
        self.player.hand = ["archer", "archer", "archer"]
        self.player.place()
        self.player.move()

        for unit in self.player.units:
            if unit.name == 'archer':
                self.archer = unit

        self.assertEqual(self.archer.pos, (1,3))
        self.assertEqual(self.player.hand, ["archer"])
        self.assertEqual(len(self.player.units), 2)
        self.assertEqual(self.player.discard_pile, ["archer", "archer"])

    @patch("builtins.input", side_effect=["archer", "2,3", "2,3", "archer", "1,3", "archer", "1,3"])
    def test_control(self, mock_input):
        self.player.hand = ["archer", "archer", "archer"]
        self.player.place()
        self.player.move()

        self.player.control()

        for unit in self.player.units:
            if unit.name == 'archer':
                self.archer = unit

        self.assertEqual(self.archer.pos, (1,3))
        self.assertEqual(self.player.hand, [])
        self.assertEqual(len(self.player.units), 3) # Control, Control, Archer
        self.assertEqual(self.player.discard_pile, ["archer", "archer", "archer"])
        self.assertEqual(self.player.control_token, 2)

    @patch("builtins.input", side_effect=["archer"])
    def test_recruit(self, mock_input):
        self.player.hand = ["archer", "archer", "archer"]
        self.player.recruit()

        self.assertEqual(self.player.hand, ["archer", "archer"])
        self.assertEqual(len(self.player.units), 1)
        self.assertEqual(self.player.discard_pile, ["archer"])

    @patch("builtins.input", side_effect=["archer"])
    def test_initiative(self, mock_input):
        self.player.hand = ["archer", "archer", "archer"]
        self.player.initiative()

        self.assertEqual(self.player.hand, ["archer", "archer"])
        self.assertEqual(len(self.player.units), 1)
        self.assertEqual(self.player.discard_pile, ["archer"])
        self.assertEqual(self.player.has_initiative, True)

    @patch("builtins.input", side_effect=["archer", "2,3", "2,3", "archer", "2,2"])
    def test_attack(self, mock_input):
        self.player.hand = ["archer", "archer", "archer"]
        self.player.place()
        self.player.attack()

        for unit in self.player.units:
            if unit.name == 'archer':
                self.archer = unit

        self.assertEqual(self.archer.pos, (2,3))
        self.assertEqual(self.player.hand, ["archer"])
        self.assertEqual(len(self.player.units), 2) # Control, Archer
        self.assertEqual(self.player.discard_pile, ["archer", "archer"])
        self.assertEqual(len(self.player2.units), 1)



