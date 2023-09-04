import os
from tkinter import *

from src.main import App

####################################################################################################

filepath = "WIN_20230718_10_17_07_Pro.jpg"
delay = 30      # In seconds

####################################################################################################

if __name__ == "__main__":
    root = Tk()
    fpath = os.path.join(os.path.dirname(__file__),"images",filepath)
    App(root,fpath,delay)
    root.mainloop()