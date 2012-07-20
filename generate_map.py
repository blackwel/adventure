#!/usr/bin/python

import sys
import random
import json
from adventure import LEFT, RIGHT, FORWARDS, BACKWARDS

def generate(mapname):
    # TODO pick a random number of rooms to generate
    room_count = random.randint(7,15)

    map_dict = dict()
    connections = []
    map_dict['connections'] = connections

    for room_num in range(room_count):
        # TODO create a room and save it in a dictionary
        room_name = "room%d" % (room_num + 1)
        room = dict()
        map_dict[room_name] = room
        

        # TODO create random monsters
        monster_count = random.randint(0,2)
        for monster_num in range(monster_count):
            create_monster(monster_num, room)

        # TODO create random items

        if room_num > 0:
            while True:
                other_room_num = random.randint(1, room_num)
                other_room_name = "room%d" % other_room_num
                direction = random.choice((LEFT, RIGHT, FORWARDS, BACKWARDS))
                if check_connection(connections, room_name, direction, other_room_name):
                    connection = { room_name : { direction : other_room_name } }
                    connections.append(connection)
                    break

    create_wizard(map_dict, room_count)

    mapfile = open(mapname, 'w+')
    json.dump(map_dict, mapfile, indent=4)
    mapfile.close()

def opposite(direction):
    if direction == LEFT:
        return RIGHT
    elif direction == RIGHT:
        return LEFT
    elif direction == FORWARDS:
        return BACKWARDS
    elif direction == BACKWARDS:
        return FORWARDS
    else:
        return None

def check_connection(connections, room_name, direction, other_room_name):
    for conect in connections:
        r = conect.keys()[0]
        d = conect[r].keys()[0]
        o = conect[r].values()[0]
        if r == room_name and d == opposite(direction):
            return False
        if o == other_room_name and d == direction:
            return False
    return True

def create_monster(monster_num, room):
    health = random.randint(10,25)
    monster_name = "monster%d" % monster_num
    monster = { 'class' : 'Monster', 'health': health }
    room[monster_name] = monster

def create_wizard(map_dict, num_rooms):
    health = random.randint(20,30)
    wizard  = { 'class' : 'wizard', 'health': health }

    room_num = random.randint(1, num_rooms)
    room_name = "room%d" % room_num
    room = map_dict[room_name]
    room["wizard"] = wizard
    # TODO - add the wizard to the chosen room

if __name__ == '__main__':
    generate(sys.argv[1])
