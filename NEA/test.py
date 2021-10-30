from math import pi as pi
from math import e as e
import os
import face_recognition
import cv2
'''x = y = 0
total = 0

for i in range (x-7, x+8):
    for z in range (y-7, y+8):
        offsetx = abs(0 - i)
        offsety = abs(0-z)
        weight = ((1 / (98 * pi)) * e ** (-(offsetx ** 2 + offsety ** 2) / 98)) / 0.513276455725204
        total += weight

print(total)'''
'''face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

main_image = face_recognition.load_image_file('./main/main.jpg')

# Find faces in test image
face_locations = face_recognition.face_locations(main_image)
gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
face_loc = []
for (x, y, w, h) in faces:
    face_loc.append((x, y, x+w, y+h))
    cv2.rectangle(main_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
print(face_loc)
print(face_location'''

array = [1, 2, 3]
print(len(array))
