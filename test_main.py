# -*- coding: UTF-8 -*-
from main \
import Rect, Tile, Room, Rooms, OuterFrame, SizeDuplicateChecker, RoomSizeGenerator

def test_Rect():
    rect = Rect(1, 2, 3, 3)
    assert (rect.x, rect.y) == (1, 2)
    assert (rect.width, rect.height) == (3, 3)
    assert (rect.ax, rect.ay) == (3, 4)


def test_Tile():
    tile = Tile(1, 2)
    assert (tile.x, tile.y) == (1, 2)
    assert tile.kind == Tile.DEFAULT

    tile = Tile(3, 4, Tile.PARTING_LINE)
    assert (tile.x, tile.y) == (3, 4)
    assert tile.kind == Tile.PARTING_LINE

def test_SizeDuplicateChecker():

    #このサイズを新しく登録しようとしたときに、
    x = 4
    y = 4
    width = 3
    height = 3

    #
    # _is_contain
    #

    #問題なし
    size = {'x': 7, 'y': 4, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker._is_contain(x, y, width, height)
    assert result == False

    # 右辺が被る
    size = {'x': 6, 'y': 4, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker._is_contain(x, y, width, height)
    assert result == True

    # 下辺が被る
    size = {'x': 4, 'y': 6, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker._is_contain(x, y, width, height)
    assert result == True

    # 左辺が被る
    size = {'x': 2, 'y': 4, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker._is_contain(x, y, width, height)
    assert result == True

    # 上辺が被る
    size = {'x': 4, 'y': 2, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker._is_contain(x, y, width, height)
    assert result == True

    #
    # prove_available_size
    #
    new_size = {'x':x, 'y':y, 'width':width, 'height':height}
    size = {'x': 7, 'y': 4, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker.prove_available_size(new_size)
    assert result == True

    new_size = {'x':x, 'y':y, 'width':width, 'height':height}
    size = {'x': 7, 'y': 4, 'width': 3, 'height':3}
    size2 = {'x': 4, 'y': 6, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size, size2])
    result = checker.prove_available_size(new_size)
    assert result == False


def test_RoomSizeGenerator():
    width = 20
    height = 20
    config = {'room_number': 2}
    generator = RoomSizeGenerator(width, height, config)

    size = generator._get_new_size()
    size2 = generator._get_new_size()
    size3 = generator._get_new_size()
    size4 = generator._get_new_size()

    checker = SizeDuplicateChecker([size2])
    result = checker._is_contain(size.get('x'), size.get('y'), size.get('width'), size.get('height'))
    assert result == False

    checker = SizeDuplicateChecker([size2, size3, size4])
    result = checker._is_contain(size.get('x'), size.get('y'), size.get('width'), size.get('height'))
    assert result == False
