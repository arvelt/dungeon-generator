# -*- coding: UTF-8 -*-
from Frame import Frame

class Dungeon:
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
        """Get a human-readable dungeon map.

        :rtype: string
        :return: Fixed-length string with a newline.
        """
        return self.dungeon.to_string()


if __name__ == '__main__':
    config = {
        'row_size': 32,
        'col_size': 32,
        'room_number' : 6
    }
    dungeon = Dungeon(config=config)
    print dungeon.to_string()
