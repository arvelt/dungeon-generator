# -*- coding: UTF-8 -*-
from dungeon_generator import Generator
import random

config = {
    'row_size': 32,  # default 20
    'col_size': 32,  # default 20
    'room_number' : random.randint(3,10),  # required
    # 'amount_water': 4,  # 0 is nothing water tile, Max 10.
    # 'debug': True,  # Display doors.
}
generatoed_dungeon = Generator(config=config)

# human readble
print generatoed_dungeon.to_string()

# When use in the program.
print generatoed_dungeon.to_array()
