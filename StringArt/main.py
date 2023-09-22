import numpy as np, PIL.Image as Image, os, math, random, time, json, cv2
from tabulate import tabulate

# Settings
Size = 500  # The size of the image 
Dots = 2000  # The amount of nails
Color = 1  # The color of the lines
continuousLine = False  # If the lines should be continuous
livePreview = True  # If the program should show a live preview
skipIfBadLine = True  # If the program should skip a random amount of nails if the line is worse than the last line
saveIt = True  # If the program should save the result
structured = False  # If True, go in a circle, if False, go in order | False: 0->1, 1->2, 2->5 ... | True: 0->1, 0->2, 0->5, ...
# End of settings

ImagePath = f"./img/{input('Image: ')}"
ImagePath += ".jpg" if os.path.exists(ImagePath + ".jpg") else ".png"
originalImage = (
    Image.open(ImagePath)
    .resize((Size, Size))
    .convert("L"))

originalImageArray = np.array(originalImage)
currentImageArray = np.zeros((Size, Size), np.uint8)

if livePreview:
    import pygame
    originalImage = pygame.image.frombytes(
        Image.open(ImagePath).resize((Size, Size)).convert("RGB").tobytes(),
        (Size, Size),
        "RGB")
    WIN = pygame.display.set_mode((Size * 2, Size)) 
    pygame.display.set_caption(f"String Art - {ImagePath}") 
    WIN.blit(originalImage, (0, 0))
    pygame.display.update()

skipIfBadLine = skipIfBadLine and not structured
run = True
nails = [
    (
        int(Size / 2 + (Size / 2 - 10) * math.cos(2 * math.pi * i / Dots)),
        int(Size / 2 + (Size / 2 - 10) * math.sin(2 * math.pi * i / Dots)),
    ) for i in range(Dots)]

def bresenham(x0, y0, x1, y1):
    img = np.zeros((Size, Size), dtype=bool)
    dx = x1 - x0
    dy = y1 - y0
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx, dy = abs(dx), abs(dy)
    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0
    D, y = 2 * dy - dx, 0
    for x in range(dx + 1):
        img[y0 + x * xy + y * yy][x0 + x * xx + y * yx] = True
        D += 2 * dy
        if D >= 0:
            y += 1
            D -= 2 * dx
    return (Color * img).astype(np.uint8)

def drawLine(start, end):
    return np.maximum.reduce([currentImageArray, (currentImageArray + bresenham(*nails[start], *nails[end]))]).clip(0, 255)


def difference(start, end):
    return cv2.norm(
        drawLine(start, end),
        originalImageArray,
        cv2.NORM_L2
    )

def findBest(origin):
    best = None
    i = 0
    while i < Dots:
        if i != origin:
            diff = difference(origin, i)
            if best == None or diff < best[2]:
                best = (origin,i,diff,)
            elif skipIfBadLine: i += int((Dots * 0.05) * random.random())
        i += 1
    return best

def update():
    if not livePreview: return
    current = pygame.image.frombytes(Image.fromarray(currentImageArray).convert("RGB").tobytes(), (Size, Size), "RGB")
    WIN.blit(current, (Size, 0))
    pygame.draw.line(WIN, (255, 255, 255), (Size, 0), (Size, Size))
    pygame.display.update((Size, 0, Size * 2, Size))

def events():
    if not livePreview: return
    global run
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False

def main():
    global currentImageArray, run
    startNail = 0
    currentNail = (random.randint(0, Dots - 1) if continuousLine else startNail)
    history = [(currentNail, currentNail)]
    startTime = time.time()
    diff = 0
    lastDiff = math.inf
    disconnects = 0
    fullLoop = False

    def stats():
        os.system("cls")
        print(
            tabulate(
                headers=["statistic", "value"],
                tabular_data=[
                    ["Time elapsed",time.strftime("%H:%M:%S", time.gmtime(time.time() - startTime)),],
                    ["Connections made", len(history)],
                    ["", ""],
                    ["Time per Line", f"{(time.time() - startTime) / len(history):.4f}s",],
                    ["Similarity Score", f"{diff:.4f}"],
                    ["Improvement", f"{(diff - lastDiff):.4f}"],
                    ["Current Start", startNail if not continuousLine else "N/A"],
                    ["Disconnects", disconnects if not continuousLine else "N/A"],
                    ["Continuous Line",continuousLine if not continuousLine else "N/A",],
                    ["", ""],
                    ["image", ImagePath],
                    ["dots", Dots],
                    ["size", Size],
                    ["color", Color],
                ],
                tablefmt="rounded_outline",
            )
        )

    def save():
        savePath = f"./results/{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}/"
        os.makedirs(savePath) 
        Image.fromarray(currentImageArray).convert("RGB").save(savePath + "result.png")
        with open(savePath + "history.json", "w") as f:
            json.dump(history, f)
        with open(savePath + "stats.json", "w") as f:
            json.dump(
                {
                    "Time elapsed": time.strftime(
                        "%H:%M:%S", time.gmtime(time.time() - startTime)
                    ),
                    "Connections made": len(history),
                    "Time per Line": f"{(time.time() - startTime) / len(history):.4f}s",
                    "Similarity Score": f"{diff:.4f}",
                    "Improvement": f"{(diff - lastDiff):.4f}",
                    "Current Start": startNail,
                    "Disconnects": disconnects,
                    "continuousLine": continuousLine,
                    "image": ImagePath,
                    "dots": Dots,
                    "size": Size,
                    "color": Color,
                },
                f,
                indent=4,
            )

    update()
    stats()
    events()

    while run:
        currentNail, endNail, diff = findBest(currentNail)
        if (diff - lastDiff) < 0:
            currentImageArray = drawLine(currentNail, endNail)
            history.append((currentNail, endNail))
            currentNail = endNail

        elif (diff - lastDiff) >= 0 or structured:
            if not continuousLine:
                disconnects += 1
                startNail += 1
                if (startNail >= Dots):
                    startNail = 0
                    if fullLoop: run = False
                    else: fullLoop = True
                currentNail = startNail
            else: run = False
        
        elif continuousLine: fullLoop = False
        if len(history) % 100 == 0 or len(history) < 100:
            update()
            stats()
            events()
        
        lastDiff = diff

    update()
    stats()
    if saveIt:
        save()
main()