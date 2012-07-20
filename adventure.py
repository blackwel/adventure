#!/usr/bin/python

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

class QuitException(Exception):
    pass

def main():
    logging.basicConfig(filename="adventure.log")

    player = characters.Player(None, 100)

    try:
        for level in (1, 2):
            mapname = "adventure%d.map" % level

            play_level(mapname, player)

            if not player.is_alive():
                return
    except QuitException:
        pass

def display_all(room):
    #todo move room forwards as much as possible
    while room is not None:
        row = room.rows()
        display_rooms = []
        for r in row:r
            display = r.display()
            display_rooms.append(display)
            #add spaces to the beginning of line to line up room 1 correctly
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
        raise QuitException()
    else:
        print "I didn't understand '%s', must be one of %r" % (action, ALL_ACTIONS)
    return True

def play_level(mapname, player):
    room1, wizard = map.create_map(mapname)
    room1.add_character(player)
    player.location = room1

    map_grid = build_map_grid(room1)

    while player.is_alive() and wizard.is_alive(): 
        display_all(room1)
        print "what do you want to do this turn pick up an item? or use an item? or move right, left, forwards, or  backwards"
        action = intern(raw_input())

        do_action(action, player)

        enemy = player.location.get_enemy()
        if enemy is not None:
            enemy.attack(player)

def build_map_grid(room1):
    map_grid = [[room1]]

    room1.coords = (0,0)

    next_rooms = [room1]
    done_romms = set()

    while next_rooms:
        current_room = next_rooms.pop()
        # TODO - calculate coordinates of current_room
        # TODO - expand map_grid if necessary
        # TODO - put current_room into map_grid at its coordinates
        # TODO - add all new neighbors of current_room to next_rooms

    return map_grid

def expand_grid(map_grid, direction):
    # TODO - expand the grid in a given direction
    pass

if __name__ == '__main__':
    sys.exit(main())
