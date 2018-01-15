#coding: utf-8

from sklearn.externals import joblib
from sklearn.model_selection import train_test_split as sk_train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import cv2
import numpy as np
import os

from captchacracker import CaptchaCracker


class RawDataHandler(CaptchaCracker):
    """处理原始图片数据的类

    This class converts raw images(file name or image array) to features
    (with labels probably).One most important function is to split raw 
    images and convert them to features, which are located in split_img_array
    and _array_to_fea() respectively. If you want to choose a another way to
    split images and convert them to features, you can directly change them
    without changing codes that use them(You may need to retrain models).
    
    Protected attributes:
        _m: a character's  array's height
        _n: a character's  array's width

    Protected methods:
    - _array_to_fea: converting a character's corresponding array to features and 
        return them(list).

    Public methods:
    - load_image: given a fname and read out return the image.
    - img_to_feas: given an image fname or image array, convert it to
        (features,labels) for former and features for latter.① When training a
        model, it receives an image's file name, so it will return image's 
        features and labels, which is the image's name(such as:"s25n4o.jpg").
        ② When we log in, we need the convert raw image's numeric array to
        features for prediction. This time, it receives an array(ndarray), 
        and convert it to features(with no labels).
        (This function 
        have been implemented in a complicated way. As in my setting, to get
        a new captcha(m*n*3,ndarray)'s feature, there is a simple method
        captcha_to_feas.Maybe will change back in the future.)
    - split_img_array: This funnction determins how to split original
        image array(containing six characters) into six arrays(list) for 
        latter training or prediction.(removed to (class)CaptchaCracker)
    - _array_to_fea: This funnction determins how to extract features
        from one character's numberic array.(removed to (class)CaptchaCracker)
    - imgs_to_feas: this is a helper function to simply getting features and 
        labels from a list of captcha image file names.(usually used when 
        training)
    - captcha_to_feas: a helper function to convert capthca array(m*n*3) to
        features.
    - get_features_labels_from_directory: a helper function to convert a
        directory of images to (features, labels)
    - train_test_split: Split arrays or matrices into random train and 
        test subsets
    """
    
    def __init__(self):
        super(RawDataHandler, self).__init__()
        self._m = 70
        self._n = 27
        self.Scaler = StandardScaler()
    
    def load_image(self, fname):
        """read and return fname image's array(m*n*3, uint8)"""
        return cv2.imread(fname)

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
        return super().split_img_array(an_img_array)

    def _array_to_fea(self, an_array):
        """Convert a character's coressponding numeric array(m*n) to features.

        Retional is simple. Give a m*n array,the function decides what
        form features shold be.

        Returns:
            A feature (*,)(1 dimentianal) extracted from "an_array" using
                methods defined in this function.
        """
        return super()._array_to_fea(an_array)

    def img_to_feas(self, img_fname_or_array):
        """Given a captcha image name or array, convert it into 6 features
        (and labels if it's an image).(try not pass array as there is a
        better way to do this: using self.captcha_to_feas)

        given a captcha's file name, convert it into 6 features,labels
        (This case occurs when we train a model)[Warning: Any changes here
        need to be implemented in captcha_to_feas() since the both convert
        images to features, and the way need to be consistent]

        Args:
            img_fname_or_array: a image file name(jpg) or an image 
                array(ndarray) in m*n*3 shape and unit8 as their
                data type.

        Returns:
            features, labels if img_fname_or_array;
            features only if image_fname_or_array is an image's m*n* array
        """ 
        # 1st extract labels(if image filename) from img_fname_or_array
        if isinstance(img_fname_or_array, np.ndarray):
            img_array = img_fname_or_array[:, :, 0]
        elif os.path.isfile(img_fname_or_array):
            _, labels = os.path.split(img_fname_or_array)
            labels, _= os.path.splitext(labels)
            if len(labels) != 6:
                print("One Image with wrong fname found...")
                return None, None
            labels = np.array([ord(l) for l in labels]) # 1 dimentional label
            img_array = self.load_image(img_fname_or_array)[:, :, 0]
        else:
            # raise Error
            raise ValueError("img_fname_or_array should be np.ndarray or a \
                image file name")
        
        img_array = self.strip_array(img_array)   # strip backgroud pixels around
        # 2nd get the features
        arrays = self.split_img_array(img_array)
        # strip background pixesl around character and resize it to (28*28)
        arrays = [self.strip_array(arr, resize_shape = (28, 28)) \
                  for arr in arrays] 
        
        feas_list = [self._array_to_fea(arr) for arr in arrays]

        # choose to return something
        if os.path.isfile(img_fname_or_array):
            return np.array(feas_list), labels
        else:
            return np.array(feas_list)
        
    def imgs_to_feas(self, img_fnames_list, *, fit_scaler = True):
        """Return feas, labels of a list of images.(usually when training)

        iterating to call img_to_feas()

        Args:
            img_fnames_list: a list of captcha images' names

        Returns:
            (features, labels)
        """
        feas_list = []
        labs_list = []
        for img_fname in img_fnames_list:
            ft, lt = self.img_to_feas(img_fname)
            if ft is None and lt is None:
                continue
            feas_list.append(ft)
            labs_list.append(lt)
        
        feas, labs = np.vstack(feas_list), np.concatenate(labs_list)
        
        if fit_scaler:
            feas = self.Scaler.fit_transform(feas)
        else:
            feas = self.Scaler.transform(feas)
        
        return feas, labs
        
    def check_img_fname(self, img_fname):
        pass

    def captcha_to_feas(self, cap):
        """Convert image to corresponding features using the way as trainnig.

        Converting image(m*n*3 array) to feas when loggin in & reserving seat.
        As in these two cases, we'll meet and decode(recognize) the captcha.
        The converting way are stored in self.Scaler
        
        Args:
            cap(ndarray)(70,160,3): The captcha retrieved via Student class.

        Returns:
            The captcha's feature, extraing from captcha array.
        """
        cap = cap[:, :, 0]

        # be consistent with the converting way in img_to_feas()
        cap = self.strip_array(cap)

        arrays = self.split_img_array(cap)
        # be consistent with the converting way in img_to_feas()
        arrays = [self.strip_array(arr, resize_shape=(28,28))\
                  for arr in arrays]

        feas_list = [self._array_to_fea(arr) for arr in arrays]
        feas = np.array(feas_list)

        feas = self.Scaler.transform(feas)
        
        return feas

    def get_features_labels_from_directory(self, dir_name, *, fit_scaler = True):
        """To get image features and labels from the given directory dir_name.

        Args:
            dir_name: the directory where images locate in.

        Returns:
            (features, labels)
        """
        if not os.path.isdir(dir_name):
            raise ValueError(dir_name, " seems not be a directory")

        image_names_list = []
        for _, _, image_names in os.walk(dir_name):
            image_names_list += image_names
        
        image_names_list = [os.path.join(dir_name, t) \
            for t in image_names_list]
        print(image_names_list)
        return self.imgs_to_feas(image_names_list, fit_scaler = fit_scaler)

    def strip_array(self, an_array, threshold = 180, resize_shape = None):
        """Strip pixels above threshold around center balck parts

        Args:
            an_array: the original array that you want strip pixels on.
            threshold: pixel's tensity above this is regarded as background.
                This is an important parameter, be careful(背景白).
            resize_shape(tuple): If you need to resize the extracted array

        Returns:
            An array cutted from the center of original array (an resized if
            resize_shape paramter is passed)
        """
        m, n = an_array.shape

        x_start = -1
        for i in range(m):
            for j in range(n):
                if an_array[i][j] < threshold:
                    x_start = i
                    break 
            if x_start > -1:
                break
        x_end = m
        for i in range(m-1, -1, -1):
            for j in range(n):
                if an_array[i][j] < threshold:
                    x_end = i+1 
            if x_end < m:
                break
        y_start = -1
        for j in range(n):
            for i in range(m):
                if an_array[i][j] < threshold:
                    y_start = j
            if y_start > -1:
                break
        y_end = n
        for j in range(n-1, -1, -1):
            for i in range(m):
                if an_array[i][j] < threshold:
                    y_end = j+1
            if y_end < n:
                break

        print(x_start, x_end, y_start, y_end)
        info_arr = an_array[x_start:x_end, y_start:y_end]
        if resize_shape is not None:
            info_arr = cv2.resize(info_arr, resize_shape, \
                        interpolation = cv2.INTER_CUBIC)
        
        if x_end - x_start < 10 or y_end - y_start < 10:
            print("something might be wrong in RawDataHandler.strip_array()")
        return info_arr
    
    def train_test_split(self, *arrays, train_size = 0.8, test_size = 0.2):
        """Split arrays or matrices into random train and test subsets
        
        http://scikit-learn.org/stable/modules/generated/\
            sklearn.model_selection.train_test_split.html
        Args:
            *arrays: sequence of indexables with same length / shape[0]
                Allowed inputs are lists, numpy arrays, scipy-sparse
                matrices or pandas dataframes.
            test_size: in what proportion you want the test sets be
            train_size: in what proportion you want the train sets be
        """

        return sk_train_test_split(*arrays, train_size = 0.8, test_size = 0.2)


class ModelHandler(object):
    """处理模型有关的内容 包括 保存 载入 模型

    This class should be model-wise and should deal and only deal with
    general model functions.

    Protected attributes:
        _model: the model belongs to ModelHandler's instance.

    Public methods:
        load_model: load model from either model file name or
            a model's instance, set it to _model.
        save_model: save the given model or self._model to fname.
        predict: using _model to predict given feature.
    """
    def __init__(self):
        super(ModelHandler, self).__init__()
        self._model = None

    def fit(self, *, feas, labs, save=False, name=None):
        """fit the model given feas, labels

        Now, models are mainly sklearn module and sklearn can handle relating
        problems nicely. Therefore, this function remains blanck.
        """
        pass

    def load_model(self, clf_or_fname, data_handler = None):
        """load model from either classifer or model file's name

        Args:
            clf_or_fname: can be name of clfer or model file name
        """
        # what if the given fname doesn't exit?
        if os.path.isfile(str(clf_or_fname)):
            _m = joblib.load(clf_or_fname)
            if data_handler is None:
                raise ValueError("'data_handler' not passed in.")
            data_handler.Scaler = _m._scaler
        else:
            _m = clf_or_fname
        self._model = _m

    def save_model(self, *, model=None, fname, scaler=None):
        """save the given model or self._model to dist as fname.
        
        Args:
            model:(optional) the model you want to save
            fname: the saving file name.
        """
        if model is None:
            setattr(self._model, '_scaler', self.Scaler)
            self.save_as(fname)
        else:
            setattr(model, '_scaler', scaler)
            joblib.dump(model, fname)
    
    def load_data(self, *, feas, labs):
        raise NotImplemented()

    def save_as(self, fname):
        """save the model with fname using joblib"""
        joblib.dump(self._model, fname)

    def predict(self, fea):
        """predict feas' correspoding labels using self._model"""
        pred = self._model.predict(fea)
        return ''.join(chr(i) for i in pred)


if __name__ == '__main__':
    # below is how modeler works
    dher = RawDataHandler()
    feas, labels = dher.imgs_to_feas(['s25n4o.jpg', "wrong_captcha_dir/0.jpg", "wrong_captcha_dir/gbw59d.jpg"])

    # create a ModelHandler instance
    mh = ModelHandler()
    # using sklearn to train a model
    clf = mh.svm.SVC()

    mh.load_model(clf)
    mh.save_as('amodel.pkl')

    mh.load_model('amodel.pkl') 
    labels = mh.predict(features)