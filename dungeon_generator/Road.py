# -*- coding: UTF-8 -*-
from Door import Door
from Tile import Tile
import copy, uuid

class Road(object):
    """ Road from door to door.
        Once instantiated, it is filled with Tile.
    """
    def __init__(self, from_door, to_door):
        self.id = str(uuid.uuid4())
        self.tiles = []
        self.from_door = Door(from_door.x, from_door.y, from_door.direction)
        self.to_door = Door(to_door.x, to_door.y, to_door.direction)
        self._fill_road(from_door, to_door)

    def get_tiles(self):
        """Get all tiles from Road.

        :rtype: List of Tile .
        :return: Return tiles. if it does not exist, return empty list.
        """
        return self.tiles

    def get_tile(self, x, y):
        """Get a tile from Road.

        :param x: potision x.
        :param y: potision y.
        :rtype: Tile class.
        :return: Return tile. if it does not exist, return None.
        """
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        else:
            return None

    def set_tile(self, x, y, new_tile):
        """Set a tile to Road.

        :param x: potision x.
        :param y: potision y.
        :param new_tile: new Tile
        """
        for index, tile in enumerate(self.tiles):
            if tile.x == x and tile.y == y:
                self.tiles[index] = new_tile

    def may_have_tile(self, x, y):
        """Whether there is a possibility of holding the tile.

        :param x: potision x.
        :param y: potision y.
        :rtype: Booean
        :return: Return True, if there is a possibility. Otherwise Fasle.
        """
        if (self.x <= x and x <= self.ax) and \
            (self.y <= y and y <= self.ay):
            return True
        else:
            return False

    def _fill_road(self, from_door, to_door):
        # 計算しやすいように、小さい座標の順から大きい座標の場所へ向かうようにする
        # 道が縦向きならY座標を基準に、横向きならX座標を基準にして判定する
        if from_door.is_vertical():
            if from_door.y < to_door.y:
                self._set_inline_range(from_door, to_door, 0, 1)
                self._pave_road(from_door, to_door, 0, 1)
            else:
                self._set_inline_range(to_door, from_door, 0, 1)
                self._pave_road(to_door, from_door, 0, 1)
        else:
            if from_door.x < to_door.x:
                self._set_inline_range(from_door, to_door, 1, 0)
                self._pave_road(from_door, to_door, 1, 0)
            else:
                self._set_inline_range(to_door, from_door, 1, 0)
                self._pave_road(to_door, from_door, 1, 0)

    def _set_inline_range(self, from_door, to_door, col_add, row_add):
        #ドアを含まない道になりうる領域を四角形とみなして保持する
        x = from_door.x + col_add
        y = from_door.y + row_add
        ax = to_door.x - col_add
        ay = to_door.y - row_add

        if x < ax:
            self.x = x
            self.ax = ax
        else:
            self.x = ax
            self.ax = x
        if y < ay:
            self.y = y
            self.ay = ay
        else:
            self.y = ay
            self.ay = y

    def _pave_road(self, from_door, to_door, col_add, row_add):
        # ドアからドアまでの道を作る
        ax = from_door.x + col_add
        ay = from_door.y + row_add
        next1 = Tile(ax, ay, Tile.WAY)
        self.tiles.append(next1)

        if self._pave_middle_polyline(ax, ay, to_door.x, to_door.y, col_add):
            return

        bx = to_door.x - col_add
        by = to_door.y - row_add
        next2 = Tile(bx, by, Tile.WAY)
        self.tiles.append(next2)

        if self._pave_middle_polyline(ax, ay, bx, by, col_add):
            return

        # 道が埋まるまで再帰的に繰り返す
        self._pave_road(next1, next2, col_add, row_add)

    def _pave_middle_polyline(self, ax, ay, bx, by, vertical):
        #縦方向の道は横がそろうまで伸ばす
        if vertical == 0:
            # 同じY位置まできたらX側を埋める
            if ay == by:
                if ax < bx:
                    start = ax
                    end = bx
                else:
                    start = bx
                    end = ax
                for x in range(start, end):
                    road = Tile(x, ay, Tile.WAY)
                    self.tiles.append(road)
                return True

        #横方向の道は横がそろうまで伸ばす
        else:
            # 同じX位置にきたらY側を埋める
            if ax == bx:
                if ay < by:
                    start = ay
                    end = by
                else:
                    start = by
                    end = ay
                for y in range(start, end):
                    road = Tile(ax, y, Tile.WAY)
                    self.tiles.append(road)
                return True

        return False
