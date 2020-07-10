import heapq
from astar import AstarSearch

class Node:
    def __init__(self, x, y, obstacle):
        self.x        = x
        self.y        = y
        self.obstacle = self.is_obstacle(obstacle)
        self.parent   = None
    
        self.f_cost   = 0 # f(x) = g(x) + h(x)
        self.g_cost   = 0
        self.h_cost   = 0 # heuristic

    def is_obstacle(self, code):
        # May look wierd, but it is used for more
        # readable numerical representation of the grid,
        # because it is easier to percieve zeros as free space. 
        # Zero now stands for True, one is the opposite.
        return code in [0, 1] and not bool(code)


    # Those methods are implemented to store
    # Node instances inside Heap Queue
    def __lt__(self, other):
        self.f_cost < other.f_cost

    def __gt__(self, other):
        self.f_cost > other.f_cost

        
class Grid:
    def __init__(self, grid_map, rows = 0, cols = 0):
        self.grid_map      = grid_map
        self.rows          = rows
        self.cols          = cols

        self.search_origin = None
        self.search_target = None
        self.node_list     = []

        if self.rows == 0 or self.cols == 0:
            # If dimenstions are not stated, grid can determine
            # them by itself. 
            self.set_size()

        self.populate()
        
    def __str__(self):
        return f"Grid {self.rows}x{self.cols}"
        
    def set_size(self):
        rows = len(self.grid_map)
        cols = list(map(len, self.grid_map))[0]
    
        self.rows, self.cols = rows, cols

    def populate(self):
        # The role of specific grid cell is
        # determined here. All the nodes are then put
        # into nodelist which is then used in A* algorithm.
        for i in range(self.rows):
            for j in range(self.cols):

                node_type = self.grid_map[i][j]
                node      = Node(i, j, node_type)
                if node_type == 2:
                    self.search_origin = node
                if node_type == 3:
                    self.search_target = node
                if not node in self.node_list:
                    self.node_list.append(node)

    def node_at(self, x, y):
        return self.node_list[x * self.cols + y]

    def neighbours_at(self, node):
        avalible = lambda n   : n.obstacle == False
        nodes    = []
        if node.x > 0:
            nodes.append(self.node_at(node.x - 1, node.y))
        if node.x < self.rows - 1:
            nodes.append(self.node_at(node.x + 1, node.y))
        if node.y > 0:
            nodes.append(self.node_at(node.x, node.y - 1))
        if node.y < self.cols - 1:
            nodes.append(self.node_at(node.x, node.y + 1))
        return list(filter(avalible, nodes))


    def clean_map(self):
        # This function is used to delete any remaining paths
        # from grid map after pathfinding is applied. Used every
        # time the map is changed.
        old_map = self.grid_map
        for i in range(self.rows):
            for j in range(self.cols):
                if old_map[i][j] == 4:
                    old_map[i][j] = 1
        
        return old_map


    def solve(self, code):
        maze     = self.grid_map
        
        solver   = AstarSearch()
        edges    = solver.find(self)

        if edges == None : return maze
        
        fst = lambda t : t[0] 
        snd = lambda t : t[1]

        for edge in edges:
            if maze[fst(edge)][snd(edge)] == 3:
                continue
            maze[fst(edge)][snd(edge)] = code
   
        return maze
        
        



