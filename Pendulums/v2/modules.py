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
            self.violet
        ]


class DoublePendulum:
    def __init__(self, x, y, tailcolor, linecolor1, linecolor2, bob1, bob2):
        self.radius1, self.radius2 = rint(2, 250), rint(2, 250)
        self.mass1, self.mass2 = rint(1, 70), rint(1, 70)
        self.a1, self.a2 = math.pi/rint(1, 100), math.pi/rint(1, 100)
        self.a1_v, self.a2_v = 0, 0
        self.g, self.tailcol = 1, tailcolor
        self.lastx2, self.lasty2 = -1, -1
        self.offsetx, self.offsety = x, y
        self.tail, self.friction = [], 1
        self.color = {
            "line1": linecolor1,
            "line2": linecolor2,
            "bob1": bob1,
            "bob2": bob2
        },
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def calcpos(self, tick):
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
            x1 = 0
            y1 = 0
            x2 = 0
            y2 = 0
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        remove = 7
        for t in self.tail:
            if tick % 10 == 0:
                r, g, b = t[4]
                if r-remove > 0: r-=remove
                if g-remove > 0: g-=remove
                if b-remove > 0: b-=remove
                t[4] = (r, g, b)
                if tick % 20 == 0: t[5] = t[5]-1
                if t[5] <= 1: self.tail.remove(t); continue

    def draw(self, WIN, tick):
        pos = [self.x1, self.y1, self.x2, self.y2]
        if tick != 1: self.tail.append([pos[2], pos[3], self.lastx2, self.lasty2, self.tailcol, 10])

        self.lastx2 = pos[2]
        self.lasty2 = pos[3]
        circleWidth = 0
        # pygame.draw.circle(WIN, COLOR.gray, (self.offsetx, self.offsety), radius=self.radius1+self.radius2+self.mass2+5, width=1)
        pygame.draw.line(WIN, self.color[0]["line1"], start_pos=(self.offsetx, self.offsety), end_pos=(self.offsetx+pos[0], self.offsety+pos[1]))
        pygame.draw.line(WIN, self.color[0]["line2"], start_pos=(self.offsetx+pos[0], self.offsety+pos[1]), end_pos=(self.offsetx+pos[2], self.offsety+pos[3]))
        pygame.draw.circle(WIN, self.color[0]["bob2"], (self.offsetx+pos[0], self.offsety+pos[1]), radius=self.mass1, width=circleWidth)
        pygame.draw.circle(WIN, self.color[0]["bob2"], (self.offsetx+pos[2], self.offsety+pos[3]), radius=self.mass2, width=circleWidth)

    def drawtail(self, WIN):
        pos = [self.x1, self.y1, self.x2, self.y2]
        # pygame.draw.line(WIN, t[4], start_pos=(self.offsetx+t[0], self.offsety+t[1]), end_pos=(self.offsetx+t[2], self.offsety+t[3]), width=t[5])
        for t in self.tail:
            pygame.draw.circle(WIN, t[4], (self.offsetx+t[0], self.offsety+t[1]), radius=t[5])
        if len(self.tail) >= 1: pygame.draw.circle(WIN, self.tail[-1][4], (self.offsetx+pos[2], self.offsety+pos[3]), radius=self.tail[-1][5]-5)

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
        pygame.draw.line(WIN, COLOR.gray, start_pos=(self.xpos, self.ypos), end_pos=(self.xpos+self.xsize, self.ypos), width=self.ysize)
        pygame.draw.line(WIN, COLOR.white, start_pos=(self.xpos, self.ypos), end_pos=(self.xpos+self.current, self.ypos), width=self.ysize)
    
    def drawtext(self, WIN, FONT, COLOR, text):
        WIN.blit(FONT.render(f'{self.text}: {text}', False, COLOR.white), (self.xpos+self.xsize+10, self.ypos))
