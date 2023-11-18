import json
from scipy.spatial import KDTree
import pandas as pd 
import plotly.express as px

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position    

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# class AStar(map, start, end):



class Map: 
    
    def __init__(self):
        self.graph = {}
        self.tree = None
        self.coordinates = []
        self.nodes = []
        self.loadMapData()
        

    def showMap(self, coordinates):
        df = pd.DataFrame(coordinates, columns=['id', 'lat', 'lon'])
        color_scale = [(0, 'orange'), (1,'red')]

        fig = px.scatter_mapbox(df, 
                                lat="lat", 
                                lon="lon", 
                                hover_name="id", 
                                # hover_data=["Address", "Listed"],
                                # color="Listed",
                                color_continuous_scale=color_scale,
                                # size="Listed",
                                zoom=8, 
                                height=800,
                                width=800)

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()

    def loadMapData(self):
        # Show directory
        # print(os.listdir())
        with open('./data/graph.json', 'r') as f:
            self.graph = json.load(f)    
            # Loop through all entry in graph
            
            for node in self.graph.keys():
                # print(self.graph[node]['info']['geometry']['coordinates'])
                coordinate = self.graph[node]['info']['geometry']['coordinates']
                self.coordinates.append([node, coordinate[1], coordinate[0]])
                self.nodes.append(node)
            # self.showMap(self.coordinates)
            self.tree = KDTree(self.coordinates)
        with open('./data/building.json', 'r') as f:
            self.buildings = json.load(f)
            self.getAllBuildings()

    def getAllBuildings(self):
        all_buildings = []
        for id in self.buildings.keys():
            building = {}
            building['id'] = id
            building['name'] = self.buildings[id]['properties']['tags']['name']
            all_buildings.append(building)
        return all_buildings                

    def getNearestNode(self, lat, lon):
        # Query the KDTree for the nearest neighbor
        distance, index = self.tree.query([lat, lon])
        return self.graph[self.nodes[index]]

    def getDestionaion(self):
        return self.graph[self.nodes[0]]

    def findShortestPath(self, lat1, lon1, lat2, lon2):
        lon2 = 106.77137
        lat2 = 10.85109

        node = self.getNearestNode(lat1, lon1)
        print(node)

        

        # Query the KDTree for the nearest neighbor
        
        

    

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

map = Map()