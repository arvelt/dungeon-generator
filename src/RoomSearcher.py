# -*- coding: UTF-8 -*-
import sys, os
sys.path.append(os.path.abspath('./src'))

import math, copy
from operator import attrgetter
from main import Room

class RoomSearcher:
    RIGHT = 'right'
    LEFT = 'left'
    TOP = 'top'
    BELOW = 'below'
    UPPER_RIGHT = 'upper_right'
    LOWER_RIGHT = 'lower_right'
    UPPER_LEFT = 'upper_left'
    LOWER_LEFT = 'lower_left'

    def __init__(self):
        self.nearest_room = {}

    def conruct_rooms_placement(self, rooms):
        self.copy_rooms = copy.deepcopy(rooms)

        nearest_rooms = []
        for room in rooms:
            nearest_rooms.append(self.analyze(room))
        return nearest_rooms

    def analyze(self, room):
        target_room = room
        comparison_destinations = []
        for room in self.copy_rooms:
            if room != target_room:
                comparison_destinations.append(room)
        return self.search_nearest_room(target_room, comparison_destinations)

    def search_nearest_room(self, room, destinations):
        distance_list = self._caluclate_room_distanse(room, destinations)
        return self.get_nearest_room(distance_list)

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
        sorted_upper = sorted(upper_list, key=lambda x:x['distance'])
        sorted_right = sorted(right_list, key=lambda x:x['distance'])
        sorted_lower = sorted(lower_list, key=lambda x:x['distance'])
        sorted_left = sorted(left_list, key=lambda x:x['distance'])
        return {
            self.TOP: self.get_first_item(sorted_upper),
            self.RIGHT: self.get_first_item(sorted_right),
            self.BELOW: self.get_first_item(sorted_lower),
            self.LEFT: self.get_first_item(sorted_left),
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
            id = destination.get('id')
            bx = destination.get('x')
            by = destination.get('y')
            distance = math.sqrt( (ax - bx) * (ax - bx) + (ay - ay) * (ay - ay))

            #マス目は左上原点なので、Y座標が逆になっているものとして計算する。
            angle = math.radians(180) - math.atan2(bx-ax,by-ay)
            distance_list.append({'id':id, 'distance': distance, 'angle':angle})
        return  distance_list
