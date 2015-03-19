# -*- coding: UTF-8 -*-
import sys, os
sys.path.append(os.path.abspath('./src'))

from Tile import Tile

def test_Tile():
    tile = Tile(1, 2)
    assert (tile.x, tile.y) == (1, 2)
    assert tile.kind == Tile.DEFAULT
