# WhulibSeater

**Naughty** program to crack whulib seat reserving system.
# Requirments
**本小工程需要依赖库，为简化安装步骤，可以安装[Anonconda3.6](https://www.anaconda.com/download/)**

**此外本工程也依赖OpenCV库。该库安装起来比较麻烦，但是其强大的功能能够简化后续开发。Windows用户可以按照[此教程](https://www.solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/)安装，[从此](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)下载相对应的编译好的文件.**
# Usage
## 1. 标准用法示例(预定位置)
	from studenter import Student
	from modeler import ModelHandler, RawDataHandler
	
	# 创建一个学生对象 (处理和网页交互)
	s = Student(id, password)
	s.set_reserve_information(reserve_information) #设置所要预定的位置信息.reserve_information是一个含有与预定相关的信息的字典
	
	# 创建一个处理数据对象和一个处理模型的对象(识别验证码)
	data_handler = RawDataHandler()
	model_handler = ModelHandler()

	# 该对象需要导入模型 (假设在当前文件夹下 已经有一个训练好的模型,名字是default.pkl)
	model_handler.load_model('default.pkl')
	
	# 开始登陆网页
	has_login = False 	# 当前还未登陆,设置为False
	while not has_login:	
		# 获得登陆验证码
		login_capthca = s.get_login_captcha()
		# 将login_captcha转换为模型可以处理的特征
		feature = data_handler.captcha_to_feas(login_capthca)
		# 识别验证码
		verification_code = model_handler.predict(login_captcha)	
		# 登陆
		has_login = s.login(verification_code)
	
	# 登陆成功 预定位置
	has_reserved = False	# 当前还未预定,设置为False
	while not has_reserved:
		reserve_captcha = s.get_reserve_captcha()
		verification_code = model_handler.predict(reserve_captcha)
		feature = data_handler.captcha_to_feas(login_capthca)	

		has_reserved = s.reserve_seat(verification_code)

	# 代码运行至此, 我们应该已预定在reserve_information中设定的座位

## 2.训练、保存、导入模型示例
### 2.1 训练、保存模型及用于预测
	from modeler import ModelHandler, RawDataHandler
	
	# 构造一个数据处理和模型处理的对象
	data_handler = RawDataHandler()
	model_handler = ModelHandler()
	# image_list是 图片名的列表
	image_list = ['s25n4o.jpg']
	
	# 使用imgs_to_feas方法把图片转换为 特征和标签
	features, labels = data_handler.imgs_to_feas(image_list)
	
	# 构造一个模型并训练
	from sklearn import svm
	clf = svm.SVC()		#构造模型
	clf.fit(X = features, y = labels)	#训练
	
	# 可以保存模型或者将之用于预测
	model_handler.save_model(model = clf, fname = 'default.pkl')#保存
	pred = model_handler.predict(features) # 对 (特征)features 进行预测
	print("The predictions are: ", pred)

### 2.2 导入模型
	from modeler import ModelHandler
	
	# 构造一个数据处理和模型处理的对象
	model_handler = ModelHandler()
	
	# 导入所保存的模型
	model_handler.load_model('defaulf.pkl')

# Appendix
> *reserve_information 示例*

	seat_information = {
		'onDate':'2018-1-11',# which date 
		'building':'1',      # which building?  1:信图
		'room': '8',         # which room? 8: 二楼东
		'hour':'null',
		'startMin':'1305',   # 1305 for 21:45 
		'endMin':'1320',     # 1320 for 22:00 as 1320/60 = 22
		'power':'null',
		'window':'null',
		# which exact seat you want to reserve.This is the id in
		# the system which you can get via "query" method. 
		'seat': '5243'  
	}

> *query_information 示例*

	query_information = {
	'onDate':'2018-1-10',
	'building':'1',
	'room': '7',
	'hour':'null',
	'startMin':'1290',
	'endMin':'1320',
	'power':'null',
	'window':'null'
	}