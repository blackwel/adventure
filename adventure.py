#!/usr/bin/python

import readline
import sys
import random

LEFT = intern('left')
RIGHT = intern('right')
FORWARDS = intern('forwards')
BACKWARDS = intern('backwards')

PICK_UP = intern('pick up')
USE = intern('use')

QUIT = intern('quit')

ALL_ACTIONS = [LEFT, RIGHT, FORWARDS, BACKWARDS, PICK_UP, USE, QUIT]


def main():
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

    player = Player(room1, 100)

    monsters = []
    monsters.append(Monster(room3, 15))
    monsters.append(Monster(room3, 15))
    monsters.append(Monster(room2, 20))
    monsters.append(Monster(room2, 15))
    monsters.append(Monster(room4, 15))
    monsters.append(Monster(room4, 20))
    monsters.append(Monster(room6, 15))
    monsters.append(Monster(room6, 5))
    monsters.append(Monster(room6, 5))
    monsters.append(Monster(room7, 25))
    monsters.append(Monster(room7, 25))

    sword = []
    sword.append(Sword(room1))

    while player.is_alive():
        display_all(room1)
        print "what do you want to do this turn pick up an item? or use an item? or move right, left, forwards, or  backwards"
        action = intern(raw_input())
        if action == PICK_UP:
            items = player.location.items
            player.pickup(items)
        elif action in [LEFT, RIGHT, FORWARDS, BACKWARDS]:
            player.move(action)
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

class Actions(object):
    pass

class Item(object):
    def __init__(self, location):
        self.location = location
        location.add_items(self)

    def use(self, player, room):
        print "nothing interesting happens"


class Weapon(Item):
    damage = 0

class Sword(Weapon):
    damage = (5,10)

    def display(self):
        return 's'

    def use(self, player, room):
        print "you attack with a sword"
        enemy = room.get_enemy()
        if enemy is None:
            print "you swing the sword and hit nothing."
            return
        d = random.randrange(self.damage[0], self.damage[1])
        print("you swing the sword for damage %d" %d)
        enemy.damage(d)

class Character(object):
    items = None
    location = None

    def __init__(self, location, health):
        self.items = []
        self.location = location
        location.add_character(self)
        self.health = health

    def move(self, direction):
        new_room = None
        if direction is LEFT:
            new_room = self.location.left
        elif direction is RIGHT:
            new_room = self.location.right
        elif direction is BACKWARDS:
            new_room = self.location.backwards
        elif direction is FORWARDS:
            new_room = self.location.forwards
        if new_room is None: raise Exception('you cannot travle any furthor')

        self.location.remove_character(self)
        new_room.add_character(self)
        self.location = new_room

    def damage(self, damage):
        self.health = self.health - damage
        print("%s has %d health left" % (self.display(), self.health))
        if self.health<= 0:
            self.location.remove_character(self)
            self.location.add_items(self.items)
            print("%s has died by death" % self.display())

    def is_alive(self):
        return self.health>=1

class Player(Character):
    def display(self):
        return "P"
    def pickup(self,items):
        self.items = self.items + items
        for i in items:
            room = i.location
            room.remove_items(i)
    def use_items(self):
        print 'your items are', [i.display() for i in self.items]
        print 'which number item do you want to use?'
        try:
            items = int(raw_input())-1
            items = self.items[items]
        except IndexError:
            print("invalid item")
            return
        items.use(self, self.location)

class Monster(Character):
    hurts  = (1,3)

    def display(self):
        return "M"

    def attack(self, player):
        d = random.randrange(self.hurts[0], self.hurts[1])
        print("the monster swipes at you for damage %d" %d)
        player.damage(d)

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
            if not isinstance(c, Player):
                return c
        return None

    def add_items(self, items):
        if isinstance(items, list):
            self.items.extend(items)
        else:
            self.items.append(items)

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
