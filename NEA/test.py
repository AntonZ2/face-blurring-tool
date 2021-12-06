"""x = y = 0
total = 0

for i in range(x-10, x+11):
    for z in range(y-10, y+11):
        offsetx = abs(0 - i)
        offsety = abs(0-z)
        weight = ((1 / (98 * pi)) * e ** (-(offsetx ** 2 + offsety ** 2) / 98))
        total += weight

print(total)"""
'''from PIL import Image
import matlab.engine
import tensorflow

eng = matlab.engine.start_matlab()
filename = str('faceavoid.jpg')
size = float(8)
eng.gaussianblur(filename, size, nargout=0)

eng.quit()'''
from PIL import Image
import matlab.engine
import os
import face_recognition

'''eng = matlab.engine.start_matlab()
image = face_recognition.load_image_file("faceavoid.jpg")
pil_image = Image.fromarray(image)
face = pil_image.crop((90, 90, 210, 210))
face.save('./temp/before.jpg')
name = '/Users/antonzhulkovskiy/Desktop/NEA/temp/before.jpg'
eng.gaussianblur(name, 10.00, nargout=0)
# Calls the blur function
blurredface = Image.open('./temp/face.jpg')
blurredfacefinal = blurredface.crop((10,10,110,110))
# Pastes the blurred face back onto the image
pil_image.paste(blurredfacefinal, (100, 100))
os.remove("./temp/face.jpg")
os.remove('./temp/before.jpg')
pil_image.show()
eng.quit()'''
face = Image.open('faceavoid.jpg')
face.save("./temp/before.jpg")
name = os.path.realpath("./temp/before.jpg")
print(name)
