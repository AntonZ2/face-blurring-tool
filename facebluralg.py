import face_recognition
from PIL import Image
import os
import cv2
import matlab.engine
import shutil
from tkinter.filedialog import asksaveasfilename


class FaceBlurAlgorithm:
    def __init__(self):
        self.eng = matlab.engine.start_matlab()

    # method to detect all the faces in the main image
    def facelocatephoto(self, intense):
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
        self.blurfaces(pil_image, face_locations, face_encodings, ignore_face_encodings, int(intense))

        # saves completed image in temporary file
        pil_image.save("./temp/finished.jpg")


    def facelocatevideo(self, intense):
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
        video = cv2.VideoCapture("./main/main.mp4")

        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        frame_size = (frame_width, frame_height)
        fps = int(video.get(5))
        output = cv2.VideoWriter('./temp/finished.mp4',
                                 cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps,
                                 frame_size)

        while video.isOpened():
            out, image = video.read()

            if not out:
                break
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Find the coordinates of each face in the main image
            face_locations = face_recognition.face_locations(image)
            # creates encodings for the faces to later be compared with the encodings for faces to be ignored
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Convert to PIL format to allow image formatting and comparison of encodings
            pil_image = Image.fromarray(image)

            # Runs the function to blur the faces
            self.blurfaces(pil_image, face_locations, face_encodings, ignore_face_encodings, int(intense))

            pil_image.save("./temp/video.jpg")

            frame = cv2.imread("./temp/video.jpg")

            output.write(frame)

            os.remove("./temp/video.jpg")

        video.release()
        output.release()

    # method to blur faces
    def blurfaces(self, pil_image, face_locations, face_encodings, ignore_face_encodings, intense):
        # Loop through faces in main image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the faces detected in main image with the faces in list of faces to ignore
            matches = face_recognition.compare_faces(ignore_face_encodings, face_encoding, tolerance=0.6)
            # if current face does not match faces in faces to ignore list blurring is applied
            if True not in matches:
                # Checks to ensure face blurring algorithm does not go outside image
                width, height = pil_image.size
                if top < intense:
                    top = intense
                elif bottom > height - intense:
                    bottom = height - intense
                if left < intense:
                    left = intense
                elif right > width - intense:
                    right = width - intense
                face = pil_image.crop((left - intense, top - intense, right + intense, bottom + intense))
                face.save("./temp/before.jpg")
                name = os.path.realpath("./temp/before.jpg")
                self.eng.gaussianblur(name, float(intense), nargout=0)
                # Calls the blur function
                blurredface = Image.open("./temp/face.jpg")
                blurredfacefinal = blurredface.crop((intense, intense, (right - left + intense),
                                                     (bottom - top + intense)))
                # Pastes the blurred face back onto the image
                pil_image.paste(blurredfacefinal, (left, top))
                os.remove("./temp/face.jpg")
                os.remove("./temp/before.jpg")

    # method to delete files after program has been executed
    def deletefiles(self):
        # For loop through all images to be ignored
        for f in os.listdir("ignore"):
            # Ignores all system files
            if not f.startswith("."):
                # deletes the image file
                os.remove(f"./ignore/{f}")
        # Delete the main image file
        try:
            os.remove("./main/main.jpg")
            os.remove("./temp/finished.jpg")
        except FileNotFoundError:
            try:
                os.remove("./main/main.mp4")
                os.remove("./temp/finished.mp4")
            except FileNotFoundError:
                pass

    # meth to save final blurred file
    def savefile(self, filetype):
        # file type validation, if main file is image these lines of code will execute
        if filetype == 'photo':
            location = asksaveasfilename(defaultextension=".jpg")
            shutil.copy('./temp/finished.jpg', location)
        # file type validation, if main file is a video these lines of code will execute
        else:
            location = asksaveasfilename(defaultextension=".mp4")
            shutil.copy('./temp/finished.mp4', location)
