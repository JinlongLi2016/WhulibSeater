# coding: utf-8
# captchacracker.py
# This script is aimed to and only aimed to deal with stuff relating to the
# models that predict captcha's lables.It's jobs include trainng and saving
# models for other module to predict.

from modeler import RawDataHandler


class CaptchaCracker(RawDataHandler):
	"""docstring for CaptchaCracker"""
	def __init__(self):
		super(CaptchaCracker, self).__init__()


if __name__ == '__main__':
	cracker = CaptchaCracker()
	# given a list of names, conve
	feas, labels = cracker.imgs_to_feas(['s25n4o.jpg', "wrong_captcha_dir/0.jpg"])
	print(feas.shape)