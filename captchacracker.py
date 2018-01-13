# coding: utf-8
# captchacracker.py
# This script is aimed to and only aimed to deal with stuff relating to the
# splitting images into separate parts and extracting features from each part.

import cv2
import numpy as np
from skimage.feature import hog 
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
        # 1 提取直方图特征
        hist_features = self.get_color_hist(an_array, nbins = 4,\
            bins_range = (0, 255))

        # 2 提取 HOG 特征
        hog_features = self.get_hog_features(an_array) # tune params?

        # 3展开得到特征
        raw_features = an_array.ravel()


        return np.concatenate((hist_features, hog_features, raw_features))

    ##########################################################################
    ############ Below is functions that extracts features ###################
    
    # Define a function to compute color histogram features  
    def get_color_hist(self, an_array, *, nbins, bins_range):
        # Compute the histogram of the color channels separately
        hist_features = np.histogram(an_array, bins=nbins, range=bins_range)[0]
        hist_features = hist_features.astype('float32')
        
        return hist_features

    # Define a function to return HOG features (and visualization, maybe)
    def get_hog_features(self, an_array, orient = 9, pix_per_cell = 3,
        cell_per_block = 3, vis=False, feature_vec=True):
        if vis == True:
            # Use skimage.hog() to get both features and a visualization
            features, hog_image = hog(an_array, orientations=orient, pixels_per_cell=(pix_per_cell, pix_per_cell),
                                      cells_per_block=(cell_per_block, cell_per_block), transform_sqrt=False, 
                                      visualise=vis, feature_vector=feature_vec)
            return features, hog_image
        else:      
            # Use skimage.hog() to get features only
            features = hog(an_array, orientations=orient, pixels_per_cell=(pix_per_cell, pix_per_cell),
                           cells_per_block=(cell_per_block, cell_per_block), transform_sqrt=False, 
                           visualise=vis, feature_vector=feature_vec)
            return features


if __name__ == '__main__':
    cracker = CaptchaCracker()
    # given a list of names, conve
    feas, labels = cracker.imgs_to_feas(['s25n4o.jpg', "wrong_captcha_dir/0.jpg", "wrong_captcha_dir/gbw59d.jpg"])
    print(labels)
    clf = svm.SVC()
    clf.fit(X = feas, y = labels)
    print(clf.predict(feas))