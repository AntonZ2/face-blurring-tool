from PIL import Image
from math import pi as pi
from math import e as e
import Cython
import time


class Blur:
    def __init__(self, filename = 'test_image.jpg', x=200, y=300, x2=400, y2=500):
        self.startx, self.starty = x, y
        self.endx, self.endy = x2, y2
        self.filename = filename

    def gaussianblur(self, image, x, y):
        rtotal = gtotal = btotal = 0
        for blurx in range(x-7, x+8):
            for blury in range(y-7, y+8):
                offsetx = blurx - x
                offsety = blury - y
                weight = (1 / (98 * pi)) * e ** (-(offsetx ** 2 + offsety ** 2) / 98) * 2
                r, g, b = (image.getpixel((blurx, blury)))
                rtotal = rtotal + (weight * r)
                gtotal = gtotal + (weight * g)
                btotal = btotal + (weight * b)
        rnew = round(rtotal)
        gnew = round(gtotal)
        bnew = round(btotal)
        return rnew, gnew, bnew

    def photoblur(self):
        file = Image.open(self.filename)
        blurredimage = Image.open('test_image.jpg')
        for x in range(self.startx, self.endx):
            for y in range(self.starty, self.endy):
                r, g, b = file.getpixel((x, y))
                r2, g2, b2 = self.gaussianblur(file, x, y)
                blurredimage.putpixel((x, y), (r2, g2, b2))
        blurredimage.show()

start_time = time.time()
run = Blur()
run.photoblur()
print("%s seconds" % (time.time() - start_time))