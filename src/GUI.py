import os 
import cv2
import time
from tkinter import *
from PIL import Image as PilImg, ImageTk

class GUI():
    def __init__(self,root):
        self.root = root
        self.win_config()
        self.widgets()

    def win_config(self):
        self.root.title('OCR 7 Segment Reader')
        self.Hscreen = self.root.winfo_screenheight()
        self.Wscreen = self.root.winfo_screenwidth()
        self.root.geometry(f"{int(self.Wscreen*0.7)}x{int(self.Hscreen*0.80)}+30+10")
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self):
        self.capture = Label(self.frame, relief=SUNKEN)
        self.capture.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky=NS+EW)

        self.save = Button(self.frame, text="Save Image", width=10, font=('Calibri',15), command=lambda: self.saveImg())
        self.save.grid(row=1,column=0, padx=5, sticky=E)

        self.Button = Button(self.frame, text='Close', width=10, font=('Calibri',15), command=lambda: self.close())
        self.Button.grid(row=1, column=1, padx=5, sticky=E)

    # Main Program #
    ####################################################################################################
    def processImg(self,img):
        self.img=img
        img = PilImg.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        img = img.resize((int(self.Wscreen*0.65),int(self.Hscreen*0.65)))
        imgtk = ImageTk.PhotoImage(image = img)
        self.capture.imgtk = imgtk
        self.capture.config(image = imgtk)

    def saveImg(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"OCR_Images")
        fname = time.strftime("%Y%m%d_%H%M%S") + ".png"
        cv2.imwrite(os.path.join(path,fname),self.img)

    def close(self):
        self.root.destroy()
        self.root.quit()

