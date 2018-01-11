#coding: utf-8

from sklearn.externals import joblib
from sklearn import svm
import cv2
import numpy as np
import os
import sklearn


class RawDataHandler(object):
    """处理原始图片数据的类"""
    def __init__(self):
        super(RawDataHandler, self).__init__()
        self._m = 70
        self._n = 27
    def load_img(self, fname):
        return cv2.imread(fname)

    def split_img_array(self, an_img_array):
        """Split the raw image arrary to 6 character arrays.

        How to cut the raw image into six part might significantly affects
        classification accuracy.And Here is the way I cut.
        Now, I'll directly split the image into 6 parts.
        """
        # note: some differences exist between OpenCV shape and NumPy shape
        array_in_shape = cv2.resize(an_img_array, (162, 70), \
            interpolation = cv2.INTER_CUBIC)
        arrays = [array_in_shape[:, st:st+27] for st in range(0, 162, 27)]
        return arrays

    def array_to_fea(self, an_array):
        """Convert a character's coressponding numeric array(m*n) to features.

        Retional is simple. Give a m*n array,the function decides what
        form features shold be. Now, I'll directly flatten it.
        """
        return an_array.ravel()

    def img_to_feas(self, img_fname):
        """Given an captcha image name, convert it into 6 features and labels.

        Simplify the image to features pipline. 
        """
        # 1st extract labels from img_fname
        if not os.path.isfile(img_fname):
            raise ValueError("image fname is not valid")
        
        _, labels = os.path.split(img_fname)
        labels, _= os.path.splitext(labels)
        if len(labels) != 6:
            print("One Image with wrong fname found...")
            return None, None
        labels = np.array([ord(l) for l in labels]) # 1 dimentional label

        # 2nd get the features
        img_array = self.load_img(img_fname)[:, :, 0] # 1-dimention is enough
        arrays = self.split_img_array(img_array)
        feas_list = [self.array_to_fea(arr) for arr in arrays]

        return np.array(feas_list), labels
        
    def imgs_to_feas(self, img_fnames_list):
        """Return feas, labels of a list of images.

        iterating to call img_to_feas()
        """
        feas_list = []
        labs_list = []
        for img_fname in img_fnames_list:
            ft, lt = self.img_to_feas(img_fname)
            if ft is None and lt is None:
                continue
            feas_list.append(ft)
            labs_list.append(lt)
        
        return np.vstack(feas_list), np.concatenate(labs_list)
        
    def check_img_fname(self, img_fname):
        pass

    def captcha_to_feas(self, cap):
        """Convert image to corresponding features using the way as trainnig.

        Converting image(m*n array) to feas when loggin in & reserving seat.
        As in these two cases, we'll meet and decode(recognize) the captcha.
        """
        arrays = self.split_img_array(cap)
        feas_list = [self.array_to_fea(arr) for arr in arrays]
        return np.array(feas_list)


class ModelHandler(object):
    """处理模型有关的内容 包括 训练 保存 载入 模型

    This class should be model-wise and should deal and only deal with
    general model functions.
    """
    def __init__(self):
        super(ModelHandler, self).__init__()
        self._clf = None
    
    # attribute's getter function
    @property
    def svm(self):
        return sklearn.svm

    def fit(self, *, feas, labs, save=False, name=None):
        """fit the model given feas, labels

        Now, models are mainly sklearn module and sklearn can handle relating
        problems nicely. Therefore, this function remains blanck.
        """
        pass

    def load_model(self, clf_or_fname):
        """load model from either classifer or model file's name

        clf_or_fname can be name of clfer or model file name
        """
        if os.path.isfile(str(clf_or_fname)):
            _m = joblib.load(clf_or_fname)
        else:
            _m = clf_or_fname
        self._model = _m

    def load_data(self, *, feas, labs):
        raise NotImplemented()

    def save_as(self, fname):
        """save the model with fname using joblib"""
        joblib.dump(self._model, fname)

    def predict(self, fea):
        """predict feas' correspoding labels"""
        return self._model.predict(fea)

if __name__ == '__main__':
    # below is how modeler works
    dher = RawDataHandler()
    feas, labels = dher.imgs_to_feas(['s25n4o.jpg'])

    # create a ModelHandler instance
    mh = ModelHandler()
    # using sklearn to train a model
    clf = mh.svm.SVC()

    mh.load_model(clf)
    mh.save_as('amodel.pkl')

    mh.load_model('amodel.pkl') 
    labels = mh.predict(features)