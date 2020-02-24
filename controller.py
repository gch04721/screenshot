from pynput import mouse

class Controller():
    def __init__(self):
        pass

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
        pass

    def listenerJoin(self):
        with mouse.Listener(on_click=self.on_click, on_move=self.on_move) as listener:
            listener.join()