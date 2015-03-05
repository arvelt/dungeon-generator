# -*- coding: UTF-8 -*-
import copy

class Rooms(object):
    """ Collection of room.
    """
    def __init__(self):
        self.rooms = []

    def add(self, room):
        """Add a room to collection.

        :param room: room class.
        """
        self.rooms.append(room)

    def get(self, id):
        """Get a room from collection.

        :param id: unique key of the room.
        :rtype: Room class
        :return: Return room. if it does not exist, return None.
        """
        for room in self.rooms:
            if room.id == id:
                return room
        else:
            return None

    def get_all(self):
        """Get all rooms from collection.

        :rtype: List
        :return: List of Room.
        """
        return copy.deepcopy(self.rooms)

    def __str__(self):
        return str([str(room) for room in self.rooms])
