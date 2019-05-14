import logging as log

# from skimage.feature import local_binary_pattern
from .config import GLOBAL_CONFIG
import cv2 as cv
import numpy as np
from skimage import feature


class Image(object):
    """Image: Image instance is a frame of video or a image

    An instance represents a frame or an image that can be used to train a model or to identify.
    """
    image = None

    def __init__(self, target, name="Init"):
        self.name = name

        if isinstance(target, str):
            # if target is img dir
            self.image = cv.imread(target)
        else:
            # if target is img
            self.image = target

    def resize(self, width, height):
        try:
            return cv.resize(src=self.image,
                             dsize=(width, height),
                             interpolation=cv.INTER_AREA)
        except Exception as err:
            log.info('%s resize failed. error: %s', self.name, err)
            return None

    def get_features(self):
        return np.append(self.get_HOG(), self.get_LBP())

    def get_HOG(self):
        # get hog and save to self.descriptor
        # 1. resize image to get copy
        copy = self.resize(GLOBAL_CONFIG.hog_width, GLOBAL_CONFIG.hog_height)
        if copy is None:
            log.error('resize failed. get hog failed')
            return
        # 2. get hog descriptor
        hog = cv.HOGDescriptor(
            (GLOBAL_CONFIG.hog_width, GLOBAL_CONFIG.hog_height), (16, 16),
            (8, 8), (8, 8), 9)
        descriptor = hog.compute(copy)

        if descriptor is None:
            return np.array([])
        else:
            return descriptor

    def get_LBP(self):
        numPoints = 24
        radius = 8
        eps = 1e-7
        copy = self.resize(GLOBAL_CONFIG.hog_width, GLOBAL_CONFIG.hog_height)
        gray = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
        lbp = feature.local_binary_pattern(gray,
                                           numPoints,
                                           radius,
                                           method="uniform")
        (hist, _) = np.histogram(lbp.ravel(),
                                 bins=np.arange(0, numPoints + 3),
                                 range=(0, numPoints + 2))
        hist = hist.astype('float')
        hist /= (hist.sum() + eps)

        return hist

    def get_src(self):
        # self.show()
        return cv.cvtColor(self.image, cv.COLOR_BGR2RGB)

    def show(self):
        cv.imshow(self.name, self.image)
        cv.waitKey(1)

    def get_width(self):
        return self.image.shape[1]

    def get_height(self):
        return self.image.shape[0]

    def cut(self, x, y, px, py):
        return Image(self.image[y:py, x:px])

    def draw_rectangle(self, x, y, px, py):
        cv.rectangle(self.image, (x, y), (px, py), (0, 255, 255), thickness=1)
