from PIL import Image
from math import pi as pi
from math import e as e


class Blur:
    def __init__(self, filename="./main/main.jpg", x=0, y=0, x2=0, y2=0):
        self.startx, self.starty = x, y
        self.endx, self.endy = x2, y2
        self.filename = filename

    def gaussianblur(self, image, x, y):
        rtotal = 0
        gtotal = 0
        btotal = 0
        for blurx in range(x-7, x+8):
            for blury in range(y-7, y+8):
                offsetx = abs((blurx - x))
                offsety = abs((blury - y))
                weight = ((1 / (98 * pi)) * e ** (-(offsetx ** 2 + offsety ** 2) / 98)) * 2
                if blurx >= 0 and blury >= 0:
                    r, g, b = (image.getpixel((blurx, blury)))
                else:
                    r, g, b = (image.getpixel((x, y)))
                rtotal += (weight * r) 
                gtotal += (weight * g) 
                btotal += (weight * b) 
        rnew = round(rtotal)
        gnew = round(gtotal)
        bnew = round(btotal)
        """for blurx in range(x-3, x+4):
            for blury in range(y-3, y+4):
                offsetx = abs(blurx - x)
                offsety = abs(blury - y)
                if blurx >= 0 and blury >= 0:
                    r, g, b = (image.getpixel((blurx, blury)))
                else:
                    r, g, b = (image.getpixel((x, y)))
                rtotal += r
                gtotal += g
                btotal += b
        rnew = round(rtotal/49)
        gnew = round(gtotal/49)
        bnew = round(btotal/49)"""

        return rnew, gnew, bnew

    def photoblur(self):
        file = Image.open(self.filename)
        blurredimage = Image.open(self.filename)
        for x in range(self.startx, self.endx):
            for y in range(self.starty, self.endy):
                r2, g2, b2 = self.gaussianblur(file, x, y)
                blurredimage.putpixel((x, y), (r2, g2, b2))
                # blurredimage.putpixel((x, y), (0, 0, 0))
        blurredface = blurredimage.crop((self.startx, self.starty, self.endx, self.endy))
        return blurredface
