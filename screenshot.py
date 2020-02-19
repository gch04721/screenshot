from UI import mainWindow

class screenshot():
    def __init__(self):
        # left/top point
        self.x1=0
        self.y1=0

        # right/bottom point
        self.x2=0
        self.y2=0

        self.width=0
        self.height=0

        self.mainUI = mainWindow()

    def __main__(self):
        self.mainUI.mainloop()

mainClass = screenshot()

if __name__ == '__main__':
    mainClass.__main__()