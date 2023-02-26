import random

class Warchest:
    def __init__(self) -> None:
        self.board = Board()
        self.crow = Player([('C', (4, 2))], {Archer: 3, Berseker: 3})
        self.wolf = Player([('W', (0, 2))], {Cavalry: 3, Knight: 3})
        self.current_player = self.decide_first_player()
    
    def decide_first_player(self):
        self.current_player = random.choice((self.crow, self.wolf))

    def play(self):
        while not self.is_ended():
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
        #TODO: Check if game has finished
        pass

class Board:
    def __init__(self) -> None:
        self.board = ['.'*5]*5
        self.pieces = []

class Player:
    def __init__(self, units, bag) -> None:
        self.units = units # Inside this list --> tuple (Type of unit, Position of unit)
        self.bag = {} # Unit: n_units
        self.bag = bag
        self.hand = []
        self.discard_pile = []
        self.control_token = 3

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
        movement = input('Place/Control/Move/Recruit/Attack/Initiative')
        movement = movement.lower()
        if movement == 'place':
            self.place()
        if movement == 'control':
            self.control()
        if movement == 'move':
            self.move()
        if movement == 'recruit':
            self.recruit()
        if movement == 'attack':
            self.attack()
        if movement == 'initiative':
            self.initiative()
        # Check if posible
        # Do movement

    def place(self):
        pass

    def control(self):
        pass

    def move(self):
        pass

    def recruit(self):
        pass

    def attack(self):
        pass

    def initiative(self):
        pass

    def check_if_unit_in_hand(self, unit):
        pass

    def check_if_unit_in_control_zone(self, unit):
        pass

    def check_if_unit_in_bag(self, unit):
        pass

class Unit:
    def __init__(self, pos) -> None:
        pos = self.pos

class Archer(Unit):
    def __init__(self, pos):
        super().__init__(pos)

class Berseker(Unit):
    def __init__(self, pos):
        super().__init__(pos)

class Cavalry(Unit):
    def __init__(self, pos):
        super().__init__(pos)

class Knight(Unit):
    def __init__(self, pos):
        super().__init__(pos)


if __name__ == '__main__':
    board = Board()
    board.print_board()