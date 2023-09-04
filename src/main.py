import cv2

from src.OCR7Seg import OCR7Seg 
from src.GUI import GUI
from src.excel import Excel

class App():
    def __init__(self,root,filepath,delay) -> None:
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.root = root
        self.filepath = filepath
        self.delay = delay
        self.capture = GUI(self.root)
        self.show_frames()
        self.timer()

    # Initialize capture for Video / Image
    def initialize(self):
        if self.filepath: img = cv2.imread(self.filepath)
        else: ret,img = self.cap.read()
    
        return img
    
    def show_frames(self):
        img = self.initialize()
        copy, self.digits = OCR7Seg(img)
        self.capture.processImg(copy)
        self.root.after(1,self.show_frames)

    def timer(self):
        Excel(self.digits)
        print("Excel Saved")
        self.root.after(self.delay*1000,self.timer)


      
        
            
