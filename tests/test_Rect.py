# -*- coding: UTF-8 -*-
import sys, os
sys.path.append(os.path.abspath('./src'))

from Rect import Rect

def test_Rect():
    rect = Rect(1, 2, 3, 3)
    assert (rect.x, rect.y) == (1, 2)
    assert (rect.width, rect.height) == (3, 3)
    assert (rect.ax, rect.ay) == (3, 4)
