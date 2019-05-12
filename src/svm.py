import logging as log
import os

import cv2 as cv
import numpy as np

from src.img import Image
from src.config import GLOBAL_CONFIG
from sklearn.svm import LinearSVC
from sklearn.externals import joblib


class Svm(object):
    def __init__(self):
        pass

    def __get_images_by_dir__(self, folder_dir):
        """__get_images_by_dir__ get image samples by dir

        Arguments:
            folder_dir {string} -- folder dir of local train images samples

        Returns:
            Image[] -- a series of Image used to train models.
        """
        images = []
        if os.path.exists(folder_dir) == False:
            return images, "%s not exist" % folder_dir

        files = os.listdir(folder_dir)

        for file_name in files:

            if GLOBAL_CONFIG.is_support_pics(
                    file_name) and not os.path.isdir(file_name):
                image = Image(folder_dir + '/' + file_name, file_name)

                # log.debug("FILE: %s" % image.name)

                images.append(image)

        return images, None

    def __get_name_by_dir__(self, dir):
        paths = dir.split('/')
        return paths[len(paths) - 1]

    def train(self, data_set_dir):
        """train train model for a data set

        every folder, there should be sub_folder such as 'positive_samples' and 'negative_samples'
        Arguments:
            data_set_dir {str} -- dataSet local path

        Returns:
            [type] -- [description]
        """
        log.debug('now begin laod data from image_dir')
        # 1. load images from data_set_dir.
        positive_samples, err1 = self.__get_images_by_dir__(
            '%s/positive_samples' % data_set_dir)
        negative_samples, err2 = self.__get_images_by_dir__(
            '%s/negative_samples' % data_set_dir)

        if err1 != None or err2 != None:
            log.error("train get data set error. details: err1: %s, err2: %s",
                      err1, err2)
            return False, ""

        # get data train and label
        features = []
        labels = []
        for img in positive_samples:
            features.append(img.get_features())
            labels.append(1)
        for img in negative_samples:
            features.append(img.get_features())
            labels.append(0)

        log.info(
            "image load successful, positive image num %d, negative image num %d"
            % (len(positive_samples), len(negative_samples)))

        log.info("features.shape: %s, labels.shapes: %s" %
                 (np.shape(features), np.shape(labels)))

        log.info('start train svm model')
        # set svm learning
        # # svm in opencv
        # self.ml = cv.ml.SVM_create()
        # self.ml.setKernel(cv.ml.SVM_LINEAR)
        # self.ml.setType(cv.ml.SVM_C_SVC)
        # self.ml.setTermCriteria(
        #     (cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_EPS, 1000, 1e-6))
        # self.ml.setDegree(3)
        # self.ml.train(features, cv.ml.ROW_SAMPLE, labels)
        # self.ml.save('data/models/svm-model.dat')

        # try sklearn.svm
        self.ml = LinearSVC()
        # set max_iter 10000, but I don't know why it not converge
        self.ml.max_iter = 10000
        self.ml.tol = 1e-6

        try:
            self.ml.fit(features, labels)
            joblib.dump(self.ml, "data/models/svm-model.dat")
        except Exception as err:
            log.error('train failed. error: %s' % err)
            return False, "Failed, details in log"
        else:
            log.info(
                'trainning finish successfully. try to save as "svm-model.dat" in "data/models/"'
            )
            return True, "data/models/svm-model.dat"

    def preidct_pic(self, target_dir):
        log.info('start image predict')
        self.ml = joblib.load("data/models/svm-model.dat")
        img = Image(target_dir, 'first')
        feature = [img.get_features()]
        # print(feature[0][1])
        label = self.ml.predict(feature)
        log.info('predict %s result: %s' % (target_dir, label))

    def preidct_video(self, target_dir):
        log.info('start video predict')
        pass


if __name__ == '__main__':
    """ just for test
    """
    svm = Svm()
    svm.train('/Users/chengze/code/smokeRecognize/data/train_data')
