# WhulibSeater

**Naughty** program to crack whulib seat reserving system.
# Requirments
* Anonconda 3.6
* OpenCV contrib 3.x 
* TensorFlow 1.x

**本小工程需要很多Python库，为简化安装步骤，可以安装[Anonconda3.6](https://www.anaconda.com/download/)**

**此外,也依赖OpenCV库,其强大的功能能够简化后续开发。Windows用户可以[从此](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)下载相对应的编译好的文件,按照[此教程](https://www.solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/)安装，**

**TensorFlow:(Windows) win+R 调出命令窗口->输入: pip install tensorflow 即可。其他系统类似。如果需要安装GPU版本请自行搜索安装方式。**
# Usage
## 1. [标准用法示例](https://github.com/JinlongLi2016/WhulibSeater/blob/master/standard_usage.py)(预定位置)
	# standard_usage.py
	from studenter import Student
	from modeler import ModelHandler, RawDataHandler
	
	# 创建一个学生对象 (处理和网页交互)
	s = Student(id, password)
	s.set_reserve_information(reserve_information) #设置所要预定的位置信息.reserve_information是一个含有与预定相关的信息的字典
	
	# 创建一个处理数据对象和一个处理模型的对象(识别验证码)
	data_handler = RawDataHandler()
	model_handler = ModelHandler()

	# 该对象需要导入模型 (假设在当前文件夹下 已经有一个训练好的模型,名字是default.pkl)(本页底有训练好的default.pkl)
	model_handler.load_model('default.pkl', data_handler = data_handler) # data_handler传入,获得图片到特征的一些参数
	
	# 开始登陆网页
	has_login = False 	# 当前还未登陆,设置为False
	while not has_login:	
		# 获得登陆验证码
		login_captcha = s.get_login_captcha()
		# 将login_captcha转换为模型可以处理的特征
		feature = data_handler.captcha_to_feas(login_captcha)# 根据前面获得参数,按照训练模型时图片转为特征的方式，将图片转为特征
		# 识别验证码
		verification_code = model_handler.predict_captcha(feature)	
		# 登陆
		has_login = s.login(verification_code)
	
	# 登陆成功 预定位置
	has_reserved = False	# 当前还未预定,设置为False
	while not has_reserved:
		reserve_captcha = s.get_reserve_captcha()
		feature = data_handler.captcha_to_feas(reserve_captcha)
		verification_code = model_handler.predict_captcha(feature)
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
	model_handler.save_model(model = clf, fname = 'default.pkl', scaler = data_handler.Scaler)#保存
	pred = model_handler.predict(features) # 对features(特征)进行预测
	
	# 正确率是?
	acc = (pred==labels)/len(pred)
	print("The predictions are: ", pred, "\nAccuracy is ", acc)

### 2.2 导入模型
	from modeler import ModelHandler, RawDataHandler
	
	# 构造一个数据处理和模型处理的对象
	model_handler = ModelHandler()
	data_handler = RawDataHandler()
	
	# 导入所保存的模型
	model_handler.load_model('defaulf.pkl', data_handler = data_handler)

# Appendix
> **reserve_information 示例**

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
		'seat': '5243'  #这个数据在测试的时候可以减去30(随便说的)以内的任何一个数
				#系统也会有对应的位置
	}

> **query_information 示例**

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

> [default.pkl](https://pan.baidu.com/s/1pLZGTAV)  密码 c3va