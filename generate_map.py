#!/usr/bin/python

import sys
import random
import json

def generate(mapname):
    # TODO pick a random number of rooms to generate
    room_count = random.randint(7,15)

    map_dict = dict()
    connections = []
    map_dict['connections'] = connections

    for room_num in range(room_count):
        # TODO create a room and save it in a dictionary
        room_name = ""
        room = dict()

        # TODO create random monsters
        monster_count = 0
        for monster_num in range(monster_count):
            create_monster(monster_num, room)

        # TODO create random items

        # TODO connect room to another random room in a random direction

        pass

    create_wizard(map_dict)

    # TODO save map to file 'mapname'
    mapfile = open(mapname, 'w+')
    json.dump(map_dict, mapfile, indent=4)
    mapfile.close()

def create_monster(monster_num, room):
    pass
    # TODO - pick a random health
    # TODO - create the monster with the health
    # TODO - add the monster to the current room

def create_wizard(map_dict):
    pass
    # TODO - pick a random room to place the wizard in
    # TODO - pick a random health for the wizard
    # TODO - create the monster with the health
    # TODO - add the wizard to the chosen room


if __name__ == '__main__':
    generate(sys.argv[1])
