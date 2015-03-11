# -*- coding: UTF-8 -*-
from Tile import Tile

class Door(Tile):
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'
    def __init__(self, x, y, direction):
        super(Door, self).__init__(x, y, kind = Tile.DOOR)
        self.direction = direction

    def is_vertical(self):
        return self.direction == self.NORTH or self.direction == self.SOUTH

    def is_horizontal(self):
        return self.direction == self.EAST or self.direction == self.WEST
