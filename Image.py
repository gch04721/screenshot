from PIL import ImageGrab, ImageTk
import os

class ImageControl():
    def __init__(self):
        self.image=None
        self.result=None

    def capture(self):
        self.image = ImageGrab.grab()
        return ImageTk.PhotoImage(self.image)
    
    def drawRect(self, x, y, width, height):
        pass