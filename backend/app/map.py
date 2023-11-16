import json
from scipy.spatial import KDTree


class Map: 
    def __init__(self):
        self.graph = {}
        self.tree = None
        self.coordinates = []
        self.nodes = []
        self.loadMapData()
        
    def loadMapData(self):
        # Show directory
        # print(os.listdir())
        with open('./data/graph.json', 'r') as f:
            self.graph = json.load(f)    
            # Loop through all entry in graph
            
            for node in self.graph.keys():
                print(self.graph[node]['info']['geometry']['coordinates'])
                coordinate = self.graph[node]['info']['geometry']['coordinates']
                self.coordinates.append([coordinate[1], coordinate[0]])
                self.nodes.append(node)
            self.tree = KDTree(self.coordinates)
    
    def getNearestNode(self, lat, lon):
        # Query the KDTree for the nearest neighbor
        distance, index = self.tree.query([lat, lon])
        return self.graph[self.nodes[index]]

# data = []
# def getNodeInfo(lat, lon):
#     features = data['features']
#     for feature in features:
#         if feature["properties"]["type"] == "node":
#             if (feature["geometry"]["coordinates"][0] == lon and feature["geometry"]["coordinates"][1] == lat):
#                 return feature

# # Load the coordinates from the JSON file
# with open('./data/sample.json', 'r') as f:
#     nodes = []
#     coordinates = []
#     data = json.load(f)
#     features = data['features']
#     for feature in features:
#         if feature["properties"]["type"] == "node":
#             nodes.append(feature)
#     # Swap lat and lon for each coordinate to match KDTree input
#     for node in nodes:
#         # [[lat, lon]] = [node["geometry"]["coordinates"][1], node["geometry"]["coordinates"][0]]
#         # coordinates.append([lat, lon])
#         # print([lat, lon])
#         lat, lon = node["geometry"]["coordinates"][0], node["geometry"]["coordinates"][1]
#         coordinates.append([lon, lat])

#     # Build the KDTree
#     tree = KDTree(coordinates)
# #   How do I add more information to my query?
# #   https://stackoverflow.com/questions/52386730/how-do-i-add-more-information-to-my-query

#     # Specify the GPS coordinate
    
# # Specify the GPS coordinate
#     lat = 10.84992
#     lon = 106.77164

#     # Query the KDTree for the nearest neighbor
#     distance, index = tree.query([lat, lon])


#     # Print the nearest neighbor
#     print(coordinates[index])
#     print(getNodeInfo(coordinates[index][0], coordinates[index][1]))

    