import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from src.config import GLOBAL_CONFIG
import logging

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

        logging.info("init Application")
        self.window = tk.Tk()
        self.window.title('烟雾识别系统')
        # set windows size
        self.window.geometry(
            "%dx%d" %
            (GLOBAL_CONFIG.windows_width, GLOBAL_CONFIG.windows_height))

        self.target_dir = tk.StringVar()

        self.__create_predict_frame__()
        self.__create_train_frame__()

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

        self.output = tk.Text(self.window)

        # default show train model
        self.__train_model__()

    def __get_file__(self):
        file_dir = filedialog.askopenfile()
        logging.info("get file dir : %s" % (file_dir))

        self.target_dir.set(file_dir)

    def __get_folder__(self):
        folder_dir = filedialog.askdirectory()
        logging.info("get folder dir : %s" % (folder_dir))
        self.target_dir.set(folder_dir)

    def __start_train__(self):
        pass

    def __start_recg__(self):
        """
        __start_recg__ [summary]

        [description]
        """
        pass

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
            self.predict_frame, text='选择视频',
            command=self.__get_file__).pack(side=tk.LEFT)
        self.start_button = tk.Button(
            self.predict_frame, text="开始识别",
            command=self.__start_recg__).pack(side=tk.RIGHT)

    def __train_model__(self):
        self.model = TRAIN_MODEL
        self.predict_frame.pack_forget()
        self.target_dir.set("尚未选择")
        self.train_frame.pack()

    def __predict_model__(self):
        self.model = PREDICT_MODEL
        self.train_frame.pack_forget()
        self.target_dir.set("尚未选择")
        self.predict_frame.pack()

    def __about_me__(self):
        messagebox.showinfo(
            title='关于',
            message='作者：张成泽\r\n'
            'github地址：https://github.com/woshichaoren000/smokeRecognize')

    def start(self):
        self.window.mainloop()
