# -*- coding: UTF-8 -*-
from Rect import Rect
from Tile import Tile
from Room import Room
from Rooms import Rooms
from Road import Road
from Roads import Roads
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

    def _pop_roads(self):
        searcher = RoomSearcher()
        pair_list = searcher.analyze_rooms(self.rooms.get_all())
        door_pair = self._transform_door_pair(pair_list)
        self._generator_road(door_pair)

    def _transform_door_pair(self, pair_list):
        col_distances = []
        row_distances = []
        door_pair = []
        for pair in pair_list:
            from_id = pair.get('from')
            to_id = pair.get('to')

            if pair.get('direction') == RoomSearcher.NORTH:
                door1 = self.rooms.get(from_id).get_north_door()
                door2 = self.rooms.get(to_id).get_south_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in col_distances:
                    if way == distance:
                        break
                else:
                    col_distances.append(distance)
                    door_pair.append((door1, door2))

            if pair.get('direction') == RoomSearcher.SOUTH:
                door1 = self.rooms.get(from_id).get_south_door()
                door2 = self.rooms.get(to_id).get_north_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in col_distances:
                    if way == distance:
                        break
                else:
                    col_distances.append(distance)
                    door_pair.append((door1, door2))

            if pair.get('direction') == RoomSearcher.EAST:
                door1 = self.rooms.get(from_id).get_east_door()
                door2 = self.rooms.get(to_id).get_west_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in row_distances:
                    if way == distance:
                        break
                else:
                    row_distances.append(distance)
                    door_pair.append((door1, door2))

            if pair.get('direction') == RoomSearcher.WEST:
                door1 = self.rooms.get(from_id).get_west_door()
                door2 = self.rooms.get(to_id).get_east_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in row_distances:
                    if way == distance:
                        break
                else:
                    row_distances.append(distance)
                    door_pair.append((door1, door2))

        return door_pair

    def _generator_road(self, door_pair):
        for doors in door_pair:
            door1 = doors[0]
            door2 = doors[1]
            self.roads.add(Road(door1, door2))

    def _pop_rooms(self):
        # RoomSizeGeneratorで取得したサイズを元に部屋を作成する
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
                        break

                if tile is None:
                    for road in self.roads.get_all():
                        if road.has_tile(col, row):
                            tile = road.get_tile(col, row)
                            if tile is None:
                                print col, row,'があるはずなのにない'
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
