import json
import math

METER = 1000

def HaversineDistance(a, b, unit=METER):
    """Give it lat, lon of two node and it will return distance between those two node"""
    (lon1, lat1) = a 
    (lon2, lat2) = b
    EARTH_RADIUS_IN_KILOMETER = 6371

    # Haversine for lon1, lat1, lon2, lat2
        # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers
    r = EARTH_RADIUS_IN_KILOMETER

    # Calculate the result
    return c * r * unit


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
    with open("graph.json", "w") as f:
        json.dump(graph.graph, f)

    with open("building.json", "w") as f:
        json.dump(buildings, f)

