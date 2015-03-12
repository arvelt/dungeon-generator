# -*- coding: UTF-8 -*-
from Tile import Tile

class Door(Tile):
    """ A door in Room.
        Door know the direction of way.
    """
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'
    def __init__(self, x, y, direction):
        super(Door, self).__init__(x, y, kind = Tile.DOOR)
        self.direction = direction

    def is_vertical(self):
        """ Whether the direction of the road or vertical direction.

        :rtype: Boolean
        :return: Return True, the direction is north or south. Otherwise False.
        """
        return self.direction == self.NORTH or self.direction == self.SOUTH

    def is_horizontal(self):
        """ Whether the direction of the road or horizontal direction.

        :rtype: Boolean
        :return: Return True, the direction is east or west. Otherwise False.
        """
        return self.direction == self.EAST or self.direction == self.WEST
