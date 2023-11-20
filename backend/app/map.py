import json
from scipy.spatial import KDTree
import pandas as pd 
import plotly.express as px
import heapq 
from math import *

DEFAULT_GOAL_RADIUS = 20
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


class MapNode:
    def __init__(self, parent=None, id=None):
        self.parent = parent
        self.id = id     

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.info == other.info


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
                self.coordinates.append([ coordinate[1], coordinate[0]])
                self.nodes.append(node)
            self.tree = KDTree(self.coordinates)
        with open('./app/building.json', 'r') as f:
            self.buildings = json.load(f)
            self.getAllBuildings()

        # self.showMap(list(self.graph.keys()), self.coordinates)

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

 
    def getNodeCoordinateById(self, id):
        node = self.graph[id]["info"]["geometry"]["coordinates"]
        return node

    def getDistanceBetweenId(self, x, y):
        return HaversineDistance(self.getNodeCoordinateById(x), self.getNodeCoordinateById(y))

    def getNeighbors(self, id):
        return self.graph[id]['neighbors']
        # neighbors = []
        # for neighbor in data:
        #     # print(neighbor)

        #     neighbor
        #     # neighbors.append((neighbor, self.getDistanceBetweenId(id, neighbor)))
        # return neighbors

    def AStar(self, start, goal_test):
        node = MapNode(None, start)
        open_list = [node]
        closed_list = []

        while(len(open_list) > 0):
            node = heapq.heappop(open_list)
            node.f = node.g + node.h
            if (goal_test(node.id)):
                return ['FOUND SOLUTION!']
            children = self.getNeighbors(node.id)

            successors = []
            for child in children:
                successors.append(MapNode(parent=node, id=child))

            for successor in successors:
                # f = g + heuristic
                child_current_cost = node.g + self.getDistanceBetweenId(node.id, successor.id)

        return FAILURE

    def getBuildingCoordinates(self, id):
        return self.buildings[id]["geometry"]["coordinates"][0]
    

    def findShortestPath(self, lat, lon, type, target_id):
        nodes = ['root']
        coords = [[lat, lon]]
        def goalTestByBuildingId(current_node_id, target_id=target_id):
            node_pos = self.getNodeCoordinateById(current_node_id)
            coordinates = self.getBuildingCoordinates(target_id)
            min_distance = HaversineDistance(node_pos, coordinates[0])
            for coordinate in coordinates:
                print(node_pos, coordinate, HaversineDistance(node_pos, coordinate))
                min_distance = min(min_distance, HaversineDistance(node_pos, coordinate))
            return min_distance <= DEFAULT_GOAL_RADIUS

        start_node = self.getNearestNode(lat, lon)
        # neighbors = self.getNeighbors(start_node)
        self.AStar(start_node, goalTestByBuildingId)
        # print(self.goalTestByBuildingId(start_node, target_id))
        # for neighbor in neighbors:
        #     nodes.append(neighbor[0])
        #     print(start_node, '->',neighbor[0])
        #     coords.append(list(reversed(self.getNodeCoordinateById(neighbor[0]))))
        # print(neighbors)

        # self.showMap(nodes, coords)