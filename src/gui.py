import tkinter
from tkinter import filedialog
from src.config import GLOBAL_CONFIG

PRE_TEXT = '选择的文件名为：'


class Application(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.target_lb_string = tkinter.StringVar()
        self.target_lb_string.set("尚未选择")
        self.master.title('烟雾识别系统')
        self.pack()
        self.__createWidgets__()

    def __createWidgets__(self):
        self.helloLabel = tkinter.Label(self, text=(
            '请选择视频文件 %s 或图片 %s ' % (GLOBAL_CONFIG.support_videos, GLOBAL_CONFIG.support_pics)))
        self.helloLabel.pack()

        self.target_lb = tkinter.Label(self, textvariable=self.target_lb_string)
        self.target_lb.pack()
        self.file_button = tkinter.Button(self, text='选择视频',command=self.__get_target__)
        self.file_button.pack()
        self.start_button = tkinter.Button(self, text="开始识别", command=self.__start_recg__)
        self.start_button.pack()
        self.quitButton = tkinter.Button(self, text='退出', command=self.quit)
        self.quitButton.pack()

    def __get_target__(self):
        dir = filedialog.askopenfilename()
        self.target_dir = dir
        dirs = str.split(dir, '/')
        self.target_name = dirs[len(dirs) - 1]
        self.target_lb_string.set(PRE_TEXT+self.target_name)

    def __start_recg__(self):
        pass

