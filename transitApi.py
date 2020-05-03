import requests
import json
from util import *


class TransitApi:
    # ----- JSON STRUCTURE -----
    # _.routes.keys() = dict_keys(['BLLB', 'BLSV', ... <route ids> ])
    # _.routes['61A'] =
    #     {'rtnm':'NORTH BRADDOCK',
    #     'rtclr':'#e0ffff',
    #     'rtdd':'61A',
    #     'rtpidatafeed': 'Port Authority Bus',
    #     'pattern': {'INBOUND': [<Point> ...], 'OUTBOUND': [<Point> ...]}
    #     'stops': [{'stpid': '2644', 'stpnm': '5TH AVE + #2358', 'lat': 40.43_, 'lon': -79.97_}, {...}, ... <stops>]
    # --------------------------
    patApiKey = read('API_KEY.txt').strip()
    domainUrl = 'http://realtime.portauthority.org/bustime/api/v3/'
    routes = None

    def __init__(self, args=None):
        self.params = {'key': self.patApiKey, 'format': 'json'}
        self.liveRoutes = []
        if args == 'u':
            self.routes = self.buildRoutes('u')
        else:
            self.routes = self.buildRoutes()

    # ----- Method List -----
    # getroutes | rt, rtpidatafeed
    # getpatterns | rt, rtpidatafeed
    # getstops | rt, dir, stpid
    # getvehicles | vid, rt, tmres, rtpidatafeed
    # -----------------------
    def queryApi(self, method, params=None):
        baseUrl = self.domainUrl + method
        params = params or {}
        params.update(self.params)
        return requests.get(baseUrl, params).json()

    def buildRoutes(self, args=None):
        if args != 'u':
            try:
                self.routes = read_json('data/routes.json')
                return self.routes
            except IOError:
                None
        print('bypassing routes.json, using api')
        routes_json = self.queryApi('getroutes')['bustime-response']['routes']
        self.routes = {}
        for i in range(len(routes_json)):
            self.routes[routes_json[i]['rt']] = {k: v for k, v in routes_json[i].items() if k != 'rt'}
        write_json('data/routes.json', self.routes)
        return self.routes

    def buildStops(self, rts=None):
        if rts == None:
            rts = [*self.routes.keys()]
        for rt in rts:
            params = {'rt': rt, 'dir': 'INBOUND',
                      'rtpidatafeed': 'Port Authority Bus'}
            stopsIN = self.queryApi('getstops', params)['bustime-response']
            params = {'rt': rt, 'dir': 'OUTBOUND',
                      'rtpidatafeed': 'Port Authority Bus'}
            stopsOUT = self.queryApi('getstops', params)['bustime-response']
            stops = stopsIN + stopsOUT
            if 'stops' in stops:
                self.routes[rt]['stops'] = stops['stops']
                print(rt + ' : ' + str(len(stops['stops'])))
                self.liveRoutes.append(rt)

    def getPattern(self,pid):
        print(pid)
        params = {'pid': pid, 'rtpidatafeed': 'Port Authority Bus'}
        pattern = self.queryApi('getpatterns', params)['bustime-response']['ptr'][0]
        return pattern


    def getBuses(self, rt):
        params = {'rt': rt}
        return self.queryApi('getvehicles', params)['bustime-response']['vehicle']
