# -*- coding: UTF-8 -*-
import random, math

list = []
output = {}

for value in xrange(1000000):
    list.append( math.floor(random.random() * 100) )

for item in list:
    for value in xrange(100):
        if (value == item):
            key = int(item)
            output[key] = output.get(key, 0) + 1

for k, v in sorted(output.items()):
    print 'No', k, '->', v
