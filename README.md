# WhulibSeater

**Naughty** program to crack whulib seat reserving system.

# Usage
## 标准用法示例
	from studenter import Student
	from modeler import ModelHandler
	
	# 创建一个学生对象 (处理和服务器交互)
	s = Student(id, password)
	s.set_reserve_information(reserve_information) #设置所要预定的位置信息.reserve_information是一个含有与预定相关的信息的字典
	
	# 创建一个处理模型的对象 (识别验证码)
	model_handler = ModelHandler()

	# 该对象需要导入模型 (假设在当前文件夹下 已经有一个训练好的模型,名字是default.pkl)
	model_handler.load_model('default.pkl')
	
	# 开始登陆网页
	has_login = False 	# 当前还未登陆,设置为False
	while not has_login:	
		# 获得登陆验证码
		login_capthca = s.get_login_captcha()	
		# 识别验证码
		verification_code = model_handler.predict(login_captcha)	
		# 登陆
		has_login = s.login(verification_code)
	
	# 登陆成功 预定位置
	has_reserved = False	# 当前还未预定,设置为False
	while not has_reserved:
		reserve_captcha = s.get_reserve_captcha()
		verification_code = model_handler.predict(reserve_captcha)
			
		has_reserved = s.reserve_seat(verification_code)

	# 代码运行至此, 我们应该已预定在reserve_information中设定的座位

	
	
	


