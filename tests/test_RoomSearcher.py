# -*- coding: UTF-8 -*-
import sys, os, math, pprint
sys.path.append(os.path.abspath('./dungeon'))

from RoomSearcher import RoomSearcher
from Room import Room

def test_RoomSearcher__caluclate_room_distanse():
    room = {'x':4, 'y':4, 'width':3, 'height':3}

    room1 = {'x':1, 'y':1, 'width':3, 'height':3}
    room2 = {'x':4, 'y':1, 'width':3, 'height':3}
    room3 = {'x':7, 'y':1, 'width':3, 'height':3}
    room4 = {'x':1, 'y':4, 'width':3, 'height':3}
    room5 = {'x':4, 'y':4, 'width':3, 'height':3}
    room6 = {'x':7, 'y':4, 'width':3, 'height':3}
    room7 = {'x':1, 'y':7, 'width':3, 'height':3}
    room8 = {'x':4, 'y':7, 'width':3, 'height':3}
    room9 = {'x':7, 'y':7, 'width':3, 'height':3}
    rooms = [room1, room2, room3, room4, room6, room7, room8, room9,]
    searcher = RoomSearcher()
    result = searcher._caluclate_room_distanse(room5, rooms)
    assert len(result) == 8

    radians = result[0].get('angle')
    assert radians == math.radians(-45)
    radians = result[1].get('angle')
    assert radians == math.radians(0)
    radians = result[2].get('angle')
    assert radians == math.radians(45)
    radians = result[3].get('angle')
    assert radians == math.radians(-90)
    radians = result[4].get('angle')
    assert radians == math.radians(90)
    radians = result[5].get('angle')
    assert radians == math.radians(-135)
    radians = result[6].get('angle')
    assert radians == math.radians(-180)
    radians = result[7].get('angle')
    assert radians == math.radians(135)

    distance = result[1].get('distance')
    assert distance == float(9)
    distance = result[3].get('distance')
    assert distance == float(9)
    distance = result[4].get('distance')
    assert distance == float(9)
    distance = result[6].get('distance')
    assert distance == float(9)

def test_RoomSearcher__get_nearest_room():
    UR_short1 = {'id': '1', 'distance':3, 'angle':math.radians(44)} # top
    UR_short2 = {'id': '2', 'distance':3, 'angle':math.radians(45)} # right
    UR_short3 = {'id': '3', 'distance':3, 'angle':math.radians(46)}
    UR_long1 = {'id': '4', 'distance':4, 'angle':math.radians(44)}
    UR_long2 = {'id': '5', 'distance':4, 'angle':math.radians(45)}
    UR_long3 = {'id': '6', 'distance':4, 'angle':math.radians(46)}
    LR_short1 = {'id': '7', 'distance':3, 'angle':math.radians(134)} # right
    LR_short2 = {'id': '8', 'distance':3, 'angle':math.radians(135)} # down
    LR_short3 = {'id': '9', 'distance':3, 'angle':math.radians(136)}
    LR_long1 = {'id': '10', 'distance':4, 'angle':math.radians(134)}
    LR_long2 = {'id': '11', 'distance':4, 'angle':math.radians(135)}
    LR_long3 = {'id': '12', 'distance':4, 'angle':math.radians(136)}
    LL_short1 = {'id': '13', 'distance':3, 'angle':math.radians(-134)}
    LL_short2 = {'id': '14', 'distance':3, 'angle':math.radians(-135)} # left
    LL_short3 = {'id': '15', 'distance':3, 'angle':math.radians(-136)} # down
    LL_long1 = {'id': '16', 'distance':4, 'angle':math.radians(-134)}
    LL_long2 = {'id': '17', 'distance':4, 'angle':math.radians(-135)}
    LL_long3 = {'id': '18', 'distance':4, 'angle':math.radians(-136)}
    UL_short1 = {'id': '19', 'distance':3, 'angle':math.radians(-44)}
    UL_short2 = {'id': '20', 'distance':3, 'angle':math.radians(-45)} # top
    UL_short3 = {'id': '21', 'distance':3, 'angle':math.radians(-46)} # left
    UL_long1 = {'id': '22', 'distance':4, 'angle':math.radians(-44)}
    UL_long2 = {'id': '23', 'distance':4, 'angle':math.radians(-45)}
    UL_long3 = {'id': '24', 'distance':4, 'angle':math.radians(-46)}

    distance_list = [
        UR_short1, UR_short2, UR_short3, UR_long1, UR_long2, UR_long3,
        LR_short1, LR_short2, LR_short3, LR_long1, LR_long2, LR_long3,
        UL_short1, UL_short2, UL_short3, UL_long1, UL_long2, UL_long3,
        LL_short1, LL_short2, LL_short3, LL_long1, LL_long2, LL_long3
    ]

    searcher = RoomSearcher()

    # 右上
    distance_list = [
        UR_short1, UR_short2, UR_long1, UR_long2
    ]
    result = searcher._get_nearest_room(distance_list)
    assert result.get(RoomSearcher.NORTH).get('id') == '1'
    assert result.get(RoomSearcher.SOUTH) is None
    assert result.get(RoomSearcher.EAST).get('id') == '2'
    assert result.get(RoomSearcher.WEST) is None

    # 右下
    distance_list = [
        LR_short1, LR_short2, LR_long1, LR_long2
    ]
    result = searcher._get_nearest_room(distance_list)
    assert result.get(RoomSearcher.NORTH) is None
    assert result.get(RoomSearcher.SOUTH).get('id') == '8'
    assert result.get(RoomSearcher.EAST).get('id') == '7'
    assert result.get(RoomSearcher.WEST) is None

    #　左下
    distance_list = [
        LL_short2, LL_short3, LL_long2, LL_long3
    ]
    result = searcher._get_nearest_room(distance_list)
    assert result.get(RoomSearcher.NORTH) is None
    assert result.get(RoomSearcher.SOUTH).get('id') == '15'
    assert result.get(RoomSearcher.EAST) is None
    assert result.get(RoomSearcher.WEST).get('id') == '14'

    # 左上
    distance_list = [
        UL_short2, UL_short3, UL_long2, UL_long3
    ]
    result = searcher._get_nearest_room(distance_list)
    assert result.get(RoomSearcher.NORTH).get('id') == '20'
    assert result.get(RoomSearcher.SOUTH) is None
    assert result.get(RoomSearcher.EAST) is None
    assert result.get(RoomSearcher.WEST).get('id') == '21'
