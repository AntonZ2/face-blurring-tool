import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
import shutil
from face_rec import facelocatePhoto

from face_rec import facelocatePhoto

# Fonts
TITLE_FONT = ('Fixedsys', 100, 'bold')
TITLE_FONT_2 = ('Fixedsys', 80, 'bold')
SUBTITLE_FONT = ('Fixedsys', 24, 'bold')
BODY_FONT = ('Verdana', 14)


class BlurringTool(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default='icon.ico')
        self.faces = []
        self.file = ''
        tk.Tk.wm_title(self, 'Face Blurring Tool')
        screen = tk.Frame(self)
        screen.pack(side='top', fill='both', expand=True)
        screen.grid_rowconfigure(0, weight=1)
        screen.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for i in (MainMenu, PageVideo, PagePhoto):
            frame = i(screen, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def avoid_file(self):
        self.faces = filedialog.askopenfilenames()
        for i in range(len(self.faces)):
            while not self.faces[i].endswith(('.jpg')) and not self.faces[i] == False:
                messagebox.showinfo("File Type Error", "Please only upload JPG")
                self.faces = filedialog.askopenfilenames()
        for i in range(len(self.faces)):
            avoidfile = Image.open(r'{}'.format(self.faces[i]))
            avoidfile = avoidfile.convert('RGB')
            avoidfile.save(r'C:/Users/az200/Desktop/NEA/ignore/{}.jpg'.format(i))

    def main_file(self, type):
        if type == 'video':
            self.file = filedialog.askopenfilename()
            while not self.file.endswith(('.mp4')) and not self.file == '':
                messagebox.showinfo("File Type Error", "Please only upload MP4")
                self.file = filedialog.askopenfilename()
            '''videofile = cv2.VideoCapture(self.file)
            frame_width = int(videofile.get(3))
            frame_height = int(videofile.get(4))
            size = (frame_width, frame_height)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            save = cv2.VideoWriter('C:/Users0/az200/Desktop/NEA/main/main.mp4', fourcc , 20.0, size)'''
            shutil.copyfile(self.file, 'C:/Users/az200/Desktop/NEA/main/main.mp4')
        else:
            self.file = filedialog.askopenfilename()
            while not self.file.endswith(('.jpg', '.png')) and not self.file == '':
                messagebox.showinfo("File Type Error", "Please only upload PNG, JPG OR JPEG")
                self.file = filedialog.askopenfilename()
            imagefile = Image.open(r'{}'.format(self.file))
            imagefile = imagefile.convert('RGB')
            imagefile.save(r'C:/Users/az200/Desktop/NEA/main/main.jpg')


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text='Face Blurring Tool', fg='#584689', font=TITLE_FONT)
        title.place(anchor='c', relx=0.5, rely=0.2)

        button_video = tk.Button(self, text='Video Blurring', fg='#584689', font=SUBTITLE_FONT,
                                 command=lambda: controller.show_frame(PageVideo))
        button_video.place(anchor='c', relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)

        button_photo = tk.Button(self, text='Photo Blurring', fg='#584689', font=SUBTITLE_FONT,
                                 command=lambda: controller.show_frame(PagePhoto))
        button_photo.place(anchor='c', relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)

        camerapath = Image.open('camera.png')
        cameraimage = ImageTk.PhotoImage(camerapath)
        camera = tk.Label(self, image=cameraimage)
        camera.photo = cameraimage
        camera.place(anchor='c', relx=0.75, rely=0.5)

        videopath = Image.open('video.png')
        videoimage = ImageTk.PhotoImage(videopath)
        video = tk.Label(self, image=videoimage)
        video.photo = videoimage
        video.place(anchor='c', relx=0.25, rely=0.5)


class PageVideo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text='File Selection for Video', fg='#584689', font=TITLE_FONT_2)
        header.place(anchor='c', relx=0.5, rely=0.2)

        button_back = tk.Button(self, text='Back to Main Menu', fg='#584689', font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor='c', relx=0.5, rely=0.05, relwidth=0.2, relheight=0.05)

        button_selectvideo = tk.Button(self, text='Upload Video', fg='#584689', font=SUBTITLE_FONT,
                                       command=lambda:  BlurringTool.main_file(parent, 'video'))
        button_selectvideo.place(anchor='c', relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)

        button_selectface = tk.Button(self, text='Upload Face to Avoid', fg='#584689', font=SUBTITLE_FONT,
                                      command=lambda:  BlurringTool.avoid_file(parent))
        button_selectface.place(anchor='c', relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)

        explanation = tk.Label(self, text='(OPTIONAL) Upload 5 images of each face that\n should be avoided in the blurring process,' 
                                          '\n One frontal view and each side of\n 3/4 view and profile as shown above', font=BODY_FONT)
        explanation.place(anchor='c', relx=0.75, rely=0.9)



        avoidfacepath = Image.open('faceavoid.png')
        avoidfaceimage = ImageTk.PhotoImage(avoidfacepath)
        avoidface = tk.Label(self, image=avoidfaceimage)
        avoidface.photo = avoidfaceimage
        avoidface.place(anchor='c', relx=0.75, rely=0.5)

        videofilepath = Image.open('videofile.png')
        videofileimage = ImageTk.PhotoImage(videofilepath)
        videofile = tk.Label(self, image=videofileimage)
        videofile.photo = videofileimage
        videofile.place(anchor='c', relx=0.25, rely=0.5)


class PagePhoto(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text='File Selection for Photographs', fg='#584689', font=TITLE_FONT_2)
        header.place(anchor='c', relx=0.5, rely=0.2)

        button_back = tk.Button(self, text='Back to Main Menu', fg='#584689', font=BODY_FONT,
                                command=lambda: controller.show_frame(MainMenu))
        button_back.place(anchor='c', relx=0.5, rely=0.05, relwidth=0.2, relheight=0.05)

        button_selectphoto = tk.Button(self, text='Upload Photograph', fg='#584689', font=SUBTITLE_FONT,
                                       command=lambda: BlurringTool.main_file(parent, 'photo'))
        button_selectphoto.place(anchor='c', relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)

        button_selectface = tk.Button(self, text='Upload Face to Avoid', fg='#584689', font=SUBTITLE_FONT,
                                      command=lambda: BlurringTool.avoid_file(parent))
        button_selectface.place(anchor='c', relx=0.75, rely=0.75, relwidth=0.4, relheight=0.1)

        explanation = tk.Label(self, text='(OPTIONAL) Upload 5 images of each face that\n should be avoided in the blurring process,' 
                                          '\n One frontal view and each side of\n 3/4 view and profile as shown above', font=BODY_FONT)
        explanation.place(anchor='c', relx=0.75, rely=0.9)

        button_done = tk.Button(self, text='DONE', fg='#584689', font=BODY_FONT,
                                command=lambda: facelocatePhoto() )
        button_done.place(anchor='c', relx=0.5, rely=0.95, relwidth=0.2, relheight=0.05)

        avoidfacepath = Image.open('faceavoid.png')
        avoidfaceimage = ImageTk.PhotoImage(avoidfacepath)
        avoidface = tk.Label(self, image=avoidfaceimage)
        avoidface.photo = avoidfaceimage
        avoidface.place(anchor='c', relx=0.75, rely=0.5)

        photofilepath = Image.open('photofile.png')
        photofileimage = ImageTk.PhotoImage(photofilepath)
        photofile = tk.Label(self, image=photofileimage)
        photofile.photo = photofileimage
        photofile.place(anchor='c', relx=0.25, rely=0.5)

gui = BlurringTool()
gui.geometry('1280x720')
gui.mainloop()