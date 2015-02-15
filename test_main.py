# -*- coding: UTF-8 -*-
from main import Rect, Tile, Room, Rooms, OuterFrame

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
