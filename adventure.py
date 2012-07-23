#!/usr/bin/python

# TODO - fix display_all() so that it adds spaces where needed

from directions import LEFT, RIGHT, FORWARDS, BACKWARDS

PICK_UP = intern('pick up')
USE = intern('use')

KONAMICODE = intern('upupdowndown')

QUIT = intern('quit')

ALL_ACTIONS = [LEFT, RIGHT, FORWARDS, BACKWARDS, PICK_UP, USE, QUIT]

import readline
import sys
import random
import logging

import characters
import items
import map

class QuitException(Exception):
    pass

def main():
    logging.basicConfig(filename="adventure.log", filemode='w+', level=logging.DEBUG)
    logging.info("Starting up adventure game")

    player = characters.Player(None, 100)

    try:
        # TODO - map file discovery
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
        for r in row:
            display = r.display()
            display_rooms.append(display)
            #add spaces to the beginning of line to line up room 1 correctly
        for i in range(5):
            line = [r[i] for r in display_rooms]
            print " ".join(line)
        room = room.backwards

def do_action(action, player):
    if action is PICK_UP:
        _items = player.location.items
        player.pickup(_items)
    elif action in [LEFT, RIGHT, FORWARDS, BACKWARDS]:
        try:
            player.move(action)
        except Exception:
            print "you walk straight into a wall great going"
    elif action is USE:
        player.use_items()
    elif action is KONAMICODE:
        print "how much health do you want?" 
        bonus = int(raw_input())
        player.health = player.health + bonus
        print  "your health is %d, you cheater, feel bad"%player.health
    elif action is QUIT:
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

        # TODO - make this accept extra spaces
        action = intern(raw_input())

        do_action(action, player)

        enemy = player.location.get_enemy()
        if enemy is not None:
            enemy.attack(player)

def build_map_grid(room1):
    map_grid = [[]]
    map_width = 0
    map_height = 0

    room1.coords = (0,0)

    next_rooms = [room1]
    done_rooms = set()

    while next_rooms:
        current_room = next_rooms.pop()
        row, col = current_room.coords

        if row => map_height or row < 0 or col >= map_width or col > 0:
            expand_grid(map_grid,row, col)       
        map_grid[row][col] = current_room    
# TODO - add all new neighbors of current_room to next_rooms
        right = current.room.right 
        if right is not None and right not in done_rooms:
            next_rooms.append(right)
        # TODO - calculate coordinates of neighbors
        # TODO - add current_room to done_rooms


    return map_grid

def expand_grid(map_grid, direction):
    # TODO - expand the grid in a given direction
    pass

if __name__ == '__main__':
    sys.exit(main())
