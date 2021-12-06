import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox, IntVar, ttk
from tkVideoPlayer import TkinterVideo
import datetime
import shutil
from SQL_faces import insert_images, retrieve_images
from face_rec import facelocatephoto, facelocatevideo, deletefiles

# Fonts
TITLE_FONT = ("Fixedsys", 100, "bold")
TITLE_FONT_2 = ("Fixedsys", 80, "bold")
SUBTITLE_FONT = ("Fixedsys", 24, "bold")
BODY_FONT = ("Verdana", 14)


class BlurringTool(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default="icon.ico")
        self.faces = []
        self.file = ""
        tk.Tk.wm_title(self, "Face Blurring Tool")
        screen = tk.Frame(self)
        screen.pack(side="top", fill="both", expand=True)
        screen.grid_rowconfigure(0, weight=1)
        screen.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for i in (MainMenu, PageVideo, PagePhoto, VideoPreview, PhotoPreview):
            frame = i(screen, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)
        self.resizable(False, False)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def avoid_file(self, save):
        self.faces = filedialog.askopenfilenames()
        for i in self.faces:
            while not i.endswith((".jpg", "jpeg", "png")) and i is not False:
                messagebox.showinfo("File Type Error", "Please only upload JPG or PNG")
                self.faces = filedialog.askopenfilenames()
        if save == 1:
            insert_images(self.faces)
            print('done!')
        else:
            for x in self.faces:
                avoidfile = Image.open(r"{}".format(x))
                avoidfile = avoidfile.convert("RGB")
                avoidfile.save(r"./ignore/{}.jpg".format(self.faces.index(x)))

    def main_file(self, form):
        retrieve_images()
        if form == "video":
            self.file = filedialog.askopenfilename()
            while not self.file.endswith(".mp4") and not self.file == "":
                messagebox.showinfo("File Type Error", "Please only upload MP4")
                self.file = filedialog.askopenfilename()
            shutil.copyfile(self.file, "./main/main.mp4")
        else:
            self.file = filedialog.askopenfilename()
            while not self.file.endswith((".jpg", ".png", "jpeg")) and not self.file == "":
                messagebox.showinfo("File Type Error", "Please only upload PNG, JPG OR JPEG")
                self.file = filedialog.askopenfilename()
            imagefile = Image.open(r"{}".format(self.file))
            imagefile = imagefile.convert("RGB")
            imagefile.save(r"./main/main.jpg")


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Face Blurring Tool", fg="#584689", font=TITLE_FONT)
        title.place(anchor="c", relx=0.5, rely=0.2)

        button_video = tk.Button(self, text="Video Blurring", fg="#584689", font=SUBTITLE_FONT,
                                 command=lambda: controller.show_frame(PageVideo))
        button_video.place(anchor="c", relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)

        button_photo = tk.Button(self, text="Photo Blurring", fg="#584689", font=SUBTITLE_FONT,
                                 command=lambda: controller.show_frame(PagePhoto))
        button_photo.place(anchor="c", relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)

        camerapath = Image.open("camera.png")
        cameraimage = ImageTk.PhotoImage(camerapath)
        camera = tk.Label(self, image=cameraimage)
        camera.photo = cameraimage
        camera.place(anchor="c", relx=0.75, rely=0.5)

        videopath = Image.open("video.png")
        videoimage = ImageTk.PhotoImage(videopath)
        video = tk.Label(self, image=videoimage)
        video.photo = videoimage
        video.place(anchor="c", relx=0.25, rely=0.5)


class PageVideo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.saveface = IntVar()

        header = tk.Label(self, text="File Selection for Video", fg="#584689", font=TITLE_FONT_2)
        header.place(anchor="c", relx=0.5, rely=0.2)

        button_back = tk.Button(self, text="Back to Main Menu", fg="#584689", font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor="c", relx=0.5, rely=0.05, relwidth=0.2, relheight=0.05)

        button_selectvideo = tk.Button(self, text="Upload Video", fg="#584689", font=SUBTITLE_FONT,
                                       command=lambda:  BlurringTool.main_file(parent, "video"))
        button_selectvideo.place(anchor="c", relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)

        button_selectface = tk.Button(self, text="Upload Faces to Avoid", fg="#584689", font=SUBTITLE_FONT,
                                      command=lambda:  BlurringTool.avoid_file(parent, self.saveface))
        button_selectface.place(anchor="c", relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)

        save_checkbox = tk.Checkbutton(self, text="check to save faces for future use", font=SUBTITLE_FONT,
                                       variable=self.saveface, onvalue=1, offvalue=0)
        save_checkbox.place(anchor="c", relx=0.75, rely=0.85)

        explanation = tk.Label(self, text="(OPTIONAL) Upload images of each face that\n"
                                          " should be avoided in the blurring process,\n"
                                          " Image should look like the one above", font=BODY_FONT)
        explanation.place(anchor="c", relx=0.75, rely=0.93)

        button_done = tk.Button(self, text="DONE", fg="#584689", font=BODY_FONT,
                                command=lambda: [facelocatevideo(round(self.intense.get())),
                                                 controller.show_frame(VideoPreview)])
        button_done.place(anchor="c", relx=0.5, rely=0.95, relwidth=0.2, relheight=0.05)

        avoidfacepath = Image.open("faceavoid.jpg")
        avoidfaceimage = ImageTk.PhotoImage(avoidfacepath)
        avoidface = tk.Label(self, image=avoidfaceimage)
        avoidface.photo = avoidfaceimage
        avoidface.place(anchor="c", relx=0.75, rely=0.5)

        videofilepath = Image.open("videofile.png")
        videofileimage = ImageTk.PhotoImage(videofilepath)
        videofile = tk.Label(self, image=videofileimage)
        videofile.photo = videofileimage
        videofile.place(anchor="c", relx=0.25, rely=0.5)

        self.intense = ttk.Scale(self, from_=5, to=10, orient=tk.HORIZONTAL)
        self.intense.set(7.5)
        self.intense.place(anchor="c", relx=0.25, rely=0.82, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="c", relx=0.25, rely=0.87)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="c", relx=0.065, rely=0.87)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="c", relx=0.43, rely=0.87)


class PagePhoto(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.saveface = IntVar()

        header = tk.Label(self, text="File Selection for Photographs", fg="#584689", font=TITLE_FONT_2)
        header.place(anchor="c", relx=0.5, rely=0.2)

        button_back = tk.Button(self, text="Back to Main Menu", fg="#584689", font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor="c", relx=0.5, rely=0.05, relwidth=0.2, relheight=0.05)

        button_selectphoto = tk.Button(self, text="Upload Photograph", fg="#584689", font=SUBTITLE_FONT,
                                       command=lambda: BlurringTool.main_file(parent, "photo"))
        button_selectphoto.place(anchor="c", relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)

        button_selectface = tk.Button(self, text="Upload Faces to Avoid", fg="#584689", font=SUBTITLE_FONT,
                                      command=lambda: BlurringTool.avoid_file(parent, self.saveface.get()))
        button_selectface.place(anchor="c", relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)

        save_checkbox = tk.Checkbutton(self, text="check to save faces for future use", font=SUBTITLE_FONT,
                                       variable=self.saveface, onvalue=1, offvalue=0)
        save_checkbox.place(anchor="c", relx=0.75, rely=0.85)

        explanation = tk.Label(self, text="(OPTIONAL) Upload images of each face that\n"
                                          " should be avoided in the blurring process,\n"
                                          " Image should look like the one above", font=BODY_FONT)
        explanation.place(anchor="c", relx=0.75, rely=0.93)

        button_done = tk.Button(self, text="DONE", fg="#584689", font=BODY_FONT,
                                command=lambda: [facelocatephoto(round(self.intense.get())),
                                                 controller.show_frame(PhotoPreview),
                                                 PhotoPreview.display(parent)])
        button_done.place(anchor="c", relx=0.5, rely=0.95, relwidth=0.2, relheight=0.05)

        avoidfacepath = Image.open("faceavoid.jpg")
        avoidfaceimage = ImageTk.PhotoImage(avoidfacepath)
        avoidface = tk.Label(self, image=avoidfaceimage)
        avoidface.photo = avoidfaceimage
        avoidface.place(anchor="c", relx=0.75, rely=0.5)

        photofilepath = Image.open("photofile.png")
        photofileimage = ImageTk.PhotoImage(photofilepath)
        photofile = tk.Label(self, image=photofileimage)
        photofile.photo = photofileimage
        photofile.place(anchor="c", relx=0.25, rely=0.5)

        self.intense = ttk.Scale(self, from_=5, to=20, orient=tk.HORIZONTAL)
        self.intense.set(8)
        self.intense.place(anchor="c", relx=0.25, rely=0.82, relwidth=0.4)
        intensity = tk.Label(self, text="Blurring Intensity", font=SUBTITLE_FONT)
        intensity.place(anchor="c", relx=0.25, rely=0.87)
        weak = tk.Label(self, text="weak", font=BODY_FONT)
        weak.place(anchor="c", relx=0.065, rely=0.87)
        strong = tk.Label(self, text="strong", font=BODY_FONT)
        strong.place(anchor="c", relx=0.43, rely=0.87)


class VideoPreview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class PhotoPreview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    def display(self):
        photo = Image.open("./temp/finished.jpg")
        width, height = photo.size
        ratio = width/height
        photo = photo.resize((700, int(700/ratio)))
        photoimage = ImageTk.PhotoImage(photo)
        photopreview = tk.Label(self, image=photoimage)
        photopreview.photo = photoimage
        photopreview.place(anchor="c", relx=0.5, rely=0.5)



gui = BlurringTool()
gui.geometry("1280x720")
gui.mainloop()
