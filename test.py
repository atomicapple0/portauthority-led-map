import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

# designate coordinate system
crs = {'init':'espc:4326'}
# zip x and y coordinates into single feature
# geometry = [Point(xy) for xy in zip(df[‘longitude’], df[‘latitude’])]

# geo_df = gpd.GeoDataFrame(df,
#  crs = crs,
#  geometry = geometry)

map = gpd.read_file('data/mapfiles/Neighborhood_SNAP.shp')
fig, ax = plt.subplots(figsize=(8,8))
map.plot(ax=ax, alpha=0.4,color='grey')
plt.xlim(-80.05,-79.89)
plt.ylim(40.40,40.48)
# show map
plt.show()