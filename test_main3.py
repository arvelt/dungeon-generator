# -*- coding: UTF-8 -*-
from main3 import Rect, Tile, Frame, Frames, OuterFrame

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


def test_Frame():
    frame = Frame(1, 1, 3, 3)

    assert len(frame.tiles) == 9

    assert frame.has_coordinate(1,1)
    assert frame.has_coordinate(3,3)
    assert frame.has_coordinate(4,3) is False
    assert frame.has_coordinate(3,4) is False
    assert frame.has_coordinate(4,4) is False

    assert frame.get_tile(1,1)
    assert frame.get_tile(4,3) is None
    assert frame.get_tile(3,4) is None
    assert frame.get_tile(4,4) is None


def test_Frames():
    frames = Frames()
    frames.add_frame(Frame(1, 1, 3, 3))
    frames.add_frame(Frame(4, 1, 3, 3))

    assert len(frames.frames) == 2
    filed = '000\n000\n000\n000\n000\n000\n'
    assert frames.to_map(1,1,6,3) == filed

    frames = Frames()
    frames.add_frame(Frame(1, 1, 3, 3))
    frames.add_frame(Frame(4, 1, 3, 3))
    frames.add_frame(Frame(1, 4, 3, 3))
    frames.add_frame(Frame(4, 4, 3, 3))
    filed = '000000\n000000\n000000\n000000\n000000\n000000\n'

    assert len(frames.frames) == 4
    assert frames.to_map(1,1,6,6) == filed


def test_OuterFrames():
    outer = OuterFrame(10, 10)
    filed = '1111133333\n1111133333\n1111133333\n1111133333\n1111133333\n2222244444\n2222244444\n2222244444\n2222244444\n2222244444\n'
    assert outer.to_map() == filed
