from util import *
from transitApi import *
import shapely.geometry as geom

global tApi
tApi = TransitApi()
tApi.buildRoutes()


class StopLED:
    def __init__(self, routes, lon, lat):
        self.lon = lon
        self.lat = lat
        self.routes = routes
        self.buses = {route: False for route in routes}
        self.color = None


class Pattern:
    def __init__(self, pid, stops):
        self.routes = PATTERNS_ROUTES[pid]
        self.pid = pid
        self.stops = [StopLED(self.routes, stop[0], stop[1]) for stop in stops]
        self.pin = PATTERNS_PINID[pid]
        self.stled = 0
        self.numled = len(stops)

global routePatterns
routePatterns = read_json('data/routePatterns.json')
routePatterns = {pid:Pattern(pid, pattern) for (pid,pattern) in routePatterns.items()}


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
        self.patterns = {pid:routePatterns[pid] for pid in ROUTES_PATTERNS[self.id]}
        self.penalty = {pid:0 for pid in ROUTES_PATTERNS[self.id]}

    def getBuses(self):
        busesJSON = self.tApi.getBuses(self.id)
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
    # _.routes.keys() = dict_keys(['54', '61s', ... <route ids> ])
    # _.routes['61s'] = <Route object>
    # --------------------------

    def __init__(self):
        self.routes = {}
        for rtName in ROUTES_ACTIVE.keys():
            self.routes[rtName] = Route(rtName)
        self.routes['71B'].penalty['61s-0'] = 100

        

T = Transit()
