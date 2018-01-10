# WhulibSeater
Naughty program to crack whulib seat reserving system

# Usage
## 以一个简单的小程序开始这趟旅行
	from studenter import Student
	from modeler import ModelHandler
	
	# 首先创建一个学生对象
	s = Student(id, password)
	s.set_reserve_information(res_information) #设置所要预定的位置信息.res_information是一个包含相关信息的字典
	
	# 创建一个模型对象
	model_handler = ModelHandler()

	# 使用模型来识别验证码
	# 首先导入模型 (假设在当前文件夹下 我们已经有一个训练好的模型,名字是default.pkl)
	model_handler.load_model('default.pkl')
	
	has_login = False # 当前并未登陆
	while not has_login:	
		# 获得登陆验证码
		capthca = s.get_login_captcha()	
		# 识别验证码
		verification_code = model_handler.predict(captcha)	
		# 登陆
		has_login = s.login(verification_code)
	
	# 登陆成功 预定位置
	has_reserved = False	# 当前并未预定成功
	while not has_reserved:
		reserve_captcha = s.get_serve_captcha()
		verification_code = model_handler.predict(reserve_captcha)
			
		has_reserved = s.reserve_seat(verification_code)

	

	
	
	


