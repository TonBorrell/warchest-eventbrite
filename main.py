import random


def read_unit():
    return input("Select unit from your hand: ")


def read_position():
    pos = input("Select position to place: ")
    pos = pos.split(",")
    pos = (pos[0], pos[1])
    return pos


class Warchest:
    def __init__(self) -> None:
        self.board = Board()
        self.crow = Player(
            [ControlZone((4, 2), "control")],
            {Archer: 3, Berseker: 3},
            {"archer": Archer, "berseker": Berseker},
        )
        self.wolf = Player(
            [ControlZone((0, 2), "control")],
            {"cavalry": 3, "knight": 3},
            {"cavalry": Cavalry, "knight": Knight},
        )
        self.crow.other_player = self.wolf
        self.wolf.other_player = self.crow

        self.current_player = self.decide_first_player()

    def decide_first_player(self):
        self.current_player = random.choice((self.crow, self.wolf))

    def play(self):
        while not self.is_ended():
            # TODO: Check if initiative
            # Show board
            # Create Hand
            self.current_player.create_hand()
            # Show Hand, Recruitment units, Discard pile
            print(self.current_player.hand)
            print(self.current_player.bag)
            print(self.current_player.discard_pile)
            # Show Control Tokens
            print(self.current_player.control_token)
            # Input movement until no units on hand
            while self.current_player.hand:
                self.current_player.turn()
            # Do movement
            # Change current player

    def is_ended(self):
        # TODO: Check if game has finished
        pass


class Board:
    def __init__(self) -> None:
        self.board = ["." * 5] * 5
        self.pieces = []


class Player:
    def __init__(self, units, bag, units_dict) -> None:
        self.units = (
            units  # Inside this list --> tuple (Type of unit, Position of unit)
        )
        self.bag = {}  # Unit: n_units
        self.bag = bag
        self.units_dict = units_dict
        self.has_initiative = False
        self.hand = []
        self.discard_pile = []
        self.control_token = 3
        self.other_player = None

    def set_other_player(self, other_player):
        self.other_player = other_player

    def create_hand(self):
        bag_list = []
        for (key, value) in self.bag.items():
            for _ in range(value):
                bag_list.append(key)
        for _ in range(3):
            random_choice = random.choice(bag_list)
            self.hand.append(random_choice)

    def turn(self):
        # Read movement
        movement = input("Place/Control/Move/Recruit/Attack/Initiative")
        movement = movement.lower()
        if movement == "place":
            self.place()
        if movement == "control":
            self.control()
        if movement == "move":
            self.move()
        if movement == "recruit":
            self.recruit()
        if movement == "attack":
            self.attack()
        if movement == "initiative":
            self.initiative()
        # Check if posible
        # Do movement

    def place(self):
        unit = read_unit()
        self.check_if_unit_in_hand(unit)
        # TODO: Loop until unit in hand
        pos = read_position()
        for unit in self.units:
            if unit.name == "control":
                if unit.is_close(pos):
                    # Set piece in board
                    unit_class = self.units_dict[unit.lower()](pos)
                    self.units.append(unit_class)
                    self.hand.remove(unit)

    def control(self):
        # Unit to discard
        unit = read_unit()
        self.check_if_unit_in_hand(unit)
        # TODO: Loop until unit in hand
        # Position to control
        pos = read_position()
        if self.check_if_pos_in_control_zone(pos):
            # Control
            self.control_position(pos)
            # Discard unit
            self.hand.remove(unit)

    def move(self):
        # From position
        # TODO: Check if unit in this position
        pos_initial = read_position()
        # Select piece of same type
        unit_to_discard = read_unit()
        self.check_if_unit_in_hand(unit)
        # TODO: Loop until unit in hand
        # To position
        pos_final = read_position()
        for unit in self.units:
            if unit.name == unit_to_discard:
                if unit.isclose(pos_final):
                    unit.pos = pos_final
                    self.hand.remove(unit_to_discard)

    def recruit(self):
        # Select unit to recruit
        unit_to_discard = read_unit()
        # Remove from hand and put on discard pile
        self.hand.remove(unit_to_discard)
        self.discard_pile.append(unit_to_discard)
        # Get one from bag
        for unit in self.bag:
            if unit_to_discard == unit.name:
                self.bag[unit] -= 1

    def attack(self):
        # Position to attack from
        pos_initial = read_position()
        # Unit of same type in hand
        unit_to_attack_with = read_unit()
        self.check_if_unit_in_hand(unit_to_attack_with)
        # TODO: Loop until unit in hand
        # To position
        pos_final = read_position()
        # Check if attack is posible
        for unit in self.hand:
            if unit.name == unit_to_attack_with.lower():
                if unit.attack(pos_final):
                    # Remove from hand and add to pile
                    self.hand.remove(unit_to_attack_with)
                    self.discard_pile.append(unit_to_attack_with)
                    # Remove from game attacked unit
                    # TODO: Remove other player by checking if match position

    def initiative(self):
        # Use unit
        unit_to_discard = read_unit()
        # Delete it from hand
        self.hand.remove(unit_to_discard)
        # Set initiative
        self.initiative = True

    def check_if_unit_in_hand(self, unit):
        if unit in self.hand:
            return True
        return False

    def check_if_pos_in_control_zone(self, pos):
        # TODO: Check if position is in control zone, control zone is a constant in the game
        pass

    def check_if_unit_in_bag(self, unit):
        pass

    def control_position(self, pos):
        unit_class = self.units_dict[ControlZone(pos)]
        self.units.append(unit_class)
        self.control_token -= 1


class Unit:
    def __init__(self, pos, name) -> None:
        self.pos = pos
        self.name = name

    def is_close(self, pos2, max_dif=1):
        if (
            self.pos[0] + max_dif == pos2[0]
            or self.pos[0] - max_dif == pos2[0]
            and self.pos[1] == pos2[1]
        ):
            return True
        if (
            self.pos[1] + max_dif == pos2[1]
            or self.pos[1] - max_dif == pos2[1]
            and self.pos[0] == pos2[0]
        ):
            return True
        return False

    def set_pos(self, pos):
        self.pos = pos


class ControlZone(Unit):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)


class Archer(Unit):
    def __init__(self, pos, name):
        super().__init__(pos, name)


class Berseker(Unit):
    def __init__(self, pos, name):
        super().__init__(pos, name)


class Cavalry(Unit):
    def __init__(self, pos, name):
        super().__init__(pos, name)


class Knight(Unit):
    def __init__(self, pos, name):
        super().__init__(pos, name)


if __name__ == "__main__":
    board = Board()
    board.print_board()
