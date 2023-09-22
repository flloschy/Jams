from PIL import Image, ImageDraw
import json, math
import numpy as np
import time

def makeGif(folder, frames):
    startT = time.time()
    connections = json.load(open("./results/" + folder + "/history.json"))
    mp4 = input("mp4? (y/n): ").lower() == "y"
    stats = json.load(open("./results/" + folder + "/stats.json"))
    Size = stats["size"]
    Dots = stats["dots"]
    Color = stats["color"]

    currentImageArray = np.zeros((Size, Size), np.uint8)

    nails = [(
            int(Size // 2 + (Size // 2 - 10) * math.cos(2 * math.pi * i /Dots)),
            int(Size // 2 + (Size // 2 - 10) * math.sin(2 * math.pi * i /Dots))
        ) for i in range(Dots)]

    def bresenham(x0, y0, x1, y1):
        img = np.zeros((Size, Size), dtype=bool)
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0

        for x in range(dx + 1):
            img[(y0 + x*xy + y*yy)][(x0 + x*xx + y*yx)] = True
            D += 2*dy
            if D >= 0:
                y += 1
                D -= 2*dx
        return (Color*img).astype(np.uint8)

    def drawLine(start, end):
        return np.maximum.reduce([currentImageArray, (currentImageArray + bresenham(*nails[start], *nails[end]))]).clip(0, 255)

    frames = max(1, min(frames, len(connections)))

    import imageio.v3 as iio

    imgs = []

    print(f"0 / {frames} (0%)", end="\r")
    count = 0

    for frame, [start, end] in enumerate(connections):
        currentImageArray = drawLine(start, end)
        if frame % (len(connections) // frames) == 0 or frame == len(connections) - 1:
            count += 1
            print(f"{count} / {frames} ({round(count / frames * 100, 2)}%)    ", end="\r")
            imgs.append(Image.fromarray(currentImageArray).convert("RGB"))

    print(f"{frames} / {frames} (100%)    ")
    print("Saving...")
    if mp4: iio.imwrite(f"./results/{folder}/result.mp4", imgs)
    else: iio.imwrite(f"./results/{folder}/result.gif", imgs, duration=1, loop=0)
    print("Done in " + str(round(time.time() - startT, 2)) + "s")

if __name__ == "__main__":
    makeGif(input("Folder: "), int(input("Frames: ")))