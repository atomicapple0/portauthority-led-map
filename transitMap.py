from util import *
from transitApi import TransitApi
import shapely.geometry as geom


class Bus:
    def __init__(self, route, id, destination, lon, lat):
        self.id = id
        self.route = route
        self.location = Location(lon, lat)
        self.currStop = None

class Route:
    # ----- DATA STRUCTURE -----
    # _.id = ('61A', '61B', '61C', '61D')
    # _.color = '#123456'
    # _.stops = [... (lon,lat)]
    # _.buses = [... <Bus object>]
    # --------------------------

    def __init__(self, id):
        self.id = id
        self.subroutes = ROUTES_ACTIVE[id]
        self.color = ROUTES_COLOR[id]
        # self.buses = self.getBuses()
        
        pids = ROUTES_PATTERN[id]
        print(pids)
        patternMainJSON = tApi.getPattern(pids[0])
        patternMain = [Stop(pt['lon'],pt['lat']) for pt in patternMainJSON['pt']]
        self.patternMain = resampleStops(patternMain)

        if len(pids) > 1:
            patternBranchJSON = tApi.getPattern(pids[1])
            patternBranch = [Stop(pt['lon'],pt['lat']) for pt in patternBranchJSON['pt']]
            patternBranch = resampleStops(patternBranch)
            
            line = geom.LineString(self.patternMain)
            self.patternBranch = []
            for point in patternBranch:
                geompt = geom.Point(point.lon,point.lat)
                unitlessDist = line.distance(geompt)
                dist = distance((llon,ulat),(llon + unitlessDist,ulat))
                if dist > STOP_DIST:
                    print(dist)
                    self.patternBranch.append(point)

    
    def getBuses(self):
        busesJSON = tApi.getBuses(self.id)
        buses = []
        for busJSON in busesJSON:
            busJSON = busJSON
            buses.append(Bus(self.id,
                             busJSON['vid'],         
                             busJSON['des'],
                             busJSON['lon'],
                             busJSON['lat']))
        return buses

class Transit:
    # ----- DATA STRUCTURE -----
    # _.routes.keys() = dict_keys(['BLLB', 'BLSV', ... <route ids> ])
    # _.routes['61A'] = <Route object>
    # --------------------------

    def __init__(self):
        self.routes = {}
        for rtName in ROUTES_ACTIVE.keys():
            self.routes[rtName] = Route(rtName)

    # def all(self):
    #     for rtid in ROUTES_ACTIVE:
    #         yield self.routes[rtid]

    # def get(self, rtid):
    #     return self.routes[rtid]

global tApi
tApi = TransitApi()
tApi.buildRoutes()

T = Transit()

plotPGH(T.routes['61s'].patternMain)
plotPGH(T.routes['61s'].patternBranch)
plotPGH(T.routes['54'].patternMain)
plotPGH(T.routes['54'].patternBranch)

