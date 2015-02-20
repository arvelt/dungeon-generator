# -*- coding: UTF-8 -*-
import math
from operator import attrgetter

class RoomSearcher:
    """WIP"""

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

    def get_nearest_room(self, potision):
        return self.nearest_room.get(potision, None)

    def analyze(self, room):
        target_room = room
        comparison_destinations = []
        for room in self.copy_rooms:
            if room != target_room:
                comparison_destinations.append(room)
        return self.search_nearest_room(target_room, comparison_destinations)

    def search_nearest_room(self, room, destinations):
        distance_list = self._caluclate_room_distanse(room, destinations)
        return self.get_nearest_room(room.get('id'), distance_list)

    def get_nearest_room(self, id, distance_list):
        upper_list = []
        right_list = []
        lower_list = []
        left_list = []
        for distance in distance_list:
            angle = math.degrees(distance.get('angle'))
            if -45 <= angle and angle < 45:
                #上
                upper_list.append(distance)
            elif 45 <= angle and angle < 135:
                #右
                right_list.append(distance)
            elif 135 <= angle and angle < -135:
                #下
                lower_list.append(distance)
            else:
                #左
                left_list.append(distance)

        sorted_upper = sorted(upper_list, key=attrgetter(distance))
        sorted_right = sorted(right_list, key=attrgetter(distance))
        sorted_lower = sorted(lower_list, key=attrgetter(distance))
        sorted_left = sorted(left_list, key=attrgetter(distance))
        return {
            'id': id,
            TOP: self.get_first_item(sorted_upper),
            RIGHT: self.get_first_item(sorted_right),
            BELOW: self.get_first_item(sorted_lower),
            RIGHT: self.get_first_item(sorted_left),
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
            angle = math.atan2(bx-ax,by-ay)
            distance_list.append({'id':id, 'distance': distance, 'angle':angle})
        return  distance_list
