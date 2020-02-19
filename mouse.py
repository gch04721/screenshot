from pynput import mouse

class MouseListener:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.width=0
        self.height=0

        self.clicked=False

    @staticmethod 
    def on_click(x, y, button, pressed):  
        if button == mouse.Button.left:
            clicked=pressed
            if clicked:
                x1 = x
                y1 = y
                print(x1, y1)
        else:
            return False

    @staticmethod
    def on_move(x, y):
        if clicked:
            print(x,y)

    def listenerJoin(self):
        with mouse.Listener(on_click=self.on_click, on_move=self.on_move) as listener:
            listener.join()