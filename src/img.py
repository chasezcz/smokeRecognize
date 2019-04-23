import cv2 as cv


class Image(object):
    """Image: Image instance is a frame of video or a image

    An instance represents a frame or an image that can be used to train a model or to identify.
    """

    def __init__(self, img):
        self.image = img
        self.hog_svm_image_width = 256
        self.hog_svm_image_height = 256

    def get_hog(self):
        # 1. resize image

        self.image = cv.resize(
            self.image, (self.hog_svm_image_width, self.hog_svm_image_height),
            interpolation=cv.INTER_NEAREST)
        cv.imshow("show", self.image)
        cv.waitKey()


tmp_img = cv.imread("/Users/chengze/Desktop/01.png")

image = Image(tmp_img)
image.get_hog()
