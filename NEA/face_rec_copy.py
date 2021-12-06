import face_recognition
from PIL import Image
import os
from blurring_algorithm import Blur
import cv2


# Function to detect all the faces in the main image
def facelocatephoto(intense):
    # List that will contain all faces that should NOT be blurred
    ignore_face_encodings = []
    # For loop to append all faces provided by user to be ignored into ignore face list
    for file in os.listdir("ignore"):
        # Only reads image files ignoring all system files
        if not file.startswith("."):
            known_face = face_recognition.load_image_file(f"./ignore/{file}")
            # attempts to detect face in each image appending it to list if face is found
            try:
                known_face_encoding = face_recognition.face_encodings(known_face)[0]
                ignore_face_encodings.append(known_face_encoding)
            # Except statement to go to next image if no face is detected
            except IndexError:
                pass

    # Load main image to find faces for blurring
    main_image = face_recognition.load_image_file("./main/main.jpg")

    # Find the coordinates of each face in the main image
    face_locations = face_recognition.face_locations(main_image)
    # creates encodings for the faces to later be compared with the encodings for faces to be ignored
    face_encodings = face_recognition.face_encodings(main_image, face_locations)
    
    # Convert to PIL format to allow image formatting and comparison of encodings
    pil_image = Image.fromarray(main_image)
    
    # Runs the function to blur the faces
    blurfaces(pil_image, face_locations, face_encodings, ignore_face_encodings, intense)

    # TESTING
    showimage(pil_image)
    
    # Delete main file and ignore files to prevent accidental use in future
    deletefiles()

def facelocatevideo():
    # List that will contain all faces that should NOT be blurred
    ignore_face_encodings = []
    # For loop to append all faces provided by user to be ignored into ignore face list
    for file in os.listdir("ignore"):
        # Only reads image files ignoring all system files
        if not file.startswith("."):
            known_face = face_recognition.load_image_file(f"./ignore/{file}")
            # attempts to detect face in each image appending it to list if face is found
            try:
                known_face_encoding = face_recognition.face_encodings(known_face)[0]
                ignore_face_encodings.append(known_face_encoding)
            # Except statement to go to next image if no face is detected
            except IndexError:
                pass
    video = cv2.VideoCapture('main.mp4')

    while True:
        out, image = video.read()




# Function to blur faces
def blurfaces(pil_image, face_locations, face_encodings, ignore_face_encodings, intense):

    # Loop through faces in main image
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the faces detected in main image with the faces in list of faces to ignore
        matches = face_recognition.compare_faces(ignore_face_encodings, face_encoding, tolerance=0.6)
        # if current face does not match faces in faces to ignore list blurring is applied
        if True not in matches:
            # Calls the blur function
            faceblur = Blur(x=left, y=top, x2=right, y2=bottom, intensity=intense)
            blurredface = faceblur.photoblur()
            # Pastes the blurred face back onto the image
            pil_image.paste(blurredface, (left, top))


# Function to delete files after program has been executed
def deletefiles():
    # For loop through all images to be ignored
    for f in os.listdir("ignore"):
        # Ignores all system files
        if not f.startswith("."):
            # deletes the image file
            os.remove(f"./ignore/{f}")
    # Delete the main image file
    os.remove("./main/main.jpg")


# TESTING
def showimage(image):
    image.show()
