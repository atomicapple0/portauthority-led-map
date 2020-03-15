INBOUND = True
OUTBOUND = False

ACTIVE_ROUTES = ['54','61A','61B','61C','61D','71B','28X']

ROUTE_DESTINATIONS = {
    '54': 
        {'North Side' : INBOUND,
         'South Side - South Hills Junct.' : OUTBOUND,
         'South Side - Bon Air' : OUTBOUND},
    '61A': 
        {'Downtown' : INBOUND,
         'Braddock' : OUTBOUND},
    '61B': 
        {'Downtown' : INBOUND,
         'Braddock Hills Shopping Ctr' : OUTBOUND},
    '61C': 
        {'Downtown' : INBOUND,
         'Mckeesport' : OUTBOUND},
    '61D': 
        {'Downtown' : INBOUND,
         'Waterfront' : OUTBOUND},
    '71B': 
        {'Downtown' : INBOUND,
         'HIGHLAND PARK' : OUTBOUND},
    '28X': 
        {'Pittsburgh International Airport' : INBOUND,
         'Downtown-Oakland-Shadyside' : OUTBOUND},
}