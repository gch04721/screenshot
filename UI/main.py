import tkinter as tk
import pyautogui
import time
from threading import Thread

from Image import ImageControl
from UI.capSetting import CaptureSetting
from UI.showImage import ShowImage

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('acapture')
        # 프로그램을 항상 위에 유지하기 위한 설정
        self.wm_attributes("-topmost", True)

        # 특정색을 투명하게 변경
        self.wm_attributes("-transparentcolor", "red")

        # 관련 변수들
        # 초기화면
        self.frame_btn = tk.Frame(self)
        self.frame1 = tk.Frame(self)

        # 관심영역 캡쳐 후 뿌려질 화면
        self.frame2 = tk.Frame(self)

        # 변수 초기화
        self.initVar()
        
        # 창 왼쪽 위 좌표
        self.x0 = None
        self.y0 = None

        # 모니터 너비, 높이
        self.width, self.height = None, None

        self.initialView()

    def initVar(self):
        # 파일 저장 관련 변수들
        self.fileLoc = None
        self.fileNmae = None
        self.videoLength = None
        self.CaptureInterval =None
        self.modeNum = None

        # ROI 창 너비, 높이
        self.newWidth, self.newHeight = None, None

        # ROI선택 시 보이는 파란 창 관련 변수
        self.rect = None

        self.threadKill = False

    def initialView(self):
        self.frame_btn.pack(side='top', fill='x')
        self.frame1.pack(expand=True, fill='both')

        # 모니터 크기 저장
        self.width, self.height = pyautogui.size() 

        # 버튼 배치
        self.Btn_sz = tk.Button(self.frame_btn, text="관심영역 지정", width=10,\
            command=lambda: self.command_sz())
        self.Btn_start = tk.Button(self.frame_btn, text="캡처 시작", state ='disabled', \
            command=lambda: self.command_start())
        self.Btn_end = tk.Button(self.frame_btn, text='종료', state ='disabled',\
            command=lambda: self.command_end())
        self.Btn_stop = tk.Button(self.frame_btn, text='일시정지', state ='disabled',\
            command=lambda: self.command_stop())

        self.Btn_sz.grid(row=0, column=0, padx=3)
        self.Btn_start.grid(row=0, column=1, padx=3)
        self.Btn_stop.grid(row=0, column=2, padx=3)
        self.Btn_end.grid(row=0, column=3, padx=3)
        
        # 빈 화면 뿌리기
        self.canvas = tk.Canvas(self.frame1, bg='red')
        self.canvas.pack(expand=True, fill='both')

    def selectROIView(self, image):
        # frame교체
        self.frame1.pack_forget()
        self.frame_btn.pack_forget()
        # 캡쳐하는 동안 프로그램 창을 숨겨둠

        self.frame2.pack(fill='both', expand=True)

        # 이미지 표시를 위한 캔버스 설정
        if self.rect:
            self.img_canvas.pack(fill='both', expand=True)
            self.img_canvas.create_image((0,0), image=self.img, anchor='nw')
        else:
            self.img_canvas = tk.Canvas(self.frame2, width=self.width, height=self.height, bd=0)
            self.img_canvas.create_image((0,0), image=self.img, anchor='nw')
            self.img_canvas.bind("<Button-1>", self.__LbtnClick)
            self.img_canvas.bind("<ButtonRelease-1>", self.__LbtnRelease)
            self.img_canvas.bind("<B1-Motion>", self.__LbtnMove)
            self.img_canvas.pack(fill='both', expand=True)

    # 관심영역 지정 버튼 눌렀을 때 
    def command_sz(self):
        self.__hide()

        # 전체화면으로 캡쳐한 화면을 보여줌
        self.__setGeo(x=0, y=0, width=self.width, height=self.height)
        self.overrideredirect(True)

        # 전체화면 캡쳐
        imgCtrl = ImageControl()
        self.img = imgCtrl.capture()

        self.selectROIView(self.img)
        
        # 프로그램 다시 표시
        self.__show()
    
    # 마우스 핸들러
    def __LbtnClick(self, event):
        self.x0 = event.x_root
        self.y0 = event.y_root
        print(self.x0, self.y0)

    def __LbtnRelease(self, event):
        self.newWidth = abs(self.x0 - event.x_root)
        self.newHeight = abs(self.y0 - event.y_root)
        
        if self.newWidth > 100 and self.newHeight > 100:
            self.overrideredirect(True)
            
            self.img_canvas.delete(self.rect)

            self.frame2.pack_forget()
            self.frame_btn.pack(side='top', fill='x')
            self.frame1.pack(fill='both', expand=True)

            # 버튼프레임과 상단표시줄로 위치가 어긋나서 바로잡기 위함.
            if self.x0 < event.x_root:
                x0_geo = self.x0
            else:
                x0_geo = event.x_root
            
            if self.y0 < event.y_root:
                y0_geo = self.y0
            else:
                y0_geo = event.y_root

            x0_geo -= 9
            if x0_geo <0:
                x0_geo = 0
            y0_geo -= (self.frame_btn.winfo_height() * 2 + 3)
            if y0_geo < 0:
                y0_geo = 0

            self.newHeight += (self.frame_btn.winfo_height())
            self.__setGeo(x0_geo, y0_geo, self.newWidth, self.newHeight)
            self.newHeight -= (self.frame_btn.winfo_height())
            self.overrideredirect(False)
            self.Btn_start['state'] = tk.NORMAL
    
    def __LbtnMove(self, event):
        if self.rect:
            self.img_canvas.delete(self.rect)
        self.rect = self.img_canvas.create_rectangle(self.x0, self.y0, event.x, event.y, fill='blue', stipple='gray50')


    def command_start(self):
        # 변수 초기화, 예외처리용
        self.initVar()
        Cap = CaptureSetting(parent=self, x0=self.x0, y0=self.y0)

    def command_end(self):
        # 캡처 종료
        self.threadKill = True
        if self.threadStopped:
            self.showImage.choice(self.imageCapture)

        self.imageCapture.imageSave(fileLoc = self.fileLoc, fileName = self.fileName)
        self.showImage.destroy()
        self.threadKill = False

        self.Btn_stop['state'] = tk.DISABLED
        self.Btn_end['state'] = tk.DISABLED

        self.pause = False
        self.Btn_stop['text'] = '일시정지'

        self.destroy()

    def command_stop(self):
        # 캡처 일시정지, 재개 가능
        self.pause = not self.pause
        if self.pause:
            self.Btn_stop['text'] = '다시시작'
            self.pause_time_start = time.time()
        else:
            self.pause_time = time.time() - self.pause_time_start
            self.Btn_stop['text'] = '일시정지'

    def capture_start(self, fileLoc=None, fileName=None, videoLen=None, modeNum=None):
        self.imageCapture = ImageControl()
        self.fileLoc = fileLoc
        self.fileName = fileName
        self.modeNum = modeNum

        self.showImage = ShowImage(parent=self, x0=self.x0 + self.newWidth, y0=self.y0)
        self.threadStopped = False

        if modeNum == 1:
            # 일시정지 활성화
            self.Btn_stop['state'] = tk.NORMAL
            self.pause = False
            auto = Thread(target=self.autoThread, args= (videoLen,))
            auto.start()
        # elif modeNum == 2:
        #     # 일시정지 활성화
        #     self.Btn_stop['state'] = tk.NORMAL
        #     self.pause = False
        elif modeNum == 3:
            self.frame1.bind('<Key>', self.__Keypressed)
            self.frame1.focus_set()
        else:
            return False
    
    def autoThread(self, videoLen):
        start_total = time.time()
        start= time.time()
        self.pause_time = 0

        while True:
            time.sleep(0.1)
            if self.pause:
                continue
            start += self.pause_time
            start_total += self.pause_time
            self.pause_time = 0
            end = time.time()
            if end - start > 1.0:
                image = self.imageCapture.capture_crop(x0= self.x0, y0=self.y0, width=self.newWidth, height=self.newHeight)
                self.showImage.setImage(image)
                if self.Btn_end['state'] == tk.DISABLED:
                    self.Btn_end['state'] = tk.NORMAL
                start = time.time()
            
            if self.threadKill:
                self.threadStopped = True
                return 

            total_time = time.time() - start_total

            if total_time > videoLen:
                break

        self.showImage.choice(self.imageCapture)

    def __Keypressed(self, event):
        if event.char == 'c':
            image = self.imageCapture.capture_crop(x0= self.x0, y0=self.y0, width=self.newWidth, height=self.newHeight)
            if self.Btn_end['state'] == tk.DISABLED:
                self.Btn_end['state'] = tk.NORMAL

            self.showImage.setImage(image)

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