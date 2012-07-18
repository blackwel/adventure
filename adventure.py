#!/usr/bin/python

# TODO - load a second map once the game has ended.
# TODO - add cheats
# TODO - build a map creator applicaton
# TODO - fix display_all() so that it adds spaces where needed

LEFT = intern('left')
RIGHT = intern('right')
FORWARDS = intern('forwards')
BACKWARDS = intern('backwards')

PICK_UP = intern('pick up')
USE = intern('use')

KONAMICODE = intern('upupdowndown')

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

    level = 1
    mapname = "adventure%d.map" % level

    room1, wizard = map.create_map(mapname)

    player = characters.Player(room1, 100)

    while player.is_alive() and wizard.is_alive(): 
        display_all(room1)
        print "what do you want to do this turn pick up an item? or use an item? or move right, left, forwards, or  backwards"
        action = intern(raw_input())

        keep_playing = do_action(action, player)
        if not keep_playing:
            break

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

def do_action(action, player):
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
    elif action == KONAMICODE:
        print "how much health do you want?" 
        bonus = int(raw_input())
        player.health = player.health + bonus
        print  "your health is %d, you cheater, feel bad"%player.health
    elif action == QUIT:
        return False
    else:
        print "I didn't understand '%s', must be one of %r" % (action, ALL_ACTIONS)
    return True

if __name__ == '__main__':
    sys.exit(main())
