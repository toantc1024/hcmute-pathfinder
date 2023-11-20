import json
from math import * 
METER = 1000
def HaversineDistance(first, second):
    lat1, lon1 = first
    lat2, lon2 = second
    R = 6378137 # this is in miles.  For Earth radius in kilometers use 6372.8 km
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    return R * c


class Graph:
    def __init__(self):
        self.graph = {}

    def addNeighbor(self, source, target):
        self.graph[source]["neighbors"].append(target)
    

    
    def getNodeProps(self, nodeId, props="info"):
        return self.graph[nodeId][props]
    def getNodePosition(self, nodeId):
        position = self.getNodeProps(nodeId)["geometry"]["coordinates"]
        return (position[0], position[1])
    
    def initNewNode(self, nodeId, info=""):
        self.graph[nodeId] = {"info": info, "neighbors": []}

graph = Graph()

with open('sample.json', 'r') as f:
    data = json.load(f)
    # Loop through all node and init a dict of node

    for entry in data["features"]:
        if (entry["properties"]["type"] == "node"):
            # Check if entry["properties"]["id"] in Graph 
            id = str(entry["properties"]["id"])
            graph.initNewNode(id, entry)
    # Loop through data as entrie
    types = {}
    buildings = {}
    for entry in data['features']:
        # Loop through data as key-value pairs
        types[entry["properties"]["type"]] = types.get(entry["properties"]["type"], 0) + 1
    #        "type": "way",
    #     "id": 239936581,
    #     "tags": {
    #       "building": "yes",
    #       "name": "X\u01b0\u1edfng TH Ngh\u1ec1 2"
    #     },
    #     "nodes": [2477049479, 2477049480, 2477049481, 2477049482, 2477049479],
    #     "timestamp": "2013-09-29T21:38:21Z",
    #     "user": "528491",
    #     "uid": 1377843,
    #     "version": 1
    #   },
        if(entry["properties"]["type"] == "way" and "tags" in entry["properties"] and "building" in entry["properties"]["tags"] and "name" in entry["properties"]["tags"]):
            buildings[entry["properties"]["id"]] = entry


        if (entry["geometry"]["type"] == "LineString"):
            lineString = entry["geometry"]["coordinates"]
            
            if("nodes" not in entry["properties"]):
                continue

            nodeString = entry["properties"]["nodes"]
            for i in range(0, len(nodeString)-1):
                id = str(nodeString[i])
                next_id = str(nodeString[i+1])
                # Check if id is in Graph
                if(next_id not in graph.getNodeProps(id, "neighbors")):
                    graph.addNeighbor(id, next_id)
                if(id not in graph.getNodeProps(next_id, "neighbors")):
                    graph.addNeighbor(next_id, id)
    with open("../backend/app/graph.json", "w") as f:
        json.dump(graph.graph, f)

    with open("../backend/app/building.json", "w") as f:
        json.dump(buildings, f)
