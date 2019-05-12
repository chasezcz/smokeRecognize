import logging as log

import cv2 as cv
import numpy as np

HOG_IMAGE_WIDTH = 256
HOG_IMAGE_HEIGHT = 256


class Image(object):
    """Image: Image instance is a frame of video or a image

    An instance represents a frame or an image that can be used to train a model or to identify.
    """

    def __init__(self, target, name="Init"):
        src = None
        self.name = name

        if isinstance(target, str):
            # if target is img dir
            src = cv.imread(target)
        else:
            # if target is img
            src = target

        # log.debug("target = %s, src = %s" % (target, src))

        # resize and save to self.image
        try:
            self.image = cv.resize(src=src,
                                   dsize=(HOG_IMAGE_WIDTH, HOG_IMAGE_HEIGHT),
                                   interpolation=cv.INTER_AREA)
        except Exception as err:
            log.info('%s resize failed. error: %s', self.name, err)

    def get_features(self):
        return np.append(self.get_HOG(), self.get_LBP())

    def get_HOG(self):
        # get hog and save to self.descriptor
        hog = cv.HOGDescriptor((HOG_IMAGE_WIDTH, HOG_IMAGE_HEIGHT), (16, 16),
                               (8, 8), (8, 8), 9)
        descriptor = hog.compute(self.image)

        if descriptor is None:
            return np.array([])
        else:
            return descriptor

    def get_LBP(self):
        return []

    def get_src(self):
        # self.show()
        return cv.cvtColor(self.image, cv.COLOR_BGR2RGB)

    def show(self):
        cv.imshow(self.name, self.image)
        cv.waitKey(0)
        cv.destroyWindow()
