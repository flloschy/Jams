import pygame, math
pygame.font.init()
from random import randint as rint

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 20)

###
radius1 = rint(2, 350)
radius2 = rint(2, 350)
mass1 = rint(1, 65)
mass2 = rint(1, 65)
a1 = math.pi/rint(-2, 10)
a2 = math.pi/rint(-2, 10)
# radius1 = 56
# radius2 = 234
# mass1 = 12
# mass2 = 35
# a1 = 1000
# a2 = 2903
a1_v = 0
a2_v = 0
g = 1

lastx2 = -1
lasty2 = -1

###
BLACK = (0, 0, 0)
RED = (255, 66, 66)
DARKRED = (87, 34, 34)
GREEN = (66, 255, 135)
DARKGREEN = (40, 94, 60)
PINK = (167, 66, 255)
DARKPINK = (66, 39, 89)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

offsetx = WIDTH//2
offsety = HEIGHT//2

clock = pygame.time.Clock()

s = pygame.Surface((WIDTH, HEIGHT))
s.set_alpha(1) #max 128
s.fill(BLACK)

friction = 0.99

tail = []
remove = 1

tick = 0



class Slider:
    def __init__(self, xsize:int, ysize:int, xpos:int, ypos:int, current:int):
        self.xsize = xsize
        self.ysize = ysize
        self.xpos = xpos
        self.ypos = ypos
        self.current = current

    def slide(self, x, y, pressed):
        if pressed:
            if x in range(self.xpos, self.xpos+self.xsize) and y in range(self.ypos, self.ypos+self.ysize):
                self.current = x - self.xpos

FPS = Slider(xsize=200, ysize=15, xpos=10, ypos=10, current=60)
GRAVITATION = Slider(xsize=200, ysize=15, xpos=10, ypos=40, current=101)
BOB1 = Slider(xsize=200, ysize=15, xpos=10, ypos=70, current=101)
BOB2 = Slider(xsize=200, ysize=15, xpos=10, ypos=100, current=101)
RADIUS1= Slider(xsize=200, ysize=15, xpos=10, ypos=130, current=101)
RADIUS2 =  Slider(xsize=200, ysize=15, xpos=10, ypos=160, current=101)

while True:
    # WIN.blit(s, (0,0))
    WIN.fill(BLACK)
    tick += 1
    if FPS.current != 199:
        WIN.blit(FONT.render(f'FPS: {FPS.current}', False, WHITE), (10, 20))
        clock.tick(FPS.current)
    else: 
        WIN.blit(FONT.render(f'FPS: max', False, WHITE), (10, 20))
    
    if  -5 <= (GRAVITATION.current-100)/12 >= -5:
        g = (GRAVITATION.current-100)/12
    WIN.blit(FONT.render(f'G Force: {g}', False, WHITE), (10, 50))

    if 1 <= (BOB1.current//2) >= 1:
        mass1 = BOB1.current//2
    WIN.blit(FONT.render(f'BOB1 Mass: {mass1}', False, WHITE), (10, 80))

    if 1 <= (BOB2.current//2) >= 1:
        mass2 = BOB2.current//2
    WIN.blit(FONT.render(f'BOB2 Mass: {mass2}', False, WHITE), (10, 110))

    if 1 <= (RADIUS1.current) >= 1:
        radius1 = RADIUS1.current
    WIN.blit(FONT.render(f'Radius1: {radius1}', False, WHITE), (10, 140))

    if 1 <= (RADIUS2.current) >= 1:
        radius2 = RADIUS2.current
    WIN.blit(FONT.render(f'Radius2: {radius2}', False, WHITE), (10, 170))



    num1 = -g * (2 * mass1 + mass2) * math.sin(a1)
    num2 = -mass2 * g * math.sin(a1 - 2 * a2)
    num3 = -2 * math.sin(a1 - a2) * mass2
    num4 = a2_v * a2_v * radius2 + a1_v * a1_v * radius1* math.cos(a1 - a2)
    den = radius1 * (2 * mass1+ mass2 - mass2 * math.cos(2 * a1 - 2 * a2))
    a1_a = (num1 + num2 + num3 * num4) / den

    num1 = 2 * math.sin(a1-a2)
    num2 = a1_v * a1_v * radius1 * (mass1 + mass2)
    num3 = g * (mass1 + mass2) * math.cos(a1)
    num4 = a2_v * a2_v * radius2 * mass2 * math.cos(a1 - a2)
    den = radius2 * (2 * mass1 + mass2 - mass2 * math.cos(2 * a1 - 2 * a2))
    a2_a = (num1 * (num2 + num3 + num4)) / den



    x1 = (radius1 * math.sin(a1))
    y1 = (radius1 * math.cos(a1))
    x2 = (x1 + radius2 * math.sin(a2))
    y2 = (y1 + radius2 * math.cos(a2))

    for t in tail:
        if tick % 5 == 0:
            rgb1, rgb2, rgb3 = t[4]
            if rgb1-remove > 0: rgb1-=remove
            if rgb2-remove > 0: rgb2-=remove
            if rgb3-remove > 0: rgb3-=remove
            t[4] = (rgb1, rgb2, rgb3)
            if rgb1-remove-1 <= 0 and rgb2-remove-1 <= 0 and rgb3-remove-1 <= 0: tail.remove(t)
        pygame.draw.line(WIN, t[4],start_pos=(t[0], t[1]), end_pos=(t[2], t[3]), width=2)


    pygame.draw.circle(WIN, (50, 50, 50), (offsetx, offsety), radius=radius1+radius2+mass2+5, width=3)
    pygame.draw.line(WIN, DARKRED, start_pos=(offsetx, offsety), end_pos=(offsetx+x1, offsety+y1))
    pygame.draw.line(WIN, DARKGREEN, start_pos=(offsetx+x1, offsety+y1), end_pos=(offsetx+x2, offsety+y2))
    pygame.draw.circle(WIN, RED, (offsetx+x1, offsety+y1), radius=mass1)
    pygame.draw.circle(WIN, GREEN, (offsetx+x2, offsety+y2), radius=mass2)

    if tick != 1: tail.append([offsetx+x2, offsety+y2, offsetx+lastx2, offsety+lasty2, PINK])

    a1_v += a1_a
    a2_v += a2_a
    a1 += a1_v
    a2 += a2_v

    lastx2 = x2
    lasty2 = y2

    a1_v *= friction
    a2_v *= friction


    pygame.draw.line(WIN, GRAY, start_pos=(10, 10), end_pos=(10+FPS.xsize, 10), width=10)
    lmb, mmb, rmb = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()
    ANY = any([lmb, mmb, rmb])
    FPS.slide(mousex, mousey, ANY)
    pygame.draw.line(WIN, WHITE, start_pos=(10, 10), end_pos=(10+FPS.current, 10), width=10)

    pygame.draw.line(WIN, GRAY, start_pos=(10, 40), end_pos=(10+GRAVITATION.xsize, 40), width=10)
    GRAVITATION.slide(mousex, mousey, ANY)
    pygame.draw.line(WIN, WHITE, start_pos=(10, 40), end_pos=(10+GRAVITATION.current, 40), width=10)

    pygame.draw.line(WIN, GRAY, start_pos=(10, 70), end_pos=(10+BOB1.xsize, 70), width=10)
    BOB1.slide(mousex, mousey, ANY)
    pygame.draw.line(WIN, WHITE, start_pos=(10, 70), end_pos=(10+BOB1.current, 70), width=10)

    pygame.draw.line(WIN, GRAY, start_pos=(10, 100), end_pos=(10+BOB2.xsize, 100), width=10)
    BOB2.slide(mousex, mousey, ANY)
    pygame.draw.line(WIN, WHITE, start_pos=(10, 100), end_pos=(10+BOB2.current, 100), width=10)

    pygame.draw.line(WIN, GRAY, start_pos=(10, 130), end_pos=(10+RADIUS1.xsize, 130), width=10)
    RADIUS1.slide(mousex, mousey, ANY)
    pygame.draw.line(WIN, WHITE, start_pos=(10, 130), end_pos=(10+RADIUS1.current, 130), width=10)

    pygame.draw.line(WIN, GRAY, start_pos=(10, 160), end_pos=(10+RADIUS2.xsize, 160), width=10)
    RADIUS2.slide(mousex, mousey, ANY)
    pygame.draw.line(WIN, WHITE, start_pos=(10, 160), end_pos=(10+RADIUS2.current, 160), width=10)







    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                while True:
                    end = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_p:
                                end = True
                            elif event.key == pygame.K_ESCAPE:
                                exit()
                    if end: break
                    pygame.display.update()
            elif event.key == pygame.K_ESCAPE:
                exit()

    pygame.display.update()