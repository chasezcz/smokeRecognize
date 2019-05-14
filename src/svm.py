import logging as log
import os

import cv2 as cv
import numpy as np
from src.video import Video
from src.img import Image
from src.config import GLOBAL_CONFIG
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import PIL.Image, PIL.ImageTk

CANVAS_IMG = None
CANVAS_IMG_PHOTO = None


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

    def __sliding_window__(self, img_width, img_height, stepSize):
        # slide a window across the image
        for y in range(0, img_height, stepSize):
            for x in range(0, img_width, stepSize):
                # yield the current window
                yield (x, y, x + 64, y + 64)

    def __overlapping_area__(self, detection_1, detection_2):

        x1_tl = detection_1[0]
        x2_tl = detection_2[0]
        x1_br = detection_1[0] + detection_1[3]
        x2_br = detection_2[0] + detection_2[3]
        y1_tl = detection_1[1]
        y2_tl = detection_2[1]
        y1_br = detection_1[1] + detection_1[4]
        y2_br = detection_2[1] + detection_2[4]
        # Calculate the overlapping Area
        x_overlap = max(0, min(x1_br, x2_br) - max(x1_tl, x2_tl))
        y_overlap = max(0, min(y1_br, y2_br) - max(y1_tl, y2_tl))
        overlap_area = x_overlap * y_overlap
        area_1 = detection_1[3] * detection_2[4]
        area_2 = detection_2[3] * detection_2[4]
        total_area = area_1 + area_2 - overlap_area
        return overlap_area / float(total_area)

    def __nms__(self, detections, threshold=.5):
        '''
        This function performs Non-Maxima Suppression.
        `detections` consists of a list of detections.
        Each detection is in the format ->
        [x-top-left, y-top-left, confidence-of-detections, width-of-detection, height-of-detection]
        If the area of overlap is greater than the `threshold`,
        the area with the lower confidence score is removed.
        The output is a list of detections.
        '''
        if len(detections) == 0:
            return []
        # Sort the detections based on confidence score
        detections = sorted(detections,
                            key=lambda detections: detections[2],
                            reverse=True)
        # Unique detections will be appended to this list
        new_detections = []
        # Append the first detection
        new_detections.append(detections[0])
        # Remove the detection from the original list
        del detections[0]
        # For each detection, calculate the overlapping area
        # and if area of overlap is less than the threshold set
        # for the detections in `new_detections`, append the
        # detection to `new_detections`.
        # In either case, remove the detection from `detections` list.
        for index, detection in enumerate(detections):
            for new_detection in new_detections:
                if self.__overlapping_area__(detection,
                                             new_detection) > threshold:
                    del detections[index]
                    break
            else:
                new_detections.append(detection)
                del detections[index]
        return new_detections

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

        log.debug("features.shape: %s, labels.shapes: %s" %
                  (np.shape(features), np.shape(labels)))

        log.info('start train svm model')
        # set svm learning, try sklearn.svm
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
                'trainning finish successfully. try to save as "svm-model.dat" in "data/models/", loss: %s'
                % (self.ml.loss))
            return True, "data/models/svm-model.dat"

    def preidct_pic(self, target_dir):
        log.debug('start image predict, load model.')
        self.ml = joblib.load("data/models/svm-model.dat")

        img = Image(target_dir, self.__get_name_by_dir__(target_dir))
        detections = []
        log.debug('img width: %d, img height: %d' %
                  (img.get_width(), img.get_height()))
        for (x, y, px,
             py) in self.__sliding_window__(img.get_width(), img.get_height(),
                                            GLOBAL_CONFIG.slide_step):
            if px > img.get_width() or py > img.get_height():
                continue
            sub_img = img.cut(x, y, px, py)

            # sub_img.show()
            feature = [sub_img.get_features()]
            label = self.ml.predict(feature)
            # log.info("features.shape: %s, labels.shapes: %s" %
            #          (np.shape(feature), np.shape(label)))
            if label[0] == 1:
                detections.append(
                    (x, y, self.ml.decision_function(feature), px - x, py - y))
                log.info('%d %d %d %d, have smoke' % (x, y, px, py))
            else:
                log.info('%d %d %d %d, have no smoke' % (x, y, px, py))

        detections = self.__nms__(detections, 3)

        # Display the results after performing NMS
        for (x, y, _, w, h) in detections:
            # Draw the detections
            img.draw_rectangle(x, y, x + w, y + h)
        img.show()
        # img = cv.cvtColor(img.image, cv.COLOR_BGR2RGB)
        # CANVAS_IMG = PIL.Image.fromarray(img)
        # CANVAS_IMG_PHOTO = PIL.ImageTk.PhotoImage(CANVAS_IMG)

    def preidct_video(self, target_dir):
        log.debug('start video predict, load model.')
        self.ml = joblib.load("data/models/svm-model.dat")
        self.video = Video(target_dir)
        mog = cv.createBackgroundSubtractorMOG2(detectShadows=True)

        for frame in self.video.get_next_frame():
            fgmask = mog.apply(frame.image)
            th = cv.threshold(fgmask.copy(), 244, 255, cv.THRESH_BINARY)[1]
            th = cv.erode(th,
                          cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)),
                          iterations=2)
            dilated = cv.dilate(th,
                                cv.getStructuringElement(
                                    cv.MORPH_ELLIPSE, (8, 3)),
                                iterations=2)
            contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL,
                                          cv.CHAIN_APPROX_SIMPLE)
            detections = []
            for c in contours:
                if cv.contourArea(c) > 500:
                    (x, y, w, h) = cv.boundingRect(c)
                    sub_img = frame.cut(x, y, x + w, y + h)
                    feature = [sub_img.get_features()]
                    label = self.ml.predict(feature)
                    log.debug("features.shape: %s, labels.shapes: %s" %
                              (np.shape(feature), np.shape(label)))
                    if label[0] == 1:
                        frame.draw_rectangle(x, y, x + w, y + h)
                    log.info('%d %d %d %d, have smoke' % (x, y, x + w, y + h))

            frame.show()
            if cv.waitKey(1) == ord('q'):
                break


if __name__ == '__main__':
    """ just for test
    """
    svm = Svm()
    svm.train('/Users/chengze/code/smokeRecognize/data/train_data')
