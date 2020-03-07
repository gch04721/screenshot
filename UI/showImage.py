import tkinter as tk

class ShowImage(tk.Toplevel):
    def __init__(self, parent=None, x0=0, y0=0):
        tk.Toplevel.__init__(self, parent)
        self.title('미리보기')
        self.wm_attributes('-topmost', True)

        self.label = tk.Label(self)
        self.label.pack(fill='both', expand=True)

        self.geometry('{}x{}+{}+{}'.format(310, 310, x0, y0))

        self.imgNum =0
        self.maxImgNum=0
        self.parent =parent

    def setImage(self, image):
        self.label.configure(image= image)
        self.label.image= image

    def choice(self, imageControl):
        width = imageControl.fullWidth
        height = int(imageControl.fullHeight / imageControl.imgNum)

        self.maxImgNum = imageControl.imgNum -1

        self.geometry('{}x{}+{}+{}'.format(width, height, 0, 0))
        self.frame1= tk.Frame(self)
        self.btn_next = tk.Button(self.frame1, text='다음', command=lambda:self.command_next())
        self.btn_prev = tk.Button(self.frame1, text='이전', command=lambda:self.command_prev())
        self.btn_del = tk.Button(self.frame1, text='삭제', command=lambda:self.command_del())
        self.btn_end = tk.Button(self.frame1, text='완료', command=lambda:self.command_end())

        self.btn_next.grid(row=0, column=0, padx=5)
        self.btn_prev.grid(row=0, column=1, padx=5)
        self.btn_del.grid(row=0, column=2, padx=5)
        self.btn_end.grid(row=0, column=3, padx=5)

        self.label.pack_forget()

        self.frame1.pack()
        self.label.pack()

        self.imgCtrl = imageControl

        self.setImage(self.imgCtrl.getImage(0))

    def command_next(self):
        self.imgNum +=1
        if self.imgNum > self.maxImgNum:
            self.imgNum = self.maxImgNum
        self.setImage(self.imgCtrl.getImage(self.imgNum))
        
    def command_prev(self):
        self.imgNum -= 1
        if self.imgNum<0:
            self.imgNum = 0
        self.setImage(self.imgCtrl.getImage(self.imgNum))

    def command_del(self):
        del self.imgCtrl.result[self.imgNum]
        self.maxImgNum -= 1
        self.imgNum = min(self.maxImgNum, self.imgNum)
        self.setImage(self.imgCtrl.getImage(self.imgNum))
    
    def command_end(self):
        self.parent.command_end()
        self.parent.threadStopped = False