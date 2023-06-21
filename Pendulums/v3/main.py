from modules import Color, DoublePendulum, Slider
from random import choice
import pygame, time, json, os
from termcolor import cprint as p
from termcolor import colored as col
pygame.font.init()

if os.path.isfile("./v3/saves/placeholder"): os.remove("./v3/saves/placeholder")

FPS = 60
TPS = FPS * 2
Color = Color()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
WIN.fill(Color.black)
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 20)
offsetx, offsety = WIDTH//2, HEIGHT//2

transparency = 40
s = pygame.Surface((WIDTH, HEIGHT))
s.set_alpha(transparency)  # max 128
s.fill(Color.black)

globalgravity = 1
zoom = 1
lastpos = (0, 0)

slider = [ Slider(200, 20, 10, 10, 200, "Gravity"), Slider(200, 20, 10, 50, TPS, "TPS") ]
c = choice(Color.listing)
Color.listing.remove(c)
Pendulums = [DoublePendulum(offsetx, offsety, c, c, c, c, c)]

clock = pygame.time.Clock()

lastFrameTick = 1
lastPhysikTick = 1
hitbox = False

def drawframe(s, Pendulums, globalgravity, slider, WIN, FONT, Color, TPS, FPS, zoom, lastpos, offsetx, offsety, hitbox):
    clock.tick(FPS)
    pygame.display.update()
    WIN.blit(s, (0, 0))


    l, m, r = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    for pend in Pendulums:
        pend.drawtail(WIN, hitbox)

    for pend in Pendulums:
        pend.g = globalgravity
        pend.draw(WIN, hitbox)

    pygame.draw.rect(WIN, Color.black, pygame.Rect(0, 0, 330, 100))

    slided = False
    for sli in slider:
        slid = sli.slide(x, y, l)
        if slid: slided = True
        sli.draw(WIN, Color)
        if sli.text == "Gravity":
            if slid: globalgravity = (sli.current-100)/100
            sli.drawtext(WIN, FONT, Color, globalgravity)
        elif sli.text == "TPS":
            if slid: TPS = (sli.current+10)
            sli.drawtext(WIN, FONT, Color, TPS)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    end = True
                    while end:
                        clock.tick(10)
                        WIN.fill((0, 0, 0))
                        x, y = pygame.mouse.get_pos()
                        _, m , r = pygame.mouse.get_pressed()
                        for pen in Pendulums:
                            pen.draw(WIN, hitbox)
                            pen.drawtail(WIN, hitbox)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    end = False
                                elif event.key == pygame.K_ESCAPE:
                                    exit()
                            elif event.type == pygame.MOUSEMOTION and m:
                                if lastpos != (x, y):
                                    offset = x - lastpos[0]
                                    offset2 = y - lastpos[1]
                                    for pen in Pendulums:
                                        if offset < 0: pen.offsetx += x - lastpos[0]
                                        elif offset > 0: pen.offsetx += x - lastpos[0]
                                        if offset2 < 0: pen.offsety += y - lastpos[1]
                                        elif offset2 > 0: pen.offsety += y - lastpos[1]
                            elif event.type == pygame.MOUSEBUTTONUP and r:
                                c = choice(Color.listing)
                                Color.listing.remove(c)
                                Pendulums.append(DoublePendulum(x, y, c, c, c, c, c))
                            elif event.type == pygame.VIDEORESIZE:
                                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                                WIDTH = event.w
                                HEIGHT = event.h
                                offsetx = WIDTH//2
                                offsety = HEIGHT//2
                                ns = pygame.Surface((WIDTH, HEIGHT))
                                ns.set_alpha(transparency)  # max 128
                                ns.fill(Color.black)
                                s = ns
                        lastpos = (x, y)
                        pygame.display.update()
                elif event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_r:
                    globalgravity = 1
                    TPS = FPS*2
                    c = choice(Color.listing)
                    Color.listing.remove(c)
                    Pendulums.clear()
                    Color.reset()
                    Pendulums.append(DoublePendulum(offsetx, offsety, c, c, c, c, c))
                    slider[0].current = 200
                    slider[1].current = TPS
                elif event.key == pygame.K_s:
                    preparedPends = []
                    for pen in Pendulums.copy(): preparedPends.append(vars(pen))
                    for pen in preparedPends: pen["tail"] = []
                    save = {"g": globalgravity, "pend": preparedPends}
                    file = f'./v3/saves/{time.strftime("%Y-%m-%d_%H-%M-%S.json")}'
                    try: json.dump(save, open(file, "x"), indent = 1)
                    except Exception: p("Saving Failed...", "red")
                    else: p("Saved", "green")
                elif event.key == pygame.K_l:
                    dirlist = os.listdir("./v3/saves/")
                    if not dirlist: p("\n--- There are no saves.\n", "red"); continue
                    p("index", "yellow", attrs=["underline"], end=''); p("\t| ", attrs=["underline"], end=''); p("Year-Month-Day_Hour-Minute-Seconds", "green", attrs=["underline"])
                    for i, file in enumerate(dirlist): p(f'{i}', "yellow", end=''); p("\t| ", end=''); p(f'{file}', "green")
                    while True:
                        try: choosen = int(input(col(f"Choose a file between 0 and {len(dirlist)-1}\n--->   ", "cyan")))
                        except KeyboardInterrupt: exit(1)
                        except: p("\n--- Input needs to be a number\n", "red"); continue
                        if not (0 <= choosen <= len(dirlist)-1): p(f"\n--- index not between 0 and {len(dirlist)-1}\n", "red")
                        else:
                            Pendulums.clear()
                            data = json.load(open(f"./v3/saves/{dirlist[choosen]}"))
                            globalgravity = data['g']
                            for pen in data['pend']:
                                Pendulums.append(DoublePendulum(
                                    pen['offsetx'],
                                    pen['offsety'],
                                    pen['tailcol'], 
                                    pen['color'][0]['line1'],
                                    pen['color'][0]['line2'],
                                    pen['color'][0]['bob1'],
                                    pen['color'][0]['bob2'],
                                    radius1=pen['radius1'],
                                    radius2=pen['radius2'],
                                    mass1=pen['mass1'],
                                    mass2=pen['mass2'],
                                    a1=pen['a1'],
                                    a2=pen['a2'],
                                    a1_v=pen['a1_v'],
                                    a2_v=pen['a2_v'],
                                    g=globalgravity,
                                    tail=pen['tail']
                                    )
                                )
                            break
                    p("loaded...", "green")

                elif event.key == pygame.K_h:
                    if hitbox: hitbox = False
                    else: hitbox = True

            elif event.type == pygame.MOUSEBUTTONUP and not slided and r:
                try: c = choice(Color.listing)
                except Exception: Color.reset()
                c = choice(Color.listing)
                Color.listing.remove(c)
                Pendulums.append(DoublePendulum(x, y, c, c, c, c, c))

            elif event.type == pygame.MOUSEMOTION and m:
                if lastpos != (x, y):
                    offset = x - lastpos[0]
                    offset2 = y - lastpos[1]
                    for pen in Pendulums:
                        if offset < 0: pen.offsetx += x - lastpos[0]
                        elif offset > 0: pen.offsetx += x - lastpos[0]
                        if offset2 < 0: pen.offsety += y - lastpos[1]
                        elif offset2 > 0: pen.offsety += y - lastpos[1]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: zoom += 1
                if event.button == 5 and zoom != 0: zoom -= 1

            elif event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                WIDTH = event.w
                HEIGHT = event.h
                offsetx = WIDTH//2
                offsety = HEIGHT//2
                ns = pygame.Surface((WIDTH, HEIGHT))
                ns.set_alpha(transparency)  # max 128
                ns.fill(Color.black)
                s = ns

    WIN.blit(FONT.render(f'FPS: {round(clock.get_fps(), 0)}', False, Color.white), (10, 70))
    lastpos = [x, y]
    return globalgravity, TPS, zoom, lastpos, s, offsetx, offsety, hitbox

def physiktick():
    for pen in Pendulums:
        pen.calcpos()

while True:
    start = time.perf_counter()
    if time.perf_counter() - lastPhysikTick > 1/TPS:
        physiktick()
        lastPhysikTick = time.perf_counter()

    if time.perf_counter() - lastFrameTick > 1/FPS:
        globalgravity, TPS, zoom, lastpos, s, offsetx, offsety, hitbox = \
            drawframe(s, Pendulums, globalgravity, slider, WIN, FONT, Color, TPS, FPS, zoom, lastpos, offsetx, offsety, hitbox)
        lastFrameTick = time.perf_counter()
