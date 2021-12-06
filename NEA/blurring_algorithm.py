from PIL import Image
from math import pi as pi
from math import e as e
# import cv2


class Blur:
    def __init__(self, filename="./main/main.jpg", x=0, y=0, x2=0, y2=0, intensity=''):

        self.startx, self.starty = x, y
        self.endx, self.endy = x2, y2
        self.filename = filename
        self.intensity = intensity
        self.div = 0
        self.divcalc()

    def divcalc(self):
        if self.intensity == 5:
            self.div = 0.3230298770315299
        elif self.intensity == 6:
            self.div = 0.41899554928302796
        elif self.intensity == 7:
            self.div = 0.513276455725204
        elif self.intensity == 8:
            self.div = 0.6017971838187421
        elif self.intensity == 9:
            self.div = 0.6816666193147171
        else:
            self.div = 0.7511968790077685

    def gaussianblur(self, image, x, y):

        rtotal = 0
        gtotal = 0
        btotal = 0
        for blurx in range(x-self.intensity, x+self.intensity+1):
            for blury in range(y-self.intensity, y+self.intensity+1):
                offsetx = abs((blurx - x))
                offsety = abs((blury - y))
                weight = ((1 / (98 * pi)) * e ** (-(offsetx ** 2 + offsety ** 2) / 98)) / self.div
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
        '''blurredface2 = cv2.cvtColor(blurredface, cv2.COLOR_RGB2BGR)
        dst = cv2.GaussianBlur(blurredface2, (10, 10), cv2.BORDER_DEFAULT)
        dst2 = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)'''
        return blurredface
