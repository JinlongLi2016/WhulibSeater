# standard_usage.py
from studenter import Student
from modeler import ModelHandler, RawDataHandler
import time
import matplotlib.pyplot as plt 

reserve_information = {
	'onDate':'2018-01-16',# which date 
	'building':'1',      # which building?  1:信图
	'room': '4',         # which room? 7: 二楼东
	'hour':'null',
	'startMin':'1290',   # 1305 for 21:45 
	'endMin':'1320',     # 1320 for 22:00 as 1320/60 = 22
	'power':'null',
	'window':'null',
	# which exact seat you want to reserve.This is the id in
	# the system which you can get via "query" method. 
	'seat': '2612'  #这个数据在测试的时候可以减去30(随便说的)以内的任何一个数
			#系统也会有对应的位置
}

print("you need to change id and password")
# 创建一个学生对象 (处理和网页交互)
id = '2018302513284'
password = '0817027'
s = Student(id, password)
s.set_reserve_information(reserve_information) #设置所要预定的位置信息.reserve_information是一个含有与预定相关的信息的字典

# 创建一个处理数据对象和一个处理模型的对象(识别验证码)
data_handler = RawDataHandler()
model_handler = ModelHandler()

# 该对象需要导入模型 (假设在当前文件夹下 已经有一个训练好的模型,名字是default.pkl)
model_handler.load_model('default.pkl', data_handler = data_handler) # data_handler传入,获得图片到特征的一些参数

wait_time = 1.5
count = 0
# 开始登陆网页
has_login = False 	# 当前还未登陆,设置为False
while (not has_login) and count < 3:
	time.sleep(wait_time) # 等待几秒钟...防止被封号
	count += 1
	# 获得登陆验证码
	login_capthca = s.get_login_captcha()

	# 将login_captcha转换为模型可以处理的特征
	feature = data_handler.captcha_to_feas(login_capthca)# 根据前面获得参数,按照训练模型时图片转为特征的方式，将图片转为特征
	# 识别验证码
	verification_code = model_handler.predict_captcha(feature)
	
	print(verification_code)
	# 登陆
	has_login = s.login(verification_code)

if count == 3 and (not has_login):
	raise ValueError("Failed to log in! Need a better model ...")

count = 0

query_information = {
	'onDate':'2018-01-16',
	'building':'1',
	'room': '5',
	'hour':'null',
	'startMin':'1290',
	'endMin':'1320',
	'power':'null',
	'window':'null'
}

# 登陆成功 预定位置
has_reserved = False	# 当前还未预定,设置为False
while (not has_reserved) and count < 3:
	time.sleep(wait_time) 

	count += 1
	s.query(query_information)

	time.sleep(wait_time)

	reserve_captcha = s.get_reserve_captcha()
	
	feature = data_handler.captcha_to_feas(reserve_captcha)
	verification_code = model_handler.predict_captcha(feature)

	print(verification_code)
	has_reserved = s.reserve_seat(verification_code)

if has_reserved:
	print("Succeeded reserving seat!")
	# 代码运行至此, 我们应该已预定在reserve_information中设定的座位
else:
	print("Failed as model's failure in decoding captchas\
		three times consecutively")