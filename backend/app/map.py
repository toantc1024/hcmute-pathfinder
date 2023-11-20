import json
from scipy.spatial import KDTree
import pandas as pd 
import plotly.express as px
import heapq 
from math import *

FAILURE = 'FAILURE'
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

    def showMap(self, nodes, coordinates):
        mapData = [];
        for i in range(0, len(nodes)):
            mapData.append([nodes[i], coordinates[i][0], coordinates[i][1]])


        df = pd.DataFrame(mapData, columns=['id', 'lat', 'lon'])
        print(df)
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
        with open('./app/graph.json', 'r') as f:
            self.graph = json.load(f)    
            for node in self.graph.keys():
                coordinate = self.graph[node]['info']['geometry']['coordinates']
                self.coordinates.append([ coordinate[0], coordinate[1]])
                self.nodes.append(node)
            self.tree = KDTree(self.coordinates)
        with open('./app/building.json', 'r') as f:
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
        # Query the K-DTree for the nearest neighbor
        distance, index =  self.tree.query([lat, lon])
        print(index)
        return self.nodes[index]  # return Node object 

    def getDestionaion(self):
        return self.graph[self.nodes[0]]

    class Node:
        def __init__(self, parent=None, id=None):
            self.parent = parent
            self.id = id     

            self.g = 0
            self.h = 0
            self.f = 0

        def __eq__(self, other):
            return self.id == other.id
    
    def getNodeCoordinateById(self, id):
        node = self.graph[id]["info"]["geometry"]["coordinates"]
        return node

    def getNeighbors(self, id):
        data = self.graph[id]['neighbors']
        neighbors = []
        for neighbor in data:
            neighbors.append((neighbor, HaversineDistance(self.getNodeCoordinateById(id), self.getNodeCoordinateById(neighbor))))
        return neighbors

    def AStar(self, start, goal_test, graph):
        # openSet = [new Node(start)]
        # node = Node(None, start)
        # frontier = [node]
        # explored = []

        # while(len(frontier) > 0):
        #     node = heapq.heappop(frontier)
        #     if(goal_test(node.id)):
        #         return node
        #     explored.append(node)
        #     for action in self.getNeighbors(node.id):   
        #         child = Node(node, action)
        #         if(not ((child in frontier) or (child in explored))):
        #             heapq.heappush(frontier, child)
        #         elif:
                    
        return FAILURE


    def findShortestPath(self, lat, lon, type, target_id):
        nodes = ['root']
        coords = [[lat, lon]]

        start_node = self.getNearestNode(lon, lat)
        neighbors = self.getNeighbors(start_node)
        for neighbor in neighbors:
            nodes.append(neighbor[0])
            coords.append(list(reversed(self.getNodeCoordinateById(neighbor[0]))))


        # self.showMap(nodes, coords)