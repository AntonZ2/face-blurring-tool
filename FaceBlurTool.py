import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox, IntVar, ttk
import os
import shutil
import datetime

# HASH FOLLOWED BY GRAY TEXT IS A COMMENT EXPLAINING SURROUNDING CODE
# objects imported from my other python files
from database import Database
from facebluralg import FaceBlurAlgorithm

# Fonts
TITLE_FONT = ("Fixedsys", 100, "bold")
TITLE_FONT_2 = ("Fixedsys", 80, "bold")
SUBTITLE_FONT = ("Fixedsys", 24, "bold")
SUBTITLE_FONT_2 = ("Fixedsys", 40, "bold")
BODY_FONT = ("Verdana", 14)

# Object initialization
DB = Database()
blur = FaceBlurAlgorithm()


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
        for i in (Login, Registration, MainMenu, PageVideo, PagePhoto, PhotoPreview):
            #removed VideoPreview from for loop
            frame = i(screen, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Login)
        self.resizable(False, False)

    # function to bring selected frame to top
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

    # function to select and move store images of faces to avoid
    def avoid_file(self, save, form):
        self.faces = filedialog.askopenfilenames()
        for i in self.faces:

            # file error handling, incase incorrect file type is selected error message will be shown
            while not i.endswith((".jpg", "jpeg", "png")) and self.faces:
                messagebox.showinfo("File Type Error", "Please only upload JPG or PNG")
                self.faces = filedialog.askopenfilenames()

        # if save faces on database checkbox is ticked, the face images uploaded will be saved for future use
        if save == 1:
            if form == 'video':
                DB.video_insert_images(self.faces)
            else:
                DB.photo_insert_images(self.faces)
        else:
            for x in self.faces:
                avoidfile = Image.open(r"{}".format(x))
                avoidfile = avoidfile.convert("RGB")
                avoidfile.save(r"./ignore/{}.jpg".format(self.faces.index(x)))

    # function to retrieve and save photo or video file to be blurred depending on the user selection
    def main_file(self, form):
        if form == "video":
            DB.video_retrieve_images()
            self.file = filedialog.askopenfilename()
            while not self.file.endswith(".mp4") and self.file:
                messagebox.showinfo("File Type Error", "Please only upload MP4")
                self.file = filedialog.askopenfilename()
            if self.file != "":
                # video saved to main folder temporarily while program is run
                shutil.copy(self.file, "./main/main.mp4")
        else:
            DB.photo_retrieve_images()
            self.file = filedialog.askopenfilename()
            while not self.file.endswith((".jpg", ".png", "jpeg")) and self.file:
                messagebox.showinfo("File Type Error", "Please only upload PNG, JPG OR JPEG")
                self.file = filedialog.askopenfilename()
            if self.file != "":
                imagefile = Image.open(r"{}".format(self.file))
                imagefile = imagefile.convert("RGB")
                # image saved to main folder temporarily while program is run
                imagefile.save(r"./main/main.jpg")


# class for the login and registration page of the UI
class Login(tk.Frame):
    def __init__(self, parent, controller):
        # inherits tk.Frame characteristics to allow for frames to be brought to front of users screen
        tk.Frame.__init__(self, parent)
        # variables storing the username and password that user inputs
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # title of the program on the login screen
        self.title = tk.Label(self, text="Face Blurring Tool", fg="#584689", font=TITLE_FONT)
        self.title.place(anchor="center", relx=0.5, rely=0.2)
        # login screen label
        self.logintitle = tk.Label(self, text="Login to use your saved faces", fg="#584689", font=SUBTITLE_FONT_2)
        self.logintitle.place(anchor="center", relx=0.5, rely=0.35)
        # Username label
        self.usernamelabel = tk.Label(self, text="Username:", fg="#584689", font=SUBTITLE_FONT)
        self.usernamelabel.place(anchor="center", relx=0.35, rely=0.45)
        # Password label
        self.passwordlabel = tk.Label(self, text="Password:", fg="#584689", font=SUBTITLE_FONT)
        self.passwordlabel.place(anchor="center", relx=0.35, rely=0.55)
        # Entry square to type in username
        self.usernameentry = tk.Entry(self, font=SUBTITLE_FONT, justify="center", textvariable=self.username)
        self.usernameentry.place(anchor="center", relx=0.54, rely=0.45, relwidth=0.29, relheight=0.07)
        # Entry square to type in password
        passwordentry = tk.Entry(self, font=SUBTITLE_FONT, justify="center", show="*", textvariable=self.password)
        passwordentry.place(anchor="center", relx=0.54, rely=0.55, relwidth=0.29, relheight=0.07)
        # Button for user to register if they dont have an account
        registerbutton = tk.Button(self, text="Register", fg="#584689", font=SUBTITLE_FONT,
                                   command=lambda: controller.show_frame(Registration))
        registerbutton.place(anchor="center", relx=0.4, rely=0.65, relwidth=0.19, relheight=0.1)
        # Button to login after credentials are inputted
        loginbutton = tk.Button(self, text="Login", fg="#584689", font=SUBTITLE_FONT,
                                command=lambda: [DB.find_user(self.username.get(), self.password.get(), 'user'),
                                                 controller.show_frame(MainMenu)
                                                 if DB.success_check()
                                                 else (controller.show_frame(Login))])
        loginbutton.place(anchor="center", relx=0.6, rely=0.65, relwidth=0.19, relheight=0.1)
        # text explaining when to login and when to continue as guest
        explanation = tk.Label(self, text="register to create an account allowing you to save faces so they never get\n"
                                          "blurred again, press below to continue as a guest without saving faces.",
                               fg="#584689", font=BODY_FONT)
        explanation.place(anchor="center", relx=0.5, rely=0.75)
        # Button to coninue as a guest
        guestbutton = tk.Button(self, text="Continue as a Guest", fg="#584689", font=SUBTITLE_FONT,
                                command=lambda: [DB.find_user('', '', 'guest'), controller.show_frame(MainMenu)])
        guestbutton.place(anchor="center", relx=0.5, rely=0.85, relwidth=0.4, relheight=0.1)

# Class frame for registration screen
class Registration(tk.Frame):
    def __init__(self, parent, controller):
        # inherits tk.Frame characteristics to allow for frames to be brought to front of users screen
        tk.Frame.__init__(self, parent)
        # Variables to store username and password entries
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.password2 = tk.StringVar()
        # program title
        self.title = tk.Label(self, text="Face Blurring Tool", fg="#584689", font=TITLE_FONT)
        self.title.place(anchor="center", relx=0.5, rely=0.2)
        # registration screen title
        self.registertitle = tk.Label(self, text="Account Registration Form", fg="#584689", font=SUBTITLE_FONT_2)
        self.registertitle.place(anchor="center", relx=0.5, rely=0.35)
        # Username label text
        self.usernamelabel = tk.Label(self, text="Username:", fg="#584689", font=SUBTITLE_FONT)
        self.usernamelabel.place(anchor="center", relx=0.35, rely=0.45)
        # password label text
        self.passwordlabel = tk.Label(self, text="Password:", fg="#584689", font=SUBTITLE_FONT)
        self.passwordlabel.place(anchor="center", relx=0.35, rely=0.55)
        # re-enter password level text
        self.password2label = tk.Label(self, text="re-enter\nPassword:", fg="#584689", font=SUBTITLE_FONT)
        self.password2label.place(anchor="center", relx=0.35, rely=0.64)
        # Username entry box
        self.usernameentry = tk.Entry(self, font=SUBTITLE_FONT, justify="center", textvariable=self.username)
        self.usernameentry.place(anchor="center", relx=0.54, rely=0.45, relwidth=0.29, relheight=0.07)
        # passwrd entry box
        self.passwordentry = tk.Entry(self, font=SUBTITLE_FONT, justify="center", show="*", textvariable=self.password)
        self.passwordentry.place(anchor="center", relx=0.54, rely=0.55, relwidth=0.29, relheight=0.07)
        # Passowrd re-enter box
        self.password2entry = tk.Entry(self, font=SUBTITLE_FONT, justify="center", show="*",
                                       textvariable=self.password2)
        self.password2entry.place(anchor="center", relx=0.54, rely=0.65, relwidth=0.29, relheight=0.07)
        # Button to go back to login screen
        self.backbutton = tk.Button(self, text="Back", fg="#584689", font=SUBTITLE_FONT,
                                    command=lambda: controller.show_frame(Login))
        self.backbutton.place(anchor="center", relx=0.4, rely=0.75, relwidth=0.19, relheight=0.1)
        # Button to register after credentials are typed in
        self.registerbutton = tk.Button(self, text="Register", fg="#584689", font=SUBTITLE_FONT,
                                        command=lambda: [DB.register_user(self.username.get(), self.password.get(),
                                                                          self.password2.get()),
                                                         self.clear_details(), controller.show_frame(Login)
                                                         if DB.success_check()
                                                         else (controller.show_frame(Registration))])
        self.registerbutton.place(anchor="center", relx=0.6, rely=0.75, relwidth=0.19, relheight=0.1)
        # explanation of all passwor parameters tat have to be met
        self.password_explained = tk.Label(self, text="Password must be at least 8 characters "
                                                      "long and should contain at least\n"
                                                      "one number, one uppercase character "
                                                      "and one lowercase character.",
                                           fg="#FF0000", font=BODY_FONT)
        self.password_explained.place(anchor="center", relx=0.5, rely=0.85)
    # method to clear typed in details if user doesnt meet requirements and has to try again
    def clear_details(self):
        self.passwordentry.delete(0, 'end')
        self.password2entry.delete(0, 'end')


# class for the main menu page of the UI
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        # inherits from parent class (BlurringTool) to allow for frames to be brought to front of users screen
        tk.Frame.__init__(self, parent)

        logout = tk.Button(self, text="Log Out", fg="#584689", font=SUBTITLE_FONT,
                           command=lambda: [DB.logout(), controller.show_frame(Login)])
        logout.place(anchor="center", relx=0.87, rely=0.05, relwidth=0.15, relheight=0.08)

        # section to place all Tkinter objects onto the main menu frame
        title = tk.Label(self, text="Face Blurring Tool", fg="#584689", font=TITLE_FONT)
        title.place(anchor="center", relx=0.5, rely=0.2)

        # button to get to video file selection page
        button_video = tk.Button(self, text="Video Blurring", fg="#584689", font=SUBTITLE_FONT,
                                 command=lambda: [controller.show_frame(PageVideo), ])
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


# class for video file selection page of the UI
class PageVideo(tk.Frame):

    # inherits from parent class (BlurringTool) to allow for frames to be brought to front of users screen
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.on_show_frame)

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
                                      command=lambda:  BlurringTool.avoid_file(parent, self.saveface.get(), "video"))
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
                                command=lambda: [DB.video_intensity_set(round(self.intense.get())),
                                                 blur.facelocatevideo(round(self.intense.get()))
                                                 ])
        # removed from tk button above = controller.show_frame(VideoPreview)

        button_done.place(anchor="center", relx=0.5, rely=0.95, relwidth=0.2, relheight=0.05)

        # button deletes all face photos saved by that user in the database for future use
        button_clear_saved = tk.Button(self, text="clear saved", fg="#584689", font=BODY_FONT,
                                       command=lambda: DB.video_cleartable())
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
        self.intense.place(anchor="center", relx=0.25, rely=0.82, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.87)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.87)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.87)

    def on_show_frame(self, event):
        self.intense.set(DB.video_intensity_get())


# class for photo file selection page of the UI
class PagePhoto(tk.Frame):

    # inherits from parent class (BlurringTool) to allow for frames to be brought to front of users screen
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Variable to decide whether face images are saved to database for future blurring
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
                                      command=lambda: BlurringTool.avoid_file(parent, self.saveface.get(), 'photo'))
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
                                command=lambda: [DB.photo_intensity_set(round(self.intense.get())),
                                                 blur.facelocatephoto(round(self.intense.get())),
                                                 controller.show_frame(PhotoPreview),
                                                 PhotoPreview.display(parent)])
        button_done.place(anchor="center", relx=0.5, rely=0.95, relwidth=0.2, relheight=0.05)

        # button to delete all of users saved faces from database.db to allow them to get blurring in images
        button_clear_saved = tk.Button(self, text="clear saved", fg="#584689", font=BODY_FONT,
                                       command=lambda: DB.photo_cleartable())
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
        self.intense.place(anchor="center", relx=0.25, rely=0.82, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.87)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.87)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.87)

    def on_show_frame(self, event):
        self.intense.set(DB.photo_intensity_get())


# class of page on UI to select save location of blurred video file and readjust blurring intensity if needed
'''class VideoPreview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.load_video)

        # reblur button allows user to chose intensity and reblur the video if they are unhappy with result
        button_reblur = tk.Button(self, text="Blur Again", fg="#584689", font=SUBTITLE_FONT,
                                  command=lambda: [os.remove("./temp/finished.mp4"),
                                                   DB.video_intensity_set(round(self.intense.get())),
                                                   blur.facelocatevideo(round(self.intense.get())),
                                                   controller.show_frame(VideoPreview)])
        button_reblur.place(anchor="center", relx=0.25, rely=0.88, relwidth=0.4, relheight=0.07)

        button_back = tk.Button(self, text="Back to Main Menu", fg="#584689", font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor="center", relx=0.75, rely=0.95, relwidth=0.2, relheight=0.05)

        # opens file dialog for user to chose save location of final file
        button_complete = tk.Button(self, text="Save File and Finish", fg="#584689", font=SUBTITLE_FONT,
                                    command=lambda: [blur.savefile("video"),
                                                     blur.deletefiles(),
                                                     controller.show_frame(MainMenu)])
        button_complete.place(anchor="center", relx=0.75, rely=0.88, relwidth=0.4, relheight=0.07)

        # scale to adjust intensity for re-blurring
        self.intense = ttk.Scale(self, from_=5, to=10, orient=tk.HORIZONTAL)
        self.intense.place(anchor="center", relx=0.25, rely=0.97, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=BODY_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.94)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.94)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.94)

        self.vid_player = TkinterVideo(master=self, pre_load=False, scaled=True)
        self.vid_player.place(anchor='center', relx=0.5, rely=0.38, relheight=0.75, relwidth=0.8)
        self.play_pause_btn = tk.Button(self, text='PLAY VIDEO', command=self.play_pause)
        self.play_pause_btn.place(anchor='center', relx=0.15, rely=0.8, relwidth=0.2, relheight=0.07)
        self.progress_slider = ttk.Scale(self, from_=0, to=0, orient="horizontal", command=self.seek)
        self.progress_slider.place(anchor='center', relx=0.6, rely=0.8, relwidth=0.68, relheight=0.07)
        self.end_time = tk.Label(self, text=str(datetime.timedelta(seconds=0)))
        self.end_time.place(anchor='center', relx=0.97, rely=0.8)

        self.vid_player.bind("<<Duration>>", self.update_duration)
        self.vid_player.bind("<<SecondChanged>>", self.update_scale)
        self.vid_player.bind("<<Ended>>", self.video_ended)

    def update_duration(self, event):
        # updates the duration after finding the duration
        self.end_time["text"] = str(datetime.timedelta(seconds=self.vid_player.duration()))[:10]
        self.progress_slider["to"] = self.vid_player.duration()

    def update_scale(self, event):
        # updates the scale value
        self.progress_slider.set(self.vid_player.current_duration())

    def load_video(self, event):
        # sets users saved blurring intensity
        self.intense.set(DB.video_intensity_get())
        # loads the video
        file_pathname = "./temp/finished.mp4"

        self.vid_player.load(file_pathname)

        self.progress_slider.config(to=0, from_=0)
        self.progress_slider.set(0)
        self.play_pause_btn["text"] = "Play"

    def seek(self, value):
        # used to seek a specific timeframe
        self.vid_player.seek(int(float(value)))

    def skip(self, value):
        # skip seconds
        self.vid_player.skip_sec(int(float(value)))
        self.progress_slider.set(self.progress_slider.get() + int(float(value)))

    def play_pause(self):
        # pauses and plays
        if self.vid_player.is_paused():
            self.vid_player.play()
            self.play_pause_btn["text"] = "Pause"

        else:
            self.vid_player.pause()
            self.play_pause_btn["text"] = "Play"

    def video_ended(self, event):
        # handle video ended
        self.progress_slider.set(self.progress_slider["to"])
        self.play_pause_btn["text"] = "Play"'''


# class of page on UI to select save location of blurred photo file and readjust blurring intensity if needed
class PhotoPreview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.on_show_frame)

        # button to reblur image if user is unhappy with blurred result
        button_reblur = tk.Button(self, text="Blur Again", fg="#584689", font=SUBTITLE_FONT,
                                  command=lambda: [os.remove("./temp/finished.jpg"),
                                                   DB.photo_intensity_set(round(self.intense.get())),
                                                   blur.facelocatephoto(round(self.intense.get())),
                                                   controller.show_frame(PhotoPreview),
                                                   PhotoPreview.display(parent)])
        button_reblur.place(anchor="center", relx=0.25, rely=0.80, relwidth=0.4, relheight=0.1)

        # opens file dialog for user to chose save location of final file
        button_complete = tk.Button(self, text="Save File and Finish", fg="#584689", font=SUBTITLE_FONT,
                                    command=lambda: [blur.savefile("photo"),
                                                     blur.deletefiles(),
                                                     controller.show_frame(MainMenu)])
        button_complete.place(anchor="center", relx=0.75, rely=0.80, relwidth=0.4, relheight=0.1)

        button_back = tk.Button(self, text="Back to Main Menu", fg="#584689", font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor="center", relx=0.75, rely=0.95, relwidth=0.2, relheight=0.05)

        # scale to adjust intensity for re-blurring
        self.intense = ttk.Scale(self, from_=5, to=20, orient=tk.HORIZONTAL)
        self.intense.place(anchor="center", relx=0.25, rely=0.87, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="center", relx=0.25, rely=0.92)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="center", relx=0.065, rely=0.92)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="center", relx=0.43, rely=0.92)

    def on_show_frame(self, event):
        self.intense.set(DB.photo_intensity_get())

    # method to load preview of blurred image for user to decide if they want to reblur it
    def display(self):
        photo = Image.open("./temp/finished.jpg")
        width, height = photo.size
        ratio = width/height
        photo = photo.resize((700, int(700/ratio)))
        photoimage = ImageTk.PhotoImage(photo)
        photopreview = tk.Label(self, image=photoimage)
        photopreview.photo = photoimage
        photopreview.place(anchor="center", relx=0.5, rely=0.35)


# program section to call the master class and start the program setting window size
if __name__ == "__main__":
    blur.deletefiles()
    FaceBlurTool = BlurringTool()
    FaceBlurTool.geometry("1440x810")
    FaceBlurTool.mainloop()

