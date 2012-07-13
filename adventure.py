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

def main():
    logging.basicConfig(filename="adventure.log")

    room1 = Room()
    room2 = Room()
    room3 = Room()
    room4 = Room()
    room5 = Room()
    room6 = Room()
    room7 = Room()
    room8 = Room()
    room9 = Room()

    room1.connect(RIGHT, room2)
    room1.connect(LEFT, room3)
    room1.connect(BACKWARDS, room4)
    room4.connect(RIGHT, room5)
    room4.connect(LEFT, room7)
    room4.connect(BACKWARDS, room6)
    room6.connect(LEFT, room8)
    room6.connect(RIGHT, room9)

    player = characters.Player(room1, 100)

    monsters = []
    monsters.append(characters.Monster(room3, 15))
    monsters.append(characters.Monster(room3, 15))
    monsters.append(characters.Monster(room2, 20))
    monsters.append(characters.Monster(room2, 15))
    monsters.append(characters.Monster(room4, 15))
    monsters.append(characters.Monster(room4, 20))
    monsters.append(characters.Monster(room6, 15))
    monsters.append(characters.Monster(room7, 15))
    monsters.append(characters.Monster(room7, 15))
    monsters.append(characters.Monster(room6, 25))
    wizard = characters.wizard(room6, 25)

    sword = []
    sword.append(items.Sword(room1))

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

class Room(object):
    left = None
    right = None
    forwards = None
    backwards = None
    characters = None
    items = None
  
    def __init__(self):
        self.characters = []
        self.items = []
    def connect(room1, direction, room2):
        if direction == RIGHT:
            room1.right = room2
            room2.left = room1
        elif direction == LEFT:
            room1.left = room2
            room2.right = room1
        elif direction == FORWARDS:
            room1.forwards = room2
            room2.backwards = room1
        elif direction == BACKWARDS:
            room1.backwards = room2
            room2.forwards = room1
        else:
            raise Exception("Invalid direction '%s', choose another direction" % direction)

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.remove(character)

    def get_enemy(self):
        for c in self.characters:
            if not isinstance(c, characters.Player):
                return c
        return None

    def add_items(self, items):
        if isinstance(items, list):
            self.items.extend(items)
            for i in items:
                i.location = self
        else:
            self.items.append(items)
            items.location = self

    def remove_items(self, items):
        if not isinstance(items, list):
            items = [items]
        for i in items:
            self.items.remove(i)

    def display(self):
        """
        This function builds an ascii art image of a single room, and returns the image as a
        list of 5 strings.
        """
        lines = []
        if self.forwards is None:
            lines.append("+-----+")
        else:
            lines.append("+-- --+")

        characters_display = "".join([c.display() for c in self.characters])

        lines.append("|" + characters_display[0:5].center(5) + "|")

        if self.left is None:
            middle_line = "|"
        else:
            middle_line = " "

        middle_line = middle_line + characters_display[5:10].center(5)


        if self.right is None:
            middle_line = middle_line + "|"
        else:
            middle_line = middle_line + " "

        lines.append(middle_line)

        items_display = "".join([i.display() for i in self.items])

        lines.append("|" + items_display[0:5].center(5) + "|")

        if self.backwards is None:
            lines.append("+-----+")
        else:
            lines.append("+-- --+")

        return lines

    def rows(self):
        while self.left is not None:
            self = self.left

        while self is not None:
            yield self
            self = self.right

if __name__ == '__main__':
    sys.exit(main())
