# -*- coding: UTF-8 -*-
import random, math, pprint, pytest

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

    def __str__(self):
        return str({
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'heigth': self.height,
        })


class Tile(object):
    """ A tile of map in dungeon.
        All unit of member value is squares, not coordinate.
    """

    DEFAULT = 'T'
    WALL = 'W'
    WAY = 'R'
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
    rooms = ''

    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def __str__(self):
        return str([str(room) for room in self.rooms])

    def to_map(self, x, y, ax, ay):
        """ Return squares as a string filled with tiles

        arguments:
        x -- potision x
        y -- potision y
        ax -- potision lower right
        ay -- potision lower left
        """

        floor = ''
        for row in range(x, ax + 1):
            line = ''
            for col in range(y, ay + 1):
                for room in self.rooms:
                    if room.has_tile(row, col):
                        tile = room.get_tile(row, col)
                        line = line + str(tile)
                        break
                else:
                    line = line + str(0)
            floor = floor + line + '\n'
        return floor


class Room(Rect):
    """ Room in dungeon.
        Once instantiated, it is filled with Tile.
    """

    tiles = ''

    def __init__(self, x, y, width, height, tmp_kind = None):
        super(Room, self).__init__(x, y, width, height)
        self.tiles = []
        self.fill_tiles(tmp_kind)

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

    # TODO
    def __eq__(self, room):
        pass


class OuterFrame(Rect):
    """ The outer frame in dungeon.
        This class has origin potisioin. Usually (1, 1).
        This class provied pop_room method.
    """
    rooms = ''

    def __init__(self, width, height, config=None):
        """
        arguments:
        width -- Outer frame width. (Mean the size of dungeon width)
        height -- Outer frame height. (Mean the size of dungeon height)
        """
        super(OuterFrame, self).__init__(1, 1, width, height)
        self.rooms = Rooms()
        if config is not None:
            self.config = config
        else:
            self.config = self.default_config
        self.pop_rooms()

    @property
    def default_config(self):
        return {
            'room_number' : 5
        }

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
        return self.rooms.to_map(self.x, self.y, self.ax, self.ay)


class RoomSizeGenerator(Rect):
    """ Generator of room in dungeon.
    """
    def __init__(self, width, height, config):
        super(RoomSizeGenerator, self).__init__(1, 1, width, height)
        self.room_number = config.get('room_number', 1)
        self.checker = SizeDuplicateChecker()

    def get_room_sizes(self):
        """ Return Size of the room to make future.
            WIP.
        """
        room_sizes = []
        for num in range(self.room_number):
            size = self._get_new_size()
            room_sizes.append(size)
        return room_sizes

    def _get_new_size(self):
        size = self._get_other_size()
        while self.checker.prove_available_size(size) == False:
            size = self._get_other_size()
        return size

    def _get_other_size(self):
        room_number = self.room_number

        # ルーム数１は大部屋
        if room_number == 1:
            x = 2
            y = 2
            width = self.width - 2
            height = self.height - 2

        # ルーム数２は最大幅の半分まで
        elif room_number == 2:
            #
            width = random.randint(10, self.width / 2 - 1)
            height = random.randint(10, self.height / 2 - 1)
            x = random.randint(self.x + 1, self.x + self.width - width - 1)
            y = random.randint(self.y + 1, self.y + self.height - height - 1)

        # それ以上のルーム数は、切り上げた偶数の半分で最大幅を割ったもの
        # MAX 30, 部屋数5 -> 最小: 5、最大: 30 / ( 6 / 2 ) = 10
        else:
            room_number = self.room_number
            if self.room_number % 2 == 1:
                room_number = room_number + 1
            room_number = room_number / 2

            # 一番外の境界部分には作らないようにする
            max_width = self.width / room_number - 1
            max_height = self.height / room_number - 1
            width = random.randint(5, max_width)
            height = random.randint(5, max_height)
            x = random.randint(self.x + 1, self.x + self.width - width - 1)
            y = random.randint(self.y + 1, self.y + self.height - height - 1)

        return {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }


class SizeDuplicateChecker(object):
    def __init__(self, test_list=None):
        if test_list is None:
            self.sizes = []
        else:
            self.sizes = test_list

    def prove_available_size(self, size):
        # 隣接しないようにサイズを2枠分大きいものとして判定する
        # 部屋同士は最低でも3マスあく
        x = size.get('x') - 1
        y = size.get('y') - 1
        width = size.get('width') + 3
        height = size.get('height') + 3

        if self._is_contain(x, y, width, height):
            return False
        else:
            self.sizes.append({
                'x': x,
                'y': y,
                'width': width,
                'height': height
            })
            return True

    def _is_contain(self, x, y, width, height):
        ax = x
        ay = y
        bx = x + width - 1
        by = y + height - 1

        for size in self.sizes:
            cx = size.get('x')
            cy = size.get('y')
            dx = size.get('width') + cx - 1
            dy = size.get('height') + cy - 1

            if ax <= dx and cx <= bx and ay <= dy and cy <= by:
                return True
                break
        else:
            return False


class RoomSearcher:
    """WIP"""

    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'DOWN'
    UPPER_RIGHT = 'upper_right'
    LOWER_RIGHT = 'lower_right'
    UPPER_LEFT = 'upper_left'
    LOWER_LEFT = 'lower_left'

    def __init__(self):
        self.nearest_room = {}

    def conruct_rooms_placement(self, rooms):
        self.copy_rooms = copy.deepcopy(rooms)
        for room in rooms:
            self.analyze(room)

    def get_nearest_room(self, potision):
        return self.nearest_room.get(potision, None)

    def analyze(self, room):
        target_room = room
        comparison_destinations = []
        for room in self.copy_rooms:
            if room != target_room:
                comparison_destinations.append(room)
        self.search_nearest_room(target_room, comparison_destinations)

    def search_nearest_room(self, room, destinations):
        # TODO WIP
        pass



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
