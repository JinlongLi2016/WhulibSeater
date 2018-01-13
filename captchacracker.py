# coding: utf-8
# captchacracker.py
# This script is aimed to and only aimed to deal with stuff relating to the
# splitting images into separate parts and extracting features from each part.

import cv2
from sklearn import svm
from sklearn.externals import joblib


class CaptchaCracker():
    """docstring for CaptchaCracker"""
    def __init__(self):
        super(CaptchaCracker, self).__init__()
    

    def split_img_array(self, an_img_array):
        """Split the raw image arrary to 6 character arrays.

        How to cut the raw image into six parts might significantly affects
        classification accuracy.And Here is the way I cut.
        Now, I'll directly split the image into 6 parts.

        Args:
            an_img_array(m*n): a captcha's image corresponding numeric array.

        Returns:
            A list of features corresponding six characters.
        """
        # note: some differences exist between OpenCV shape and NumPy shape
        array_in_shape = cv2.resize(an_img_array, (162, 70), \
            interpolation = cv2.INTER_CUBIC)
        arrays = [array_in_shape[:, st:st+27] for st in range(0, 162, 27)]
        return arrays

    def _array_to_fea(self, an_array):
        """Convert a character's coressponding numeric array(m*n) to features.

        Retional is simple. Give a m*n array,the function decides what
        form features shold be. Now, I'll directly flatten it.

        Returns:
            A feature (*,)(1 dimentianal) extracted from "an_array" using
                methods defined in this function.
        """
        # 归一化 [-1, 1)
        an_array = an_array.astype('float16')
        an_array = (an_array - 128) / 128
        
        return an_array.ravel()

if __name__ == '__main__':
    cracker = CaptchaCracker()
    # given a list of names, conve
    feas, labels = cracker.imgs_to_feas(['s25n4o.jpg', "wrong_captcha_dir/0.jpg", "wrong_captcha_dir/gbw59d.jpg"])
    print(labels)
    clf = svm.SVC()
    clf.fit(X = feas, y = labels)
    print(clf.predict(feas))