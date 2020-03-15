from util import *

class Bus:
    def __init__(self, id, route, destination, lat, lon, timestamp):
        self.id = id
        self.route = route
        direction = None #### To Do ####
        self.direction = direction
        self.location = (lat,lon)
        self.timestamp = timestamp
        self.currStop = None

class Route:
    def __init__(self, id, color, stops, n):
        self.id = id
        self.color = color
        self.stops = self.resampleStops(stops, n)
        self.bus_ids = None
        self.buses = None
    
    def resampleStops(self, stops, n):
        I = pathLength(stops) / (n-1)
        D = 0
        newStops = stops[0]
        for i in range(1,len(stops)):
            d = distance(stops[i-1],stops[i])
            if (D+d) >= I:
                q = Stop()
                q.x = stops[i-1] + ((I-D)/d) * (stops[i] - stops[i-1])
                q.y = stops[i-1] + ((I-D)/d) * (stops[i] - stops[i-1])
                newStops.append(q)
                stops.insert(i,q)
                D = 0
            else:
                D = D+d
        return newStops