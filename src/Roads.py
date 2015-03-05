# -*- coding: UTF-8 -*-

class Roads(object):
    def __init__(self):
        self.roads = []

    def add_road(self, tile):
        self.roads.append(tile)

    def get_road(self, x, y):
        for tile in self.roads:
            if tile.x == x and tile.y == y:
                return tile
        else:
            return None

    def get_roads(self):
        return copy.deepcopy(self.roads)

    def __str__(self):
        return str([str(road) for road in self.roads])
