import face_recognition
from PIL import Image
import os
from blurring_algorithm import Blur
import cv2

def facelocatePhoto():
  known_face_encodings = []
  for file in os.listdir('ignore'):
    if not file.startswith('.'):
      known_face = face_recognition.load_image_file(f'./ignore/{file}')
      try:
        known_face_encoding = face_recognition.face_encodings(known_face)[0]
        known_face_encodings.append(known_face_encoding)
      except:
        pass

  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  # Load test image to find faces in
  main_image = face_recognition.load_image_file('./main/main.jpg')

  # Find faces in test image
  face_locations = face_recognition.face_locations(main_image)
  #gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
  #faces = face_cascade.detectMultiScale(gray, 1.1, 4)
  #face_loc = []
  #for (x, y, w, h) in faces:
  #  face_loc.append((x, y, x + w, y + h))
  face_encodings = face_recognition.face_encodings(main_image, face_locations)

  # Convert to PIL format
  pil_image = Image.fromarray(main_image)

  # Loop through faces in test image
  for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    print('yes')
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
    for i in matches:
      if not i:
        print('no')
        # Draw box
        #draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))
        faceblur = Blur(x=left, y=top, x2=right, y2=bottom)
        blurredface = faceblur.photoblur()
        pil_image.paste(blurredface, (left, top))

  '''folders = ['main', 'ignore']
  for i in folders:
    completefiles = glob.glob(f'./{i}')
    for f in completefiles:
        os.remove(f)'''
  #delete files after program is done
  for f in os.listdir('ignore'):
    if not f.startswith('.'):
      os.remove(f'./ignore/{f}')
  os.remove('./main/main.jpg')



  # Display image
  pil_image.show()

facelocatePhoto()
