import logging as log

import demjson

CONFIG_FILE_DIR = './data/config/config.json'


class Config(object):
    config = {}

    def __init__(self):
        self.config = demjson.decode_file(CONFIG_FILE_DIR)
        self.support_videos = self.config["supportVideoName"]
        self.support_pics = self.config["supportPicName"]
        self.windows_width = self.config["windowsWidth"]
        self.windows_height = self.config["windowsHeight"]
        self.hog_width = self.config["hogWidth"]
        self.hog_height = self.config["hogHeight"]
        self.slide_step = self.config["slideStep"]
        self.frame_interval = self.config["frameInterval"]

    def __get_format_by_dir__(self, dir):
        paths = dir.split('.')
        return paths[len(paths) - 1]

    def is_support_pics(self, dir):
        format_name = self.__get_format_by_dir__(dir)
        log.debug('get format_name: %s' % format_name)
        if format_name in self.support_pics:
            return True
        return False

    def is_support_videos(self, dir):
        format_name = self.__get_format_by_dir__(dir)
        if format_name in self.support_videos:
            return True
        return False


GLOBAL_CONFIG = Config()
