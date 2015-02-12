# -*- coding: UTF-8 -*-
import random, math

class Tile:
    TILE = 0
    WALL = 2
    WAY = 5
    PARTING_LINE = 1

    kind = TILE
    x = 0
    y = 0
    max_row = 0
    max_col = 0

    def __init__(self, x, y, max_row, max_col):
        self.x = x
        self.y = y
        self.max_row = max_row
        self.max_col = max_col



class Dungeon:
    max_row = 32
    max_col = 32
    min_size = 10
    dungeon = [[Tile(row, col, max_row, max_col) for col in xrange(max_col)] for row in xrange(max_row)]

    def __init__(self):
        self.split_space()

    def to_string(self):
        for row in self.dungeon:
            print ''.join([str(col.kind) for col in row])

    def split_space(self):
        room_size = {
            'start_row': 0,
            'start_col': 0,
            'end_row': self.max_row,
            'end_col': self.max_col
        }

        probability = math.floor(random.random() * 100)
        if probability < 50:
            count = 0
        else:
            count = 1

        probability = math.floor(random.random() * 100)
        if probability < 50:
            state = 0
        else:
            state = 1

        self.fill_range(room_size, count, state)

    def fill_range(self, room_size, count, state):
        start_row = room_size.get('start_row')
        start_col = room_size.get('start_col')
        end_row = room_size.get('end_row')
        end_col = room_size.get('end_col')

        new_size = self.dichotomous_split(room_size, count, state)

        for row_index, row in enumerate(self.dungeon[start_row:end_row]):
            for col_index, col in enumerate(row[start_col:end_col]):
                if (row_index == new_size.get('target_row') and new_size.get('target_col') is None):
                    self.dungeon[row_index][col_index].kind = Tile.PARTING_LINE
                if (col_index == new_size.get('target_col') and new_size.get('target_row') is None):
                    self.dungeon[row_index][col_index].kind = Tile.PARTING_LINE

        count = count + 1
        rest_row = new_size.get('end_row') - new_size.get('start_row')
        rest_col = new_size.get('end_col') - new_size.get('start_col')

        if (rest_row < self.min_size and rest_col < self.min_size):
            return
        else:
            self.fill_range(new_size, count, state)

    def dichotomous_split(self, room_size, count, state):
        begin_row = room_size.get('start_row')
        begin_col = room_size.get('start_col')
        end_row = room_size.get('end_row')
        end_col = room_size.get('end_col')

        width = end_row - begin_row
        height = end_col - begin_col

        if (count % 2 == 0):
            target_row = width / 2
            target_col = None
            end_row = target_row

        else :
            target_row = None
            target_col = height / 2
            end_col = target_col

        return {
            'start_row': begin_row,
            'start_col': begin_col,
            'end_row': end_row,
            'end_col': end_col,
            'target_row': target_row,
            'target_col': target_col
        }


dungeon = Dungeon()
dungeon.to_string()
