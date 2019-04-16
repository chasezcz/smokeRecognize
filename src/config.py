import demjson

CONFIG_FILE_DIR = './config/config.json'


class Config(object):
    config = {}

    def __init__(self):
        self.config = demjson.decode_file(CONFIG_FILE_DIR)
        self.support_videos = self.config["supportVideoName"]
        self.support_pics = self.config["supportPicName"]

GLOBAL_CONFIG = Config()
