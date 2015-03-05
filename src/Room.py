# -*- coding: UTF-8 -*-
from Rect import Rect
from Tile import Tile
import uuid, random

class Room(Rect):
    """ Room in dungeon.
        Once instantiated, it is filled with Tile.
    """

    tiles = ''

    def __init__(self, x, y, width, height, tmp_kind = None):
        super(Room, self).__init__(x, y, width, height)
        self.id = str(uuid.uuid4())
        self.tiles = []
        self.doors = []
        self.fill_tiles(tmp_kind)
        self.make_door()

    def fill_tiles(self, tmp_kind):
        for col in range(self.x, self.ax + 1):
            for row in range(self.y, self.ay + 1):
                self.tiles.append(Tile(col , row, tmp_kind))

    def get_tile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        else:
            return None

    def has_tile(self, x, y):
        if (self.x <= x and x <= self.x + self.width - 1) and \
            (self.y <= y and y <= self.y + self.height - 1):
            return True
        else:
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }

    def make_door(self):
        #上辺
        dx = random.randint(self.x + 1, self.ax - 1)
        dy = self.y
        tile = self.get_tile(dx, dy)
        tile.kind = Tile.DOOR
        self.doors.append(tile)

        #下辺
        dx = random.randint(self.x + 1, self.ax - 1)
        dy = self.ay
        tile = self.get_tile(dx, dy)
        tile.kind = Tile.DOOR
        self.doors.append(tile)

        #右辺
        dx = self.ax
        dy = random.randint(self.y + 1, self.ay - 1)
        tile = self.get_tile(dx, dy)
        tile.kind = Tile.DOOR
        self.doors.append(tile)

        #左辺
        dx = self.x
        dy = random.randint(self.y + 1, self.ay - 1)
        tile = self.get_tile(dx, dy)
        tile.kind = Tile.DOOR
        self.doors.append(tile)

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
