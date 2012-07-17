#!/usr/bin/python

#build a file format for the map
#


LEFT = intern('left')
RIGHT = intern('right')
FORWARDS = intern('forwards')
BACKWARDS = intern('backwards')

PICK_UP = intern('pick up')
USE = intern('use')

QUIT = intern('quit')

ALL_ACTIONS = [LEFT, RIGHT, FORWARDS, BACKWARDS, PICK_UP, USE, QUIT]

import readline
import sys
import random
import characters
import items
import logging
import map

def main():
    logging.basicConfig(filename="adventure.log")

    room1, wizard = map.create_map()

    player = characters.Player(room1, 100)

    while player.is_alive() and wizard.is_alive(): 
        display_all(room1)
        print "what do you want to do this turn pick up an item? or use an item? or move right, left, forwards, or  backwards"
        action = intern(raw_input())
        if action == PICK_UP:
            _items = player.location.items
            player.pickup(_items)
        elif action in [LEFT, RIGHT, FORWARDS, BACKWARDS]:
            try:
                player.move(action)
            except Exception:
                print "you walk straight into a wall great going"
        elif action == USE:
            player.use_items()
        elif action == QUIT:
            break
        else:
            print "I didn't understand '%s', must be one of %r" % (action, ALL_ACTIONS)

        enemy = player.location.get_enemy()
        if enemy is not None:
            enemy.attack(player)

def display_all(room):
    while room is not None:
        row = room.rows()
        display_rooms = []
        for r in row:
            display = r.display()
            display_rooms.append(display)
        for i in range(5):
            line = [r[i] for r in display_rooms]
            print " ".join(line)
        room = room.backwards


if __name__ == '__main__':
    sys.exit(main())
