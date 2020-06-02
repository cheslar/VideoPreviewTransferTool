import tkinter
from tkinter import filedialog
from tkinter import *
import os
import cv2
import PIL.Image, PIL.ImageTk
from shutil import copy2
import sys
from pathlib import Path


class Content:
    input = ""
    i = 0
    input_files = []
    num_input_files = 0
    output = "/Users/rchesla/Desktop/ClientFolders"
    output_folders = []
    srcnum = 0

class App:
    def __init__(self, window, window_title,video_source=0):
        self.window = window
        self.window.title(Content.input_files[Content.i])
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        def UploadAction():
            directory = tkinter.filedialog.askdirectory()
        def Apply(event=None):
            #src = "" + Content.input + '/' + Content.input_files[Content.i] + ""
            src = str(Content.input_files[Content.i])
            dst = "" + Content.output + '/' + self.variable.get() + ""
            copy2(src, dst)
            for x in range(len(Content.output_folders)):
                # print(dst, " vs ", Content.output_folders[x])
                if Content.output_folders[x] in dst:
                    Content.srcnum = x
            os.rename(str(Content.input_files[Content.i]), str(Content.input_files[Content.i]) + "(transferred)")

        def Next(event=None):
            self.window.destroy()
            Content.i += 1
            if (Content.i < Content.num_input_files):
                #App(tkinter.Tk(), "Tkinter and OpenCV", Content.input + '/' + Content.input_files[Content.i])
                App(tkinter.Tk(), "Tkinter and OpenCV", str(Content.input_files[Content.i]))
            else:
                sys.exit()

        #canvas = tkinter.Canvas(background="white")

        self.variable = tkinter.StringVar()
        self.variable.set(Content.output_folders[Content.srcnum])
        self.opt = tkinter.OptionMenu(self.window, self.variable, *Content.output_folders)
        self.opt.config(width=40)
        self.opt.place(relx=0.84, rely=0.05, anchor=CENTER)


        self.btn_apply = tkinter.Button(text='Apply', command=Apply)
        self.btn_apply.config(height=5, width= 20)
        self.btn_apply.place(relx=0.77, rely=0.94, anchor=CENTER)

        self.btn_next = tkinter.Button(text='Next', command=Next)
        self.btn_next.config(height=5, width= 20)
        self.btn_next.place(relx=0.92, rely=0.94, anchor=CENTER)

        self.delay = 15
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class Source:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Select Source')
        self.window.geometry('400x400')

        def getSource():
            Content.input = tkinter.filedialog.askdirectory()
            self.window.destroy()
        # def getDest():
        #     Content.output = tkinter.filedialog.askdirectory()
        #     self.window.destroy()
        self.btn_source = tkinter.Button(text='Select Source Drive', command=getSource)
        self.btn_source.place(relx=0.5, rely=0.45, anchor=CENTER)
        # self.btn_dest = tkinter.Button(text='Select Destination', command=getDest)
        # self.btn_dest.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.window.mainloop()

Source()
# Content.input_files = os.listdir(Content.input)
Content.input_files = sorted(Path(Content.input).iterdir(), key=os.path.getmtime)
Content.num_input_files = len(Content.input_files) #- 1
Content.output_folders = os.listdir(Content.output)
#print(Content.input_files[0])
App(tkinter.Tk(), "Tkinter and OpenCV", str(Content.input_files[Content.i]))
