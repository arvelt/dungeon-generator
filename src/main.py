# -*- coding: UTF-8 -*-
from Frame import Frame

class Dungeon:
    row_size = 32
    col_size = 32

    def __init__(self, config=None):
        self.dungeon = Frame(self.col_size, self.row_size, config)


    def __str__(self):
        return str(self.dungeon)

    def to_string(self):
        return self.dungeon.to_string()


if __name__ == '__main__':
    config = {
        'room_number' : 6
    }
    dungeon = Dungeon()
    print dungeon.to_string()
