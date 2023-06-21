from PIL import Image
from perlin_noise import PerlinNoise
from json import load
import random
import pygame
from entitys import plants
from termcolor import colored
import random

pygame.font.init()

class STATISTICS:
    def __init__(self):
        self.font = pygame.font.SysFont("./bin/font.ttf", 30)
    
    def draw(self, WIN, plants:int, fps:int, tps:int):
        txt = [f"Plants: {plants}", f"FPS: {fps}", f"TPS: {tps}"]
        y = 20
        for t in txt:
            dark_render = self.font.render(t, False, (0, 0, 0))
            light_render = self.font.render(t, False, (255, 255, 255))
            WIN.blit(dark_render, (20+2, y+2))
            WIN.blit(dark_render, (20-2, y+2))
            WIN.blit(dark_render, (20+2, y-2))
            WIN.blit(dark_render, (20-2, y-2))
            WIN.blit(light_render, (20, y))
            y+= 20



class GENERATOR:
    def __init__(self):
        self.surface = None
        self.img = None
        self.font = pygame.font.SysFont("./bin/font.ttf", 30)

    def make_noise(self, WIN, overwrite_seed=False, overwrite_octaves=False, overwrite_water_threshold=False, draw_loading=False):

        settings = load(open("./settings.json"))["generator"] # load settings

        width, height = settings["width"], settings["height"]
        blocksize = settings["blocksize"]

        map_img = Image.new("RGB", (width, height)) # create Image

        seed = abs(random.randint(0, 10**10) if settings["randomseed"] else settings["seed"]) # generate seed
        noise = PerlinNoise(
            octaves=settings["octaves"] if not overwrite_octaves else overwrite_octaves,
            seed=seed if not overwrite_seed else overwrite_seed
        ) # generate noise

        water_threshold = settings["waterthreshold"] if not overwrite_water_threshold else overwrite_water_threshold # load water_threshold

        def spinning_cursor(multiply=230):
            while True:
                for cursor in '|'*multiply + '/'*multiply + '-'*multiply +'\\'*multiply:
                    yield cursor

        # draw Image
        spinner = spinning_cursor()
        i = 0
        for x in range(0, width, blocksize):

            if draw_loading: 
                # WIN.fill((0, 0, 0))
                percent = i / ( len(range(0, width, blocksize))*len(range(0, height, blocksize)) )

                render = self.font.render(f"Creating Map ({round(percent*100, 2)}%)", False, (255, 0, 0))

                rect1 = pygame.Rect(0, 0, WIN.get_width()*percent, 30)
                rect2 = pygame.Rect(0, 0, WIN.get_width(), 30)

                pygame.draw.rect(WIN, (0, 0, 0), rect2)
                pygame.draw.rect(WIN, (255, 255, 255), rect1)
                WIN.blit(render, (WIN.get_width()/2-render.get_width()/2, render.get_height()/2-5))
                pygame.display.update()

            for y in range(0, height, blocksize):
                i += 1
                # if y%4 == 0: loading_bar(i)
                if i%4==0: print(f"\033[F [{colored(next(spinner), color='yellow')}] Generating Map ({colored(round( (   i / ( len(range(0, width, blocksize))*len(range(0, height, blocksize)) )   )*100), color='cyan')}%)")
                point = noise([x/width, y/height]) # get noise value
                for ox in range(0, blocksize):
                    for oy in range(0, blocksize):
                        if point <= water_threshold:
                            map_img.putpixel((x+ox, y+oy), (0, 0, 255-int(255*abs(point-water_threshold))))  #draw relative water color
                        else:
                            map_img.putpixel((x+ox, y+oy), (0, 255-int(255*abs(point-water_threshold)), 0))  #draw relative grass color


        print(f"\033[F [{colored('✓', color='green')}] Generating Map {' '*10}")
        print(f" [{colored('⨉', color='red')}] Saving Map")

        map_img.save("./bin/current_map.png") # save image
        self.surface = pygame.image.load("./bin/current_map.png") # load pygame surface
        self.img = map_img.copy() # store PIL image

        print(f"\033[F [{colored('✓', color='green')}] Saving Map")
        print("\n")

    def draw_map(self, WIN, position=(0, 0)):
        if self.surface == None: return
        WIN.blit(self.surface, position) # draw generated Map


class PLANT_MANAGER:
    def __init__(self, img):
        self.plants = []
        self.cords = []
        self.index = 0
        self.classes = plants.get_classes()
        self.img = img
        self.settings = load(open("./settings.json"))["plantmanager"]

    def tick(self, random_ticks=100):
        l = len(self.plants)
        if l < 5: return
        if l < random_ticks: random_ticks = l

        for _ in range(0, random_ticks):
            plant = random.choice(self.plants)
            if plant.tick():
                self.cords.remove((plant.x, plant.y))
                self.plants.remove(plant)
                self.index -= 1

    def draw(self, WIN):
        for plant in self.plants:
            plant.draw(WIN)

    def add_plant(self, x, y):
        plant = random.choice(self.classes)[0]
        x = 10 * round(x/10)
        y = 10 * round(y/10)
        exec(f"self.plants.append(plants.{plant}({x}, {y}))")
        self.cords.append((x, y))
        self.index += 1

    def reset(self):
        self.plants.clear()
        self.cords.clear()
        self.index = 0

    def can_grow(self, x, y):
        r, g, b = self.img.getpixel((x, y)) # get RGB color value of point
        if (x, y) in self.cords: return False
        if g == 0: return False
        if r != 0 or b != 0: return False

        def f(x): return x**2

        percent = 255-g

        return random.random() < f(percent)/10000    # exponential
        # return random.random() < percent    #  liniar

    def grow(self, x, y):
        if self.index >= self.settings["max"]: return
        if self.can_grow(x, y):
            self.add_plant(x, y)