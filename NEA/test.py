from math import pi as pi
from math import e as e

x = y = 0
total = 0

for i in range (x-7, x+8):
    for z in range (y-7, y+8):
        offsetx = abs(0 - i)
        offsety = abs(0-z)
        weight = ((1 / (98 * pi)) * e ** (-(offsetx ** 2 + offsety ** 2) / 98)) / 0.513276455725204
        total += weight

print(total)
