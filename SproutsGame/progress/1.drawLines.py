import pygame, math

WIN = pygame.display.set_mode((800, 800))


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def toTuple(self):
        return (self.x, self.y)

class Line:
    def __init__(self, color):
        self.color = color
        self.points:list[point] = []
    def addPoint(self, x, y):
        if len(self.points) < 2:
            self.points.append(point(x, y))
            return
        
        latest = self.points[-1]
        if ((x - latest.x)**2 + (y - latest.y)**2)**0.5 > 30:
            self.points.append(point(x, y))
            return
    def draw(self, WIN, x, y, drawing):
        if len(self.points) < 2: return
        if drawing:
            pygame.draw.lines(WIN, self.color, False, [p.toTuple() for p in self.points] + [(x, y)], 5)
        else:
            pygame.draw.lines(WIN, self.color, False, [p.toTuple() for p in self.points], 5)


lines:list[Line] = []
while True:
    l, m, r = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                lines.append(Line((255, 255, 255)))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                lines[-1].points.append(point(x, y))


    if l:
        lines[-1].addPoint(x, y)

    for i, line in enumerate(lines[::-1]):
        line.draw(WIN, x, y, i==0 and l)

    pygame.display.update()
    WIN.fill((0, 0, 0))