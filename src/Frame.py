# -*- coding: UTF-8 -*-
from Rect import Rect
from Tile import Tile
from Room import Room
from Rooms import Rooms
from Roads import Roads
from RoomSearcher import RoomSearcher
from RoomSizeGenerator import RoomSizeGenerator
import pprint

class Frame(Rect):
    """ The display frame shape.
        Upper left is the origin.
        The origin starts (1, 1).
    """
    def __init__(self, width, height, config):
        """
        arguments:
        width -- Outer frame width. (Mean the size of dungeon width)
        height -- Outer frame height. (Mean the size of dungeon height)
        """
        super(Frame, self).__init__(1, 1, width, height)
        self.config = config
        self.rooms = Rooms()
        self._pop_rooms()
        self.roads = Roads()
        self._pop_roads()
        self._make_map()

    def _pop_roads(self):
        searcher = RoomSearcher()
        pair_list = searcher.analyze_rooms(self.rooms.get_all())
        door_pair = self._transform_door_pair(pair_list)
        self._generator_road(door_pair)

    def _transform_door_pair(self, pair_list):
        col_way = []
        col_roads = []
        row_way = []
        row_roads = []
        for pair in pair_list:
            from_id = pair.get('from')
            to_id = pair.get('to')

            if pair.get('direction') == 'north':
                door1 = self.rooms.get(from_id).get_north_door()
                door2 = self.rooms.get(to_id).get_south_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in col_way:
                    if way == distance:
                        break
                else:
                    col_way.append(distance)
                    col_roads.append((door1, door2))

            if pair.get('direction') == 'south':
                door1 = self.rooms.get(from_id).get_south_door()
                door2 = self.rooms.get(to_id).get_north_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in col_way:
                    if way == distance:
                        break
                else:
                    col_way.append(distance)
                    col_roads.append((door1, door2))

            if pair.get('direction') == 'east':
                door1 = self.rooms.get(from_id).get_east_door()
                door2 = self.rooms.get(to_id).get_west_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in row_way:
                    if way == distance:
                        break
                else:
                    row_way.append(distance)
                row_roads.append((door1, door2))

            if pair.get('direction') == 'west':
                door1 = self.rooms.get(from_id).get_west_door()
                door2 = self.rooms.get(to_id).get_east_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in row_way:
                    if way == distance:
                        break
                else:
                    row_way.append(distance)
                    row_roads.append((door1, door2))

        return {
            'col_doors': col_roads,
            'row_doors': row_roads
        }

    def _generator_road(self, door_pair):
        col_doors = door_pair.get('col_doors')
        row_doors = door_pair.get('row_doors')

        for doors in col_doors:
            door1 = doors[0]
            door2 = doors[1]
            if door1.y < door2.y:
                self._pave_col_road(door1, door2)
            else:
                self._pave_col_road(door2, door1)
        for doors in row_doors:
            door1 = doors[0]
            door2 = doors[1]
            if door1.x < door2.x:
                self._pave_row_road(door1, door2)
            else:
                self._pave_row_road(door2, door1)

    def _pave_col_road(self, north_door, south_door):
        """ Make raods from door to door.
            The direction of the north-south.
        """
        ax = north_door.x
        ay = north_door.y + 1
        next1 = Tile(ax, ay, Tile.WAY)
        self.roads.add(next1)

        # 同じY位置まできたらX側を埋める
        if ay == south_door.y:
            if ax < south_door.x:
                start = ax
                end = south_door.x
            else:
                start = south_door.x
                end = ax
            for x in range(start, end):
                road = Tile(x, ay, Tile.WAY)
                self.roads.add(road)
            return

        bx = south_door.x
        by = south_door.y - 1
        next2 = Tile(bx, by, Tile.WAY)
        self.roads.add(next2)

        # 同じY位置まできたらX側を埋める
        if ay == by:
            if ax < bx:
                start = ax
                end = bx
            else:
                start = bx
                end = ax
            for x in range(start, end):
                road = Tile(x, ay, Tile.WAY)
                self.roads.add(road)

        # 道が埋まるまで再帰的に繰り返す
        else:
            self._pave_col_road(next1, next2)


    def _pave_row_road(self, west_door, east_door):
        """ Make raods from door to door.
            The direction of the door east-west.
        """
        ax = west_door.x + 1
        ay = west_door.y
        next1 = Tile(ax, ay, Tile.WAY)
        self.roads.add(next1)

        # 同じX位置にきたらY側を埋める
        if ax == east_door.x:
            if ay < east_door.y:
                start = ay
                end = east_door.y
            else:
                start = east_door.y
                end = ay
            for y in range(start, end):
                road = Tile(ax, y, Tile.WAY)
                self.roads.add(road)
            return

        bx = east_door.x - 1
        by = east_door.y
        next2 = Tile(bx, by, Tile.WAY)
        self.roads.add(next2)

        # 同じX位置にきたらY側を埋める
        if ax == bx:
            if ay < by:
                start = ay
                end = by
            else:
                start = by
                end = ay
            for y in range(start, end):
                road = Tile(ax, y, Tile.WAY)
                self.roads.add(road)

        # 道が埋まるまで再帰的に繰り返す
        else:
            self._pave_row_road(next1, next2)

    def _pop_rooms(self):
        """ Pop rooms in dungeons.
            See RoomSizeGenerator details.
        """
        room_generator = RoomSizeGenerator(self.width, self.height, self.config)
        sizes = room_generator.get_room_sizes()
        for index, size in enumerate(sizes):
            room = Room(size.get('x'), size.get('y'), size.get('width'), size.get('height'))
            self.rooms.add(room)

    def _make_map(self):
        x = self.x
        y = self.y
        ax = self.ax
        ay = self.ay
        self.dungeon_map = [[0 for j in range(self.ay)] for i in range(ax)]

        # xとyを順にインクリメントしながら、該当するマスのタイルを取得していく
        floor = ''
        for row in range(x, ax + 1):
            line = ''
            for col in range(y, ay + 1):
                tile = None
                for room in self.rooms.get_all():
                    if room.has_tile(col, row):
                        tile = room.get_tile(col, row)
                        break

                if tile is None:
                    tile = self.roads.get(col, row)

                if tile:
                    self.dungeon_map[row-1][col-1] = str(tile)
                    line = line + str(tile)
                else:
                    self.dungeon_map[row-1][col-1] = str(0)
                    line = line + str(0)
            floor = floor + line + '\n'

        self.dungeon_string = floor

    def to_string(self):
        """Get a human-readable dungeon map.

        :rtype: string
        :return: Fixed-length string with a newline.
        """
        return self.dungeon_string

    def to_array(self):
        """Get a two-dimensional array of dungeon map.

        :rtype: array
        :return: Secondary sequence.
        """
        return self.dungeon_map
