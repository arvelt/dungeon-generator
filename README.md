#Dungeon generator [![Build Status](https://travis-ci.org/arvelt/dungeon-generator.svg?branch=master)](https://travis-ci.org/arvelt/dungeon-generator)

##Demo  
![alt tag](https://raw.github.com/arvelt/dungeon-generator-python/master/examples/demo.gif)

##Usage
```
$ pip install dungeon-generator
```

```
from dungeon import Generator
import random

config = {
    'row_size': 32,
    'col_size': 32,
    'room_number' : random.randint(3,10),
    'amount_water': 7,
}
generatoed_dungeon = Generator()
print dungeon.to_string()

# When use in the program.
print dungeon.to_array()
```

##License
MIT

##Inside API document  
http://arvelt.github.io/dungeon-generator-python/index.html
