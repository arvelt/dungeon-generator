# -*- coding: UTF-8 -*-
import sys, os, math
sys.path.append(os.path.abspath('./src'))

from RoomSearcher import RoomSearcher

def test_RoomSearcher():
    room1 = {'x':1, 'y':1, 'width':3, 'height':3}
    room2 = {'x':4, 'y':1, 'width':3, 'height':3}
    rooms = [room1, room2]
    searcher = RoomSearcher()
    result = searcher._caluclate_room_distanse(room1, [room2])

    assert len(result) == 1

    distance = result[0].get('distance')
    radians = result[0].get('angle')
    print result
    assert distance == float(3)
    assert radians == math.radians(90)
