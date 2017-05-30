# -*- coding: UTF-8 -*-
from Rect import Rect
from Tile import Tile
import uuid, random, math

class Waterway(Rect):
    """ Waterway in dungeon.

        Randomly pop water tile in dungeon.
        Water to pop divided into pond and tributary.
    """
    def __init__(self, x, y, width, height, config):
        super(Waterway, self).__init__(x, y, width, height)
        self.config = config
        self.tiles = []
        self._pop_water()

    def get_tiles(self):
        """ Get tile collection from Waterway.

        :rtype: List.
        :return: Return tile of list. if it does not exist, return empty list.
        """
        return self.tiles

    def get_tile(self, x, y):
        """ Get a tile from Waterway.

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

    def _pop_water(self):
        # いずれの処理もタイルの重複を生むが、問題ないので気にしない
        self._pop_pond()
        self._pop_tributary()

    def _pop_pond(self):
        # 象限ごとにおおまかに目安を決めて、ある程度の大きさの沼を沸かせる

        amount_water = self.config.get('amount_water', 0)
        if amount_water == 0:
            return

        orthant_seed = random.randint(1,4)

        # 第一象限
        if orthant_seed == 1:
            base_col = self.x + self.width / 2
            base_row = self.y
            self._pop_orthant_pond(base_col, base_row)

        # 第二象限
        if orthant_seed == 2:
            base_col = self.x
            base_row = self.y
            self._pop_orthant_pond(base_col, base_row)

        # 第三象限
        if orthant_seed == 3:
            base_col = self.x
            base_row = self.y + self.height / 2
            self._pop_orthant_pond(base_col, base_row)

        # 第四象限
        if orthant_seed == 4:
            base_col = self.x + self.width / 2
            base_row = self.y + self.height / 2
            self._pop_orthant_pond(base_col, base_row)

    def _pop_orthant_pond(self, base_col, base_row):
        # 基準となる範囲をずらして、一定の領域に沼を沸かせる
        col_add = int(math.floor( random.randint(2, self.width / 3) ))
        row_add = int(math.floor( random.randint(2, self.height / 3) ))
        col_adjust = self.width / 3
        row_adjust = self.height / 3

        col = int(math.floor( random.randint(base_col, base_col + col_adjust) ))
        row = int(math.floor( random.randint(base_row, base_row + row_adjust) ))
        for x in range(col, col + col_add):
            for y in range(row, row + row_add):
                self.tiles.append(Tile(x, y, Tile.WATER))

    def _pop_tributary(self):
        # 縦か横かの目安を決めて、時々ずらしながら川を沸かせる
        # config.amount_water が多いほど川は増える amount_waterは最大10

        amount_water = self.config.get('amount_water', 0)
        if amount_water == 0:
            return
        if amount_water < 0:
            return
        if 10 < amount_water:
            amount_water = 10

        _cols = []
        _rows = []

        direction_seed = random.randint(1,3)
        if direction_seed == 1:
            for count in range(amount_water):
                self._pop_horizontal_tributary(_cols)

        if direction_seed == 2:
            for count in range(amount_water):
                self._pop_vertical_tributary(_rows)

        if direction_seed == 3:
            for count in range(amount_water):
                self._pop_horizontal_tributary(_cols)
                self._pop_vertical_tributary(_rows)

    def _pop_horizontal_tributary(self, _cols):
        col = random.randint(self.x, self.ax)
        for _col in _cols:
            if _col == col:
                return
        else:
            for row in range(self.y, self.ay + 1):
                polygonal_seed = random.randint(1, 7)
                if polygonal_seed == 1:
                    col = random.randint(self.x, self.ax)
                self.tiles.append(Tile(col, row, Tile.WATER))

    def _pop_vertical_tributary(self, _rows):
        row = random.randint(self.y, self.ay)
        for _row in _rows:
            if _row == row:
                return
        else:
            for col in range(self.x, self.ax + 1):
                polygonal_seed = random.randint(1, 7)
                if polygonal_seed == 1:
                    row = random.randint(self.y, self.ay)
                self.tiles.append(Tile(col, row, Tile.WATER))
