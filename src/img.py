import logging as log

import cv2 as cv

HOG_IMAGE_WIDTH = 256
HOG_IMAGE_HEIGHT = 256


class Image(object):
    """Image: Image instance is a frame of video or a image

    An instance represents a frame or an image that can be used to train a model or to identify.
    """

    def __init__(self, target, name):
        src = None
        self.name = name

        if isinstance(target, str):
            # if target is img dir
            src = cv.imread(target)
        else:
            # if target is img
            src = target

        log.debug("target = %s, src = %s" % (target, src))

        # resize and save to self.image
        self.image = cv.resize(src=src,
                               dsize=(HOG_IMAGE_WIDTH, HOG_IMAGE_HEIGHT),
                               interpolation=cv.INTER_AREA)

    def get_hog_feature(self):
        # get hog_feature and save to self.descriptor

        hog = cv.HOGDescriptor((HOG_IMAGE_WIDTH, HOG_IMAGE_HEIGHT), (16, 16),
                               (8, 8), (8, 8), 9)
        self.descriptor = hog.compute(self.image)

        if self.descriptor is None:
            self.descriptor = []
        else:
            self.descriptor = self.descriptor.ravel()

    def show(self):
        cv.imshow("target_name", self.image)
        cv.waitKey(0)
        cv.destroyWindow()
