import json
from scipy.spatial import KDTree
import pandas as pd 
import plotly.express as px
import heapq 
from math import *
from constants import *
from collections import deque
DEFAULT_GOAL_RADIUS = 14
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
        return other is not None and self.id == other.id


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

    def BFS(self, start, goal_test):
        #Quang
        #tạo node đầu none
        start_node = MapNode(None, start)
        #hàng đợi 2 chiều
        queue = deque([start_node])
        explored_nodes = set()  

        path = []  

        while queue:
            current_node = queue.popleft()

            if current_node.id in explored_nodes:
                continue

            explored_nodes.add(current_node.id)

            for neighbor_id in self.getNeighbors(current_node.id):
                if neighbor_id not in explored_nodes:
                    neighbor_node = MapNode(parent=current_node, id=neighbor_id)
                    queue.append(neighbor_node)

                    if goal_test(neighbor_id):
                        # Reached the goal, accumulate the path
                        while neighbor_node:
                            path.append(neighbor_node.id)
                            neighbor_node = neighbor_node.parent

                        # Reverse the path to get the correct order
                        path.reverse()

                        # Show the map with the entire path
                        nodes = path
                        coords = [list(reversed(self.getNodeCoordinateById(p))) for p in path]
                        self.showMap(nodes, coords)

                        return path

        # If the queue is empty and no goal is found
        return FAILURE


    def DFS(self, start, goal_test):
        # Cuong
        pass 

    def AStar(self, start, goal_test, heuristic):
        # Toan
        node = MapNode(None, start)
        
        # Heuristic cost
        node.h = heuristic(node.id)
        node.g = 0
        node.f = node.g + node.h

        open_list = [(node.f, node)]
        
        closed_list = []

        explored_nodes = [start]
        nodes = [start]
        explored_coords = [list(reversed(self.getNodeCoordinateById(start)))]
        coords= [list(reversed(self.getNodeCoordinateById(start)))]
        while(len(open_list) > 0):
            node = heapq.heappop(open_list)[1]
            explored_nodes.append(node.id)
            explored_coords.append(list(reversed(self.getNodeCoordinateById(node.id))))
            if (goal_test(node.id)):
                path = []
                while(node.parent != None):
                    path.append(node.id)
                    node = node.parent
                path.append(node.id)
                path.reverse()
                # Show solution map
                for p in path:
                    nodes.append(p)
                    coords.append(list(reversed(self.getNodeCoordinateById(p))))
                # Show explored map
                self.showMap(nodes, coords)
                # Show explored map
                # self.showMap(explored_nodes, explored_coords)

                return coords
            closed_list.append(node)
            children = []
            for neighbor in self.getNeighbors(node.id):
                child = MapNode(parent=node, id=neighbor)
                child.g = node.g + self.getDistanceBetweenId(node.id, neighbor)
                child.h = heuristic(child.id)
                child.f = child.g + child.h
                children.append(child)
                # coords.append(list(reversed(self.getNodeCoordinateById(neighbor))))

            for child in children:
                is_in_open_list = False
                for item in open_list:
                    if (item[1].id == child.id):
                        is_in_open_list = True
                if is_in_open_list:
                    continue
                is_in_closed_list = False
                for item in closed_list:
                    if (item.id == child.id):
                        is_in_closed_list = True

                if is_in_closed_list:
                    continue

                heapq.heappush(open_list, (child.f, child))
        # print('Failed')
        # self.showMap(nodes, coords)
        return FAILURE

    def getBuildingCoordinates(self, id):
        return self.buildings[id]["geometry"]["coordinates"][0]
    

    def findShortestPath(self, lat, lon, type, target_id, algorithm):
        def heuristic(current_node_id, target_id=target_id):
            node_pos = self.getNodeCoordinateById(current_node_id)
            coordinates = self.getBuildingCoordinates(target_id) 
            min_distance = HaversineDistance(node_pos, coordinates[0])
            for coordinate in coordinates:
                min_distance = min(min_distance, HaversineDistance(node_pos, coordinate))
            return min_distance 

        def goalTestByBuildingId(current_node_id, target_id=target_id):
            return heuristic(current_node_id, target_id) <= DEFAULT_GOAL_RADIUS

        start_node = self.getNearestNode(lat, lon)
        if(algorithm == BFS):
            return self.BFS(start_node, goal_test=goalTestByBuildingId)
        elif (algorithm == DFS):
            return self.DFS(start_node, goal_test=goalTestByBuildingId)
        elif (algorithm == ASTAR):
            return self.AStar(start_node,goal_test=goalTestByBuildingId, heuristic=heuristic)
        # print(self.goalTestByBuildingId(start_node, target_id))
