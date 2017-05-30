# -*- coding: UTF-8 -*-
from Frame import Frame
import random

class Generator(object):
    """ Generator two-dimensional map for roguelike.

        Config:

        - row_size: Vertical size of the map.
        - col_size: Horizontal size of the map.
        - room_number: Number of rooms to pop in the map.
    """
    def __init__(self, config={}):
        self.row_size = config.get('col_size', 20)
        self.col_size = config.get('row_size', 20)
        self.dungeon = Frame(self.col_size, self.row_size, config)

    def to_string(self):
        """ Call Frame.to_string()

            See Frame.to_string detail.
        """
        return self.dungeon.to_string()

    def to_array(self):
        """ Call Frame.to_array()

            See Frame.to_array detail.
        """
        return self.dungeon.to_array()
