#!/usr/bin/python

import random

class Item(object):
    def __init__(self, location=None):
        self.location = location
        if location:
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

class Potion(Item):
    heal = (10, 25)

    def display(self):
        return 'h'
    
    def use(self, player, room):
        player.remove_items(self)
        h = random.randrange(self.heal[0], self.heal[1])
        print "you heal yourself for %d" %h
        player.health = player.health+h
