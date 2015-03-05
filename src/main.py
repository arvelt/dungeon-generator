# -*- coding: UTF-8 -*-
from operator import attrgetter
from Rect import Rect
from RoomSearcher import RoomSearcher
from RoomSizeGenerator import RoomSizeGenerator
import math, pprint, pytest, uuid, copy, random

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
        col_way = []
        col_roads = []
        row_way = []
        row_roads = []
        pair_list = searcher.get_road_pair()
        for pair in pair_list:
            from_id = pair.get('from')
            to_id = pair.get('to')

            if pair.get('direction') == 'north':
                door1 = self.rooms.get_room(from_id).get_north_door()
                door2 = self.rooms.get_room(to_id).get_south_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                for way in col_way:
                    if way == distance:
                        break
                else:
                    col_way.append(distance)
                    col_roads.append((door1, door2))

            if pair.get('direction') == 'south':
                door1 = self.rooms.get_room(from_id).get_south_door()
                door2 = self.rooms.get_room(to_id).get_north_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                for way in col_way:
                    if way == distance:
                        break
                else:
                    col_way.append(distance)
                    col_roads.append((door1, door2))

            if pair.get('direction') == 'east':
                door1 = self.rooms.get_room(from_id).get_east_door()
                door2 = self.rooms.get_room(to_id).get_west_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                for way in row_way:
                    if way == distance:
                        break
                else:
                    row_way.append(distance)
                row_roads.append((door1, door2))

            if pair.get('direction') == 'west':
                door1 = self.rooms.get_room(from_id).get_west_door()
                door2 = self.rooms.get_room(to_id).get_east_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                for way in row_way:
                    if way == distance:
                        break
                else:
                    row_way.append(distance)
                    row_roads.append((door1, door2))

        door_pair = {
            'col_doors': col_roads,
            'row_doors': row_roads
        }

        self.generator_road(door_pair)

        # for room in self.rooms.get_rooms():
        #     for target in nearest_rooms:
        #         if room.id == target.get('id'):
        #             self.generator_road(room, target)

    def generator_road(self, door_pair):
        col_doors = door_pair.get('col_doors')
        row_doors = door_pair.get('row_doors')

        for doors in col_doors:
            door1 = doors[0]
            door2 = doors[1]
            if door1.y < door2.y:
                self.pave_col_road(door1, door2)
            else:
                self.pave_col_road(door2, door1)
        for doors in row_doors:
            door1 = doors[0]
            door2 = doors[1]
            if door1.x < door2.x:
                self.pave_row_road(door1, door2)
            else:
                self.pave_row_road(door2, door1)

    def pave_col_road(self, up_door, down_door):
        ax = up_door.x
        ay = up_door.y + 1
        next1 = Tile(ax, ay, Tile.WAY)
        self.roads.add_road(next1)

        if ay == down_door.y:
            if ax < down_door.x:
                start = ax
                end = down_door.x
            else:
                start = down_door.x
                end = ax
            for x in range(start, end):
                road = Tile(x, ay, Tile.WAY)
                self.roads.add_road(road)
            return

        bx = down_door.x
        by = down_door.y - 1
        next2 = Tile(bx, by, Tile.WAY)
        self.roads.add_road(next2)

        if ay == by:
            if ax < bx:
                start = ax
                end = bx
            else:
                start = bx
                end = ax
            for x in range(start, end):
                road = Tile(x, ay, Tile.WAY)
                self.roads.add_road(road)
        else:
            self.pave_col_road(next1, next2)


    def pave_row_road(self, left_door, right_door):
        ax = left_door.x + 1
        ay = left_door.y
        next1 = Tile(ax, ay, Tile.WAY)
        self.roads.add_road(next1)

        if ax == right_door.x:
            if ay < right_door.y:
                start = ay
                end = right_door.y
            else:
                start = right_door.y
                end = ay
            for y in range(start, end):
                road = Tile(ax, y, Tile.WAY)
                self.roads.add_road(road)
            return

        bx = right_door.x - 1
        by = right_door.y
        next2 = Tile(bx, by, Tile.WAY)
        self.roads.add_road(next2)

        if ax == bx:
            if ay < by:
                start = ay
                end = by
            else:
                start = by
                end = ay
            for y in range(start, end):
                road = Tile(ax, y, Tile.WAY)
                self.roads.add_road(road)
        else:
            self.pave_row_road(next1, next2)

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
                    if room.has_tile(col, row):
                        tile = room.get_tile(col, row)
                        break

                if tile is None:
                    tile = self.roads.get_road(col, row)

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
        self.dungeon = OuterFrame(self.col_size, self.row_size, config)


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
