# -*- coding: UTF-8 -*-
from operator import attrgetter
from RoomSearcher import RoomSearcher
from RoomSizeGenerator import RoomSizeGenerator
import math, pprint, pytest, uuid, copy, random

class Rect(object):
    """ Shape of map base.
        All unit of member value is squares, not coordinate.
    """

    def __init__(self, x, y, width, height):
        """
        arguments:
        x -- potision x
        y -- potision y
        width -- shape width
        height -- shape height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.ax = x + width -1
        self.ay = y + height -1
        self.mx = (self.x + self.ax) / 2
        self.my = (self.y + self.ay) / 2

    def __str__(self):
        return str({
            'x': self.x,
            'y': self.y,
            'ax': self.ax,
            'ay': self.ay,
            'mx': self.mx,
            'my': self.my,
            'width': self.width,
            'heigth': self.height,
        })


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


class Rooms(object):
    """ Collection of room.
    """
    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def get_room(self, id):
        for room in self.rooms:
            if room.id == id:
                return room

    def get_rooms(self):
        return copy.deepcopy(self.rooms)

    def __str__(self):
        return str([str(room) for room in self.rooms])


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
        for row in range(self.x, self.ax + 1):
            for col in range(self.y, self.ay + 1):
                self.tiles.append(Tile(row , col, tmp_kind))

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

    # TODO
    def __eq__(self, room):
        pass


class OuterFrame(Rect):
    """ The outer frame in dungeon.
        This class has origin potisioin. Usually (1, 1).
        This class provied pop_room method.
    """
    def __init__(self, width, height, config=None):
        """
        arguments:
        width -- Outer frame width. (Mean the size of dungeon width)
        height -- Outer frame height. (Mean the size of dungeon height)
        """
        super(OuterFrame, self).__init__(1, 1, width, height)
        self.rooms = Rooms()
        self.roads = Roads()
        if config is not None:
            self.config = config
        else:
            self.config = self.default_config
        self.pop_rooms()
        self.make_roads()

    @property
    def default_config(self):
        return {
            'room_number' : 5
        }

    def make_roads(self):
        searcher = RoomSearcher()
        searcher.analyze_rooms(self.rooms.get_rooms())
        nearest_rooms = searcher.get_room_direction()

        # TODO これをうまくやる
        print searcher.get_road_pair()

        for room in self.rooms.get_rooms():
            for target in nearest_rooms:
                if room.id == target.get('id'):
                    self.generator_road(room, target)

    def generator_road(self, room, target_size):
        if target_size.get(RoomSearcher.NORTH):
            door = room.get_north_door()
            x = door.x
            y = door.y - 1
            road = Tile(x, y, Tile.WAY)
            self.roads.add_road(road)

        if target_size.get(RoomSearcher.SOUTH):
            door = room.get_south_door()
            x = door.x
            y = door.y + 1
            road = Tile(x, y, Tile.WAY)
            self.roads.add_road(road)

        if target_size.get(RoomSearcher.EAST):
            door = room.get_east_door()
            x = door.x + 1
            y = door.y
            road = Tile(x, y, Tile.WAY)
            self.roads.add_road(road)

        if target_size.get(RoomSearcher.WEST):
            door = room.get_west_door()
            x = door.x - 1
            y = door.y
            road = Tile(x, y, Tile.WAY)
            self.roads.add_road(road)

    def pop_rooms(self):
        """ Pop rooms in dungeons.
            See RoomSizeGenerator details.
        """
        room_generator = RoomSizeGenerator(self.width, self.height, self.config)
        sizes = room_generator.get_room_sizes()
        for index, size in enumerate(sizes):
            room = Room(size.get('x'), size.get('y'), size.get('width'), size.get('height'))
            self.rooms.add_room(room)

    def __str__(self):
        return str(self.rooms)

    def to_map(self):
        x = self.x
        y = self.y
        ax = self.ax
        ay = self.ay

        floor = ''
        for row in range(x, ax + 1):
            line = ''
            for col in range(y, ay + 1):
                tile = None
                for room in self.rooms.get_rooms():
                    if room.has_tile(row, col):
                        tile = room.get_tile(row, col)
                        break

                if tile is None:
                    tile = self.roads.get_road(row, col)

                if tile:
                    line = line + str(tile)
                else:
                    line = line + str(0)
            floor = floor + line + '\n'
        return floor

class Border:
    """WIP"""
    x = 0
    y = 0
    def __init__(self):
        pass

class BorderLine:
    """WIP"""
    line = ''
    def __init__(self):
        line = []


class Dungeon:
    row_size = 32
    col_size = 32

    def __init__(self, config=None):
        self.dungeon = OuterFrame(self.row_size, self.col_size, config)


    def __str__(self):
        return str(self.dungeon)

    def to_map(self):
        return self.dungeon.to_map()


if __name__ == '__main__':
    config = {
        'room_number' : 6
    }
    dungeon = Dungeon()
    print dungeon.to_map()
