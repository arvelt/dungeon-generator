# -*- coding: UTF-8 -*-
import sys, os
sys.path.append(os.path.abspath('./src'))

import math, copy
from operator import attrgetter

class RoomSearcher(object):
    EAST = 'east'
    WEST = 'west'
    NORTH = 'north'
    SOUTH = 'south'

    def get_door_pairs(self, rooms):
        """ Get door pairs from all rooms.

        It is a combination of the door nearest the room from the door of each side of the room.
        :rtype: List of Tupple

            | [0] from_door
            | [1] to_door
        :return: Return List of door tuple.
        """
        self.all_rooms = []
        for room in rooms:
            self.all_rooms.append({
                'id': room.id,
                'x': room.mx,
                'y': room.my
            })

        divided_rooms = self._devide_room()
        combinations_of_nearest_room = self._get_near_conbination(divided_rooms)
        pair_list = self._adjust_result_analyze(combinations_of_nearest_room)
        door_pair = self._transform_door_pair(pair_list, rooms)
        return door_pair

    def _adjust_result_analyze(self, rooms):
        # 一番近い部屋同士の組み合わせを、東西南北ごとに作る
        # 以下の形式を返す
        # [{
        #     'from': room id,
        #     'to': room id,
        #     'direction': direction of north, south, east and west,
        # }]
        self.nearest_rooms = rooms
        road_pair = []
        for nearest_room in rooms:
            from_id = nearest_room.get('id')

            north = nearest_room.get(self.NORTH)
            if north is not None:
                to_id = north.get('id')
                direction = self.NORTH
                road_pair.append({
                    'from': from_id,
                    'to': to_id,
                    'direction': self.NORTH,
                })

            south = nearest_room.get(self.SOUTH)
            if south is not None:
                to_id = south.get('id')
                direction = self.SOUTH
                road_pair.append({
                    'from': from_id,
                    'to': to_id,
                    'direction': self.SOUTH,
                })

            east = nearest_room.get(self.EAST)
            if east is not None:
                to_id = east.get('id')
                direction = self.EAST
                road_pair.append({
                    'from': from_id,
                    'to': to_id,
                    'direction': self.EAST,
                })

            west = nearest_room.get(self.WEST)
            if west is not None:
                to_id = west.get('id')
                direction = self.WEST
                road_pair.append({
                    'from': from_id,
                    'to': to_id,
                    'direction': self.WEST,
                })
        return road_pair

    def _transform_door_pair(self, pair_list, rooms):
        # 部屋の組み合わせからドアの組わせを作る
        # 以下の形式を返す
        # [(
        #    Door, One of the door to be the start of road.
        #    Door  One of the foor to be the end of road.
        # )]
        col_distances = []
        row_distances = []
        door_pair = []
        for pair in pair_list:
            from_id = pair.get('from')
            to_id = pair.get('to')

            for room in rooms:
                if room.id == from_id:
                    from_room = room
                if room.id == to_id:
                    to_room = room

            if pair.get('direction') == RoomSearcher.NORTH:
                door1 = from_room.get_north_door()
                door2 = to_room.get_south_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in col_distances:
                    if way == distance:
                        break
                else:
                    col_distances.append(distance)
                    door_pair.append((door1, door2))

            if pair.get('direction') == RoomSearcher.SOUTH:
                door1 = from_room.get_south_door()
                door2 = to_room.get_north_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in col_distances:
                    if way == distance:
                        break
                else:
                    col_distances.append(distance)
                    door_pair.append((door1, door2))

            if pair.get('direction') == RoomSearcher.EAST:
                door1 = from_room.get_east_door()
                door2 = to_room.get_west_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in row_distances:
                    if way == distance:
                        break
                else:
                    row_distances.append(distance)
                    door_pair.append((door1, door2))

            if pair.get('direction') == RoomSearcher.WEST:
                door1 = from_room.get_west_door()
                door2 = to_room.get_east_door()
                distance = (door2.x - door1.x) * (door2.x - door1.x) + (door2.y - door1.y) * (door2.y - door1.y)
                # 距離が同じならばドアの組み合わせは同じなので除く
                for way in row_distances:
                    if way == distance:
                        break
                else:
                    row_distances.append(distance)
                    door_pair.append((door1, door2))

        return door_pair

    def _devide_room(self):
        # 基準になる部屋とそれ以外の部屋、という組み合わせを作る
        # [(target_room, comparison_destinations[])] を返す
        devided_rooms = []
        for room in self.all_rooms:
            target_room = room
            comparison_destinations = []
            for room in self.all_rooms:
                if room.get('id') != target_room.get('id'):
                    comparison_destinations.append(room)
            devided_rooms.append((target_room, comparison_destinations))
        return devided_rooms

    def _get_near_conbination(self, divided_rooms):
        # 基準になる部屋と東西南北の方向ごとに一番近い部屋の組み合わせのリストを返す
        # 以下の形式を返す
        # {
        #     # Below, see _search_nearest_room detail.
        #     'id':
        #     # Below, see _get_nearest_room detail.
        #     'north':
        #     'south':
        #     'east':
        #     'west'
        # }
        combinations_of_nearest_room = []
        for divided in divided_rooms:
            target_room = divided[0]
            comparison_destinations = divided[1]
            combinations_of_nearest_room.append(
                self._search_nearest_room(target_room, comparison_destinations)
            )
        return combinations_of_nearest_room

    def _search_nearest_room(self, room, destinations):
        # 基準になる部屋から、一番近い部屋を探す
        # 以下の形式を返す。
        # {
        #     'id': ID of standard room,
        #     Other keys, see _get_nearest_room detail.
        # }
        distance_list = self._caluclate_room_distanse(room, destinations)
        result = self._get_nearest_room(distance_list)
        result['id'] = room.get('id')
        return result

    def _get_nearest_room(self, distance_list):
        # 全ての部屋に対する距離の中から、東西南北のそれぞれの方向で一番近い距離を探す
        # 以下の形式を返す。
        # {
        #     'north' : {
        #         'id': Destination room id,
        #         'distance': Distance from room to room,
        #         'angle': Angle of destination room.
        #     } or None,
        #     'south' : {
        #         'id': Destination room id,
        #         'distance': Distance from room to room,
        #         'angle': Angle of destination room.
        #     } or None,
        #     'east' : {
        #         'id': Destination room id,
        #         'distance': Distance from room to room,
        #         'angle': Angle of destination room.
        #     } or None,
        #     'west' : {
        #         'id': Destination room id,
        #         'distance': Distance from room to room,
        #         'angle': Angle of destination room.
        #     } or None,
        # }
        upper_list = []
        right_list = []
        lower_list = []
        left_list = []

        # 角度を元にして四方に振り分ける
        for distance in distance_list:
            angle = math.degrees(distance.get('angle'))
            if -45 <= angle and angle < 45:
                #上
                upper_list.append(distance)
            elif 45 <= angle and angle < 135:
                #右
                right_list.append(distance)
            elif -135 <= angle and angle < -45:
                #左
                left_list.append(distance)
            else:
                #下
                lower_list.append(distance)

        # それぞれのリストの中身をdistanceの値をキーにしてソートする
        # 最も近い部屋までの距離と
        sorted_upper = sorted(upper_list, key=lambda x:x['distance'])
        sorted_right = sorted(right_list, key=lambda x:x['distance'])
        sorted_lower = sorted(lower_list, key=lambda x:x['distance'])
        sorted_left = sorted(left_list, key=lambda x:x['distance'])
        return {
            self.NORTH: self._get_first_item(sorted_upper),
            self.EAST: self._get_first_item(sorted_right),
            self.SOUTH: self._get_first_item(sorted_lower),
            self.WEST: self._get_first_item(sorted_left),
        }

    def _get_first_item(self, list, default=None):
        try:
            return list[0]
        except IndexError:
            return default

    def _caluclate_room_distanse(self, room, destinations):
        # 基準になる部屋から、すべての部屋に対して距離を計算する
        distance_list = []
        ax = room.get('x')
        ay = room.get('y')
        for destination in destinations:
            bx = destination.get('x')
            by = destination.get('y')
            distance = (bx - ax) * (bx - ax) + (by - ay) * (by - ay)

            #マス目は左上原点なので、Y座標が逆になっているものとして計算する。
            #右側面を正の値、左側面を負の値、上方が0度、下方が180/-180度となるものとする。
            radius = math.atan2(bx-ax,by-ay)
            if 0 < radius:
                angle = math.radians(180) - math.atan2(bx-ax,by-ay)
            else:
                angle = math.radians(-180) - math.atan2(bx-ax,by-ay)
            distance_list.append({
                'id': destination.get('id'),
                'distance': distance,
                'angle':angle
            })
        return  distance_list
