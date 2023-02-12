import pygame, math, random, time
pygame.mixer.init()
pygame.font.init()

class Assets:
    def __init__(self):
        self.BRICK = pygame.image.load("./assets/Brick_texture.png")
        self.CURSOR = pygame.transform.scale(pygame.image.load("./assets/CrossHair.png"), (14, 14))
        self.CURSORBIG = pygame.transform.scale(pygame.image.load("./assets/CrossHair.png"), (18, 18))
        self.ARROW = pygame.image.load("./assets/wavy_gray_scale_arrow.png")
        temp = pygame.Surface((self.ARROW.get_width()*3, self.ARROW.get_height()))
        temp.fill((0, 0, 0))
        temp.set_colorkey((0, 0, 0))
        temp.blit(self.ARROW, (self.ARROW.get_width()*2, 0))
        self.ARROW = temp
        self.ARROWTURNED = self.ARROW
        self.CAT = pygame.transform.scale(pygame.image.load("./assets/cat.png"), (50, 50))
        self.BLOB = pygame.image.load("./assets/Sprite-0001.png")
        self.BLOB.set_alpha(100)
        self.KNIFE = pygame.transform.scale(pygame.image.load("./assets/knife.png"), (50, 50))
        temp = pygame.Surface((self.KNIFE.get_width(), self.KNIFE.get_height()*3))
        temp.fill((0, 0, 0))
        temp.set_colorkey((0, 0, 0))
        temp.blit(self.KNIFE, (0, 0))
        self.KNIFE = temp
        self.KNIFETUREND = self.KNIFE
        self.HEART = pygame.image.load("./assets/REDHEART.png")
        self.GEMS = pygame.image.load("./assets/gems_db16.png")
        self.GEMBLUE = pygame.Surface((self.GEMS.get_width()//2, self.GEMS.get_height()//3))
        self.GEMBLUE.fill((0, 0, 0))
        self.GEMBLUE.set_colorkey((0, 0, 0))
        self.GEMBLUE.blit(self.GEMS, (0, -(1*(self.GEMS.get_height()//3))))
        self.GEMGREEN = pygame.Surface((self.GEMS.get_width()//2, self.GEMS.get_height()//3))
        self.GEMGREEN.fill((0, 0, 0))
        self.GEMGREEN.set_colorkey((0, 0, 0))
        self.GEMGREEN.blit(self.GEMS, (-self.GEMS.get_width()//2, -(1*(self.GEMS.get_height()//3))))
        self.GEMRED = pygame.Surface((self.GEMS.get_width()//2, self.GEMS.get_height()//3))
        self.GEMRED.fill((0, 0, 0))
        self.GEMRED.set_colorkey((0, 0, 0))
        self.GEMRED.blit(self.GEMS, (0, -(2*(self.GEMS.get_height()//3))))
        self.GEMWHITE = pygame.Surface((self.GEMS.get_width()//2, self.GEMS.get_height()//3))
        self.GEMWHITE.fill((0, 0, 0))
        self.GEMWHITE.set_colorkey((0, 0, 0))
        self.GEMWHITE.blit(self.GEMS, (-self.GEMS.get_width()//2, -(2*(self.GEMS.get_height()//3))))
        self.COLLECTSOUND = pygame.mixer.Sound("./assets/ScoreUpdateSound (1).wav")
        self.BEEP = pygame.mixer.Sound("./assets/sfx.wav")
        self.HITCIRCLE = pygame.image.load("./assets/effect_bombdrop.png")
        self.HIT = pygame.Surface((self.HITCIRCLE.get_width()//4, self.HITCIRCLE.get_height()))
        self.HIT.fill((0, 0, 0))
        self.HIT.set_colorkey((0, 0, 0))
        self.HIT.blit(self.HITCIRCLE, (-((self.HITCIRCLE.get_width()//4)*1), 0))
        self.HITX = pygame.Surface((self.HITCIRCLE.get_width()//4, self.HITCIRCLE.get_height()))
        self.HITX.fill((0, 0, 0))
        self.HITX.set_colorkey((0, 0, 0))
        self.HITX.blit(self.HITCIRCLE, (0, 0))
        self.RATTHING = pygame.image.load("./assets/image.png")
def play():
    if pygame.mixer.music.get_busy(): return
    r = random.randint(0, 3)
    if r == 0:
        pygame.mixer.music.load("./assets/IanToujou_-_Arithmetic_Flow.mp3")
    elif r == 1:
        pygame.mixer.music.load("./assets/IanToujou_-_Gateway_Diffraction.mp3")
    elif r == 2:
        pygame.mixer.music.load("./assets/IanToujou_-_My_vacuum_cleaner_ate_my_cat.mp3")
    elif r == 3:
        pygame.mixer.music.load("./assets/IanToujou_-_Techno_Switch.mp3")
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play()

class WIN:
    def __init__(self):
        self.display = pygame.display.set_mode((500, 500))
        pygame.display.set_icon(ast.CAT)
        pygame.display.set_caption("Save The Cat!!!")
        pygame.mouse.set_visible(False)
    def update(self):
        pygame.display.update()
        eventUpdate()
    def drawGround(self):
        global ast
        for x in range(0, 500, ast.BRICK.get_width()):
            for y in range(0, 500, ast.BRICK.get_height()):
                self.display.blit(ast.BRICK, (x, y))
ast = Assets()
win = WIN()
blobs = [(random.randint(0, 500), random.randint(0, 500)) for _ in range(0, 50)]
gems = [] # {type:1|2|3|4, x:1, y:2, time:time.time()+5}
rats = [] 
lives = 3
dif = 10
ang = 0
start = time.time()
scores = {
    'gems': {
        1: 0,
        2: 0,
        3: 0,
        4: 0
    },
    'kills': 0,
    'hits': 0
}

def eventUpdate():
    global gems
    global ang
    global lives
    global rats
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        elif e.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            ang = math.atan2(250-x, 250-y) * (180/math.pi)
            ang += 90
            if ang < 0: ang = 360 + ang
            ast.ARROWTURNED = pygame.transform.rotate(ast.ARROW, ang)
            ast.KNIFETUREND = pygame.transform.rotate(ast.KNIFE, ang+90)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = pygame.mouse.get_pos()
                for gem in gems:
                    if gem['x'] < x < gem['x'] + ast.GEMS.get_width()//2:
                        if gem['y'] < y < gem['y'] + ast.GEMS.get_height()//3:
                            scores['gems'][gem['type']] += 1
                            if gem['type'] == 2: #green
                                lives += 1
                                ast.BEEP.play()
                                ast.COLLECTSOUND.play()
                            elif gem['type'] == 1: #blue
                                rats.clear()
                            elif gem['type'] == 3: #red
                                for _ in range(0, 10*dif+10): spawnRats()
                            elif gem['type'] == 4: #white
                                gems.clear()
                                continue
                            gems.remove(gem)
                            ast.COLLECTSOUND.play()
def drawCursor():
    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        win.display.blit(ast.CURSORBIG, (x-ast.CURSORBIG.get_width()//2, y-ast.CURSORBIG.get_height()//2))
    else:
        win.display.blit(ast.CURSOR, (x-ast.CURSOR.get_width()//2, y-ast.CURSOR.get_height()//2))
def drawArrow():
    win.display.blit(ast.ARROWTURNED, (250-ast.ARROWTURNED.get_width()//2, 250-ast.ARROWTURNED.get_height()//2))
def drawCat():
    win.display.blit(ast.CAT, (250-ast.CAT.get_width()//2, 250-ast.CAT.get_height()//2))
def drawBlobs():
    for x, y in blobs:
        win.display.blit(ast.BLOB, (x, y))
def drawKnife():
    win.display.blit(ast.KNIFETUREND, (250-ast.KNIFETUREND.get_width()//2, 250-ast.KNIFETUREND.get_height()//2))
    
    # draw knife hitbox
    # pygame.draw.rect(win.display, (255, 0, 0), (
    #     250+(math.sin((ang-90)/(180/math.pi))*65)-10, 
    #     250+(math.cos((ang-90)/(180/math.pi))*65)-10, 
    #     20, 
    #     20))
def drawLives():
    for l in range(0, lives):
        win.display.blit(ast.HEART, (5+(l*(ast.HEART.get_width()+5)), 5))
def drawGems():
    global gems
    for gem in gems:
        if gem['type'] == 1:
            win.display.blit(ast.GEMBLUE, (gem['x'], gem['y']))
        elif gem['type'] == 2:
            win.display.blit(ast.GEMGREEN, (gem['x'], gem['y']))
        elif gem['type'] == 3:
            win.display.blit(ast.GEMRED, (gem['x'], gem['y']))
        elif gem['type'] == 4:
            win.display.blit(ast.GEMWHITE, (gem['x'], gem['y']))
        if time.time() > gem['time']:
            gems.remove(gem)
def spawnGems():
    if random.randint(0, (100*(10-dif))+10) == 0:
        gems.append({'type':random.randint(1, 4), 'x':random.randint(0, 500), 'y':random.randint(0, 500), 'time':time.time()+2})
def drawRats():
    global rats
    for r in rats:
        win.display.blit(ast.RATTHING, (r[0], r[1]))
def spawnRats():
    global rats
    if random.randint(0, (100*dif)+10) == 0:
        t = random.randint(0, 360)
        x = 500*math.cos(t) + 250
        y = 500*math.sin(t) + 250
        rats.append([x, y])
def moveRats():
    global rats
    global lives
    global scores
    for rat in rats:
        if rat[0] < 250-ast.RATTHING.get_width()//2:
            rat[0] += 1
        elif rat[0] > 250-ast.RATTHING.get_width()//2:
            rat[0] -= 1
        if rat[1] < 250-ast.RATTHING.get_height()//2:
            rat[1] += 1
        elif rat[1] > 250-ast.RATTHING.get_height()//2:
            rat[1] -= 1
        if rat[0] < 250+ast.RATTHING.get_width()//2 and rat[0]+ast.RATTHING.get_width()//2 > 250-ast.RATTHING.get_width()//2:
            if rat[1] < 250+ast.RATTHING.get_height()//2 and rat[1]+ast.RATTHING.get_height()//2 > 250-ast.RATTHING.get_width()//2:
                scores['hits'] += 1
                lives -= 1
                rats.remove(rat)
                ast.BEEP.play()
                continue
        if pygame.Rect(250+(math.sin((ang-90)/(180/math.pi))*65)-10, 250+(math.cos((ang-90)/(180/math.pi))*65)-10, 20, 20).colliderect((rat[0], rat[1], ast.RATTHING.get_width(), ast.RATTHING.get_height())):
            scores['kills'] += 1
            rats.remove(rat)
def drawDif():
    for x in range(0, 10):
        if x < dif:
            win.display.blit(ast.HIT, (10+((ast.HIT.get_width()+10)*x), 480-ast.HIT.get_height()))
        else:
            win.display.blit(ast.HITX, (10+((ast.HITX.get_width()+10)*x), 480-ast.HITX.get_height()))
def updateDif():
    global dif
    global start
    if time.time() - start > 20:
        start = time.time()
        if dif > 0:
            dif -= 1

def loop():
    if lives <= 0:
        return False
    play()
    win.drawGround()
    drawBlobs()
    drawArrow()
    drawCat()
    drawKnife()
    moveRats()
    spawnRats()
    drawRats()
    drawGems()
    drawLives()
    drawCursor()
    spawnGems()
    drawDif()
    updateDif()
    win.update()
    return True


font = pygame.font.Font("./assets/font.ttf", 15)

def introScreen():
    pygame.mouse.set_visible(True)
    while True: 
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break
        win.drawGround()
        win.display.blit(ast.HEART, (5, 5))
        win.display.blit(ast.HEART, (40, 5))
        win.display.blit(ast.HEART, (75, 5))
        win.display.blit(font.render("Health here, no heart -> you loose",True, (255, 255, 255), (0, 0, 0)), (120, 11))
        win.display.blit(ast.CAT, (250-ast.CAT.get_width()//2, 250-ast.CAT.get_height()//2))
        win.display.blit(font.render("Here is your Cat! (it doesn't like rat thingys)", True, (255, 255, 255), (0, 0, 0)), (100, 280))
        win.display.blit(ast.HIT, (5, 460))
        win.display.blit(ast.HIT, (25, 460))
        win.display.blit(ast.HIT, (45, 460))
        win.display.blit(ast.HIT, (65, 460))
        win.display.blit(ast.HIT, (85, 460))
        win.display.blit(ast.HIT, (105, 460))
        win.display.blit(ast.HITX, (125, 460))
        win.display.blit(ast.HITX, (145, 460))
        win.display.blit(ast.HITX, (165, 460))
        win.display.blit(font.render("This is the difficulty status going from 0 to 10", True, (255, 255, 255), (0, 0, 0)), (187, 450-20))
        win.display.blit(font.render("Higher difficulty = more rats, less gems", True, (255, 255, 255), (0, 0, 0)), (187, 470-20))
        win.display.blit(font.render("difficulty gets higher every 20 seconds!", True, (255, 255, 255), (0, 0, 0)), (187, 470))
        win.display.blit(ast.GEMBLUE, (5, 50))
        win.display.blit(font.render("Blue gems remove rats", True, (255, 255, 255), (0, 0, 0)), (35, 57))
        win.display.blit(ast.GEMGREEN, (5, 80))
        win.display.blit(font.render("Green gems give you live", True, (255, 255, 255), (0, 0, 0)), (35, 87))
        win.display.blit(ast.GEMRED, (5, 110))
        win.display.blit(font.render("Red gems Spawn more rats", True, (255, 255, 255), (0, 0, 0)), (35, 117))
        win.display.blit(ast.GEMWHITE, (5, 140))
        win.display.blit(font.render("White gems remove all gems", True, (255, 255, 255), (0, 0, 0)), (35, 147))
        win.display.blit(ast.CURSOR, (480, 50))
        win.display.blit(font.render("This is your Cursor", True, (255, 255, 255), (0, 0, 0)), (345, 48))
        win.display.blit(font.render("-> Use left click to collect gems", True, (255, 255, 255), (0, 0, 0)), (35, 177))
        win.display.blit(ast.RATTHING, (465, 400))
        win.display.blit(font.render("This is the rat thing", True, (255, 255, 255), (0, 0, 0)), (330, 400-4))
        win.display.blit(font.render("Press <ESC> to start playing!", True, (255, 255, 255), (0, 0, 0)), (5, 400-4))
        win.display.blit(font.render("You need to kill the rats with the knife,", True, (255, 255, 255), (0, 0, 0)), (5+235, 300-200))
        win.display.blit(font.render("and collect gems with your cursor,", True, (255, 255, 255), (0, 0, 0)), (5+250, 300+20-200))
        win.display.blit(font.render("which also controls the knife", True, (255, 255, 255), (0, 0, 0)), (5+270, 300+20+20-200))
        win.update()

def endScreen():
    pygame.mouse.set_visible(True)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        win.drawGround()
        win.display.blit(font.render("You loose!", True, (255, 255, 255), (0, 0, 0)), (230, 5))
        win.display.blit(ast.GEMBLUE, (5, 50))
        win.display.blit(font.render(f"Collected {scores['gems'][1]} Blue Gems", True, (255, 255, 255), (0, 0, 0)), (35, 56))
        win.display.blit(ast.GEMGREEN, (5, 100))
        win.display.blit(font.render(f"Collected {scores['gems'][2]} Green Gems", True, (255, 255, 255), (0, 0, 0)), (35, 106))
        win.display.blit(ast.GEMRED, (5, 150))
        win.display.blit(font.render(f"Collected {scores['gems'][3]} Red Gems", True, (255, 255, 255), (0, 0, 0)), (35, 156))
        win.display.blit(ast.GEMWHITE, (5, 200))
        win.display.blit(font.render(f"Collected {scores['gems'][4]} White Gems", True, (255, 255, 255), (0, 0, 0)), (35, 206))
        win.display.blit(ast.CAT, (5, 250))
        win.display.blit(font.render(f"Cat got hurt {scores['hits']} times :(", True, (255, 255, 255), (0, 0, 0)), (60, 266))
        win.display.blit(ast.RATTHING, (5, 320))
        win.display.blit(font.render(f"{scores['kills']} rat things got killed :)", True, (255, 255, 255), (0, 0, 0)), (40, 266+50))
        win.display.blit(ast.CURSORBIG, (5, 370))
        win.display.blit(font.render(f"Your Score: {scores['kills']//2-scores['hits'] + (scores['gems'][1]*.5 + scores['gems'][2]*1.2 + scores['gems'][3]*1.5 + scores['gems'][4]*-.5)}", True, (255, 255, 255), (0, 0, 0)), (40, 370))
        win.update()

introScreen()
pygame.mouse.set_visible(False)




clock = pygame.time.Clock()
while True:
    if not loop():
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        break
    clock.tick(60)
endScreen()