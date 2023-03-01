class Unit:
    def __init__(self, pos, name) -> None:
        self.pos = pos
        self.name = name

    def is_close(self, pos2, max_dif=1, diagonal=False):
        """
        The aim of this function is to check if a position is close to another.
        Max_dif is the maximum distance to consider close, and diagonal is a boolean to check for diagonals
        """
        pos2 = (int(pos2[0]), int(pos2[1]))
        for i in range(1, max_dif + 1):
            if (self.pos[0] + i == pos2[0] or self.pos[0] - i == pos2[0]) and self.pos[
                1
            ] == pos2[1]:
                return True
            if (self.pos[1] + i == pos2[1] or self.pos[1] - i == pos2[1]) and self.pos[
                0
            ] == pos2[0]:
                return True
            if diagonal:
                if (self.pos[0] + i == pos2[0] or self.pos[0] - i == pos2[0]) and (
                    self.pos[1] + i == pos2[1] or self.pos[1] - i == pos2[1]
                ):
                    return True
        return False

    def set_pos(self, pos):
        self.pos = pos


class Royal(Unit):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)


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
