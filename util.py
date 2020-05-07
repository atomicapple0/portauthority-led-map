import math
import json
import collections
from geopy.distance import geodesic
from shapely.geometry import LineString

Stop = collections.namedtuple('Stop', ['lon', 'lat'])
Location = collections.namedtuple('Location', ['lon', 'lat'])

INBOUND = True
OUTBOUND = False

# 54-0 94
# 54-1 19
# 61s-0 94
# 61s-1 13
# 71B-0 78
# 28X-0 87

ROUTES_ACTIVE = {'54':['54'], '61s':['61A', '61B', '61C', '61D'], '71B':['71B'], '28X':['28X']}
ROUTES_COLOR = {'54':0xFF0000, '61s':0x00FF00, '71B':0x0000FF, '28X':0xFFFF00}
ROUTES_PIDS = {'54':[7049, 7132], '61s':[7254,6782], '71B':[6571], '28X':[7154]}
ROUTES_PATTERNS = {'54':['54-0'], '61s':['61s-0','61s-1'], '71B':['71B-0','61s-0'], '28X':['28X-0']}
PATTERNS_ROUTES = {'54-0':['54'],'54-1':['54'],'61s-0':['61','71B'],'61s-1':['61','71B'],'71B-0':['71B'],'28X-0':['28X']}
PATTERNS_PINID = {'54-0':0,'54-1':1,'61s-0':2,'61s-1':3,'71B-0':4,'28X-0':5}
STOP_DIST = 500  # (in "meters")

ROUTES_DESTINATION = {
    '54':
        {'North Side': INBOUND,
         'South Side - South Hills Junct.': OUTBOUND,
         'South Side - Bon Air': OUTBOUND},
    '61A':
        {'Downtown': INBOUND,
         'Braddock': OUTBOUND},
    '61B':
        {'Downtown': INBOUND,
         'Braddock Hills Shopping Ctr': OUTBOUND},
    '61C':
        {'Downtown': INBOUND,
         'Mckeesport': OUTBOUND},
    '61D':
        {'Downtown': INBOUND,
         'Waterfront': OUTBOUND},
    '71B':
        {'Downtown': INBOUND,
         'HIGHLAND PARK': OUTBOUND},
    '28x':
        {'Pittsburgh International Airport': INBOUND,
         'Downtown-Oakland-Shadyside': OUTBOUND},
}

global llon, rlon, blat, ulat

llon = -80.022
rlon = -79.915
blat = 40.422
ulat = 40.467


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(filename, text):
    with open(filename, 'w') as f:
        json.dump(text, f, indent=4)

def flatten(l):
    return [item for sublist in l for item in sublist]


def distance(a, b):
    return geodesic(a, b).ft


def pathLength(stops):
    d = 0
    for i in range(1, len(stops)):
        d += distance(stops[i-1], stops[i])
    return d

def coordDist(unitlessDist):
    return distance((llon,ulat),(llon + unitlessDist,ulat))


def resampleStops(stops, d):
    n = int(pathLength(stops) // d)
    line = LineString(stops)
    newStops = [line.interpolate(i/float(n - 1), normalized=True)
                for i in range(n)]
    newStops = [Stop(point.x, point.y) for point in newStops]
    return newStops


def plotPGH(shapes):
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    import matplotlib.pyplot as plt

    try:
        x = shapes[0][0][0]
    except:
        shapes = [shapes]

    map = gpd.read_file('data/mapfiles/Neighborhood_SNAP.shp')
    fig, ax = plt.subplots(figsize=(10,8))
    map.plot(ax=ax, alpha=0.4,color='green')
    colors = ['b', 'g', 'r', 'c', 'm', 'k', 'w', 'b']
    for i,shape in enumerate(shapes):
        df = pd.DataFrame({'lon':[point.lon for point in shape],
                        'lat':[point.lat for point in shape]})
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
        gdf.plot(ax=ax, color=colors[i], alpha=0.5, markersize=5)
    plt.xlim(llon,rlon)
    plt.ylim(blat,ulat)
    plt.show()

