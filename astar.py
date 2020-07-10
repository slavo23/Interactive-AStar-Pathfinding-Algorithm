import heapq

class AstarSearch:
    def __init__(self):
        self.open_set   = []
        self.closed_set = []


    def get_steps(self, end):
        steps = []

        while end.parent != None:
            steps.append((end.x, end.y))
            end = end.parent
        
        return steps


    def update_node(self, n1, n2, end, min_cost):
        n1.g_cost = min_cost
        n1.h_cost = self.heuristic(n1, end)
        n1.parent = n2
        n1.f_cost = n1.g_cost + n1.h_cost


    def heuristic(self, n1, n2):
        return abs(n1.x - n2.x) + abs(n1.y - n2.y)


    def find(self, grid):
        start     = grid.search_origin
        goal      = grid.search_target
        node_list = grid.node_list

        
        heapq.heappush(self.open_set, start)
        path = None
        while len(self.open_set) > 0:
            current = heapq.heappop(self.open_set)
            self.closed_set.append(current)
            
            if current == goal:
                path = self.get_steps(goal)
                return path
            
            adjacent = grid.neighbours_at(current)
        
            for adj in adjacent:
                if adj not in self.closed_set:
                    if adj in self.open_set:
                        if adj.g_cost > current.g_cost + 1:
                            self.update_node(adj, current, goal, current.g_cost + 1)
                    else:
                        self.update_node(adj, current, goal, current.g_cost + 1)
                        heapq.heappush(self.open_set, adj)
        return path