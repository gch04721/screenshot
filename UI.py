import tkinter as tk
import pyautogui

from Mouse import MouseListener
from Image import ImageControl

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('test')

        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "white")
        self.frame1 = tk.Frame(self)
        self.frame1.pack()

        # 모니터 크기
        self.width, self.height = pyautogui.size()

        # 버튼 배치
        Btn_sz = tk.Button(self.frame1, text="크기조절", width=10, overrelief='sunken',\
            command=lambda: self.command_sz())
        Btn_start = tk.Button(self.frame1, text="자동캡처", width=10, overrelief='sunken',\
            command=lambda: self.command_start())
        Btn_cut = tk.Button(self.frame1, text="캡처", width =10, overrelief='sunken',\
            command=lambda: self.command_cut())

        Btn_sz.grid(row=0, column=0)
        Btn_cut.grid(row=0, column=1)
        Btn_start.grid(row=0, column=2)
    
    def command_sz(self):
        self.frame1.pack_forget()
        self.hide()

        # 전체화면 캡쳐 후 영역 선택을 위해 뿌려줌
        imgCtrl = ImageControl()
        img = imgCtrl.capture()

        self.resize(x=0, y=0, width=self.width, height=self.height)
        self.overrideredirect(True)
        frame2 = tk.Frame(self)
        frame2.pack()

        label = tk.Label(frame2, width=self.width, height=self.height, bg='white', image=img)
        label.image= img
        label.pack()
        self.show()

        mouse = MouseListener()
        mouse.listenerJoin()

    def command_start(self):
        pass

    def command_cut(self):
        pass

    def hide(self):
        self.withdraw()
    
    def show(self):
        self.update()
        self.deiconify()

    def resize(self, x, y, width, height):
        self.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))
