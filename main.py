from dungeon import Generator
import random

config = {
    'row_size': 32,
    'col_size': 32,
    'room_number' : random.randint(3,10),
    'amount_water': 7,
}
generatoed_dungeon = Generator()
print generatoed_dungeon.to_string()
