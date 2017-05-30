# Dungeon generator [![Build Status](https://travis-ci.org/arvelt/dungeon-generator.svg?branch=master)](https://travis-ci.org/arvelt/dungeon-generator)

## Demo  
![alt tag](https://raw.github.com/arvelt/dungeon-generator/master/examples/demo.gif)

## Usage
```
$ pip install dungeon-generator
```

```
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
```

```
Items.
+ is walls.
- is floors.
# is loads.
^ is water.
~ is near by door. (in debug only)
```


## License
MIT

## Inside API document  
http://arvelt.github.io/dungeon-generator/index.html
