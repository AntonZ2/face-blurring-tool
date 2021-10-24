import face_recognition
from PIL import Image, ImageDraw
import os
from blurring_algorithm import Blur
import glob

def facelocatePhoto():
  known_face_encodings = []
  for file in os.listdir('ignore'):
    known_face = face_recognition.load_image_file(f'./ignore/{file}')
    try:
      known_face_encoding = face_recognition.face_encodings(known_face)[0]
      known_face_encodings.append(known_face_encoding)
    except:
      continue 


  # Load test image to find faces in
  main_image = face_recognition.load_image_file('./main/main.jpg')

  # Find faces in test image
  face_locations = face_recognition.face_locations(main_image)
  face_encodings = face_recognition.face_encodings(main_image, face_locations)

  # Convert to PIL format
  pil_image = Image.fromarray(main_image)

  # Create a ImageDraw instance
  # draw = ImageDraw.Draw(pil_image)

  # Loop through faces in test image
  for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
    dontblur = False
    for i in matches:
    # If match
      if i == True:
        dontblur = True
    if dontblur == False:
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

  # Display image
  pil_image.show()

