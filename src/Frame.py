# -*- coding: UTF-8 -*-
from Rect import Rect
from Tile import Tile
from Room import Room
from Rooms import Rooms
from Road import Road
from Roads import Roads
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
        self.rooms = Rooms()
        self._pop_rooms()
        self.roads = Roads()
        self._pop_roads()
        self._make_map()

    def _pop_rooms(self):
        # RoomSizeGeneratorで取得したサイズを元に部屋を作成する
        room_generator = RoomSizeGenerator(self.width, self.height, self.config)
        sizes = room_generator.get_room_sizes()
        for index, size in enumerate(sizes):
            room = Room(size.get('x'), size.get('y'), size.get('width'), size.get('height'))
            self.rooms.add(room)

    def _pop_roads(self):
        # RoomSearcherで取得した部屋から部屋への扉の組み合わせから道を作成する
        rooms = self.rooms.get_all()
        searcher = RoomSearcher()
        door_pairs = searcher.get_door_pairs(rooms)
        for doors in door_pairs:
            door1 = doors[0]
            door2 = doors[1]
            road = Road(door1, door2)
            # 部屋と衝突せず、かつ隣接しない道だけが有効
            if not self._is_collided(rooms, road) and not self._is_adjoing(rooms, road):
                self.roads.add(road)

    def _is_adjoing(self, rooms, road):
        # 道が部屋に隣接してできてしまう場合はTrue、そうでなければFalse
        for room in rooms:
            # 道につながっているドアは除いて、道の四角形の１マス分大きい形とぶつかれば、隣接しているということである
            if room.has_door(road.from_door) or room.has_door(road.to_door):
                pass
            else:
                if Util.is_colliding_square(room.x, room.y, room.ax, room.ay, road.x-1, road.y-1, road.ax+1, road.ay+1):
                    return True
        else:
            return False

    def _is_collided(self, rooms, road):
        # 道がいずれかの部屋の座標と衝突してしまう場合はTrue、そうでなければFalse
        for room in rooms:
            if Util.is_colliding_square(room.x, room.y, room.ax, room.ay, road.x, road.y, road.ax, road.ay):
                return True
        else:
            return False

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
                    if room.has_tile(col, row):
                        tile = room.get_tile(col, row)
                        if tile:
                            break

                if tile is None:
                    for road in self.roads.get_all():
                        if road.may_have_tile(col, row):
                            tile = road.get_tile(col, row)
                            if tile:
                                break

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
        :return: Two-dimensional array.
        """
        return self.dungeon_map
