import pygame

class test_plant():
    def __init__(self, x, y):
        self.x, self.y = x, y
        
        self.gives_hunger = 1
        self.gives_thirst = 2

        self.live_spand = 500
        self.live_time = 0

        self.growes = 20
        self.grow = 0

        self.size = 10 #px
        self.t = 0

        self.color = (94, 230, 60)

    def tick(self):
        if self.grow == self.growes:
            self.live_time += 1
            if self.size == 0: return True
            if self.live_spand < self.live_time:
                self.t += 1
                if self.t % 2 == 0:
                    self.size -= 1
        else:
            self.grow += 1

    def draw(self, WIN):
        if self.grow == self.growes:
            pygame.draw.rect(WIN, self.color, (self.x-self.size/2, self.y-self.size/2, self.size, self.size))
        elif self.grow == self.growes-1:
            self.size += 2
            pygame.draw.rect(WIN, (255, 255, 255), (self.x-self.size/2, self.y-self.size/2, self.size, self.size))
            self.size -= 2
        else:
            pygame.draw.rect(WIN, (self.grow*(self.color[0]/self.growes), self.grow*(self.color[1]/self.growes), self.grow*(self.color[2]/self.growes)), (self.x-self.size/2, self.y-self.size/2, self.size, self.size))










import inspect, sys
def get_classes():
    return inspect.getmembers(sys.modules[__name__], inspect.isclass)