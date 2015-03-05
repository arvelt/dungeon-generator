# -*- coding: UTF-8 -*-

class Rect(object):
    """ Shape of map base.
        All unit of member value is squares, not coordinate.
    """

    def __init__(self, x, y, width, height):
        """
        arguments:
        x -- potision x
        y -- potision y
        width -- shape width
        height -- shape height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.ax = x + width -1
        self.ay = y + height -1
        self.mx = (self.x + self.ax) / 2
        self.my = (self.y + self.ay) / 2

    def __str__(self):
        return str({
            'x': self.x,
            'y': self.y,
            'ax': self.ax,
            'ay': self.ay,
            'mx': self.mx,
            'my': self.my,
            'width': self.width,
            'heigth': self.height,
        })
