def DFS(self, start, goal_test):
    stack = [MapNode(None, start)]
    explored_nodes = []
    explored_coords = []

    while stack:
        node = stack.pop()
        explored_nodes.append(node.id)
        explored_coords.append(list(reversed(self.getNodeCoordinateById(node.id))))

        if goal_test(node.id):
            path = []
            while node.parent is not None:
                path.append(node.id)
                node = node.parent
            path.append(node.id)
            path.reverse()

            # Show solution map
            nodes, coords = [], []
            for p in path:
                nodes.append(p)
                coords.append(list(reversed(self.getNodeCoordinateById(p))))
            self.showMap(nodes, coords)

            return coords

        if node.id not in explored_nodes:
            explored_nodes.append(node.id)
            children = []
            for neighbor in self.getNeighbors(node.id):
                child = MapNode(parent=node, id=neighbor)
                children.append(child)

            stack.extend(children)

    # If no path is found
    # Show explored map
    self.showMap(explored_nodes, explored_coords)
    return FAILURE
