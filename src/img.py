import cv2 as cv

HOG_IMAGE_WIDTH = 256
HOG_IMAGE_HEIGHT = 256


class Image(object):
    """Image: Image instance is a frame of video or a image

    An instance represents a frame or an image that can be used to train a model or to identify.
    """

    def __init__(self, img_dir):
        self.image = cv.resize(src=cv.imread(img_dir),
                               dsize=(HOG_IMAGE_WIDTH, HOG_IMAGE_HEIGHT),
                               interpolation=cv.INTER_AREA)

        hog = cv.HOGDescriptor(
            (self.hog_svm_image_width, self.hog_svm_image_height), (16, 16),
            (8, 8), (8, 8), 9)
        self.descriptor = hog.compute(self.image)

        if self.descriptor is None:
            self.descriptor = []
        else:
            self.descriptor = self.descriptor.ravel()
