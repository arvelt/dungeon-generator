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
        self.walls = []

        self.has_road = False
        """ Whther the at least one of the road, or not."""

        self.north_road_id = None
        """ The road id on north side. If not exist, None."""

        self.south_road_id = None
        """ The road id on south side. If not exist, None."""

        self.east_road_id = None
        """ The road id on east side. If not exist, None."""

        self.west_road_id = None
        """ The road id on west side. If not exist, None."""

        self._fill_tiles(tmp_kind)
        self._make_door()
        self._wrap_walls()

    def _fill_tiles(self, tmp_kind):
        for col in range(self.x, self.ax + 1):
            for row in range(self.y, self.ay + 1):
                self.tiles.append(Tile(col , row, tmp_kind))

    def _wrap_walls(self):
        # ４隅が重複するが問題ないので気にしなくて良い

        # 上辺
        start = self.x - 1
        end = self.ax + 1
        row = self.y - 1
        for col in range(start, end + 1):
            self.walls.append(Tile(col , row, Tile.WALL))

        # 下辺
        start = self.x - 1
        end = self.ax + 1
        row = self.ay + 1
        for col in range(start, end + 1):
            self.walls.append(Tile(col , row, Tile.WALL))

        # 左辺
        west_door = self.get_west_door()
        start = self.y - 1
        end = self.ay + 1
        col = self.x - 1
        for row in range(start, end + 1):
            self.walls.append(Tile(col , row, Tile.WALL))

        # 右辺
        east_door = self.get_east_door()
        start = self.y - 1
        end = self.ay + 1
        col = self.ax + 1
        for row in range(start, end + 1):
            self.walls.append(Tile(col , row, Tile.WALL))

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
        if (self.x - 1 <= x and x <= self.ax + 1) and \
            (self.y - 1  <= y and y <= self.ay + 1):
            return True
        else:
            return False

    def get_door(self, x, y):
        """ Get a door from Room.

        :param x: potision x.
        :param y: potision y.
        :rtype: Door class.
        :return: Return door. if it does not exist, return None.
        """
        for door in self.doors:
            if door.x == x and door.y == y:
                return door
        else:
            return None

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

    def get_wall(self, x, y):
        """ Get a wall from Room.

        :param x: potision x.
        :param y: potision y.
        :rtype: Tile class.
        :return: Return tile. if it does not exist, return None.
        """
        for wall in self.walls:
            if wall.x == x and wall.y == y:
                return wall
        else:
            return None

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
        """ Get a door on the north side.

        :rtype: Door
        :return: Return Door.
        """
        for door in self.doors:
            if door.y == self.y:
                return door

    def get_south_door(self):
        """ Get a door on the south side.

        :rtype: Door
        :return: Return Door.
        """
        for door in self.doors:
            if door.y == self.ay:
                return door

    def get_east_door(self):
        """ Get a door on the east side.

        :rtype: Door
        :return: Return Door.
        """
        for door in self.doors:
            if door.x == self.ax:
                return door

    def get_west_door(self):
        """ Get a door on the west side.

        :rtype: Door
        :return: Return Door.
        """
        for door in self.doors:
            if door.x == self.x:
                return door
