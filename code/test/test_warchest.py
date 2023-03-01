import unittest

from code.warchest import Warchest


class WarchestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.player1 = "Test1"
        self.player2 = "Test2"
        self.game = Warchest(self.player1, self.player2)
        self.game.current_player = self.game.crow
        self.game.other_player = self.game.wolf

    def test_change_player_no_initiatives(self):
        self.game.crow.has_initiative = False
        self.game.wolf.has_initiative = False

        self.game.change_player(check_initiatives=False)

        self.assertEqual(self.game.current_player, self.game.wolf)

    def test_change_player_with_initiatives(self):
        self.game.crow.has_initiative = True
        self.game.wolf.has_initiative = False

        self.game.change_player(check_initiatives=True)

        self.assertEqual(self.game.current_player, self.game.crow)

    def test_change_player_with_both_initiatives(self):
        self.game.crow.has_initiative = True
        self.game.wolf.has_initiative = True

        self.game.change_player(check_initiatives=True)

        self.assertEqual(self.game.current_player, self.game.wolf)

    def test_is_ended(self):
        self.game.current_player = self.game.crow
        self.game.crow.control_token = 0

        end = self.game.is_ended()

        self.assertEqual(end, self.game.crow)
