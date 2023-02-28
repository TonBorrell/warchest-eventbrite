import random

from code.functions.read_unit import read_unit
from code.functions.read_position import read_position

from code.unit import ControlZone


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
            bag_list.extend(key for _ in range(value))
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
            if unit.name == "control" and unit.is_close(pos):
                # Set piece in board
                unit_class = self.units_dict[unit_to_place.lower()](pos, unit_to_place)
                self.units.append(unit_class)
                self.hand.remove(unit_to_place)
                self.discard_pile.append(unit_to_place)

    def control(self):
        # Unit to discard
        unit = self.read_unit_until_in_hand()
        # Position to control
        pos = read_position("Select position you want to control: ")
        controllable = False
        while not controllable:
            controllable = self.check_if_pos_controllable(pos)
            if not controllable:
                pos = read_position("Select a position occupied by you: ")
        # Control
        self.control_position(pos)
        self.control_token -= 1
        # Discard unit
        self.hand.remove(unit)
        # Check if control zone was controlled by other player
        other_player_unit = self.get_unit_by_pos(pos, other=True)
        if other_player_unit:
            if other_player_unit.name == "control":
                self.other_player.units.remove(other_player_unit)
                self.other_player.control_token += 1

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
        # Check if unit can make that attack
        can_attack = unit.attack(pos)
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
        return unit in self.hand

    def read_pos_until_correct(
        self, input_message="Select position to place: ", is_occupied=True
    ):  # is_occupied means that position reading is occupied by some unit, True --> Ocuppied
        pos_correct = False
        if is_occupied:
            while not pos_correct:
                pos = input(input_message)
                pos = pos.split(",")
                pos = (int(pos[0]), int(pos[1]))
                pos_correct = self.check_if_unit_in_pos(pos)
                if not pos_correct:
                    print("Position not occupied by any unit")
        else:
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
        return self.bag[unit] > 0

    def get_unit_by_pos(self, pos, other=False):
        units_to_check = self.other_player.units if other else self.units
        for unit in units_to_check:
            if unit.pos == pos:
                return unit

    def control_position(self, pos):
        unit_class = ControlZone(pos, "control")
        self.units.append(unit_class)
        self.control_token -= 1