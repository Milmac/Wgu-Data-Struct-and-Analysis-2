# Milan Macura #000989289

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, start_vertex, end_vertex, weight=0.0):
        self.edge_weights[(start_vertex, end_vertex)] = weight
        self.adjacency_list[start_vertex].append(end_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=0.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    # Big O Notation for this code block:  O(n)
    # Return the distance between 2 addresses
    def get_distance(self, address1, address2):
        v1 = None
        v2 = None
        for x in list(self.adjacency_list.keys()):
            if v1 is not None and v2 is not None:
                break
            if address1 in x.label:
                v1 = x
            if address2 in x.label or x.label in address2:
                v2 = x
        distance = self.edge_weights[v1, v2]
        return distance
