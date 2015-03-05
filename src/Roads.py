# -*- coding: UTF-8 -*-

class Roads(object):
    """ Collections of Road.
    """
    def __init__(self):
        self.roads = []

    def add(self, tile):
        """Add a road to collection.

        :param tile: tile class.
        """
        self.roads.append(tile)

    def get(self, x, y):
        """Get a road from collection.

        :param x: potision x.
        :param y: potision y.
        :rtype: tile or None
        :return: Return tile. if it does not exist, return None.
        """
        for tile in self.roads:
            if tile.x == x and tile.y == y:
                return tile
        else:
            return None

    def get_all(self):
        """Get all roads from collection.

        :rtype: List
        :return: List of Tile.
        """
        return copy.deepcopy(self.roads)

    def __str__(self):
        return str([str(road) for road in self.roads])
