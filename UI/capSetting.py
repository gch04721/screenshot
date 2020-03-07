import tkinter as tk
import tkinter.filedialog as fileDialog

class CaptureSetting(tk.Toplevel):
    def __init__(self, parent, x0, y0):
        tk.Toplevel.__init__(self, parent)
        self.title('setting')
        self.wm_attributes("-topmost", True)
        self.geometry('{}x{}+{}+{}'.format(320,370,x0,y0))

        self.parent = parent

        # 파일 저장 위치 관련 UI
        self.loc_label = tk.Label(self, text='파일을 저장할 위치')
        self.loc_frame = tk.Frame(self)
        self.loc_entry = tk.Entry(self.loc_frame, width=30, bd=3)
        self.loc_btn = tk.Button(self.loc_frame, text="찾기...", \
            command=lambda: self.command_find())

        self.loc_entry.grid(row=0, column=0, padx=2, pady=5)
        self.loc_btn.grid(row=0, column=1, padx=2, pady=5)
        self.loc_label.pack()
        self.loc_frame.pack()
        

        # 파일 이름 지정 관련 UI
        self.name_label = tk.Label(self, text='파일 이름')
        self.name_frame = tk.Frame(self)
        self.name_entry = tk.Entry(self.name_frame, width=25, bd=3)

        self.name_entry.grid(row=0, column=0, padx=2, pady=5)
        self.name_label.pack()
        self.name_frame.pack()

        # 모드 선택 관련 UI
        self.mode_label = tk.Label(self, text='모드 선택')
        self.mode_frame = tk.Frame(self)
        self.radioVar = tk.IntVar()
        self.auto_radio = tk.Radiobutton(self.mode_frame, text="자동", value=1,\
            variable=self.radioVar, command= lambda:self.command_auto())
        # self.semi_radio = tk.Radiobutton(self.mode_frame, text='반자동', value=2,\
        #     variable=self.radioVar, command= lambda:self.command_auto(), state= tk.DISABLED)
        self.manual_radio = tk.Radiobutton(self.mode_frame, text='수동', value=3,\
            variable=self.radioVar, command= lambda:self.command_manual())

        self.auto_radio.grid(row=5, column=0, padx=2, pady=5)
        #self.semi_radio.grid(row=5, column=1, padx=2, pady=5)
        self.manual_radio.grid(row=5, column=2, padx=2, pady=5)
        self.mode_label.pack()
        self.mode_frame.pack()

        # 영상 길이, 캡처 간격 세팅
        self.videoLen_frame = tk.Frame(self)
        vcmd = (self.register(self.validate),\
               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.videoLength_Min_entry = tk.Entry(self.videoLen_frame, width=10, bd=3, validate = 'key', validatecommand = vcmd)
        self.videoLength_Sec_entry = tk.Entry(self.videoLen_frame, width=15, bd=3, validate = 'key', validatecommand = vcmd)

        # self.CaptureInterval_entry = tk.Entry(self, width=25, bd=3, validate = 'key', validatecommand = vcmd)

        self.label_min = tk.Label(self.videoLen_frame, text='분')
        self.label_sec = tk.Label(self.videoLen_frame, text='초')
        self.label1 = tk.Label(self, text='영상 길이')
        # self.label2 = tk.Label(self, text='캡처 간격')

        self.videoLength_Min_entry.grid(row=0, column=0, padx=2, pady=5)
        self.label_min.grid(row=0, column=1, padx=2, pady=5)
        self.videoLength_Sec_entry.grid(row=0, column=2, padx=2, pady=5)
        self.label_sec.grid(row=0, column=3, padx=2,pady=5)

        self.label1.pack()
        self.videoLen_frame.pack()
        # self.label2.pack()
        # self.CaptureInterval_entry.pack()
        
        # 시작, 종료 버튼
        self.btn_frame = tk.Frame(self)
        self.btn_end = tk.Button(self.btn_frame, text="종료",\
            command=lambda: self.command_end2())
        self.btn_start = tk.Button(self.btn_frame, text='시작',\
            command=lambda: self.command_end())

        self.btn_start.grid(row=0, column=0, padx=2, pady=5)
        self.btn_end.grid(row=0, column=1, padx=10, pady=5)
        self.btn_frame.pack()

        self.videoLength_Min_entry['state'] = tk.DISABLED
        self.videoLength_Sec_entry['state'] = tk.DISABLED
        # self.CaptureInterval_entry['state'] = tk.DISABLED

    def command_find(self):
        self.fileLoc = fileDialog.askdirectory()
        
        self.loc_entry.delete(0, 'end')
        self.loc_entry.insert(0, self.fileLoc)

    def command_manual(self):
        self.videoLength_Min_entry['state'] = tk.DISABLED
        self.videoLength_Sec_entry['state'] = tk.DISABLED
        # self.CaptureInterval_entry['state'] = tk.DISABLED

    def command_auto(self):
        self.videoLength_Min_entry['state'] = tk.NORMAL
        self.videoLength_Sec_entry['state'] = tk.NORMAL
        # self.CaptureInterval_entry['state'] = tk.NORMAL

    def command_end(self):
        modeNum =self.radioVar.get()

        self.fileName = self.name_entry.get()
        if modeNum == 1 or modeNum == 2:

            video_min = self.videoLength_Min_entry.get()
            video_sec = self.videoLength_Sec_entry.get()

            video_min = float(video_min)
            video_sec = float(video_sec)
            self.videoLength = video_min * 60.0 + video_sec

            # self.CaptureInterval = self.CaptureInterval_entry.get()
            # self.CaptureInterval = float(self.CaptureInterval)
        elif modeNum == 3:
            self.videoLength= 0
            # self.CaptureInterval = 0
        
        self.parent.capture_start(fileLoc=self.fileLoc, fileName=self.fileName, videoLen=self.videoLength, modeNum=modeNum)
        
        self.destroy()
    
    def command_end2(self):
        self.destroy()

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        elif value_if_allowed == '':
            return True
        else:
            return False