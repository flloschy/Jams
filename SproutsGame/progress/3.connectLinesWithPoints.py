import pygame, math, numpy as np

WIN = pygame.display.set_mode((800, 800))

def isConnectedToNode(nodes, point):
        for node in nodes:
            distance = math.sqrt((point.x - node.pos.x)**2 + (point.y - node.pos.y)**2)
            if distance <= 10:
                return True
        return False

def isConnectedToNodes(nodes, start, end):
    radius = 10
    startNode = False
    endNode = False
    for node in nodes:
        distanceStart = math.sqrt((start.x - node.pos.x)**2 + (start.y - node.pos.y)**2)
        distanceEnd = math.sqrt((end.x - node.pos.x)**2 + (end.y - node.pos.y)**2)

        if distanceStart <= radius:
            startNode = node
        if distanceEnd <= radius:
            endNode = node
    if not startNode and not endNode:
        return False, False
    return startNode, endNode

def intersect(point1, point2):
    A = point1[0]
    B = point1[1]
    C = point2[0]
    D = point2[1]

    def ccw(A,B,C):
        return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
    
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def intersectsWithOtherLine(line, other):

    for l in other[:-1]:
        for p in [(x, line.points[i+1]) for i, x in enumerate(line.points) if i!= len(line.points) - 1]:
            for p2 in [(x, l.points[i+1]) for i, x in enumerate(l.points) if i!= len(l.points) - 1]:
                if intersect(p, p2):
                    return True
    return False

def intersectItSelf(points):
    return False
        


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.t = (x, y)

class Node:
    def __init__(self, x, y):
        self.pos = Point(x, y)
        self.connections = []

    def draw(self, WIN):
        color = (200, 200, 200) if len(self.connections) == 3 else (100, 100, 100)
        pygame.draw.circle(WIN, color, self.pos.t, 10)
    
    def addConnection(self, line):
        if len(self.connections) == 3: return False
        self.connections.append(line)
        return True
    
    def validate(self, nodes):
        for node in nodes:
            distance = math.sqrt((node.pos.x - self.pos.x)**2 + (node.pos.y - self.pos.y)**2)
            if distance < 50:
                return False
        return True

class Line:
    def __init__(self, x, y):
        self.points = [Point(x, y)]
        self._latestXY = (x, y)
        self.done = False
    
    def draw(self, WIN, lines, nodes):
        if not self.done:
            for pos in self.points[:-1]:
                pygame.draw.circle(WIN, (240, 240, 240), pos.t, 20, 2)
            pygame.draw.circle(WIN, (220, 220, 220), self.points[-1].t, 50, 2)

            points = self.points + [Point(self._latestXY[0], self._latestXY[1])]

            intersections = []

            for i, A, B in [(i, x, points[i+1]) for i, x in enumerate(points) if i != len(points) -1]:
                for line in lines[:-1]:
                    for C, D in [(x, line.points[i+1]) for i, x in enumerate(line.points) if i!= len(line.points) - 1]:
                        if intersect((A, B), (C, D)):
                            intersections.append(i)
            
            

            for i, A, B in [(i, x, points[i+1]) for i, x in enumerate(points) if i != len(points) -1]:
                color = (0, 255, 0)
                if i == 0:
                    if not isConnectedToNode(nodes, A):
                        color = (0, 0, 255)
                if i == len(points) - 2:
                    if not isConnectedToNode(nodes, B):
                        color = (0, 0, 255)
                if i in intersections:
                    color = (255, 0, 0)


                pygame.draw.line(WIN, color, A.t, B.t, 5)

        else:
            pygame.draw.lines(WIN, (0, 0, 0), False, [p.t for p in self.points] + [self._latestXY], 5)
    
    def validate(self, lines, nodes):
        self.points.append(Point(self._latestXY[0], self._latestXY[1]))

        startNode, endNode = isConnectedToNodes(nodes, self.points[0], self.points[-1])
        intersectWithOther = intersectsWithOtherLine(self, lines)
        intersectWithSelf = intersectItSelf(self.points)

        if startNode and endNode and (not intersectWithOther) and (not intersectWithSelf):
            if startNode == endNode:
                if len(startNode.connections) > 1: return False
            if len(startNode.connections) > 2: return False
            if len(endNode.connections) > 2: return False

            startNode.addConnection(self)
            endNode.addConnection(self)

            self.points[0] = Point(startNode.pos.x, startNode.pos.y)
            self.points[-1] = Point(endNode.pos.x, endNode.pos.y)


            return True
            
        return False

    def drag(self, x, y):
        self._latestXY = (x, y)
        distance = math.sqrt((self.points[-1].x - x)**2 + (self.points[-1].y - y)**2)
        if distance <= 50: return False
        self.points.append(Point(x, y))
        return False

mode = "placing"
nodes:list[Node] = []
lines:list[Line] = []

while True:
    x, y = pygame.mouse.get_pos()
    l, m, r = pygame.mouse.get_pressed()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and mode == "placing":
                if Node(x, y).validate(nodes):
                    nodes.append(Node(x, y))
            elif event.button == 1 and mode == "none":
                mode = "drawing"
                lines.append(Line(x, y))
            elif event.button == 3 and mode == "drawing":
                mode = "none"
                lines.remove(lines[-1])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and mode == "drawing":
                if lines[-1].validate(lines, nodes):
                    lines[-1].done = True
                else:
                    lines = lines[:-1]
                mode = "none"

    if r and mode == "placing":
        mode = "none"
    if l and mode == "drawing":
        lines[-1].drag(x, y)


    for node in nodes:
        node.draw(WIN)
    for line in lines:
        line.draw(WIN, lines, nodes)


    pygame.display.update()
    WIN.fill((255, 255, 255))

    print(mode)