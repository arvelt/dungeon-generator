# -*- coding: UTF-8 -*-

class Tile(object):
    """ A tile of map in dungeon.
        All unit of member value is squares, not coordinate.
    """

    DEFAULT = 'T'
    WALL = 'W'
    WAY = 'L'
    DOOR = 'D'
    PARTING_LINE = 'A'


    def __init__(self, x, y, kind = None):
        """
        arguments:
        x -- potision x
        y -- potision y
        kind -- kind of map (Default is 'T')
        """
        self.x = x
        self.y = y
        if kind is None:
            self.kind = self.DEFAULT
        else:
            self.kind = kind

    def __str__(self):
        return str(self.kind)
