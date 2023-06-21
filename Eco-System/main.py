import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
print()
import pygame
import time
from json import load
from modules import *
generator = GENERATOR()
static = STATISTICS()

settings = load(open("./settings.json"))["main"]

WIN = pygame.display.set_mode((settings["width"], settings["height"]))
generator.make_noise(WIN, draw_loading=True)
plant_manager = PLANT_MANAGER(generator.img)


fps_start = time.time()
tps_start = time.time()
while True:
    start = time.time()
    if (start - fps_start) >= (1/settings["fps"]):
        generator.draw_map(WIN)
        plant_manager.draw(WIN)
        static.draw(WIN, len(plant_manager.plants), int(1/(start - fps_start)), int(1/(start-tps_start)))

        pygame.display.update()
        fps_start = time.time()

    if (start - tps_start) >= (1/settings["tps"]):

        plant_manager.tick()
        plant_manager.grow(
            random.randint(5, settings["width"]-5),
            random.randint(5, settings["height"]-5)
        )

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(0)
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_r:
                    generator.make_noise(WIN, draw_loading=True)
                    plant_manager.img = generator.img
                    plant_manager.reset()

        tps_start = time.time()

    time.sleep(0.01)