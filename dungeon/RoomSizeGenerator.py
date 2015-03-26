# -*- coding: UTF-8 -*-
from Util import Util
import random

class NoFreeSpaceException(Exception):
    pass

class RoomSizeGenerator(object):
    """ Generator of room in dungeon.
    """
    def __init__(self, width, height, config):
        self.x = 1
        self.y = 1
        self.width = width
        self.height = height
        self.room_number = config.get('room_number', 3)
        self.checker = SizeDuplicateChecker()

    def get_room_sizes(self):
        """　Get available sizes for Room.

        :rtype: List of dictionary.

            | x: Potision of room x. Express upper left squares.
            | y: Potision of room y. Express upper left squares.
            | width: Width of room.
            | height: Height of room.
        :return: Return sizes.
        """
        room_sizes = []
        for num in range(self.room_number):
            try:
                size = self._get_new_size()
                room_sizes.append(size)
            except NoFreeSpaceException:
                pass
        return room_sizes

    def _get_new_size(self):
        size = self._get_other_size()
        count = 0
        while self.checker.prove_available_size(size) == False:
            count = count + 1
            size = self._get_other_size()
            # 10000回繰り返しても見つからなければもう空きがないとみなして飛ばす
            if count > 10000:
                raise NoFreeSpaceException()
        return size

    def _get_other_size(self):
        room_number = self.room_number

        # ルーム数１は大部屋
        if room_number == 1:
            x = 2
            y = 2
            width = self.width - 2
            height = self.height - 2

        # ルーム数２は最大幅の半分までが最大幅
        elif room_number == 2:
            #
            width = random.randint(10, self.width / 2 - 1)
            height = random.randint(10, self.height / 2 - 1)
            x = random.randint(self.x + 1, self.x + self.width - width - 1)
            y = random.randint(self.y + 1, self.y + self.height - height - 1)

        # それ以上のルーム数は、切り上げた偶数の半分で最大幅を割ったものが最大幅
        # 例えば MAX 30, 部屋数5 -> 最小: 5、最大: 30 / ( 6 / 2 ) = 10
        else:
            room_number = self.room_number
            if self.room_number % 2 == 1:
                room_number = room_number + 1
            room_number = room_number / 2

            # 一番外の境界部分には作らないようにする
            max_width = self.width / room_number - 1
            max_height = self.height / room_number - 1
            width = random.randint(4, max_width)
            height = random.randint(4, max_height)
            x = random.randint(self.x + 1, self.x + self.width - width - 1)
            y = random.randint(self.y + 1, self.y + self.height - height - 1)

        return {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }


class SizeDuplicateChecker(object):
    def __init__(self, test_list=None):
        if test_list is None:
            self.sizes = []
        else:
            self.sizes = test_list

    def prove_available_size(self, size):
        # 隣接しないようにサイズを2枠分大きいものとして判定する
        # 部屋同士は最低でも3マスあく
        x = size.get('x') - 1
        y = size.get('y') - 1
        width = size.get('width') + 3
        height = size.get('height') + 3

        if self._is_contain(x, y, width, height):
            return False
        else:
            self.sizes.append({
                'x': x,
                'y': y,
                'width': width,
                'height': height
            })
            return True

    def _is_contain(self, x, y, width, height):
        ax = x
        ay = y
        bx = x + width - 1
        by = y + height - 1

        for size in self.sizes:
            cx = size.get('x')
            cy = size.get('y')
            dx = size.get('width') + cx - 1
            dy = size.get('height') + cy - 1

            if Util.is_colliding_square(ax, ay, bx, by, cx, cy, dx, dy):
                return True
                break
        else:
            return False
