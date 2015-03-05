# -*- coding: UTF-8 -*-
from operator import attrgetter
from Rect import Rect
from Tile import Tile
from Room import Room
from Rooms import Rooms
from Roads import Roads
from RoomSearcher import RoomSearcher
from RoomSizeGenerator import RoomSizeGenerator
from Frame import Frame
import math, pprint, pytest

class Dungeon:
    row_size = 32
    col_size = 32

    def __init__(self, config=None):
        self.dungeon = Frame(self.col_size, self.row_size, config)


    def __str__(self):
        return str(self.dungeon)

    def to_map(self):
        return self.dungeon.to_map()


if __name__ == '__main__':
    config = {
        'room_number' : 6
    }
    dungeon = Dungeon()
    print dungeon.to_map()
