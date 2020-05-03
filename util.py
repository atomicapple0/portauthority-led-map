import math
import json
import collections
from geopy.distance import geodesic


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(filename, text):
    with open(filename, 'w') as f:
        json.dump(text, f, indent=4)


Stop = collections.namedtuple('Stop', ['x', 'y'])


def distance(a, b):
    return geodesic(a, b).m


def pathLength(stops):
    d = 0
    for i in range(1, len(stops)):
        d += distance(stops[i-1], stops[i])
    return d
