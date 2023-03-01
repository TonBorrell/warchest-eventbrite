class Board:
    def __init__(self) -> None:
        self.board = ["." * 5] * 5
        self.control_areas = [(2, 0), (2, 4), (0, 1), (1, 3), (3, 1), (4, 3)]
        self.pieces = {}  # All unit class

    def show_board(self):
        list_rows = ['A', 'B', 'C', 'D', 'E']
        print('    0 1 2 3 4')
        print('    ---------')
        for i in range(5):
            print(list_rows[i], end=' | ')
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
