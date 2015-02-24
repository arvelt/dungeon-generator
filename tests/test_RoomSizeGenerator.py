# -*- coding: UTF-8 -*-
import sys, os
sys.path.append(os.path.abspath('./src'))

from RoomSizeGenerator import RoomSizeGenerator, SizeDuplicateChecker


#
# FIXME なんかこのテストが動かなくなってるけどよくわからない
#

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
    size = {'x': 10, 'y': 4, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker.prove_available_size(new_size)
    assert result == True

    new_size = {'x':x, 'y':y, 'width':width, 'height':height}
    size = {'x': 7, 'y': 4, 'width': 3, 'height':3}
#    size2 = {'x': 4, 'y': 6, 'width': 3, 'height':3}
    checker = SizeDuplicateChecker([size])
    result = checker.prove_available_size(new_size)
    assert result == False


def test_RoomSizeGenerator():
    width = 20
    height = 20
    config = {'room_number': 3}
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
