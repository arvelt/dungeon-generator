# -*- coding: UTF-8 -*-
from Rect import Rect
from Tile import Tile
from Room import Room
from Rooms import Rooms
from Road import Road
from Roads import Roads
from Waterway import Waterway
from Util import Util
from RoomSearcher import RoomSearcher
from RoomSizeGenerator import RoomSizeGenerator

class Frame(Rect):
    """ The display frame shape.
        Upper left is the origin.
        The origin starts (1, 1).
    """
    def __init__(self, width, height, config):
        super(Frame, self).__init__(1, 1, width, height)
        self.config = config
        self._pop_rooms()
        self._pop_roads()
        self._pop_waterway()
        self._make_map()

    def _pop_rooms(self):
        self.rooms = Rooms()

        # RoomSizeGeneratorで取得したサイズを元に部屋を作成する
        room_generator = RoomSizeGenerator(self.width, self.height, self.config)
        sizes = room_generator.get_room_sizes()
        for index, size in enumerate(sizes):
            room = Room(size.get('x'), size.get('y'), size.get('width'), size.get('height'))
            self.rooms.add(room)

    def _pop_roads(self):
        self.roads = Roads()

        # RoomSearcherで取得した部屋から部屋への扉の組み合わせから道を作成する
        rooms = self.rooms.get_all()
        searcher = RoomSearcher()
        door_pairs = searcher.get_door_pairs(rooms)
        for doors in door_pairs:
            door1 = doors[0]
            door2 = doors[1]
            road = Road(door1, door2)
            # 部屋に隣接しない道ならば有効
            if not self._is_adjacent(rooms, road):
                self.roads.add(road)

        # 道がひとつもない部屋があれば消す
        if len(self.rooms.get_all()) > 1:
            self.rooms.combine_roads(self.roads.get_all())
            for room in self.rooms.get_all():
                if not room.has_road:
                    self.rooms.delete(room.id)

    def _is_adjacent(self, rooms, road):
        # 道が部屋に隣接してできている場合はTrue、そうでなければFalse
        for room in rooms:
            for tile in road.get_tiles():
                if self._check_adjacent_each_direction(room, tile):
                    return True
        else:
            return False

    def _check_adjacent_each_direction(self, room, tile):
        # 道の１マスの上下左右にドアでも壁でもない部屋のマスがあればTrue、そうでなければFalse
        x = tile.x + 1
        y = tile.y
        if self._is_adjacent_tile(room, x, y):
            return True

        x = tile.x - 1
        y = tile.y
        if self._is_adjacent_tile(room, x, y):
            return True

        x = tile.x
        y = tile.y + 1
        if self._is_adjacent_tile(room, x, y):
            return True

        x = tile.x
        y = tile.y - 1
        if self._is_adjacent_tile(room, x, y):
            return True

        return False

    def _is_adjacent_tile(self, room, x, y):
        if room.has_tile(x, y):
            target_tile = room.get_tile(x, y)
            if target_tile is not None and target_tile.kind != Tile.DOOR and target_tile.kind != Tile.WALL:
                return True
        return False

    def _pop_waterway(self):
        self.waterway = Waterway(self.x, self.y, self.width, self.height, self.config)

    def _make_map(self):
        x = self.x
        y = self.y
        ax = self.ax
        ay = self.ay
        self.dungeon_map = [[0 for j in range(ay)] for i in range(ax)]

        # xとyを順にインクリメントしながら、該当するマスのタイルを取得していく
        floor = ''
        for row in range(x, ax + 1):
            line = ''
            for col in range(y, ay + 1):
                tile = None
                for room in self.rooms.get_all():

                    # 部屋を取得
                    if room.has_tile(col, row):
                        tile = room.get_tile(col, row)

                        # 道を取得（道は壁を通るため先にも見る
                        if tile is None:
                            for road in self.roads.get_all():
                                if road.may_have_tile(col, row):
                                    tile = road.get_tile(col, row)
                                    if tile:
                                        break
                        # 壁を取得
                        if tile is None:
                            tile = room.get_wall(col, row)
                        if tile:
                            break

                # 道を取得
                if tile is None:
                    for road in self.roads.get_all():
                        if road.may_have_tile(col, row):
                            tile = road.get_tile(col, row)
                            if tile:
                                break

                # 水路を取得
                if tile is None:
                    tile = self.waterway.get_tile(col, row)

                if tile:
                    _tile = str(tile)
                    if tile.kind == tile.DOOR and self.config.get('debug', False) == False:
                        _tile = tile.DEFAULT
                    self.dungeon_map[row-1][col-1] = _tile
                    line = line + _tile
                else:
                    self.dungeon_map[row-1][col-1] = str(' ')
                    line = line + str(' ')
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
        :return: Two-dimensional array.
        """
        return self.dungeon_map
