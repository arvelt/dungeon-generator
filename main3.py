# -*- coding: UTF-8 -*-
import random, math, pprint, pytest

class ROOPEND(Exception):
    pass


class Rect(object):
    def __init__(self, x, y, width, height):
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
    DEFAULT = 0
    WALL = 2
    WAY = 5
    PARTING_LINE = 1

    def __init__(self, x, y, kind = None):
        self.x = x
        self.y = y
        if kind is None:
            self.kind = self.DEFAULT
        else:
            self.kind = kind

    def __str__(self):
        return str(self.kind)


class Frames(object):
    frames = ''

    def __init__(self):
        self.frames = []

    def add_frame(self, frame):
        self.frames.append(frame)

    def __str__(self):
        return str([str(frame) for frame in self.frames])

    def to_map(self, x, y, ax, ay):
        floor = ''
        for row in range(x, ax + 1):
            line = ''
            for col in range(y, ay + 1):
                for frame in self.frames:
                    if frame.has_coordinate(row, col):
                        tile = frame.get_tile(row, col)
                        line = line + str(tile)
                        break
            floor = floor + line + '\n'
        return floor


class Frame(Rect):
    tiles = ''

    def __init__(self, x, y, width, height, tmp_kind = None):
        super(Frame, self).__init__(x, y, width, height)
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

    def has_coordinate(self, x, y):
        if (self.x <= x and x <= self.x + self.width - 1) and \
            (self.y <= y and y <= self.y + self.height - 1):
            return True
        else:
            return False


class OuterFrame(Rect):
    frames = ''

    def __init__(self, width, height, config=None):
        super(OuterFrame, self).__init__(1, 1, width, height)
        self.frames = Frames()
        if config is not None:
            self.config = config
        else:
            self.config = self.default_config
        self.split_frames()

    @property
    def default_config(self):
        return {
            'room_number' : 4
        }

    def split_frames(self):
        frame_spliter = FrameSpliter(self.width, self.height, self.config)
        sizes = frame_spliter.get_frame_size()

        for index, size in enumerate(sizes):
            frame = Frame(size.get('x'), size.get('y'), size.get('width'), size.get('height'), index)
            self.frames.add_frame(frame)

    def __str__(self):
        return str(self.frames)

    def to_map(self):
        return self.frames.to_map(self.x, self.y, self.ax, self.ay)

class FrameSpliter(Rect):
    def __init__(self, width, height, config):
        super(FrameSpliter, self).__init__(1, 1, width, height)
        self.room_number = config.get('room_number', 4)

    def four_frame(self):
        room_number = self.room_number
        row_split = room_number / 2
        col_split = room_number / 2

        row_adding = self.width / row_split
        col_adding = self.height / row_split

        room_sizes = []
        room_sizes.append({
            'x': self.x,
            'y': self.y,
            'width': row_adding,
            'height': col_adding
        })

        room_sizes.append({
            'x': self.x + row_adding,
            'y': self.y,
            'width': row_adding,
            'height': col_adding
        })

        room_sizes.append({
            'x': self.x,
            'y': self.y + col_adding,
            'width': row_adding,
            'height': col_adding
        })

        room_sizes.append({
            'x': self.x + row_adding,
            'y': self.y + col_adding,
            'width': row_adding,
            'height': col_adding
        })

        return room_sizes

    def get_frame_size(self):
        if self.room_number == 4:
            return self.four_frame()



class Rooms(object):
    rooms = []

    def add_romms(room):
        self.append(room)


class Room(Frame):
    pass


class Dungeon:
    row_size = 10
    col_size = 10

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
