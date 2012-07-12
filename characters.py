#!/usr/bin/python

from adventure import LEFT, RIGHT, FORWARDS, BACKWARDS
import items
import random

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

    def __init__(self, location, health):
        Character.__init__(self, location, health)
        if random.random() < 0.3:
            self.items.append(items.Potion())
  
    def display(self):
        return "M"

    def attack(self, player):
        d = random.randrange(self.hurts[0], self.hurts[1])
        print("the monster swipes at you for damage %d" %d)
        player.damage(d)
