import random


def read_unit():
    return input("Select unit from your hand: ")


def read_position():
    pos = input("Select position to place: ")
    pos = pos.split(",")
    pos = (int(pos[0]), int(pos[1]))
    return pos


class Warchest:
    def __init__(self) -> None:
        self.board = Board()
        self.crow = Player(
            "crow",
            [ControlZone((2, 4), "control")],
            {"archer": 3, "mercenary": 3},
            {"archer": Archer, "mercenary": Mercenary},
            self.board,
        )
        self.wolf = Player(
            "wolf",
            [ControlZone((2, 0), "control"), Crossbowman((2, 2), "crossbowman")],
            {"crossbowman": 3, "knight": 3},
            {"crossbowman": Crossbowman, "knight": Knight},
            self.board,
        )
        self.crow.other_player = self.wolf
        self.wolf.other_player = self.crow

        # self.current_player = self.decide_first_player()
        self.current_player = self.crow
        self.other_player = self.wolf

    def decide_first_player(self):
        return random.choice((self.crow, self.wolf))

    def play(self):
        while not self.is_ended():
            # TODO: Change only when both have played
            # TODO: Check if initiative
            # Show board
            self.board.show_board()
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
                self.board.show_board()
                print(self.current_player.hand)
                print(self.current_player.discard_pile)
            # Do movement
            # Change current player
            self.change_player()

    def change_player(self):
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

    def is_ended(self):
        # TODO: Check if game has finished
        pass


class Board:
    def __init__(self) -> None:
        self.board = ["." * 5] * 5
        self.control_areas = [(2, 0), (2, 4), (0, 1), (1, 3), (3, 1), (4, 3)]
        self.pieces = {}  # All unit class

    def show_board(self):
        for i in range(5):
            for j in range(5):
                print(self.is_pos_active((j, i)), end=" ")
            print()

    def is_pos_active(self, pos):
        for units_list in self.pieces.values():
            for unit in units_list:
                if unit.pos == pos:
                    return unit.name[0].upper()
        if pos in self.control_areas:
            return "@"
        return "."


class Player:
    def __init__(self, name, units, bag, units_dict, board) -> None:
        self.name = name
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
        self.board = board
        self.board.pieces[self.name] = units

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
            self.bag[random_choice] -= 1

    def turn(self):
        # Read movement
        movement = input(
            "Make an action (Place/Control/Move/Recruit/Attack/Initiative): "
        )
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

    def read_unit_until_in_hand(self):
        unit = None
        while not self.check_if_unit_in_hand(unit):
            if unit is not None:
                print("Unit not on hand, please select one from your hand of units")
            unit = read_unit()
        return unit

    def place(self):
        unit_to_place = self.read_unit_until_in_hand()
        pos = self.read_pos_until_correct(
            input_message="Select position to place: ", is_occupied=False
        )
        for unit in self.units:
            if unit.name == "control":
                if unit.is_close(pos):
                    # Set piece in board
                    unit_class = self.units_dict[unit_to_place.lower()](
                        pos, unit_to_place
                    )
                    self.units.append(unit_class)
                    self.hand.remove(unit_to_place)
                    self.discard_pile.append(unit_to_place)

    def control(self):
        # Unit to discard
        unit = self.read_unit_until_in_hand()
        # Position to control
        pos = read_position()
        controllable = False
        while not controllable:
            controllable = self.check_if_pos_controllable(pos)
            if not controllable:
                print("Select a position occupied by you: ")
                pos = read_position()
        # Control
        self.control_position(pos)
        # Discard unit
        self.hand.remove(unit)

    def move(self):
        # From position
        pos_initial = self.read_pos_until_correct(
            input_message="Select position to move from: "
        )
        # Select piece of same type
        unit_to_discard = self.read_unit_until_in_hand()
        unit_in_initial_pos = self.get_unit_by_pos(pos_initial)
        if unit_to_discard != unit_in_initial_pos.name:
            print(
                "Unit selected not in position spectified, restarting the move maneuver"
            )
            self.move()
        # To position
        pos_final = self.read_pos_until_correct(
            input_message="Select position to move to: ", is_occupied=False
        )
        if unit_in_initial_pos.is_close(pos_final, diagonal=True):
            unit_in_initial_pos.pos = pos_final
            self.hand.remove(unit_in_initial_pos.name)

    def recruit(self):
        # Select unit to recruit
        unit_to_discard = self.read_unit_until_in_hand()
        # Remove from hand and put on discard pile
        self.hand.remove(unit_to_discard)
        self.discard_pile.append(unit_to_discard)

    def attack(self):
        # Position to attack from
        pos_initial = self.read_pos_until_correct(
            input_message="Select position to attack from: "
        )
        # Unit of same type in hand
        unit_to_attack_with = self.read_unit_until_in_hand()
        unit_in_initial_pos = self.get_unit_by_pos(pos_initial)
        if unit_to_attack_with != unit_in_initial_pos.name:
            print(
                "Unit selected not in position spectified, restarting the attack maneuver"
            )
            self.attack()
        # To position
        pos_final = self.read_pos_until_correct(
            input_message="Select position to attack to: ", is_occupied=False
        )
        # Check if attack is posible
        if self.pre_attack_maneuver(unit_in_initial_pos, pos_final):
            # Remove from hand and add to pile
            self.hand.remove(unit_to_attack_with)
            self.discard_pile.append(unit_to_attack_with)
            self.other_player.units.remove(self.has_other_unit)
            self.has_other_unit = None

    def pre_attack_maneuver(self, unit, pos):
        # Check if other player has unit in that position
        self.has_other_unit = self.get_unit_by_pos(pos, other=True)
        print(self.has_other_unit)
        # Check if unit can make that attack
        can_attack = unit.attack(pos)
        print(can_attack)
        if self.has_other_unit is not None and can_attack:
            return True
        return False

    def initiative(self):
        if not self.has_initiative:
            # Use unit
            unit_to_discard = self.read_unit_until_in_hand()
            # Delete it from hand
            self.hand.remove(unit_to_discard)
            self.discard_pile.append(unit_to_discard)
            # Set initiative
            self.has_initiative = True
        else:
            print("You already have initiative")

    def check_if_unit_in_hand(self, unit):
        if unit in self.hand:
            return True
        return False

    def read_pos_until_correct(
        self, input_message="Select position to place: ", is_occupied=True
    ):  # is_occupied means that position reading is occupied by some unit, True --> Ocuppied
        if is_occupied:
            pos_correct = False
            while not pos_correct:
                pos = input(input_message)
                pos = pos.split(",")
                pos = (int(pos[0]), int(pos[1]))
                pos_correct = self.check_if_unit_in_pos(pos)
                if not pos_correct:
                    print("Position not occupied by any unit")
        else:
            pos_correct = False
            while not pos_correct:
                pos = input(input_message)
                pos = pos.split(",")
                pos = (int(pos[0]), int(pos[1]))
                pos_correct = self.check_if_unit_not_in_pos(pos)
                if not pos_correct:
                    print("Position occupied by a unit")

        return pos

    def check_if_pos_controllable(self, pos):
        is_control_zone = self.check_if_pos_in_control_zone(pos)
        is_pos_occuped = self.check_if_unit_in_pos(pos)
        is_already_controlled = self.check_if_pos_controlled(pos)

        return is_control_zone and is_pos_occuped and not is_already_controlled

    def check_if_pos_controlled(self, pos):
        for unit in self.units:
            if unit.name == "control":
                if unit.pos == pos:
                    return True
        return False

    def check_if_unit_in_pos(self, pos):
        for unit in self.units:
            if pos == unit.pos:
                return True
        return False

    def check_if_unit_not_in_pos(self, pos):
        for unit in self.units:
            if pos == unit.pos:
                return False
        return True

    def check_if_pos_in_control_zone(self, pos):
        for control_zone in self.board.control_areas:
            if pos == control_zone:
                return True
        return False

    def check_if_unit_in_bag(self, unit):
        if self.bag[unit] > 0:
            return True
        else:
            return False

    def get_unit_by_pos(self, pos, other=False):
        if other:
            units_to_check = self.other_player.units
        else:
            units_to_check = self.units

        for unit in units_to_check:
            if unit.pos == pos:
                return unit

    def control_position(self, pos):
        unit_class = ControlZone(pos, "control")
        self.units.append(unit_class)
        self.control_token -= 1


class Unit:
    def __init__(self, pos, name) -> None:
        self.pos = pos
        self.name = name

    def is_close(self, pos2, max_dif=1, diagonal=False):
        pos2 = (int(pos2[0]), int(pos2[1]))
        for i in range(1, max_dif + 1):
            if (
                self.pos[0] + i == pos2[0]
                or self.pos[0] - i == pos2[0]
                and self.pos[1] == pos2[1]
            ):
                return True
            if (
                self.pos[1] + i == pos2[1]
                or self.pos[1] - i == pos2[1]
                and self.pos[0] == pos2[0]
            ):
                return True
            if diagonal:
                if (self.pos[0] + i == pos2[0] or self.pos[0] - i == pos2[0]) and (
                    self.pos[1] + i == pos2[1] or self.pos[1] - i == pos2[1]
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

    def attack(self, pos):
        if self.is_close(pos, max_dif=2, diagonal=True):
            return True
        return False


class Mercenary(Unit):
    def __init__(self, pos, name):
        super().__init__(pos, name)

    def attack(self, pos):
        if self.is_close(pos, diagonal=True):
            return True
        return False


class Crossbowman(Unit):
    def __init__(self, pos, name):
        super().__init__(pos, name)

    def attack(self, pos):
        if self.is_close(pos, max_dif=2, diagonal=False):
            return True
        return False


class Knight(Unit):
    def __init__(self, pos, name):
        super().__init__(pos, name)

    def attack(self, pos):
        if self.is_close(pos, diagonal=True):
            return True
        return False


if __name__ == "__main__":
    game = Warchest()
    game.play()
