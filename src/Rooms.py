# -*- coding: UTF-8 -*-
import copy

class Rooms(object):
    """ Collection of room.
    """
    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def get_room(self, id):
        for room in self.rooms:
            if room.id == id:
                return room

    def get_rooms(self):
        return copy.deepcopy(self.rooms)

    def __str__(self):
        return str([str(room) for room in self.rooms])
