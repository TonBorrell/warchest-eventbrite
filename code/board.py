class Board:
    def __init__(self, name_player_1='Crow', name_player_2='Wolf') -> None:
        self.name_player_1 = name_player_1
        self.name_player_2 = name_player_2
        self.board = ["." * 5] * 5
        self.control_areas = [(2, 0), (2, 4), (0, 1), (1, 3), (3, 1), (4, 3)]
        self.pieces = {}  # All unit class

    def show_board(self):
        for i in range(5):
            for j in range(5):
                print(self.is_pos_active((j, i)), end=" ")
            print()

    def is_pos_active(self, pos):
        for keys, units_list in self.pieces.items():
            for unit in units_list:
                if unit.pos == pos:
                    if unit.name == 'control':
                        return keys[0].upper()
                    return unit.name[0].upper()
        return "@" if pos in self.control_areas else "."
