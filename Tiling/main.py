import pygame, time, os, random, numpy as np

tileSize = pygame.image.load("./tiles/_.png").get_size()[0]
tiles = 40
size = tiles * tileSize

WIN = pygame.display.set_mode((size, size))
input()
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

placements = [[None for _ in range(tiles)] for _ in range(tiles)]
placements[0][0] = random.choice(imgs)

WIN.blit(placements[0][0]['img'], (0, 0))
u()

def placeTile(x, y):
    if placements[y][x] != None: return


    top = None
    left = None
    right = None
    bottom = None

    if (y-1 in range(0, tiles)):
        if (placements[y-1][x] != None):
            top = placements[y-1][x]['connect']['B']
    if (x-1 in range(0, tiles)):
        if (placements[y][x-1] != None):
            left = placements[y][x-1]['connect']['R']
    if (x+1 in range(0, tiles)):
        if (placements[y][x+1] != None):
            right = placements[y][x+1]['connect']['L']
    if (y+1 in range(0, tiles)):
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
    WIN.blit(available['img'], (x*tileSize, y*tileSize))
    u()
    # time.sleep(0.001)

def getFreePos():
    lst = []
    for x in range(tiles):
        for y in range(tiles):
            if placements[y][x] == None: lst.append([x, y])
    return lst

done = []
queue = [(0, 0)]
while getFreePos():
    while len(queue) != 0:
        [x, y] = queue.pop()
        if x not in range(tiles) or y not in range(tiles): continue
        if (x, y) in done: continue
        placeTile(x, y)
        n = placements[y][x]
        if (n['connect']['T']): queue.append((x, y-1))
        if (n['connect']['B']): queue.append((x, y+1))
        if (n['connect']['L']): queue.append((x-1, y))
        if (n['connect']['R']): queue.append((x+1, y))
        done.append((x, y))

        queue.sort(key=lambda x: random.random()-0.5)
    queue.clear()

    if (getFreePos()):
        [x, y] = random.choice(getFreePos())
        queue.append((x, y))


# if (getFreePos()):
#     while not np.all(placements):
#         [x, y] = random.choice(getFreePos())
#         placeTile(x, y)

input("Enter to close")
pygame.image.save( WIN, './results/' + str(random.randint(0, 10000)) + ".png" )



