import rhinoscriptsyntax as rs
import csv
from random import random
from collections import deque

'''add a dot to the point as a dictionary identifier to the point
location'''

class Graph:
    ''' Define graph '''
    def __init__(self, startpos, endpos):
        self.startpos = startpos
        self.endpos = endpos

        self.vertices = [startpos]
        self.edges = []
        self.success = False

        self.vex2idx = {startpos:0}
        self.neighbors = {0:[]}
        self.distances = {0:0.}

        self.sx = endpos[0] - startpos[0]
        self.sy = endpos[1] - startpos[1]

    def add_vex(self, pos):
        try:
            idx = self.vex2idx[pos]
        except:
            idx = len(self.vertices)
            self.vertices.append(pos)
            self.vex2idx[pos] = idx
            self.neighbors[idx] = []
        return idx

    def add_edge(self, idx1, idx2, cost):
        self.edges.append((idx1, idx2))
        self.neighbors[idx1].append((idx2, cost))
        self.neighbors[idx2].append((idx1, cost))


    def randomPosition(self):
        rx = random()
        ry = random()

        posx = self.startpos[0] - (self.sx / 2.) + rx * self.sx * 2
        posy = self.startpos[1] - (self.sy / 2.) + ry * self.sy * 2
        return posx, posy

def dijkstra(G):
    '''
    Dijkstra algorithm for finding shortest path from start position to end.
    '''
    srcIdx = G.vex2idx[G.startpos]
    dstIdx = G.vex2idx[G.endpos]

    # build dijkstra
    nodes = list(G.neighbors.keys())
    dist = {node: float('inf') for node in nodes}
    prev = {node: None for node in nodes}
    dist[srcIdx] = 0

    while nodes:
        curNode = min(nodes, key=lambda node: dist[node])
        nodes.remove(curNode)
        if dist[curNode] == float('inf'):
            break

        for neighbor, cost in G.neighbors[curNode]:
            newCost = dist[curNode] + cost
            if newCost < dist[neighbor]:
                dist[neighbor] = newCost
                prev[neighbor] = curNode

    # retrieve path
    path = deque()
    curNode = dstIdx
    while prev[curNode] is not None:
        path.appendleft(G.vertices[curNode])
        curNode = prev[curNode]
    path.appendleft(G.vertices[curNode])
    return list(path)


objectIds  = rs.GetObjects("pick points", rs.filter.point)
count = 0
data = []
filepath = "V:/DataforProjects/functGrad/dataRhino.csv"

dataHeader = ['Node Number', 'GUID', 'Point Coordinates']
str(dataHeader)
dataHeader = data.append(dataHeader)


for id in objectIds:
    ptCoords = rs.PointCoordinates(id)
    dataFormat = [str(count), str(id), str(ptCoords)]

    #print(dataFormat.format(count, id, ptCoords))
    data.append(dataFormat)
    count = count + 1

#print(data)
with open(filepath, 'wb') as csvfile:
    writing = csv.writer(csvfile)
    writing.writerows(data)

'''loop through all the points to find the 3 closest points without
adding a line that is already there'''

for x in objectIds:
    lines = []
    insidelines = []
    lineLengths = []
    
    #DRAW A SEARCH CIRCLE
    cir_radius = 3  
    search_space = rs.AddCircle(x, cir_radius)
    #test if the point is inside the circle
    cir_area = rs.CurveAreaCentroid(search_space)
    
    for y in objectIds:

        if rs.Distance(x, y) > 0:

            distance_from_center = rs.Distance(y, cir_area[0])
            #print(cir_area[0], x)
            #print(distance_from_center)

            if distance_from_center > 0:
                centerpt = rs.AddPoint(cir_area[0])
                point_test = rs.AddLine(y, centerpt)
                #print(search_space, point_test)
                crv_intersection = rs.CurveCurveIntersection(search_space, point_test)
                #print(crv_intersection)
                

                if crv_intersection is None:
                    line = rs.AddLine(x, y)
                    print("inside circle")
                    lines.append(line)
                    lineLengths.append(rs.CurveLength(line))

                else:
                    for intersection in crv_intersection:
                        if intersection[0] == 1:
                            print("Point")
                            rs.DeleteObject(point_test)


                rs.DeleteObject(centerpt)

    rs.DeleteObject(search_space)

    zipped = dict(zip(lines, lineLengths))
    lines.sort(key=zipped.get)
    #print(lines[:3])
    
    #print(lines_sorted)
    rs.DeleteObjects(lines[3:])