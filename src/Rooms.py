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
        return self.rooms

    def delete(self, id):
        """ Get a room from collection.

        :param id: unique key of the room.
        """
        for room in self.rooms[:]:
            if room.id == id:
                self.rooms.remove(room)

    def combine_roads(self, roads):
        """ Combine room and road. All room checks.

        When has door, the room records each direction road id.
        :param roads: List of road.
        """
        # 全ての部屋と全ての道を探索し、部屋につながっている道があればその道のIDを設定する
        for room in self.rooms:
            for road in roads:
                if room.has_door(road.from_door) or room.has_door(road.to_door):
                    from_door = road.from_door
                    to_door = road.to_door

                    north_door = room.get_north_door()
                    if (north_door.x == from_door.x and north_door.y == from_door.y) or \
                        (north_door.x == to_door.x and north_door.y == to_door.y):
                        room.has_road = True
                        room.north_road_id = road.id

                    south_door = room.get_south_door()
                    if (south_door.x == from_door.x and south_door.y == from_door.y) or \
                        (south_door.x == to_door.x and south_door.y == to_door.y):
                        room.has_road = True
                        room.south_road_id = road.id

                    east_door = room.get_east_door()
                    if (east_door.x == from_door.x and east_door.y == from_door.y) or \
                        (east_door.x == to_door.x and east_door.y == to_door.y):
                        room.has_road = True
                        room.east_road_id = road.id

                    west_door = room.get_west_door()
                    if (west_door.x == from_door.x and west_door.y == from_door.y) or \
                        (west_door.x == to_door.x and west_door.y == to_door.y):
                        room.has_road = True
                        room.west_road_id = road.id

    def get_copy_all(self):
        """ Get all copy of rooms from collection.
            When performing a destructive operation , use this.

        :rtype: List
        :return: List of Room.
        """
        return copy.deepcopy(self.rooms)

    def __str__(self):
        return str([str(room) for room in self.rooms])
