# -*- coding: UTF-8 -*-
import sys, os
sys.path.append(os.path.abspath('./src'))

import math, copy
from operator import attrgetter

class RoomSearcher:
    EAST = 'east'
    WEST = 'west'
    NORTH = 'north'
    SOUTH = 'south'

    def __init__(self):
        pass

    def get_copy_room_direction(self):
        return copy.deepcopy(self.nearest_rooms)

    def get_copy_road_pair(self):
        return copy.deepcopy(self.road_pair)

    def analyze_rooms(self, rooms):
        self.all_rooms = []
        for room in rooms:
            self.all_rooms.append({
                'id': room.id,
                'x': room.mx,
                'y': room.my
            })

        nearest_rooms = []
        for room in self.all_rooms:
            nearest_rooms.append(self.analyze(room))
        result = self.adjust_result_analyze(nearest_rooms)
        self.road_pair = result
        return copy.deepcopy(self.road_pair)

    def adjust_result_analyze(self, rooms):
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

    def analyze(self, room):
        target_room = room
        comparison_destinations = []
        for room in self.all_rooms:
            if room.get('id') != target_room.get('id'):
                comparison_destinations.append(room)
        return self.search_nearest_room(target_room, comparison_destinations)

    def search_nearest_room(self, room, destinations):
        distance_list = self._caluclate_room_distanse(room, destinations)
        result = self.get_nearest_room(distance_list)
        result['id'] = room.get('id')
        return result

    def get_nearest_room(self, distance_list):
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
            self.NORTH: self.get_first_item(sorted_upper),
            self.EAST: self.get_first_item(sorted_right),
            self.SOUTH: self.get_first_item(sorted_lower),
            self.WEST: self.get_first_item(sorted_left),
        }

    def get_first_item(self, list, default=None):
        try:
            return list[0]
        except IndexError:
            return default

    def _caluclate_room_distanse(self, room, destinations):
        distance_list = []
        ax = room.get('x')
        ay = room.get('y')
        for destination in destinations:
            bx = destination.get('x')
            by = destination.get('y')
            distance = math.sqrt( (bx - ax) * (bx - ax) + (by - ay) * (by - ay))

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
