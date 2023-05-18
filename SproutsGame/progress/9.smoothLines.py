import pygame, math, numpy as np, random

from scipy import interpolate
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 20)
errorMsg = ""
player1 = "p1"
player1wins = 0
player2 = "p2"
player2wins = 0
playerTurn = True


class NodeColors:
    active = (200, 200, 200)
    inactive = (100, 100, 100)
class Settings:
    minNodePlaceDistance = 50
    nodeCircleSize = 10
    lineGhostCircleColor = (240, 240, 240)
    lineGhostCircleSize = 20
    lineRadiusColor = (220, 220, 220)
    lineRadius = 50
    lineThickness = 5
    linePreviewOK = (0, 255, 0)
    linePreviewNotConnected = (0, 0, 255)
    linePreviewIntersection = (255, 0, 0)
    player1Color = (242, 148, 227)
    player2Color = (148, 212, 242)
    windowWidth = 1200
    windowHeight = 700
    fieldWidth = 700
    fieldHeight = 700
    normalTextColor = (255, 255, 255)
    errorTextColor = (255, 0, 0)
    backgroundColor = (255, 255, 255)
    menuBackgroundColor = (50, 50, 50)
    splitLineColor = (0, 0, 0)
    buttonInactive = (100, 100, 100)
    buttonHover = (200, 200, 200)
    buttonPress = (150, 150, 150)
class Mode:
    placing = "Place starting points, right click to start"
    none = "<p>'s turn"
    drawing = "<p> draws"
    doting = "<p> place dot"
    end = "game over, left click to start again"

WIN = pygame.display.set_mode((Settings.windowWidth, Settings.windowHeight))
field = pygame.Surface((Settings.fieldHeight, Settings.fieldWidth))

def nearestPointOnLines(lines, xM, yM):
    def ray(line, cast: tuple = ((0, 0), (0, 0))):
        x1, x2, y1, y2 = line[0].x, line[1].x, line[0].y, line[1].y
        x3, x4, y3, y4 = cast[0][0], cast[1][0], cast[0][1], cast[1][1]
        den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if den == 0:
            return False
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
        u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den
        if 1 > t > 0 and u > 0:
            x5, y5 = x1+t*(x2-x1), y1+t*(y2-y1)
            return [x5, y5], math.sqrt((x5-x3)**2 + (y5-y3)**2)
        return False

    def cast(lines:list, cast):
        points = []
        for line in lines:
            ray_ = ray(line, cast)
            if ray_:
                points.append(ray_)
        try: return points
        except: return False

    def cast_all(lines:list, pos:tuple=(0, 0), pov:float=360, rot:float=0, casts:int=30):
        t = math.pi*2 - abs(((pov/360)-1)*(math.pi/180)*360)
        points = []
        for angle in np.arange(0, t, t/casts):
            angle += math.pi*2 - abs(((rot/360)-1)*(math.pi/180)*360)
            x1, y1 = pos[0], pos[1]
            x2, y2 = pos[0]+1, pos[1]+1
            line = (pos,
                ((x2 - x1) * math.cos(90 - angle) - (y2 - y1) * math.sin(90 - angle) + x1,
                (x2 - x1) * math.sin(90 - angle) + (y2 - y1) * math.cos(90 - angle) + y1))

            cased_point = cast(lines, line)
            if not cased_point: continue
            points.append(cased_point)
        return points
    
    def closest(casts):
        if not casts: return False
        close = casts[0][0][1]
        index = 0
        
        for i, (_, length) in enumerate(casts):
            if length < close:
                index = i
                close = length
        return casts[index][0]

    casts = []

    for line in lines:
        for point in cast_all([(x, line.points[i+1]) for i, x in enumerate(line.points) if i!= len(line.points) - 1], (xM, yM)):
            casts.append(point[0])

    close = closest(casts)
    if not close: return False
    return Point(close[0], close[1])

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
        self.connections = 0

    def draw(self, WIN):
        color = NodeColors.active if self.connections == 3 else NodeColors.inactive
        pygame.draw.circle(WIN, color, self.pos.t, Settings.nodeCircleSize)
    
    def addConnection(self, amount=1):
        if self.connections + amount > 3: return False
        self.connections += amount
        return True
    
    def validate(self, nodes):
        for node in nodes:
            distance = math.sqrt((node.pos.x - self.pos.x)**2 + (node.pos.y - self.pos.y)**2)
            if distance < Settings.minNodePlaceDistance:
                return False
        return True

class Line:
    def __init__(self, x, y, color):
        self.points = [Point(x, y)]
        self._latestXY = (x, y)
        self.done = False
        self.color = color
    
    def draw(self, WIN, lines, nodes, drawCircles=True):
        if not self.done:
            if drawCircles:
                for pos in self.points[:-1]:
                    pygame.draw.circle(WIN, Settings.lineGhostCircleColor, pos.t, Settings.lineGhostCircleSize, 2)
                pygame.draw.circle(WIN, Settings.lineRadiusColor, self.points[-1].t, Settings.lineRadius, 2)

            points = self.points + [Point(self._latestXY[0], self._latestXY[1])]

            intersections = []

            for i, A, B in [(i, x, points[i+1]) for i, x in enumerate(points) if i != len(points) -1]:
                for line in lines[:-1]:
                    for C, D in [(x, line.points[i+1]) for i, x in enumerate(line.points) if i!= len(line.points) - 1]:
                        if intersect((A, B), (C, D)):
                            intersections.append(i)
            
            

            for i, A, B in [(i, x, points[i+1]) for i, x in enumerate(points) if i != len(points) -1]:
                color = Settings.linePreviewOK
                if i == 0:
                    if not isConnectedToNode(nodes, A):
                        color = Settings.linePreviewNotConnected
                if i == len(points) - 2:
                    if not isConnectedToNode(nodes, B):
                        color = Settings.linePreviewNotConnected
                if i in intersections:
                    color = Settings.linePreviewIntersection


                pygame.draw.line(WIN, color, A.t, B.t, Settings.lineThickness)

        else:
            if len(self.points) > 1:
                pygame.draw.lines(WIN, (0, 0, 0), False, [p.t for p in self.points], Settings.lineThickness)
            else:
                pygame.draw.lines(WIN, (0, 0, 0), False, [p.t for p in self.points] + [self._latestXY], Settings.lineThickness)


    def smoothOut(self):
        if len(self.points) > 5:
            x = [p.x for p in self.points]
            y = [p.y for p in self.points]
            t = np.linspace(0, 1, len(self.points) - 2, endpoint=True)
            t = np.append([0, 0, 0], t)
            t = np.append(t, [1, 1, 1])
            tck, u = interpolate.splprep([x, y], s=0)
            unew = np.arange(0, 1.01, 0.01)
            out = interpolate.splev(unew, tck)
            self.points = [Point(out[0][i], out[1][i]) for i in range(len(out[0]))]
    
    def validate(self, lines, nodes):
        global errorMsg
        self.points.append(Point(self._latestXY[0], self._latestXY[1]))

        startNode, endNode = isConnectedToNodes(nodes, self.points[0], self.points[-1])
        intersectWithOther = intersectsWithOtherLine(self, lines)
        intersectWithSelf = intersectItSelf(self.points)

        if startNode:
            if endNode:
                if not intersectWithOther:
                    if not intersectWithSelf:
                        if startNode == endNode:
                            if startNode.connections > 1: 
                                errorMsg = "targeted node has to many connections"
                                return False
                        if startNode.connections > 2:
                            errorMsg = "starting node has to many connections"
                            return False
                        if endNode.connections > 2: 
                            errorMsg = "end node has to many connections"
                            return False

                        startNode.addConnection()
                        endNode.addConnection()

                        return True
                    else:
                        errorMsg = "line intersects it self"
                else:
                    errorMsg = "line intersects other lines"
            else:
                errorMsg = "line has no end connection to a node"
        else:
            errorMsg = "line has no start connection to a node"

        return False

    def drag(self, x, y):
        self._latestXY = (x, y)
        distance = math.sqrt((self.points[-1].x - x)**2 + (self.points[-1].y - y)**2)
        if distance <= Settings.lineRadius: return False
        self.points.append(Point(x, y))
        return False

class Button:
    def __init__(self, x, y, lable, width, height):
        self.pos = Point(x, y)
        self.width = width
        self.height = height
        self.lable = font.render(lable, True, Settings.normalTextColor)
        self.last = False

    def draw(self, WIN, x, y, l):
        trigger = False
        color = Settings.buttonInactive
        if x in range(self.pos.x, self.pos.x + self.width):
            if y in range(self.pos.y, self.pos.y + self.height):
                if not l and self.last:
                    trigger = True
                self.last = l
                if l:
                    color = Settings.buttonPress
                else:
                    color = Settings.buttonHover
        pygame.draw.rect(WIN, color, (self.pos.x, self.pos.y, self.width, self.height))
        WIN.blit(self.lable, (self.pos.x + self.width/2 - self.lable.get_width()/2, self.pos.y + self.height/2 - self.lable.get_height() / 2))
        return trigger



def generateTutorials():
    def connectDots():
        surface = pygame.Surface((100, 100))
        surface.fill(Settings.menuBackgroundColor)
        node1 = Node(10, 50)
        node2 = Node(90, 50)
        line = Line(10, 50, Settings.linePreviewOK)
        line.drag(50, 50)
        line._latestXY = (90, 50)
        line.done = True
        line.draw(surface, [], [node1, node2])
        node1.draw(surface)
        node2.draw(surface)
        return surface
    def crossLine():
        surface = pygame.Surface((100, 100))
        surface.fill(Settings.menuBackgroundColor)
        node1 = Node(50, 10)
        node2 = Node(50, 90)
        node3 = Node(10, 50)
        node4 = Node(90, 50)
        line1 = Line(10, 50, Settings.linePreviewOK)
        line1._latestXY = (90, 50)
        line1.done = True
        line1.draw(surface, [], [node1, node2, node3, node4])
        line2 = Line(50, 10, Settings.linePreviewIntersection)
        line2._latestXY = (50, 90)
        line2.done = True
        line2.draw(surface, [line1], [node1, node2, node3, node4], False)
        node1.draw(surface)
        node2.draw(surface)
        node3.draw(surface)
        node4.draw(surface)
        return surface
    def loop():
        surface = pygame.Surface((100, 100))
        surface.fill(Settings.menuBackgroundColor)
        node1 = Node(50, 50)
        node2 = Node(0, 50)
        line1 = Line(50, 50, Settings.linePreviewOK)
        line1.drag(0+20, 50)
        line1._latestXY = (0, 50)
        line1.done = True
        line1.draw(surface, [], [node1, node2], False)
        line2 = Line(50, 50, Settings.linePreviewOK)
        line2.points.append(Point(50, 10))
        line2.points.append(Point(90, 10))
        line2.points.append(Point(90, 90))
        line2.points.append(Point(50, 90))
        line2._latestXY = (50, 50)
        line2.done = True
        line2.draw(surface, [], [node1, node2], False)
        node1.draw(surface)
        node2.draw(surface)

        return surface
    def connections():
        surface = pygame.Surface((100, 100))
        surface.fill(Settings.menuBackgroundColor)
        node1 = Node(10, 10)
        node2 = Node(90, 10)
        node3 = Node(90, 90)
        node4 = Node(10, 90)
        node5 = Node(50, 50)

        line1 = Line(10, 10, Settings.linePreviewOK)
        line1._latestXY = (50, 50)
        line1.done = True
        line1.draw(surface, [], [])

        line2 = Line(90, 10, Settings.linePreviewOK)
        line2._latestXY = (50, 50)
        line2.done = True
        line2.draw(surface, [], [])

        line3 = Line(10, 90, Settings.linePreviewOK)
        line3._latestXY = (50, 50)
        line3.done = True
        line3.draw(surface, [], [])

        line4 = Line(90, 90, Settings.linePreviewIntersection)
        line4._latestXY = (50, 50)
        line4.done = True
        line4.draw(surface, [], [])

        node1.draw(surface)
        node2.draw(surface)
        node3.draw(surface)
        node4.draw(surface)
        node5.connections = 3
        node5.draw(surface)

        return surface
    
    surface = pygame.Surface((220, 220))
    surface.fill(Settings.menuBackgroundColor)
    surface.blit(connectDots(), (0, 0))
    surface.blit(crossLine(), (110, 0))
    surface.blit(loop(), (0, 110))
    surface.blit(connections(), (110, 110))

    return surface

mode = Mode.placing
nodes:list[Node] = []
lines:list[Line] = []
RestartButton = Button(Settings.fieldWidth + 5, Settings.fieldHeight - 140, "Restart", 250, 30)
Player1WinButton = Button(Settings.fieldWidth + 5, Settings.fieldHeight - 105, "Manual Player1 Win", 250, 30)
Player2WinButton = Button(Settings.fieldWidth + 5, Settings.fieldHeight - 70, "Manual Player2 Win", 250, 30)
tutorial = generateTutorials()
while True:
    x, y = pygame.mouse.get_pos()
    l, m, r = pygame.mouse.get_pressed()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                errorMsg = ""
            if event.button == 1 and mode == Mode.placing:
                if x - 10 > 0 and x + 10 < Settings.fieldWidth:
                    if y - 10 > 0 and y + 10 < Settings.fieldHeight:
                        if Node(x, y).validate(nodes):
                            nodes.append(Node(x, y))
                        else:
                            errorMsg = "node needs to be placed further apart"
                    else:
                        errorMsg = "node needs to be place inside the field"
                else:
                    errorMsg = "node needs to be placed inside the field"
            elif event.button == 1 and mode == Mode.none:
                mode = Mode.drawing
                lines.append(Line(x, y, Settings.player1Color if playerTurn else Settings.player2Color))
            elif event.button == 3 and mode == Mode.drawing:
                mode = Mode.none
                lines.remove(lines[-1])
            elif event.button == 1 and mode == Mode.end:
                lines.clear()
                nodes.clear()
                player1wins += playerTurn
                player2wins += not playerTurn
                mode = Mode.placing
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and mode == Mode.drawing:
                if lines[-1].validate(lines, nodes):
                    lines[-1].done = True
                    lines[-1].smoothOut()
                    mode = Mode.doting
                else:
                    lines = lines[:-1]
                    mode = Mode.none
            elif event.button == 1 and mode == Mode.doting:
                nearest = nearestPointOnLines(lines, x, y)
                if nearest:
                    toClose = False
                    for node in nodes:
                        distance = math.sqrt((node.pos.x - nearest.x)**2 + (node.pos.y - nearest.y)**2)
                        if distance < Settings.minNodePlaceDistance:
                            toClose = True

                if not toClose:
                    mode = Mode.none
                    playerTurn = not playerTurn
                    nodes.append(Node(nearest.x, nearest.y))
                    nodes[-1].addConnection(2)
                else:
                    errorMsg = "Nodes need to be placed further apart"

    if mode == Mode.placing or mode == Mode.doting:
        for node in nodes:
            pygame.draw.circle(field, Settings.lineGhostCircleColor, node.pos.t, Settings.minNodePlaceDistance)
    
    
    if r and mode == Mode.placing:
        if len(nodes) == 0:
            errorMsg = "Need at least one point to start"
        else:
            mode = Mode.none
    if l and mode == Mode.drawing:
        lines[-1].drag(x, y)
    if mode == Mode.doting:
        nearest = nearestPointOnLines(lines, x, y)
        if nearest:
            pygame.draw.circle(field, Settings.lineRadiusColor, (nearest.x, nearest.y), Settings.nodeCircleSize)


    atLeastOneAvailable = False
    for line in lines:
        line.draw(field, lines, nodes)
    for node in nodes:
        node.draw(field)
        if node.connections < 3:
            atLeastOneAvailable = True
    
    if not atLeastOneAvailable and nodes:
        winText = font.render(f"{player1 if playerTurn else player2} won!", True, Settings.player1Color if playerTurn else Settings.player2Color)
        WIN.blit(winText, (Settings.fieldWidth + 5, 80))
        mode = Mode.end
        for line in lines:
            line.color = Settings.player1Color if playerTurn else Settings.player2Color
        

    textRender = font.render("Task: " + mode.replace("<p>", player1 if playerTurn else player2), True, Settings.normalTextColor)
    errorRender = font.render("Error: " + errorMsg, True, Settings.errorTextColor)
    player1Render = font.render(f"{player1} wins: {player1wins}", True, Settings.player1Color)
    player2Render = font.render(f"{player2} wins: {player2wins}", True, Settings.player2Color)


    WIN.blit(player1Render, (Settings.fieldWidth + 5, 5))
    WIN.blit(player2Render, (Settings.fieldWidth + 5, 30))
    WIN.blit(textRender, (Settings.fieldWidth + 5, 55))
    WIN.blit(errorRender, (Settings.fieldWidth + 5, Settings.fieldHeight - errorRender.get_height() - 5))
    

    WIN.blit(field, (0, 0))
    pygame.draw.line(WIN, Settings.splitLineColor, (Settings.fieldWidth, 0), (Settings.fieldWidth, Settings.fieldHeight), 7)
    if Player1WinButton.draw(WIN, x, y, l):
        mode = Mode.end
        playerTurn = True
    if Player2WinButton.draw(WIN, x, y, l):
        mode = Mode.end
        playerTurn = False
    if RestartButton.draw(WIN, x, y,l):
        mode = Mode.placing
        nodes.clear()
        lines.clear()
        playerTurn = random.choice([True, False])

    WIN.blit(tutorial, ((Settings.windowWidth - Settings.fieldWidth) / 2 - tutorial.get_width()/2 + Settings.fieldWidth, Settings.fieldHeight / 2 - tutorial.get_height() / 2))

    pygame.display.update()

    field.fill(Settings.backgroundColor)
    WIN.fill(Settings.menuBackgroundColor)