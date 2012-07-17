#!/usr/bin/python

from adventure import RIGHT, LEFT, BACKWARDS, FORWARDS
import characters
import items
import logging
import json
import itertools

def create_map(filename="adventure.map"):    

    mapfile = open(filename)

    map_dict = json.load(mapfile)

    room_dict = map_dict["room1"]

    directions = set((LEFT, RIGHT, BACKWARDS, FORWARDS))

    room_contents = (k for k in room_dict.keys() if k not in directions)

    modules = itertools.chain(
        characters.__dict__.iteritems(),
        items.__dict__.iteritems())
    types = dict(((k,v) for (k,v) in modules if type(v) is type))

    wizard = None

    room = Room()
    for k in room_contents:
        entry = room_dict[k]
        classname = entry.pop('class')
        _type = types[classname]
        item = _type(location=room, **entry)
        if isinstance(item, characters.Character):
            room.add_character(item)
        elif isinstance(item, items.Item):
            room.add_items(item)
        else:
            raise Exception("invalid entry in room")
        if isinstance(item, characters.wizard):
            wizard = item

    return room, wizard

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

    return room1, wizard

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
