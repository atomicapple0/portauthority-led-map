from util import *
from transitApi import *
import shapely.geometry as geom


def filterStopsBoundingBox(stops, llon, rlon, blat, ulat):
    def isInBox(stop, llon, rlon, blat, ulat):
        return llon <= stop.lon and stop.lon <= rlon and blat <= stop.lat and ulat <= ulat
    return [stop for stop in stops if isInBox(stop, llon, rlon, blat, ulat)]

def scaleLat(stops,s):
    for i,stop in enumerate(stops) :
        stop = Stop(stop.lon, blat + (stop.lat - blat) * s)
        stops[i] = stop
    return stops

global tApi
tApi = TransitApi()

routePatterns = {}

for rtid in ROUTES_ACTIVE.keys():

    pids = ROUTES_PATTERN[rtid]
    patternMainJSON = tApi.getPattern(pids[0])
    patternMain = [Stop(pt['lon'], pt['lat']) for pt in patternMainJSON['pt']]
    patternMain = resampleStops(patternMain, 100)

    routePatterns[rtid + '-0'] = patternMain
    if len(pids) > 1:
        patternSecondaryJSON = tApi.getPattern(pids[1])
        patternSecondary = [Stop(pt['lon'], pt['lat']) for pt in patternSecondaryJSON['pt']]

        line = geom.LineString(patternMain)
        patternSecondaryFilter = []
        numBranches = 0
        for point in patternSecondary:
            geompt = geom.Point(point.lon, point.lat)
            unitlessDist = line.distance(geompt)
            dist = coordDist(unitlessDist)
            if dist > 100:
                patternSecondaryFilter.append(point)
        routePatterns[rtid + '-1'] = patternSecondaryFilter

temp61s = routePatterns['61s-1'] 
routePatterns['61s-1'] = filterStopsBoundingBox(temp61s,-80,-79.96,40.43,40.445)
routePatterns['61s-2'] = filterStopsBoundingBox(temp61s,-79.94,-79.90,40.41,40.44)
routePatterns['54-1'] = filterStopsBoundingBox(routePatterns['54-1'],-79.99,-79.94,40.44,40.47)
routePatterns['71B-temp'] = filterStopsBoundingBox(routePatterns['71B-0'],-79.93,-79.91,40.45,40.48)
routePatterns['71B-0'] = [stop for stop in routePatterns['71B-0'] if stop not in routePatterns['71B-temp']]
def scaleLatAll(routePatterns,s):
    for id in routePatterns.keys():
        routePatterns[id] = filterStopsBoundingBox(routePatterns[id], llon, rlon, blat, ulat)
        routePatterns[id] = scaleLat(routePatterns[id], s)
        routePatterns[id] = resampleStops(routePatterns[id], STOP_DIST)
        routePatterns[id] = scaleLat(routePatterns[id], 1 / s)
scaleLatAll(routePatterns,2.5)
temp = {0:routePatterns['61s-2'], 1:routePatterns['71B-temp']}
scaleLatAll(temp,6)
routePatterns['61s-2'] = temp[0]
del routePatterns['71B-temp']
routePatterns['71B-0'] += temp[1]
fullRoutes = [routePatterns[id] for id in routePatterns.keys()]
plotPGH(fullRoutes)
print(len(flatten(fullRoutes)))

write_json('data/routeShapes.json',routePatterns)