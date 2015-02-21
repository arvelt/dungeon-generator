# -*- coding: UTF-8 -*-
import sys, os, math
sys.path.append(os.path.abspath('./src'))

from RoomSearcher import RoomSearcher

def test_RoomSearcher__caluclate_room_distanse():
    room1 = {'x':4, 'y':4, 'width':3, 'height':3}
    room2 = {'x':7, 'y':7, 'width':3, 'height':3}
    room3 = {'x':7, 'y':1, 'width':3, 'height':3}
    rooms = [room2, room3]
    searcher = RoomSearcher()
    result = searcher._caluclate_room_distanse(room1, rooms)

    assert len(result) == 2

    distance = result[0].get('distance')
    radians = result[0].get('angle')
    print math.degrees(result[0].get('angle'))
    print math.degrees(result[1].get('angle'))
    assert distance == float(3)
    assert radians == math.radians(135)

    distance = result[1].get('distance')
    radians = result[1].get('angle')
    assert distance == float(3)
    assert radians == math.radians(45)
