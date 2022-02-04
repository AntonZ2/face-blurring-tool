import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox, IntVar, ttk
import os
import shutil
# import cv2
# from tkVideoPlayer import TkinterVideo
# import datetime
from SQL_faces import insert_images, retrieve_images, cleartable
from face_rec import facelocatephoto, facelocatevideo, deletefiles, savefile

# Fonts
TITLE_FONT = ("Fixedsys", 100, "bold")
TITLE_FONT_2 = ("Fixedsys", 80, "bold")
SUBTITLE_FONT = ("Fixedsys", 24, "bold")
BODY_FONT = ("Verdana", 14)


# master class to control which screen GUI shows and file handling
class BlurringTool(tk.Tk):
    def __init__(self, *args, **kwargs):
        # calls the Tk library to use OOP for frames in GUI
        tk.Tk.__init__(self, *args, **kwargs)
        # list stores file locations of images of faces to not be blurred
        self.faces = []
        # file location of file to be blurred image or video
        self.file = ""
        tk.Tk.wm_title(self, "Face Blurring Tool")
        screen = tk.Frame(self)
        screen.pack(side="top", fill="both", expand=True)
        screen.grid_rowconfigure(0, weight=1)
        screen.grid_columnconfigure(0, weight=1)
        # tuple stores the frames of the GUI
        self.frames = {}
        # loop to flip through every frame in TkInter, each child object represents a frame and every function within it
        for i in (MainMenu, PageVideo, PagePhoto, VideoPreview, PhotoPreview):
            frame = i(screen, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)
        self.resizable(False, False)

    # function to bring selected frame to top
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # function to select and move store images of faces to avoid
    def avoid_file(self, save):
        self.faces = filedialog.askopenfilenames()
        for i in self.faces:
            # file error handling, incase incorrect file type is selected error message will be shown
            while not i.endswith((".jpg", "jpeg", "png")) and i is not False:
                messagebox.showinfo("File Type Error", "Please only upload JPG or PNG")
                self.faces = filedialog.askopenfilenames()
        # if save faces on database checkbox is ticked, the face images uploaded will be saved for future use
        if save == 1:
            insert_images(self.faces)
        else:
            for x in self.faces:
                avoidfile = Image.open(r"{}".format(x))
                avoidfile = avoidfile.convert("RGB")
                avoidfile.save(r"./ignore/{}.jpg".format(self.faces.index(x)))

    # function to retrieve and save photo or video file to be blurred depending on the user selection
    def main_file(self, form):
        retrieve_images()
        if form == "video":
            self.file = filedialog.askopenfilename()
            while not self.file.endswith(".mp4") and not self.file == "":
                messagebox.showinfo("File Type Error", "Please only upload MP4")
                self.file = filedialog.askopenfilename()
                # video saved to main folder temporarily while program is run
            shutil.copy(self.file, "./main/main.mp4")
        else:
            self.file = filedialog.askopenfilename()
            while not self.file.endswith((".jpg", ".png", "jpeg")) and not self.file == "":
                messagebox.showinfo("File Type Error", "Please only upload PNG, JPG OR JPEG")
                self.file = filedialog.askopenfilename()
            imagefile = Image.open(r"{}".format(self.file))
            imagefile = imagefile.convert("RGB")
            # image saved to main folder temporarily while program is run
            imagefile.save(r"./main/main.jpg")

# object for the main menu page of the UI
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        # inherits from parent class (BlurringTool) to allow for frames to be brought to front of users screen
        tk.Frame.__init__(self, parent)

        # section to place all Tkinter objects onto the main menu frame
        title = tk.Label(self, text="Face Blurring Tool", fg="#584689", font=TITLE_FONT)
        title.place(anchor="center", relx=0.5, rely=0.2)

        # button to get to video file selection page
        button_video = tk.Button(self, text="Video Blurring", fg="#584689", font=SUBTITLE_FONT,
                                 command=lambda: controller.show_frame(PageVideo))
        button_video.place(anchor="center", relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)

        # button to get to photo file selection page
        button_photo = tk.Button(self, text="Photo Blurring", fg="#584689", font=SUBTITLE_FONT,
                                 command=lambda: controller.show_frame(PagePhoto))
        button_photo.place(anchor="center", relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)

        camerapath = Image.open("./GUI/camera.png")
        cameraimage = ImageTk.PhotoImage(camerapath)
        camera = tk.Label(self, image=cameraimage)
        camera.photo = cameraimage
        camera.place(anchor="center", relx=0.75, rely=0.5)

        videopath = Image.open("./GUI/video.png")
        videoimage = ImageTk.PhotoImage(videopath)
        video = tk.Label(self, image=videoimage)
        video.photo = videoimage
        video.place(anchor="center", relx=0.25, rely=0.5)

# object for video file selection page of the UI
class PageVideo(tk.Frame):

    # inherits from parent class (BlurringTool) to allow for frames to be brought to front of users screen
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Variable stores the value of blurring strenght user selects on drag bar
        self.saveface = IntVar()
        # section for placing objects onto the frame on the GUI
        header = tk.Label(self, text="File Selection for Video", fg="#584689", font=TITLE_FONT_2)
        header.place(anchor="center", relx=0.5, rely=0.2)
        # button sends back to main menu
        button_back = tk.Button(self, text="Back to Main Menu", fg="#584689", font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor="center", relx=0.5, rely=0.05, relwidth=0.2, relheight=0.05)
        # button calls the method in parent class to allow user to select main video file
        button_selectvideo = tk.Button(self, text="Upload Video", fg="#584689", font=SUBTITLE_FONT,
                                       command=lambda:  BlurringTool.main_file(parent, "video"))
        button_selectvideo.place(anchor="center", relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)
        # button calls method in parent class to allow user to select face photos to avoid in blurring
        button_selectface = tk.Button(self, text="Upload Faces to Avoid", fg="#584689", font=SUBTITLE_FONT,
                                      command=lambda:  BlurringTool.avoid_file(parent, self.saveface))
        button_selectface.place(anchor="center", relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)
        # check box, if ticked face photo uploaded will be saved to database faces.db
        save_checkbox = tk.Checkbutton(self, text="check to save faces for future use", font=SUBTITLE_FONT,
                                       variable=self.saveface, onvalue=1, offvalue=0)
        save_checkbox.place(anchor="center", relx=0.71, rely=0.85)

        explanation = tk.Label(self, text="(OPTIONAL) Upload images of each face that\n"
                                          " should be avoided in the blurring process,\n"
                                          " Image should look like the one above", font=BODY_FONT)
        explanation.place(anchor="center", relx=0.75, rely=0.93)
        # When button is pressed blurring is applied to all faces in video
        button_done = tk.Button(self, text="DONE", fg="#584689", font=BODY_FONT,
                                command=lambda: [facelocatevideo(round(self.intense.get())),
                                                 controller.show_frame(VideoPreview)])
        button_done.place(anchor="center", relx=0.5, rely=0.95, relwidth=0.2, relheight=0.05)
        # button deletes all face photos saved by that user in the database for future use
        button_clear_saved = tk.Button(self, text="clear saved", fg="#584689", font=BODY_FONT,
                                       command=lambda: cleartable())
        button_clear_saved.place(anchor="center", relx=0.91, rely=0.85, relwidth=0.08, relheight=0.05)

        avoidfacepath = Image.open("./GUI/faceavoid.jpg")
        avoidfaceimage = ImageTk.PhotoImage(avoidfacepath)
        avoidface = tk.Label(self, image=avoidfaceimage)
        avoidface.photo = avoidfaceimage
        avoidface.place(anchor="center", relx=0.75, rely=0.5)

        videofilepath = Image.open("./GUI/videofile.png")
        videofileimage = ImageTk.PhotoImage(videofilepath)
        videofile = tk.Label(self, image=videofileimage)
        videofile.photo = videofileimage
        videofile.place(anchor="center", relx=0.25, rely=0.5)
        # drag scale to adjust blurring intensity of faces
        self.intense = ttk.Scale(self, from_=5, to=10, orient=tk.HORIZONTAL)
        self.intense.set(7.5)
        self.intense.place(anchor="center", relx=0.25, rely=0.82, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.87)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.87)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.87)


#
class PagePhoto(tk.Frame):

    # inherits from parent class (BlurringTool) to allow for frames to be brought to front of users screen
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # saves the integer value of face blurring intensity set by user
        self.saveface = IntVar()

        header = tk.Label(self, text="File Selection for Photographs", fg="#584689", font=TITLE_FONT_2)
        header.place(anchor="center", relx=0.5, rely=0.2)
        # button for user to go back to menu
        button_back = tk.Button(self, text="Back to Main Menu", fg="#584689", font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor="center", relx=0.5, rely=0.05, relwidth=0.2, relheight=0.05)
        # button to select mail file for blurring to be applied to
        button_selectphoto = tk.Button(self, text="Upload Photograph", fg="#584689", font=SUBTITLE_FONT,
                                       command=lambda: BlurringTool.main_file(parent, "photo"))
        button_selectphoto.place(anchor="center", relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)
        # button for user to select photos of faces not to be blurred
        button_selectface = tk.Button(self, text="Upload Faces to Avoid", fg="#584689", font=SUBTITLE_FONT,
                                      command=lambda: BlurringTool.avoid_file(parent, self.saveface.get()))
        button_selectface.place(anchor="center", relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)
        # save face checkbox to save faces to avoid on database faces.db for faces not to be blurred in the future
        save_checkbox = tk.Checkbutton(self, text="check to save faces for future use", font=SUBTITLE_FONT,
                                       variable=self.saveface, onvalue=1, offvalue=0)
        save_checkbox.place(anchor="center", relx=0.71, rely=0.85)

        explanation = tk.Label(self, text="(OPTIONAL) Upload images of each face that\n"
                                          " should be avoided in the blurring process,\n"
                                          " Image should look like the one above", font=BODY_FONT)
        explanation.place(anchor="center", relx=0.75, rely=0.93)
        # button to apply blurring to image and go to preview page to see final image
        button_done = tk.Button(self, text="DONE", fg="#584689", font=BODY_FONT,
                                command=lambda: [facelocatephoto(round(self.intense.get())),
                                                 controller.show_frame(PhotoPreview),
                                                 PhotoPreview.display(parent)])
        button_done.place(anchor="center", relx=0.5, rely=0.95, relwidth=0.2, relheight=0.05)
        # button to delete all of users saved faces from database.db to allow them to get blurring in images
        button_clear_saved = tk.Button(self, text="clear saved", fg="#584689", font=BODY_FONT,
                                       command=lambda: cleartable())
        button_clear_saved.place(anchor="center", relx=0.91, rely=0.85, relwidth=0.08, relheight=0.05)

        avoidfacepath = Image.open("./GUI/faceavoid.jpg")
        avoidfaceimage = ImageTk.PhotoImage(avoidfacepath)
        avoidface = tk.Label(self, image=avoidfaceimage)
        avoidface.photo = avoidfaceimage
        avoidface.place(anchor="center", relx=0.75, rely=0.5)

        photofilepath = Image.open("./GUI/photofile.png")
        photofileimage = ImageTk.PhotoImage(photofilepath)
        photofile = tk.Label(self, image=photofileimage)
        photofile.photo = photofileimage
        photofile.place(anchor="center", relx=0.25, rely=0.5)
        # drag bar to allow for intensity of blurring of faces to be adjusted before blurring is applied
        self.intense = ttk.Scale(self, from_=5, to=20, orient=tk.HORIZONTAL)
        self.intense.set(8)
        self.intense.place(anchor="center", relx=0.25, rely=0.82, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.87)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.87)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.87)

# object of page on UI to select save location of blurred video file and readjust blurring intensity if needed
class VideoPreview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        button_reblur = tk.Button(self, text="Blur Again", fg="#584689", font=SUBTITLE_FONT,
                                  command=lambda: [os.remove("./temp/finished.jpg"),
                                                   facelocatevideo(round(self.intense.get())),
                                                   controller.show_frame(PhotoPreview),
                                                   PhotoPreview.display(parent)])
        button_reblur.place(anchor="center", relx=0.25, rely=0.80, relwidth=0.4, relheight=0.1)

        button_complete = tk.Button(self, text="Save File and Finish", fg="#584689", font=SUBTITLE_FONT,
                                    command=lambda: [savefile("video"),
                                                     deletefiles("final"),
                                                     controller.show_frame(MainMenu)])
        button_complete.place(anchor="center", relx=0.75, rely=0.80, relwidth=0.4, relheight=0.1)

        self.intense = ttk.Scale(self, from_=5, to=20, orient=tk.HORIZONTAL)
        self.intense.set(8)
        self.intense.place(anchor="center", relx=0.25, rely=0.87, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.92)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.92)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.92)

        # videoplayer = TkinterVideo(master=self, scaled=True, pre_load=False)
        # videoplayer.place(anchor="center")
        # videoplayer.place(anchor="center", relx=0.64, rely=0.36)


class PhotoPreview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button_reblur = tk.Button(self, text="Blur Again", fg="#584689", font=SUBTITLE_FONT,
                                  command=lambda: [os.remove("./temp/finished.jpg"),
                                                   facelocatephoto(round(self.intense.get())),
                                                   controller.show_frame(PhotoPreview),
                                                   PhotoPreview.display(parent)])
        button_reblur.place(anchor="center", relx=0.25, rely=0.80, relwidth=0.4, relheight=0.1)

        button_complete = tk.Button(self, text="Save File and Finish", fg="#584689", font=SUBTITLE_FONT,
                                    command=lambda: [savefile("photo"),
                                                     deletefiles("final"),
                                                     controller.show_frame(MainMenu)])
        button_complete.place(anchor="center", relx=0.75, rely=0.80, relwidth=0.4, relheight=0.1)

        self.intense = ttk.Scale(self, from_=5, to=20, orient=tk.HORIZONTAL)
        self.intense.set(8)
        self.intense.place(anchor="center", relx=0.25, rely=0.87, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.92)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.92)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.92)

    def display(self):
        photo = Image.open("./temp/finished.jpg")
        width, height = photo.size
        ratio = width/height
        photo = photo.resize((700, int(700/ratio)))
        photoimage = ImageTk.PhotoImage(photo)
        photopreview = tk.Label(self, image=photoimage)
        photopreview.photo = photoimage
        photopreview.place(anchor="center", relx=0.5, rely=0.35)


if __name__ == "__main__":
    deletefiles("start")
    gui = BlurringTool()
    gui.geometry("1280x720")
    gui.mainloop()
