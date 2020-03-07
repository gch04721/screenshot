from UI.main import mainWindow

class ACapture():
    def __init__(self):
        self.mainUI = mainWindow()

    def __main__(self):
        self.mainUI.mainloop()
        

if __name__ == '__main__':
    mainClass = ACapture()

    mainClass.__main__()