import math
import json
import collections
from geopy.distance import geodesic
from shapely.geometry import LineString

Stop = collections.namedtuple('Stop', ['lon', 'lat'])
Location = collections.namedtuple('Location', ['lon', 'lat'])

INBOUND = True
OUTBOUND = False

ROUTES_ACTIVE = {'54':['54'], '61s':['61A', '61B', '61C', '61D'], '71B':['71B'], '28X':['28X']}
ROUTES_COLOR = {'54':0xFF0000, '61s':0x00FF00, '71B':0x0000FF, '28X':0xFFFF00}
ROUTES_PATTERN = {'54':[7049, 7132], '61s':[7254,6782], '71B':[6571], '28X':[7249]}

STOP_DIST = 100  # (in meters)

ROUTE_DESTINATIONS = {
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

llon = -80.05
rlon = -79.89
blat = 40.40
ulat = 40.48


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(filename, text):
    with open(filename, 'w') as f:
        json.dump(text, f, indent=4)


def distance(a, b):
    return geodesic(a, b).ft


def pathLength(stops):
    d = 0
    for i in range(1, len(stops)):
        d += distance(stops[i-1], stops[i])
    return d


def resampleStops(stops):
    n = int(pathLength(stops) // STOP_DIST)
    line = LineString(stops)
    newStops = [line.interpolate(i/float(n - 1), normalized=True)
                for i in range(n)]
    newStops = [Stop(point.x, point.y) for point in newStops]
    return newStops


def plotPGH(points):
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    import matplotlib.pyplot as plt

    df = pd.DataFrame({'lon':[point.lon for point in points],
                       'lat':[point.lat for point in points]})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

    map = gpd.read_file('data/mapfiles/Neighborhood_SNAP.shp')
    fig, ax = plt.subplots(figsize=(8,8))
    map.plot(ax=ax, alpha=0.4,color='green')
    gdf.plot(ax=ax, color='red', alpha=0.5, markersize=10)
    plt.xlim(llon,rlon)
    plt.ylim(blat,ulat)
    plt.show()

