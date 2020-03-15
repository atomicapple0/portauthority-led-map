import requests, json
from util import *
from data import *

class TransitApi:
    patApiKey = read('API_KEY.txt').strip()
    domainUrl = 'http://realtime.portauthority.org/bustime/api/v3/'
    routes = None

    def __init__(self, args=None):
        self.params = {'key':self.patApiKey, 'format':'json'}
        self.liveRoutes = []
        if args == 'u':
            self.routes = self.buildRoutes('u')
        else:
            self.routes = self.buildRoutes()
    
    def queryApi(self, method, params=None):
        baseUrl = self.domainUrl + method
        params = params or {}
        params.update(self.params)
        return requests.get(baseUrl,params).json()
    
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
            self.routes[routes_json[i]['rt']] = {k:v for k,v in routes_json[i].items() if k != 'rt'}
        self.buildStops()
        write_json('data/routes.json', self.routes)
        return self.routes
    
    def buildStops(self, rts=None):
        if rts == None:
            rts = [*self.routes.keys()]
        for rt in rts:
            params = {'rt':rt, 'dir':'INBOUND', 'rtpidatafeed':'Port Authority Bus'}
            stops = self.queryApi('getstops', params)['bustime-response']
            if 'stops' in stops:
                self.routes[rt]['stops'] = stops['stops']
                print(rt + ' : ' + str(len(stops['stops'])))
                self.liveRoutes.append(rt)