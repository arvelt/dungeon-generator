# -*- coding: UTF-8 -*-

class Roads(object):
    """ Collections of Road.
    """
    def __init__(self):
        self.roads = []

    def add(self, road):
        """Add a road to collection.

        :param tile: tile class.
        """
        self.roads.append(road)

    def get(self, id):
        """Get a road from collection.

        :param id: unique key of the road.
        :rtype: Road class
        :return: Return road. if it does not exist, return None.
        """
        for road in self.roads:
            if road.id == id:
                return road
        else:
            return None

    def get_all(self):
        """Get all roads from collection.

        :rtype: List
        :return: List of Tile.
        """
        return self.roads

    def get_copy_all(self):
        """ Get all copy of roads from collection.
            When performing a destructive operation , use this.

        :rtype: List
        :return: List of Tile.
        """
        return copy.deepcopy(self.roads)

    def __str__(self):
        return str([str(road) for road in self.roads])
