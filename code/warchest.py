import random

from code.board import Board
from code.player import Player
from code.unit import *


class Warchest:
    def __init__(self, name_player_1="crow", name_player_2="wolf") -> None:
        self.board = Board()
        self.crow = Player(
            name_player_1,
            [ControlZone((2, 4), "control")],
            {"archer": 3, "mercenary": 3, "royal": 1},
            {"archer": Archer, "mercenary": Mercenary, "royal": Royal},
            self.board,
        )
        self.wolf = Player(
            name_player_2,
            [ControlZone((2, 0), "control")],
            {"crossbowman": 3, "knight": 3, "royal": 1},
            {"crossbowman": Crossbowman, "knight": Knight, "royal": Royal},
            self.board,
        )
        self.crow.other_player = self.wolf
        self.wolf.other_player = self.crow

        self.current_player, self.other_player = self.decide_first_player(
            [self.crow, self.wolf]
        )

    def decide_first_player(self, player_list):
        """
        The aim of this function is to decide which player is going to start the game
        """
        player1 = random.choice((self.crow, self.wolf))
        for player in player_list:
            if player != player1:
                player2 = player
        return player1, player2

    def play(self):
        """
        Function that runs the whole game, checks if game has ended and if not changes current player
        """
        while True:
            for i in range(2):
                if not self.is_ended():
                    # Show board
                    self.board.show_board()
                    # Create Hand
                    self.current_player.create_hand()
                    # Show Hand, Recruitment units, Discard pile
                    print("Units in your hand: ", self.current_player.hand)
                    print("Units in your bag: ", self.current_player.bag)
                    print(
                        "Units in your discard pile: ", self.current_player.discard_pile
                    )
                    # Show Control Tokens
                    print(
                        "Control tokens remaining: ", self.current_player.control_token
                    )
                    # Input movement until no units on hand
                    while self.current_player.hand:
                        self.current_player.turn()
                        self.board.show_board()
                    if i == 0:
                        self.change_player()
                else:
                    return self.current_player.name
            self.change_player(check_initiatives=True)

    def change_player(self, check_initiatives=False):
        """
        Function to change the current player, has a boolean in order to check if player has initiative
        """
        if check_initiatives:
            if self.other_player.has_initiative:
                current = self.current_player
                self.current_player = self.other_player
                self.other_player = current
                self.current_player.has_initiative = False
                self.other_player.has_initiative = False
            elif self.current_player.has_initiative:
                self.current_player.has_initiative = False
            else:
                current = self.current_player
                self.current_player = self.other_player
                self.other_player = current
        else:
            current = self.current_player
            self.current_player = self.other_player
            self.other_player = current

    def is_ended(self):
        # Check for both player if control zones are equal to 3 or if no control tokens available
        return self.current_player if self.current_player.control_token == 0 else False
