import pygame, time, os, random, numpy as np

WIN = pygame.display.set_mode((800, 800))

imgs = [{
    'img': pygame.image.load("./tiles/" + file),
    'connect': {
        'T': "T" in file,
        'L': "L" in file,
        'R': "R" in file,
        'B': "B" in file
    }
} for file in os.listdir("./tiles")]
# print(imgs)

def u(): pygame.display.update()

placements = [[None for _ in range(50)] for _ in range(50)]
placements[0][0] = random.choice(imgs)

WIN.blit(placements[0][0]['img'], (0, 0))
u()

def placeTile(x, y):
    top = None
    left = None
    right = None
    bottom = None

    if (y-1 in range(0, 50)):
        if (placements[y-1][x] != None):
            top = placements[y-1][x]['connect']['B']
    if (x-1 in range(0, 50)):
        if (placements[y][x-1] != None):
            left = placements[y][x-1]['connect']['R']
    if (x+1 in range(0, 50)):
        if (placements[y][x+1] != None):
            right = placements[y][x+1]['connect']['L']
    if (y+1 in range(0, 50)):
        if (placements[y+1][x] != None):
            bottom = placements[y+1][x]['connect']['T']

    lst = [
        img for img in imgs
        if  ((img['connect']['T'] if top else (not img['connect']['T'])) if top != None else True) and
            ((img['connect']['L'] if left else (not img['connect']['L'])) if left != None else True) and
            ((img['connect']['R'] if right else (not img['connect']['R'])) if right != None else True) and
            ((img['connect']['B'] if bottom else (not img['connect']['B'])) if bottom != None else True)
    ]
    available = random.choice(lst)
    placements[y][x] = available
    WIN.blit(available['img'], (x*16, y*16))
    u()
    # time.sleep(0.3)

def getFreePos():
    lst = []
    for x in range(50):
        for y in range(50):
            if placements[y][x] == None: lst.append([x, y])
    return lst

while not np.all(placements):
    [x, y] = random.choice(getFreePos())
    placeTile(x, y)

pygame.image.save( WIN, './results/' + str(random.randint(0, 10000)) + ".png" )




