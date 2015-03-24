# -*- coding: UTF-8 -*-
import sys, os, random
sys.path.append(os.path.abspath('./src'))
from dungeon_generator import Dungeon

def main():
    config = {
        'row_size': 32,
        'col_size': 32,
        'room_number' : random.randint(3,10),
        'amount_water': 7,
    }
    dungeon = Dungeon(config=config)
    print dungeon.to_string()

main()
#      ^^^  ^  ++++++    ^    ^^
#       ^^  ^^ +_~__+    ^
# ^^^^  ^^  ^^##~___+ ++++++++  ^^
#    +++++++++#+____+^+____~_+^
#    +_____~_+#+___~###~_____+   ^
#    +_______+#+__~_+ +_____~+
#    +~_____~##+++#++ +_~____+^^^
#    +____~__+^  ^#   ++#+++++
#    +++++#+++^   ########     ^
#        ^# ^^^   ^++++++#++   ^
#        ^# ^^^   ^+_____~_+^   ^^
#        ^#^^^^   ^+______~+^^^^ ^
#      +++#++^^^^^^+~______+   ^ ^
#  ^  ^+__~_+^^   ^+___~___+     ^
#  ^   +~___+^^^^^^++++#++++   ^ ^
# ^^   +____+^^  #######      ^^ ^
# ^^^^^+___~###++#+++^^#^^^    ^ ^
#  ^^^^+__~_+^#+_~__+^ ####    ^ ^
#      +++#++ #+___~###^^^#^^^^^^^
#      ^  # ^ #+____+^#   #    ^ ^
#      ^^##^^###~___+^#^++#++++  ^
#  ++++++#++^# +____+^# +_~___+
# ^+_____~_+^# +__~_+^###~____+
# ^+~_____~### ++++++^  +_____+^
#  +_______+   ^     ^  +____~+^
#  +____~__+   ^     ^  +_____+^
# ^+++++++++   ^     ^ ^+__~__+^^
#      ^^^           ^  +++++++^^
#      ^ ^           ^   ^     ^^^
#      ^ ^    ^ ^    ^   ^      ^
# ^^^^^^^^^   ^ ^    ^          ^
#      ^ ^^^^^^^^^^^^^^^^^^    ^^^