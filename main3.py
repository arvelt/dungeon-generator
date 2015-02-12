# -*- coding: UTF-8 -*-
import random, math, pprint

class ROOPEND(Exception):
    pass


class Tile:
    TILE = 0
    WALL = 2
    WAY = 5
    PARTING_LINE = 1

    kind = TILE
    x = 0
    y = 0
    max_row = 0
    max_col = 0

    def __init__(self, x, y, max_row, max_col):
        self.x = x
        self.y = y
        self.max_row = max_row
        self.max_col = max_col


class Rooms():
    rooms = []

    def add_room(room):
        self.append(room)


class Room():
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, ax, ay, bx, by):
        self.x = ax
        self.y = ay
        self.width = bx - ax
        self.height = by - ay

    def to_string(self):
        print {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'heigth': self.height,
        }

class Islands():
    islands = []

    def add_island(island):
        self.append(island)


class Island(Room):
    pass


class Dungeon:
    max_row = 32
    max_col = 32
    min_size = 10
    dungeon = [[Tile(row, col, max_row, max_col) for col in xrange(max_col)] for row in xrange(max_row)]
    rooms = 0

    def __init__(self):
        self.rooms = Room(0, 0, self.max_row, self.max_col)
        self.rooms.to_string()


    def to_string(self):
        for row in self.dungeon:
            print ''.join([str(col.kind) for col in row])




dungeon = Dungeon()
dungeon.to_string()
