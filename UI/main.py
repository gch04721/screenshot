import tkinter as tk
import pyautogui

from Image import ImageControl

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('test')
        # 프로그램을 항상 위에 유지하기 위한 설정
        self.wm_attributes("-topmost", True)

        # 특정색을 투명하게 변경
        self.wm_attributes("-transparentcolor", "red")
        
        # 초기화면
        self.frame_btn = tk.Frame(self)
        self.frame_btn.pack(side='top', fill='x')
        self.frame1 = tk.Frame(self)
        self.frame1.pack(expand=True, fill='both')

        # 관심영역 캡쳐 후 뿌려질 화면
        self.frame2 = tk.Frame(self)

        # 모니터 크기 저장
        self.width, self.height = pyautogui.size() 

        # 버튼 배치
        Btn_sz = tk.Button(self.frame_btn, text="관심영역 지정", width=10,\
            command=lambda: self.command_sz())
        Btn_start = tk.Button(self.frame_btn, text="캡처 시작", \
            command=lambda: self.command_start())
        Btn_end = tk.Button(self.frame_btn, text='중단', \
            command=lambda: self.command_end())
        Btn_stop = tk.Button(self.frame_btn, text='일시정지', \
            command=lambda: self.command_stop())

        Btn_sz.grid(row=0, column=0, padx=3)
        Btn_start.grid(row=0, column=1, padx=3)
        Btn_end.grid(row=0, column=2, padx=3)
        Btn_stop.grid(row=0, column=3, padx=3)

        # 빈 화면 뿌리기
        canvas = tk.Canvas(self.frame1, bg='red')
        canvas.pack(expand=True, fill='both')

    def command_sz(self):
        # frame교체
        self.frame1.pack_forget()
        self.frame_btn.pack_forget()
        # 캡쳐하는 동안 프로그램 창을 숨겨둠
        self.__hide()

        # 전체화면 캡쳐
        imgCtrl = ImageControl()
        self.img = imgCtrl.capture()

        # 전체화면으로 캡쳐한 화면을 보여줌
        self.__setGeo(x=0, y=0, width=self.width, height=self.height)
        self.overrideredirect(True)
        self.frame2.pack(fill='both', expand=True)

        # 이미지 표시를 위한 라벨 설정
        #self.label = tk.Label(self.frame2, width=self.width, height=self.height, bg='red', image=img)
        self.img_canvas = tk.Canvas(self.frame2, width=self.width, height=self.height, bd=0)
        self.img_canvas.create_image((0,0), image=self.img, anchor='nw')
        self.img_canvas.bind("<Button-1>", self.__LbtnClick)
        self.img_canvas.bind("<ButtonRelease-1>", self.__LbtnRelease)
        self.img_canvas.bind("<B1-Motion>", self.__LbtnMove)
        self.rect = None
        self.img_canvas.pack(fill='both', expand=True)

        # 프로그램 다시 표시
        self.__show()
    
    # 마우스 핸들러
    def __LbtnClick(self, event):
        self.x0 = event.x_root
        self.y0 = event.y_root
        print(self.x0, self.y0)

    def __LbtnRelease(self, event):
        newWidth = abs(self.x0 - event.x_root)
        newHeight = abs(self.y0 - event.y_root)
        
        if newWidth > 100 and newHeight > 100:
            print(self.x0, self.y0, newWidth, newHeight)
            self.overrideredirect(True)

            self.frame2.pack_forget()
            self.frame_btn.pack(side='top', fill='x')
            self.frame1.pack(fill='both', expand=True)
            
            self.x0 -= 9
            if self.x0 <0:
                self.x0 = 0
            self.y0 -= (self.frame_btn.winfo_height() * 2 + 3)
            if self.y0 < 0:
                self.y0 = 0

            newHeight += (self.frame_btn.winfo_height())

            self.__setGeo(self.x0, self.y0, newWidth, newHeight)
            self.overrideredirect(False)
    
    def __LbtnMove(self, event):
        if self.rect:
            self.img_canvas.delete(self.rect)
        self.rect = self.img_canvas.create_rectangle(self.x0, self.y0, event.x, event.y, fill='blue', stipple='gray50')


    def command_start(self):
        pass

    def command_end(self):
        pass

    def command_stop(self):
        pass


    def __hide(self):
        self.withdraw()
    
    def __show(self):
        self.update()
        self.deiconify()

    def __setGeo(self, x, y, width, height):
        geoStr = "{}x{}+{}+{}".format(width, height, x, y)
        print(geoStr)
        self.wm_geometry(geoStr)
    def resize(self, x, y, width, height):
        pass
