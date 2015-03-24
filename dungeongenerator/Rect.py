# -*- coding: UTF-8 -*-

class Rect(object):
    """ Shape of map base.

        All unit of member value is squares, not coordinate.
    """

    def __init__(self, x, y, width, height):
        self.x = x
        """X squares in the lower right."""

        self.y = y
        """Y squares in the lower right."""

        self.width = width
        """Size of width"""

        self.height = height
        """Size of height"""

        self.ax = x + width -1
        """X squares in the lower right. Automatic calculation from the argument"""

        self.ay = y + height -1
        """Y squares in the lower right. Automatic calculation from the argument"""

        self.mx = (self.x + self.ax) / 2
        """X squares midpoint. Automatic calculation from the argument"""

        self.my = (self.y + self.ay) / 2
        """Y squares midpoint. Automatic calculation from the argument"""

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
