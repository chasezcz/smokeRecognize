import logging as log
import os

import src.log
from src.img import Image


class Svm(object):
    def __init__(self):
        pass

    def __get_files_by_dir__(self, folder_dir):
        """__get_files_by_dir__ [summary]

        Arguments:
            folder_dir {[string]} -- [description]

        Returns:
            [type] -- [description]
        """
        images = []
        if os.path.exists(folder_dir) == False:
            return images, "%s not exist" % folder_dir

        files = os.listdir(folder_dir)
        for file_name in files:

            if not os.path.isdir(file_name):
                image = Image(folder_dir + '/' + file_name)
                # images.append(image)
                image.append(folder_dir + '/' + file_name)

        return images, None

    def train(self, data_set_dir):
        """train: train model for a data set

        every folder, there should be sub_folder such as 'positive_samples' and 'negative_samples'
        Arguments:
            data_set_dir {[str]} -- dataSet local path
        """

        # 1. load images from data_set_dir.
        self.positive_samples, err1 = self.__get_files_by_dir__(
            '%s/positive_samples' % data_set_dir)
        self.negative_samples, err2 = self.__get_files_by_dir__(
            '%s/negative_samples' % data_set_dir)
        log.error(err1)
        if err1 != None or err2 != None:
            log.error("train get data set error. details: err1: %s, err2: %s",
                      err1, err2)
            return False, ""

        log.info(
            "image load successful, positive image num %d, negative image num %d"
            % (len(self.positive_samples), len(self.negative_samples)))

        # 2. train svm

    def predict(self, target_dir):
        pass


if __name__ == '__main__':
    src.log.init()
    svm = Svm()
    svm.train('Users/chengze/Desktop')
