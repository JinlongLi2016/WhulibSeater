# coding: utf-8
# captchacracker.py
# This script is aimed to and only aimed to deal with stuff relating to the
# split images into separate parts and extract features from each part.

from sklearn import svm
from sklearn.externals import joblib

from modeler import RawDataHandler


class CaptchaCracker(RawDataHandler):
	"""docstring for CaptchaCracker"""
	def __init__(self):
		super(CaptchaCracker, self).__init__()


if __name__ == '__main__':
	cracker = CaptchaCracker()
	# given a list of names, conve
	feas, labels = cracker.imgs_to_feas(['s25n4o.jpg', "wrong_captcha_dir/0.jpg", "wrong_captcha_dir/gbw59d.jpg"])
	print(labels)
	clf = svm.SVC()
	clf.fit(X = feas, y = labels)
	print(clf.predict(feas))