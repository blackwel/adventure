#!/usr/bin/python

import sys
import random
import json
from directions import LEFT, RIGHT, FORWARDS, BACKWARDS
import unittest

def generate(mapname):
    room_count = random.randint(7,15)

    map_dict = dict()
    connections = []
    map_dict['connections'] = connections

    for room_num in range(room_count):
        room_name = "room%d" % (room_num + 1)
        room = dict()
        map_dict[room_name] = room
        
        monster_count = random.randint(0,2)
        for monster_num in range(monster_count):
            create_monster(monster_num, room)

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

    # TODO - add error check that the map can be displayed before we save it

    mapfile = open(mapname, 'w+')
    json.dump(map_dict, mapfile, indent=4)
    mapfile.close()

def opposite(direction):
    if direction is LEFT:
        return RIGHT
    elif direction is RIGHT:
        return LEFT
    elif direction is FORWARDS:
        return BACKWARDS
    elif direction is BACKWARDS:
        return FORWARDS
    else:
        return None

def check_connection(connections, room_name, direction, other_room_name):
    for conect in connections:
        r = conect.keys()[0]
        d = conect[r].keys()[0]
        o = conect[r].values()[0]
        if r == room_name and d is opposite(direction):
            return False
        if o == other_room_name and d is direction:
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

class TestOpposite(unittest.TestCase):
    def test_opposite(self):
        self.assertIs(opposite(LEFT), RIGHT)
        self.assertIs(opposite(RIGHT), LEFT)
        self.assertIs(opposite(FORWARDS), BACKWARDS)
        self.assertIs(opposite(BACKWARDS), FORWARDS)

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.connections = [ { "room2" : { "right" : "room1" } } ]

    def test_same(self):
        # TODO - implement this test case
        pass

    def test_opposite(self):
        # TODO - fix this test failure
        self.assertFalse( check_connection(self.connections, "room7", LEFT, "room2") )

def run_tests():
    unittest.main('generate_map')

if __name__ == '__main__':
    generate(sys.argv[1])
