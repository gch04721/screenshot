from pynput import mouse
import tkinter as tk
from PIL import ImageGrab

class MouseControl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.button_pressed = False
        self.x1 =0
        self.x2 =0
        self.y1 =0
        self.y2 =0

        # tkinter 환경설정
        # 투명 배경을 이용해 사용자가 범위를 지정하도록 설정
        self.title('test')
        self.overrideredirect(True)
        self.lift()
        canvas = tk.Canvas(self, width =1920, height = 1080, bg = 'white')
        canvas.pack()
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", "white")
        
        
    def on_move(self,x, y):
        #@print(x,y)
        pass
    
    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            self.button_pressed = pressed

            # 현재 클릭 드래그로 화면 지정하게 사용중
            # 키보드 인풋을 이용하여 범위를 지정하도록 변경
            if pressed:
                self.x1 = x
                self.y1 = y
                print(x, y)
            if not pressed:
                self.x2 = x
                self.y2 = y
                print(x,y)
                img_name = 'capture.png'
                
                # 이미지를 저장 후 불러와서 띄우려고 하는중 
                area = (self.x1, self.y1, self.x1 + abs(self.x1 - self.x2), self.y1 + abs(self.y1 - self.y2))
                print(area)
                img = ImageGrab.grab(bbox = area)
                # img = img.crop(box = (self.x1, self.y1, self.x2, self.y2))
                img.save(img_name)
                self.geometry(str(abs(self.x1 - self.x2)) + 'x' + str(abs(self.y1-self.y2)) + '+' + str(self.x1) + '+' + str(self.y1))
                canvas= tk.Canvas(self, width = abs(self.x1 - self.x2), height = abs(self.y1 - self.y2))
                canvas.pack()
                image = tk.PhotoImage(file = img_name)           
                canvas.create_image(image.width(), image.height(), image=image)
        if button == mouse.Button.right:
            self.quit()
            return False

root = MouseControl()

def on_move(x, y):
    root.on_move(x, y)

def on_click(x,y, button, pressed):
    root.on_click(x, y, button, pressed)

listener = mouse.Listener(on_move = on_move, on_click = on_click)
listener.start()

root.mainloop()