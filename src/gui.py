import logging as log
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import PIL.Image, PIL.ImageTk

import cv2 as cv

from src.config import GLOBAL_CONFIG
from src.img import Image as Img
from src.svm import Svm
from src.svm import CANVAS_IMG, CANVAS_IMG_PHOTO

PREDICT_MODEL = 0
TRAIN_MODEL = 1


class Application(object):
    """
    Application 程序的桌面控件实现

    """

    def __init__(self, master=None):
        """
        __init__: just a init func

        in this function, it will create window and frame which the app need.
        """

        log.info("init Application")
        self.svm = Svm()
        self.window = tk.Tk()
        self.window.title('烟雾识别系统')
        # set windows size
        self.window.geometry(
            "%dx%d" %
            (GLOBAL_CONFIG.windows_width, GLOBAL_CONFIG.windows_height))

        self.target_dir = tk.StringVar()

        self.__create_predict_frame__()
        self.__create_train_frame__()

        # set menu
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        run_model = tk.Menu(menubar)
        run_model.add_command(label='模型训练', command=self.__train_model__)
        run_model.add_separator()
        run_model.add_command(label='目标预测', command=self.__predict_model__)

        menubar.add_cascade(label='模式', menu=run_model)

        about_me = tk.Menu(menubar)
        about_me.add_command(label='关于我', command=self.__about_me__)
        about_me.add_separator()
        about_me.add_command(label='退出', command=self.window.quit)
        menubar.add_cascade(label='关于', menu=about_me)

        # Redirect output to the GUI
        # self.output = scrolledtext.ScrolledText(
        #     self.window).pack(side=tk.BOTTOM)
        # output_lb = tk.Label(self.window, text='实时日志').pack(side=tk.BOTTOM)
        # redir = RedirectText(self.output)
        # sys.stderr = redir

        # default show train model
        self.__predict_model__()

    def __get_file__(self):
        file_dir = filedialog.askopenfilename()

        log.info("get file dir : %s" % (file_dir))
        if GLOBAL_CONFIG.is_support_pics(file_dir):
            log.info('get pic')
            self.__show_img__(file_dir)
        elif GLOBAL_CONFIG.is_support_videos(file_dir):
            log.info("get video")
            self.__show_video__(file_dir)
        else:
            messagebox.showerror('error', '文件格式有误，仅支持jpg，png，mp4，avi')
            return
        self.target_dir.set(file_dir)

    def __show_img__(self, dir):
        # TODO: preview image every select image
        img = Img(dir, 'first').get_src()
        # photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
        # self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        # self.canvas.update()
        pass

    def __show_video__(self, dir):
        # TODO: preview video every select video
        pass

    def __get_folder__(self):
        folder_dir = filedialog.askdirectory()
        log.info("get folder dir : %s" % (folder_dir))
        self.target_dir.set(folder_dir)

    def __create_train_frame__(self):
        self.train_frame = tk.Frame(self.window)
        train_lb = tk.Label(self.train_frame, text="训练模式")
        train_lb.pack()

        tip_frame = tk.Frame(self.train_frame)
        tip_lb = tk.Label(tip_frame, text='训练数据集地址：').pack(side=tk.LEFT)
        data_set_lb = tk.Label(
            tip_frame, textvariable=self.target_dir).pack(side=tk.RIGHT)
        tip_frame.pack()

        self.select_train_data_bt = tk.Button(self.train_frame,
                                              text='选择训练数据集',
                                              command=self.__get_folder__)
        self.select_train_data_bt.pack(side=tk.LEFT)
        self.select_train_data_bt = tk.Button(self.train_frame,
                                              text='开始训练',
                                              command=self.__start_train__)
        self.select_train_data_bt.pack(side=tk.RIGHT)

    def __create_predict_frame__(self):
        self.predict_frame = tk.Frame(self.window)
        train_lb = tk.Label(self.predict_frame, text="识别模式")
        train_lb.pack()

        self.helloLabel = tk.Label(self.predict_frame,
                                   text=('请选择视频文件 %s 或图片 %s ' %
                                         (GLOBAL_CONFIG.support_videos,
                                          GLOBAL_CONFIG.support_pics))).pack()

        tip_frame = tk.Frame(self.predict_frame)
        tip_lb = tk.Label(tip_frame, text='目标地址：').pack(side=tk.LEFT)
        target_lb = tk.Label(tip_frame,
                             textvariable=self.target_dir).pack(side=tk.RIGHT)
        tip_frame.pack()
        self.file_button = tk.Button(
            self.predict_frame, text='选择文件',
            command=self.__get_file__).pack(side=tk.LEFT)
        self.start_button = tk.Button(
            self.predict_frame, text="开始识别",
            command=self.__start_recg__).pack(side=tk.RIGHT)
        # to show result
        # CANVAS_IMG = PIL.Image.open('data/img/welcome.gif')
        # CANVAS_IMG_PHOTO = PIL.ImageTk.PhotoImage(CANVAS_IMG)
        # self.canvas = tk.Canvas(self.predict_frame, width=256, height=256)
        # self.canvas.create_image(0, 0, image=CANVAS_IMG_PHOTO, anchor=tk.NW)
        # self.canvas.pack(side=tk.BOTTOM)

    def __train_model__(self):
        log.info("switch to train model")
        self.model = TRAIN_MODEL
        self.predict_frame.pack_forget()
        self.target_dir.set("尚未选择")
        self.train_frame.pack()

    def __predict_model__(self):
        log.info("switch to predict model")
        self.model = PREDICT_MODEL
        self.train_frame.pack_forget()
        self.target_dir.set("尚未选择")
        self.predict_frame.pack()

    def __about_me__(self):
        messagebox.showinfo(
            title='关于',
            message='作者：张成泽\r\n'
            'github地址：https://github.com/woshichaoren000/smokeRecognize')

    def __start_train__(self):
        if len(self.target_dir.get()) < 6:
            messagebox.showinfo(title='错误', message='请先选择数据集')

        config_correct, self.model_dir = self.svm.train(self.target_dir.get())
        if config_correct == False:
            messagebox.showerror(title='错误', message='训练失败，请重新选择数据集，具体错误见日志文件')
        else:
            messagebox.showinfo(title='训练成功',
                                message='训练成功, 模型地址为 %s' % self.model_dir)

    def __start_recg__(self):

        if GLOBAL_CONFIG.is_support_pics(self.target_dir.get()):
            img = self.svm.preidct_pic(self.target_dir.get())
            # self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
            # self.canvas.update()
        elif GLOBAL_CONFIG.is_support_videos(self.target_dir.get()):
            self.svm.preidct_video(self.target_dir.get())

    def start(self):
        self.window.mainloop()


class RedirectText(object):
    def __init__(self, text_ctrl):
        """Constructor"""
        self.output = text_ctrl

    def write(self, string):
        self.output.insert(tk.END, string)

    def flush(self):
        pass
