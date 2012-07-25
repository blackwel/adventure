#!/usr/bin/python

# TODO - fix duplicate pick up of second potion

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
        for level in range(1,4):
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

def display_grid(map_grid):
    for row in map_grid:
        display_rooms = []
        for r in row:
            display = None
            if r is None:
                display = ["       " for i in xrange(5)]
            else:
                display = r.display()
            display_rooms.append(display)
        for i in range(5):
            line = [r[i] for r in display_rooms]
            print " ".join(line)

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
        display_grid(map_grid)
        print "what do you want to do this turn pick up an item? or use an item? or move right, left, forwards, or  backwards"

        # TODO - make this accept extra spaces
        action = intern(raw_input())

        do_action(action, player)

        enemy = player.location.get_enemy()
        if enemy is not None:
            enemy.attack(player)

def build_map_grid(room1):
    map_grid = [[None]]
    map_width = 0
    map_height = 0

    room1.coords = [0,0]

    next_rooms = [room1]
    done_rooms = set()

    while next_rooms:
        current_room = next_rooms.pop()
        row, col = current_room.coords

        logging.debug("row, col: %d %d"  % (row, col))
        if row >= map_height or row < 0 or col >= map_width or col > 0:
            offset = expand_grid(map_grid,row, col, next_rooms)
            current_room.coords[0] = current_room.coords[0] + offset[0]
            current_room.coords[1] = current_room.coords[1] + offset[1]
            row = row + offset[0]
            col = col + offset[1]

        logging.debug("expanded row, col: %d %d   size: %d %d" %
                      (row, col, len(map_grid), len(map_grid[0])))
        logging.debug("row length: %d" % len(map_grid[row]))
        if map_grid[row][col] is not None:
            raise Exception("duplicate room")
        map_grid[row][col] = current_room
    
        right = current_room.right 
        if right is not None and right not in done_rooms:
            next_rooms.append(right)
            right.coords = [row, col + 1]

        forwards = current_room.forwards 
        if forwards is not None and forwards not in done_rooms:
            next_rooms.append(forwards)
            forwards.coords = [row -1, col]

        backwards = current_room.backwards 
        if backwards is not None and backwards not in done_rooms:
            next_rooms.append(backwards)
            backwards.coords = [row +1, col]

        left  = current_room.left 
        if left is not None and left not in done_rooms:
            next_rooms.append(left)
            left.coords = [row, col - 1]
        done_rooms.add(current_room)

    # TODO - check why there are extra blank rows at the end

    return map_grid

def expand_grid(map_grid, row, col, next_rooms):
    height = len(map_grid)
    width = len(map_grid[0])

    offset = [0, 0]

    if row < 0:
        logging.debug("expanding backwards")
        offset[0] = 1
        new_row = [None for i in range(width)]
        map_grid.insert(0, new_row)
    if col < 0:
        logging.debug("expanding left")
        offset[1] = 1
        width = width +1 
        for row in map_grid:
            row.insert(0, None)
    if row >= height:
        logging.debug("expanding backwards")
        new_row = [None for i in range(width)]
        map_grid.append(new_row)
    if col >= width:
        logging.debug("expanding right")
        for row in map_grid:
            row.append(None)

    for row in map_grid:
        for room in row:
            if room is not None:
                room.coords[0] = room.coords[0] + offset[0]
                room.coords[1] = room.coords[1] + offset[1]

    for room in next_rooms:
        room.coords[0] = room.coords[0] + offset[0]
        room.coords[1] = room.coords[1] + offset[1]
    return offset

if __name__ == '__main__':
    sys.exit(main())
