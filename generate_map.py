#!/usr/bin/python

import sys
import random

def generate(mapname):
    # TODO pick a random number of rooms to generate
    room_count = random.randint(7,15)

    for room_num in range(room_count):
        # TODO create a room and save it in a dictionary

        # TODO create random monsters

        # TODO create random items

        # TODO connect room to another random room in a random direction

        pass

    # TODO create wizard

    # TODO save map to file 'mapname'

if __name__ == '__main__':
    generate(sys.argv[1])
