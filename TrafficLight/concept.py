import math
import pygame, time, random

pygame.font.init()
pygame.display.set_caption("Traffic Light Simulator")
FONT = pygame.font.SysFont("arial", 30)
WIN = pygame.display.set_mode((500, 500))


class State:
    red = 0
    yellow = 1
    green = 2
    yellow2 = 3

class Light:
    def __init__(self, x1, y1, x2, y2, width1, width2, height1, height2, init_state):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.rect1 = pygame.Rect(x1, y1, width1, height1)
        self.rect2 = pygame.Rect(x2, y2, width2, height2)
        self.state = init_state
        self.tick = 0
        self.incoming1 = 1
        self.incoming2 = 1
        self.waiting1 = 0
        self.waiting2 = 0

    def update(self):
        self.waiting1 += random.random() * self.incoming1
        self.waiting2 += random.random() * self.incoming2

        if self.state == State.green:
            self.waiting1 = max(self.waiting1 - 1 - random.random() * 8, 0)
            self.waiting2 = max(self.waiting2 - 1 - random.random() * 8, 0)


    def render(self):
        color = (
            255 * (self.state == State.red or self.state == State.yellow or self.state == State.yellow2),
            255 * (self.state == State.green or self.state == State.yellow or self.state == State.yellow2),
            0
        )
        pygame.draw.rect(WIN, color, self.rect1)
        pygame.draw.rect(WIN, color, self.rect2)


    def light(self):
        self.tick -= 1
        if self.tick <= 0 or (self.state == State.green and self.waiting1 < 2 and self.waiting2 < 2): 
            if self.state == State.red:
                self.state = State.yellow
                self.tick = 1
            elif self.state == State.yellow:
                self.state = State.green
                self.tick = int((math.log10((self.waiting1 + self.waiting2) / 1.25 + 1) / 2) * 30)
            elif self.state == State.green:
                self.state = State.yellow2
                self.tick = 2
            elif self.state == State.yellow2:
                self.state = State.red
                return True
        return False
 
roadWidth = 100
lightWidth = 10

light1 = Light(
    500/2 - roadWidth/2 - lightWidth, 500/2 ,
    500/2 + roadWidth/2, 500/2 - roadWidth/2,
    lightWidth, lightWidth, roadWidth/2, roadWidth/2,
    State.red
)

light2 = Light(
    500/2 - roadWidth/2, 500/2  - roadWidth/2 - lightWidth,
    500/2, 500/2 + roadWidth/2,
    roadWidth/2, roadWidth/2, lightWidth, lightWidth,
    State.green
)

selected = None

toggle = False
start = time.time()
while True:
    WIN.fill((45, 150, 55))

    pygame.draw.rect(WIN, (0, 0, 0), (500/2 - roadWidth/2, 0, roadWidth, 500))
    pygame.draw.rect(WIN, (0, 0, 0), (0, 500/2 - roadWidth/2, 500, roadWidth))

    if selected == 1:
        pygame.draw.rect(WIN, (255, 255, 255), (0,500/2 - roadWidth/2, 10, roadWidth), border_radius=1)
        render = FONT.render(str(round(light1.incoming1, 2)), True, (255, 255, 255))
        WIN.blit(render, (0, 500/2 - roadWidth/2 - 30))
    elif selected == 3:
        pygame.draw.rect(WIN, (255, 255, 255), (500-10,500/2 - roadWidth/2, 10, roadWidth), border_radius=1)
        render = FONT.render(str(round(light1.incoming2, 2)), True, (255, 255, 255))
        WIN.blit(render, (500- render.get_width(), 500/2 + roadWidth/2))
    elif selected == 2:
        pygame.draw.rect(WIN, (255, 255, 255), (500/2 - roadWidth/2, 0, roadWidth, 10), border_radius=1)
        render = FONT.render(str(round(light2.incoming1, 2)), True, (255, 255, 255))
        WIN.blit(render, (500/2 + roadWidth/2, 0))
    elif selected == 4:
        pygame.draw.rect(WIN, (255, 255, 255), (500/2 - roadWidth/2, 500-10, roadWidth, 10), border_radius=1)
        render = FONT.render(str(round(light2.incoming2, 2)), True, (255, 255, 255))
        WIN.blit(render, (500/2 - roadWidth/2 - render.get_width(), 500-30))

    if time.time() - start > 0.25:
        light1.update()
        light2.update()
        start = time.time()
        if toggle:
            if light1.light(): toggle = False
        else:
            if light2.light(): toggle = True

    light1.render()
    light2.render()


    render = FONT.render(str(round(light1.waiting1)), True, (255, 255, 255))
    WIN.blit(render, (20, light1.y1 + light1.rect1.height/2 - render.get_height()/2))

    render = FONT.render(str(round(light1.waiting2)), True, (255, 255, 255))
    WIN.blit(render, (500 - render.get_width() - 20, light1.y2 + light1.rect2.height/2 - render.get_height()/2))

    render = FONT.render(str(round(light2.waiting1)), True, (255, 255, 255))
    render = pygame.transform.rotate(render, 90)
    WIN.blit(render, (light2.x1 + light2.rect1.width/2 - render.get_width()/2, 20))

    render = FONT.render(str(round(light2.waiting2)), True, (255, 255, 255))
    render = pygame.transform.rotate(render, 90)
    WIN.blit(render, (light2.x2 + light2.rect2.width/2 - render.get_width()/2, 500 - 20 - render.get_height()))


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if selected == None:
                    selected = 1
                else:
                    selected += 1
                    if selected == 5:
                        selected = None
            if event.key == pygame.K_UP:
                if selected == 1:
                    light1.incoming1 += 0.25
                elif selected == 3:
                    light1.incoming2 += 0.25
                elif selected == 2:
                    light2.incoming1 += 0.25
                elif selected == 4:
                    light2.incoming2 += 0.25
            if event.key == pygame.K_DOWN:
                if selected == 1:
                    light1.incoming1 = max(light1.incoming1 - 0.25, 0)
                elif selected == 3:
                    light1.incoming2 = max(light1.incoming2 - 0.25, 0)
                elif selected == 2:
                    light2.incoming1 = max(light2.incoming1 - 0.25, 0)
                elif selected == 4:
                    light2.incoming2 = max(light2.incoming2 - 0.25, 0)
