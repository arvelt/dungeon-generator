# -*- coding: UTF-8 -*-
class Dungeon:
    max_row = 32
    max_col = 32
    dungeon = [[0 for col in xrange(max_col)] for row in xrange(max_row)]

    def __init__(self):
        self.split_space()

    def to_string(self):
        for row in self.dungeon:
            print ''.join([str(col) for col in row])

    def split_space(self):
        self.fill_range(3, 0, 0, self.max_row, self.max_col)

    def fill_range(self, count, start_row, start_col, end_row, end_col):
        begin_row = start_row
        begin_col = start_col
        target_row = end_row
        target_col = end_col
        for row_index, row in enumerate(self.dungeon[start_row:end_row]):
            for col_index, col in enumerate(row[start_col:end_col]):
                target_range = self.dichotomous_split(count, row_index, start_row, start_col, col_index, end_row, end_col)
                begin_row = target_range[0]
                begin_col = target_range[1]
                target_row = target_range[2]
                target_col = target_range[3]

        count = count - 1
        if (count == 0):
            return
        else:
            self.fill_range(count, begin_row, begin_col, target_row, target_col)

    def dichotomous_split(self, count, row_index, start_row, start_col, col_index, end_row, end_col):
        begin_row = start_row
        begin_col = start_col
        target_row = end_row
        target_col = end_col

        if (count % 2 == 0):
            target_row = (end_row - start_row) / 2
            if (row_index == target_row):
                self.dungeon[row_index][col_index] = 1
        else :
            target_col = (end_col - start_col) / 2
            if (col_index == target_col):
                self.dungeon[row_index][col_index] = 1

        return (
            begin_row,
            begin_col,
            target_row,
            target_col
        )


dungeon = Dungeon()
dungeon.to_string()
