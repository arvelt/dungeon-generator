# -*- coding: UTF-8 -*-
from Frame import Frame

class Dungeon:
    def __init__(self, config={}):
        self.row_size = config.get('col_size', 20)
        self.col_size = config.get('row_size', 20)
        self.dungeon = Frame(self.col_size, self.row_size, config)


    def __str__(self):
        return str(self.dungeon)

    def to_string(self):
        return self.dungeon.to_string()


if __name__ == '__main__':
    config = {
        'row_size': 32,
        'col_size': 32,
        'room_number' : 6
    }
    dungeon = Dungeon(config=config)
    print dungeon.to_string()
