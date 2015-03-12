# -*- coding: UTF-8 -*-
from Door import Door
from Tile import Tile
import copy, uuid

class Road(object):
    def __init__(self, from_door, to_door):
        self.id = str(uuid.uuid4())
        self.tiles = []
        self.from_door = Door(from_door.x, from_door.y, from_door.direction)
        self.to_door = Door(to_door.x, to_door.y, to_door.direction)
        self.fill_road(from_door, to_door)
        print 'this road is', self.x, self.y, 'to', self.ax, self.ay

    def get_tile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        else:
            return None

    def set_tile(self, x, y, new_tile):
        for index, tile in enumerate(self.tiles):
            if tile.x == x and tile.y == y:
                self.tiles[index] = new_tile

    def has_tile(self, x, y):
        if (self.x <= x and x <= self.ax) and \
            (self.y <= y and y <= self.ay):
            print [(tile.x, tile.y) for tile in self.tiles]
            return True
        else:
            return False

    def fill_road(self, from_door, to_door):
        print 'start', from_door.x, from_door.y, 'and', to_door.x, to_door.y
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
