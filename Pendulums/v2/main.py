from modules import Color, DoublePendulum, Slider
from random import randint as rint
from random import choice
import pygame, time
pygame.font.init()

TPS = 60
Color = Color()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 20)
offsetx = WIDTH//2
offsety = HEIGHT//2

globalgravity = 1
zoom = 0

c = choice(Color.listing)
Color.listing.remove(c)
Pendulums = [DoublePendulum(offsetx, offsety, c, c, c, c, c)]

clock = pygame.time.Clock()
s = pygame.Surface((WIDTH, HEIGHT))
s.set_alpha(80)  # max 128
s.fill(Color.black)

laspos = [0, 0]

slider = [
    Slider(200, 20, 10, 10, 200, "Gravitation"),
    Slider(200, 20, 10, 50, 100, "TPS")
]

tick = 0
FPS = 0
WIN.fill(Color.black)
last = time.perf_counter()
lastT = time.perf_counter()
blackboxrect = pygame.Rect(0, 0, 330, 85)
while True:
    start = time.perf_counter()
    clock.tick(60)
    WIN.blit(s, (0, 0))
    # WIN.fill(Color.black)

    l, m, r = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()

    for pend in Pendulums:
        pend.drawtail(WIN)

    for pend in Pendulums:
        pend.g = globalgravity
        if start - lastT > 1/TPS: pend.calcpos(tick)
        pend.draw(WIN, tick)
    if start - lastT > 1/TPS:lastT = time.perf_counter()

    pygame.draw.rect(WIN, Color.black, blackboxrect)
    slided = False
    for sli in slider:
        slid = sli.slide(x, y, l)
        slided = slid
        sli.draw(WIN, Color)
        if sli.text == "Gravitation":
            if slid: globalgravity = (sli.current-100)/100
            sli.drawtext(WIN, FONT, Color, globalgravity)
        elif sli.text == "TPS":
            if slid: TPS = (sli.current+10)/2
            sli.drawtext(WIN, FONT, Color, TPS)

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
                    if end:
                        break
                    pygame.display.update()
            elif event.key == pygame.K_ESCAPE:
                exit()

        elif event.type == pygame.MOUSEBUTTONUP and not slided and r:
            c = choice(Color.listing)
            Color.listing.remove(c)
            Pendulums.append(DoublePendulum(x, y, c, c, c, c, c))

        elif event.type == pygame.MOUSEMOTION and m:
            if laspos != (x, y):
                offset = x - laspos[0]
                offset2 = y - laspos[1]
                for pen in Pendulums:
                    if offset < 0: pen.offsetx += x - laspos[0]
                    elif offset > 0: pen.offsetx += x - laspos[0]
                    if offset2 < 0: pen.offsety += y - laspos[1]
                    elif offset2 > 0: pen.offsety += y - laspos[1]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: zoom += 1
            if event.button == 5 and zoom != 0: zoom -= 1

    if start-last > 0.01:
        laspos = [x, y]
        last = time.perf_counter()

    tick += 1
    WIN.blit(FONT.render(f'FPS: {round(FPS, 0)}', False, Color.white), (10, 70))
    FPS = clock.get_fps()
    pygame.display.update()
