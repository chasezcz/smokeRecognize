from src.config import GLOBAL_CONFIG
import cv2 as cv
import logging as log
from src.img import Image


class Video(object):
    video = None

    def __init__(self, target, name='Init'):
        self.name = name
        try:
            if isinstance(target, str):
                # if target is video dir
                self.video = cv.VideoCapture(target)
            else:
                # if target is video
                self.video = target
        except Exception as err:
            log.error("load video failed, details: %s" % err)

    def get_next_frame(self):

        frame_index = 0
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                log.error("Can't receive frame (stream end?). Exiting ...")
                break
            if frame_index % GLOBAL_CONFIG.frame_interval == 0:
                yield Image(frame)
            frame_index = frame_index + 1
