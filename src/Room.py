# -*- coding: UTF-8 -*-
from Rect import Rect
from Tile import Tile
from Door import Door
import uuid, random

class Room(Rect):
    """ Room in dungeon.
        Once instantiated, it is filled with Tile.
    """
    def __init__(self, x, y, width, height, tmp_kind = None):
        super(Room, self).__init__(x, y, width, height)
        self.id = str(uuid.uuid4())
        self.tiles = []
        self.doors = []
        self._fill_tiles(tmp_kind)
        self._make_door()

    def _fill_tiles(self, tmp_kind):
        for col in range(self.x, self.ax + 1):
            for row in range(self.y, self.ay + 1):
                self.tiles.append(Tile(col , row, tmp_kind))


    def get_tile(self, x, y):
        """ Get a tile from Room.

        :param x: potision x.
        :param y: potision y.
        :rtype: Tile class.
        :return: Return tile. if it does not exist, return None.
        """
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        else:
            return None

    def set_tile(self, x, y, new_tile):
        """ Set a tile to Room.

        :param x: potision x.
        :param y: potision y.
        :param new_tile: new Tile
        """
        for index, tile in enumerate(self.tiles):
            if tile.x == x and tile.y == y:
                self.tiles[index] = new_tile

    def has_tile(self, x, y):
        """ Whether holds the tile.

        :param x: potision x.
        :param y: potision y.
        :rtype: Booean
        :return: Return True, if holds the tile. Otherwise Fasle.
        """
        if (self.x <= x and x <= self.x + self.width - 1) and \
            (self.y <= y and y <= self.y + self.height - 1):
            return True
        else:
            return False

    def has_door(self, door):
        """ Whether holds the door.

        :param x: potision x.
        :param y: potision y.
        :rtype: Booean
        :return: Return True, if holds the tile. Otherwise Fasle.
        """
        if door.kind != Tile.DOOR:
            return False
        for room_door in self.doors:
            if room_door.x == door.x and room_door.y == door.y:
                return True
        else:
            return False

    def _make_door(self):
        #上辺
        dx = random.randint(self.x + 1, self.ax - 1)
        dy = self.y
        door = Door(dx, dy, Door.NORTH)
        self.set_tile(dx, dy, door)
        self.doors.append(door)

        #下辺
        dx = random.randint(self.x + 1, self.ax - 1)
        dy = self.ay
        door = Door(dx, dy, Door.SOUTH)
        self.set_tile(dx, dy, door)
        self.doors.append(door)

        #右辺
        dx = self.ax
        dy = random.randint(self.y + 1, self.ay - 1)
        door = Door(dx, dy, Door.EAST)
        self.set_tile(dx, dy, door)
        self.doors.append(door)

        #左辺
        dx = self.x
        dy = random.randint(self.y + 1, self.ay - 1)
        door = Door(dx, dy, Door.WEST)
        self.set_tile(dx, dy, door)
        self.doors.append(door)

    def get_north_door(self):
        for door in self.doors:
            if door.y == self.y:
                return door

    def get_south_door(self):
        for door in self.doors:
            if door.y == self.ay:
                return door

    def get_east_door(self):
        for door in self.doors:
            if door.x == self.ax:
                return door

    def get_west_door(self):
        for door in self.doors:
            if door.x == self.x:
                return door
