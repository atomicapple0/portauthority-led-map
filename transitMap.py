from util import *
from transitApi import *
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
        self.tApi = TransitApi()
        self.tApi.buildRoutes()
        # self.buses = self.getBuses()
        
        pids = ROUTES_PATTERN[id]
        patternMainJSON = self.tApi.getPattern(pids[0])
        patternMain = [Stop(pt['lon'],pt['lat']) for pt in patternMainJSON['pt']]
        self.patternMain = resampleStops(patternMain)

        if len(pids) > 1:
            patternSecondaryJSON = self.tApi.getPattern(pids[1])
            patternSecondary = [Stop(pt['lon'],pt['lat']) for pt in patternSecondaryJSON['pt']]
            patternSecondary = resampleStops(patternSecondary)
            
            line = geom.LineString(self.patternMain)
            patternBranches = []
            isPrevBranch = False
            numBranches = 0
            for point in patternSecondary:
                geompt = geom.Point(point.lon,point.lat)
                unitlessDist = line.distance(geompt)
                dist = coordDist(unitlessDist)
                if dist > STOP_DIST:
                    if isPrevBranch:
                        patternBranches[numBranches - 1].append(point)
                    else:
                        patternBranches.append([point])
                        numBranches += 1
                    isPrevBranch = True
                else:
                    isPrevBranch = False
            
            # for branch in patternBranches:
            #     plotPGH(branch)
            
            extend = True
            while extend and len(patternBranches) > 1:
                extend = False
                extendPatternBranches = []
                for i in range(1,len(patternBranches),2):
                    prevBranch = patternBranches[i-1]
                    currBranch = patternBranches[i]
                    prevLine = geom.LineString(prevBranch)
                    currLine = geom.LineString(currBranch)
                    unitlessDist = prevLine.distance(currLine) 
                    dist = coordDist(unitlessDist)
                    if dist < 50 * STOP_DIST:
                        extendPatternBranches.append(prevBranch + currBranch)
                        extend = True
                    else:
                        extendPatternBranches.append(prevBranch) 
                        extendPatternBranches.append(currBranch)
                odd = [] if len(patternBranches) % 2 == 0 else [patternBranches[len(patternBranches) - 1]]
                patternBranches = extendPatternBranches + odd


            self.patternBranches = []
            for branch in extendPatternBranches:
                if pathLength(branch) > 10 * STOP_DIST:
                    self.patternBranches.append(branch)
            

    
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


T = Transit()

# plotPGH(T.routes['61s'].patternMain)
# plotPGH(T.routes['61s'].patternBranches[0])
# plotPGH(T.routes['61s'].patternBranches[1])
# plotPGH(T.routes['54'].patternMain)
# plotPGH(T.routes['54'].patternBranches[0])
# plotPGH(T.routes['54'].patternBranches[1])

mass = T.routes['28X'].patternMain + T.routes['71B'].patternMain + T.routes['61s'].patternMain +  T.routes['61s'].patternBranches[0] + T.routes['61s'].patternBranches[1] + T.routes['54'].patternMain +  T.routes['54'].patternBranches[0] +  T.routes['54'].patternBranches[1]
plotPGH(mass)
plotPGH(T.routes['71B'].patternMain)