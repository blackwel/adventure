#!/usr/bin/python

from directions import RIGHT, LEFT, BACKWARDS, FORWARDS
import characters
import items
import logging
import json
import itertools

directions = set((LEFT, RIGHT, BACKWARDS, FORWARDS))


def load_types(*args):
    modules = itertools.chain(*[m.__dict__.iteritems() for m in args])
    return dict(((k,v) for (k,v) in modules if type(v) is type))

types = load_types(characters, items)

def create_map(filename="adventure.map"):    

    mapfile = open(filename)

    map_dict = json.load(mapfile, strict=False)

    wizard = None

    connections = map_dict.pop('connections')
    rooms = dict()

    for room_name in map_dict.keys():
        room_dict = map_dict[room_name]
        room_contents = room_dict.keys()

        room = Room()
        for k in room_contents:
            #print k
            entry = room_dict[k]
            classname = entry.pop('class')
            _type = None
            try:
                _type = types[classname]
            except KeyError as er:
                logging.error("type not found! %r, types: %r" %
                              (er, types.keys()))
                raise
            item = _type(location=room, **entry)
            if isinstance(item, characters.wizard):
                wizard = item
        rooms[room_name] = room

    for c in connections:
        room_name = c.keys()[0]
        direction, other_room = c[room_name].items()[0]
        #print room_name, direction, other_room
        room = rooms[room_name]
        other = rooms[other_room]
        direction = intern(str(direction))
        room.connect(direction, other)

    return rooms['room1'], wizard

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
        if direction is RIGHT:
            room1.right = room2
            room2.left = room1
        elif direction is LEFT:
            room1.left = room2
            room2.right = room1
        elif direction is FORWARDS:
            room1.forwards = room2
            room2.backwards = room1
        elif direction is BACKWARDS:
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
