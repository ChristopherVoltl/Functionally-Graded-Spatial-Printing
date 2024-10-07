import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import convert_data_Version2 as cdata

class Graph:
    def __init__(self, points):
        self.vertices = []
        self.edges = {}
        self.adj_list = {}
        self.distances = {}

        # Generate n random points in 3D cartesian space
        #self.points = np.random.rand(n, 3)
        testpt = np.random.rand(100, 3)
        n = len(points)
        self.points = np.array(points)
        

        # Add each point as a vertex to the graph
        for i in range(n):
            self.vertices.append(i)
            self.adj_list[i] = []
            self.distances[i] = {}

        # Add connections between each point and its three closest neighbors
        for i in range(n):
            distances = np.linalg.norm(self.points - self.points[i], axis=1)
            sorted_indices = np.argsort(distances)
            for j in sorted_indices[1:5]:
                if not self.has_edge(i, j):
                    self.add_edge(i, j, distances[j])

        # Sort the edges based on connectivity
        sorted_edges = []
        visited = [False] * n
        stack = [0]
        current_vertex = 0
        while len(sorted_edges) < len(self.edges):
            neighbors = self.adj_list[current_vertex]
            for neighbor in neighbors:
                if self.has_edge(current_vertex, neighbor) and not visited[neighbor]:
                    sorted_edges.append((current_vertex, neighbor))
                    visited[neighbor] = True
                    stack.append(neighbor)
                    current_vertex = neighbor
                    break
            else:
                if stack:
                    current_vertex = stack.pop()
                else:
                    for vertex in self.vertices:
                        if not visited[vertex]:
                            stack.append(vertex)
                            current_vertex = vertex
                            break
                    else:
                        break

        self.sorted_edges = sorted_edges

        # Generate a gradient of colors for the edges
        cmap = plt.get_cmap('Reds')
        norm = colors.Normalize(vmin=0, vmax=len(self.sorted_edges)-1)
        self.edge_colors = [cmap(norm(i)) for i in range(len(self.sorted_edges))]

    def has_edge(self, u, v):
        return (u, v) in self.edges or (v, u) in self.edges

    def add_edge(self, u, v, weight):
        self.edges[(u, v)] = weight
        self.edges[(v, u)] = weight
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
        self.distances[u][v] = weight
        self.distances[v][u] = weight

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2])
        for i, edge in enumerate(self.sorted_edges):
            u, v = edge
            ax.plot([self.points[u][0], self.points[v][0]], [self.points[u][1], self.points[v][1]], [self.points[u][2], self.points[v][2]], color=Red)
        plt.show()



if __name__ == '__main__':

    print("meow")
    

    #convert text file into a dict
    pt_data = 'fea/data/wall003NLIST.txt'

    pt_csv = 'fea/data/pt_data.csv'

    cdata.text_to_csv(pt_data, pt_csv)

    cdata.delete_rows_with_header(pt_csv, "NODE")

    pt_data = cdata.read_csv_to_dicts(pt_csv, delimiter=',')
    cdata.write_json('pt_data.json', pt_data)

    pt_json = './pt_data.json'

    pt_json = cdata.read_json(pt_json, encoding='utf-8')
    ansys = cdata.StructuralData()

    for i in range(len(pt_json)):
        #print(type(x_json[i]))
        for key, value in pt_json[i].items():
            if key == "X":
                value = cdata.convert_to_float(value)
                #convert to inch
                if type(value) is float:
                    value = value*39.3701
                    ansys.coordinates.append([value, 'none' , 'none'])

    for i in range(len(pt_json)):
        #print(type(y_json[i]))
        for key, value in pt_json[i].items():
            if key == "Y":
                value = cdata.convert_to_float(value)
                #convert to inch
                if type(value) is float:
                    value = value*39.3701
                    ansys.coordinates[i][1] = value

    for i in range(len(pt_json)):
        #print(type(z_json[i]))
        for key, value in pt_json[i].items():
            if key == "Z":
                value = cdata.convert_to_float(value)
                #convert to inch
                if type(value) is float:
                    value = value*39.3701
                    ansys.coordinates[i][2] = value 

    graph = Graph(ansys.coordinates)
    graph.plot()
    print(graph.edges)