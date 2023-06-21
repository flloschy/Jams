import math, pygame
from random import randint as rint

class Color:
    def __init__(self):
        self.black = (0, 0, 0)
        self.gray = (130, 130, 130)
        self.white = (255, 255, 255)
        #
        self.red = (166, 57, 50)
        self.orange = (240, 123, 46)
        self.yellow = (212, 206, 47)
        self.green = (69, 166, 50)
        self.blue = (50, 237, 190)
        self.pink = (141, 50, 166)
        self.violet = (111, 64, 199)
        #
        self.darkgray = (50, 50, 50)
        self.darkred = (87, 28, 24)
        self.darkorage = (69, 42, 24)
        self.darkyellow = (66, 65, 23)
        self.darkgreen = (36, 87, 24)
        self.darkblue = (22, 69, 57)
        self.darkpink = (73, 24, 87)
        self.darkviolet = (44, 30, 69)
        #
        self.listing = [
            self.red,
            self.orange,
            self.yellow,
            self.green,
            self.blue,
            self.pink,
            self.white,
            self.violet,
        ]
        #
        # for _ in range(0, 500):
        #     self.listing.append((rint(0, 255), rint(0, 255), rint(0, 255)))


    def reset(self):
        self.listing = [
            self.red,
            self.orange,
            self.yellow,
            self.green,
            self.blue,
            self.pink,
            self.white,
            self.violet,
        ]
        # for _ in range(0, 500):
        #     self.listing.append((rint(0, 255), rint(0, 255), rint(0, 255)))

class DoublePendulum:
    def __init__(self, x, y, tailcolor, linecolor1, linecolor2, colorbob1, colorbob2, radius1=None, radius2=None, mass1=None, mass2=None, a1=None, a2=None, a1_v=None, a2_v=None, g=None, tail=None):
        if radius1 == None: self.radius1 = rint(20, 400)
        else: self.radius1 = radius1
        if radius2 == None: self.radius2 = rint(20, 400)
        else: self.radius2 = radius2
        if mass1 == None: self.mass1 = rint(1, 80)
        else: self.mass1 = mass1
        if mass2 == None: self.mass2 = rint(1, 80)
        else: self.mass2 = mass2
        if a1 == None: self.a1 = math.pi/rint(1, 8)
        else: self.a1 = a1
        if a2 == None: self.a2 = math.pi/rint(1, 8)
        else: self.a2 = a2
        if a1_v == None: self.a1_v = 0
        else: self.a1_v = a1_v
        if a2_v == None: self.a2_v = 0
        else: self.a2_v = a2_v
        if g == None: self.g = 1
        else: self.g = g
        self.tailcol = tailcolor
        self.lastx2, self.lasty2 = -1, -1
        self.offsetx, self.offsety = x, y
        if tail == None: self.tail = []
        else: self.tail = tail
        self.friction = 1
        self.color = {"line1": linecolor1, "line2": linecolor2, "bob1": colorbob1, "bob2": colorbob2},
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0

    def calcpos(self):
        try:
            num1 = -self.g * (2 * self.mass1 + self.mass2) * math.sin(self.a1)
            num2 = -self.mass2 * self.g * math.sin(self.a1 - 2 * self.a2)
            num3 = -2 * math.sin(self.a1 - self.a2) * self.mass2
            num4 = self.a2_v * self.a2_v * self.radius2 + self.a1_v * self.a1_v * self.radius1* math.cos(self.a1 - self.a2)
            den = self.radius1 * (2 * self.mass1+ self.mass2 - self.mass2 * math.cos(2 * self.a1 - 2 * self.a2))
            self.a1_a = (num1 + num2 + num3 * num4) / den
            #######################################
            num1 = 2 * math.sin(self.a1-self.a2)
            num2 = self.a1_v * self.a1_v * self.radius1 * (self.mass1 + self.mass2)
            num3 = self.g * (self.mass1 + self.mass2) * math.cos(self.a1)
            num4 = self.a2_v * self.a2_v * self.radius2 * self.mass2 * math.cos(self.a1 - self.a2)
            den = self.radius2 * (2 * self.mass1 + self.mass2 - self.mass2 * math.cos(2 * self.a1 - 2 * self.a2))
            self.a2_a = (num1 * (num2 + num3 + num4)) / den
            #########################################
            x1 = (self.radius1 * math.sin(self.a1))
            y1 = (self.radius1 * math.cos(self.a1))
            x2 = (x1 + self.radius2 * math.sin(self.a2))
            y2 = (y1 + self.radius2 * math.cos(self.a2))
            ##################################
            self.a1_v += self.a1_a
            self.a2_v += self.a2_a
            self.a1 += self.a1_v
            self.a2 += self.a2_v
            ############
            self.a1_v *= self.friction
            self.a2_v *= self.friction
            ####################
        except:
            self.a1 = 0
            self.a2 = 0
            self.calcpos()
        else:
            self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
            remove = 1
            for t in self.tail:
                r, g, b = t[4]
                if r-remove > 0: r-=remove
                if g-remove > 0: g-=remove
                if b-remove > 0: b-=remove
                if r-remove-1 <= 0 and g-remove-1 <= 0 and b-remove-1 <= 0: self.tail.remove(t); continue
                t[4] = (r, g, b)
                t[5] -= 0.25
                if t[5] <= 1: self.tail.remove(t); continue

    def draw(self, WIN, hitbox):
        pos = [self.x1, self.y1, self.x2, self.y2]
        self.tail.append([pos[2], pos[3], self.lastx2, self.lasty2, self.tailcol, 10])

        self.lastx2, self.lasty2 = pos[2], pos[3]
        circleWidth = 10
        def drawhitbox():
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(self.offsetx, self.offsety, pos[0], pos[1]), width=1) #line1
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(self.offsetx+pos[0], self.offsety+pos[1], -(pos[0]-pos[2]), -(pos[1]-pos[3])), width=1) #line2
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(self.offsetx+pos[0]-self.mass1, self.offsety+pos[1]-self.mass1, self.mass1*2, self.mass1*2), width=1) #bob1
            pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(self.offsetx+pos[2]-self.mass2, self.offsety+pos[3]-self.mass2, self.mass2*2, self.mass2*2), width=1) #bob2
            if self.mass1+self.radius1+self.radius2 > self.mass2+self.radius1+self.radius2: 
                pygame.draw.rect(WIN, (0, 255, 0), pygame.Rect(self.offsetx-(self.radius1+self.radius2+self.mass1), self.offsety-(self.radius1+self.radius2+self.mass1), (self.radius1+self.radius2+self.mass1)*2, (self.radius1+self.radius2+self.mass1)*2), width=1)
            else:
                pygame.draw.rect(WIN, (0, 255, 0), pygame.Rect(self.offsetx-(self.radius1+self.radius2+self.mass2), self.offsety-(self.radius1+self.radius2+self.mass2), (self.radius1+self.radius2+self.mass2)*2, (self.radius1+self.radius2+self.mass2)*2), width=1)

        if self.inWinLine(WIN, self.offsetx, self.offsety, pos[0], pos[1]):
            pygame.draw.line(WIN, self.color[0]["line1"], start_pos=(self.offsetx, self.offsety), end_pos=(self.offsetx+pos[0], self.offsety+pos[1]))
        if self.inWinLine(WIN, self.offsetx+pos[0], self.offsety+pos[1], -(pos[0]-pos[2]), -(pos[1]-pos[3])):
            pygame.draw.line(WIN, self.color[0]["line2"], start_pos=(self.offsetx+pos[0], self.offsety+pos[1]), end_pos=(self.offsetx+pos[2], self.offsety+pos[3]))
        if self.inWinBob(WIN, self.offsetx+pos[0], self.offsety+pos[1], self.mass1):
            pygame.draw.circle(WIN, (0, 0, 0), (self.offsetx+pos[0], self.offsety+pos[1]), radius=self.mass1-(circleWidth), width=0)
            pygame.draw.circle(WIN, self.color[0]["bob2"], (self.offsetx+pos[0], self.offsety+pos[1]), radius=self.mass1, width=circleWidth)
        if self.inWinBob(WIN, self.offsetx+pos[2], self.offsety+pos[3], self.mass2):
            pygame.draw.circle(WIN, (0, 0, 0), (self.offsetx+pos[2], self.offsety+pos[3]), radius=self.mass2-(circleWidth), width=0)
            pygame.draw.circle(WIN, self.color[0]["bob2"], (self.offsetx+pos[2], self.offsety+pos[3]), radius=self.mass2, width=circleWidth)

        if hitbox: drawhitbox()

    def drawtail(self, WIN, hitbox):
        pos = [self.x1, self.y1, self.x2, self.y2]
        # pygame.draw.line(WIN, t[4], start_pos=(self.offsetx+t[0], self.offsety+t[1]), end_pos=(self.offsetx+t[2], self.offsety+t[3]), width=t[5])
        for t in self.tail:
            if self.inWinLine(WIN, self.offsetx+t[0], self.offsety+t[1], self.offsetx+t[2], self.offsety+t[3]):
                pygame.draw.line(WIN, t[4], start_pos=(self.offsetx+t[0], self.offsety+t[1]), end_pos=(self.offsetx+t[2], self.offsety+t[3]), width=int(t[5]))
            if self.inWinBob(WIN, self.offsetx+t[0], self.offsety+t[1], int(t[5])):
                pygame.draw.circle(WIN, t[4], (self.offsetx+t[0], self.offsety+t[1]), radius=int(t[5]))
            if hitbox:
                pygame.draw.rect(WIN, (0, 0, 255), pygame.Rect(self.offsetx+t[0]-int(t[5]), self.offsety+t[1]-int(t[5]), int(t[5])*2, int(t[5])*2), width=1) #circle
                pygame.draw.rect(WIN, (0, 0, 255), pygame.Rect(self.offsetx+t[0], self.offsety+t[1], -(t[0]-t[2]), -(t[1]-t[3])), width=1) #line

        if len(self.tail) >= 1: pygame.draw.circle(WIN, self.tail[-1][4], (self.offsetx+pos[2], self.offsety+pos[3]), radius=self.tail[-1][5]-5)

    def inWinBob(self, WIN, x, y, radius):
        if x-radius > WIN.get_width(): return False
        if y-radius > WIN.get_height(): return False
        if x+radius < 0: return False
        if y+radius < 0: return False
        return True

    def inWinLine(self, WIN, x, y, sizex, sizey):
        if x + sizex < 0 and x - sizex < 0: return False
        if y + sizey < 0 and y - sizey < 0: return False
        if x + sizex > WIN.get_width() and x - sizex > WIN.get_width(): return False
        if y + sizey > WIN.get_height() and y - sizey > WIN.get_height(): return False
        return True





        if self.offsetx + pos[0] < 0: return False
        if self.offsety + pos[1] < 0: return False
        # if (self.offsetx + pos[0]) - (pos[0]-pos[2]) > WIN.get_width(): return False
        # if (self.offsety+pos[1]) - (pos[1]-pos[3]) > WIN.get_height(): return False
        if (self.offsetx + pos[0]) - (pos[0]-pos[2]) > 1000: return False
        if (self.offsety+pos[1]) - (pos[1]-pos[3]) > 1000: return False
        return True

class Slider:
    def __init__(self, xsize:int, ysize:int, xpos:int, ypos:int, current:int, text:str):
        self.xsize = xsize
        self.ysize = ysize
        self.xpos = xpos
        self.ypos = ypos
        self.current = current
        self.text = text

    def slide(self, x, y, pressed):
        if pressed:
            if x in range(self.xpos, self.xpos+self.xsize+2) and y in range(self.ypos, self.ypos+self.ysize):
                self.current = x - self.xpos
                return True

    def draw(self, WIN, COLOR):
        pygame.draw.line(WIN, COLOR.darkred, start_pos=(self.xpos, self.ypos), end_pos=(self.xpos+self.xsize, self.ypos), width=self.ysize)
        pygame.draw.line(WIN, COLOR.red, start_pos=(self.xpos, self.ypos), end_pos=(self.xpos+self.current, self.ypos), width=self.ysize)
    
    def drawtext(self, WIN, FONT, COLOR, text):
        WIN.blit(FONT.render(f'{self.text}: {text}', False, COLOR.white), (self.xpos+self.xsize+10, self.ypos))
