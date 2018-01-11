# coding: utf-8
# studenter.py

from bs4 import BeautifulSoup
from http import cookiejar
from io import BytesIO
from matplotlib import pyplot as plt
import os
from PIL import Image
from urllib import request, parse

import numpy as np

from modeler import RawDataHandler
from modeler import ModelHandler
 
class Student():
    """This class represents a student to interact with the webpage.

    The class represents a student whose main activities are to interacting
    with remote hosts.It contains information of the students, reserving
    seats' information and should never deal with the details of CAPTCHA part.
    All it needs to do is to use APIs of CAPTCHA(model) part.

    Protected attributes:
    - _id, _pd: id number and password used to log in the websit.
    - _reserver: the object to process dirty interaction with the website,
        Remain the same (meanning you cannot change it)
        when call these methods: "get_login_captcha", "login"
        "get_reserve_captcha" and "reserve_seat", which are activities
        related in one session.Because it handles
        the cookie needed in the seesion with the website automatically.
        In fact, it's an "OpenerDirector" object from urllib.request.
        More actions on cookie may be added in the future to support more
        customized actions like containing two students(id, pd) in one Student
        object and students(id, pd) can be distinguished via cookies.
    - _reserving_information(dict):a dict containing relating information.

    Public methods:
    - get_login_captcha: return log in captcha (in array form) and set
        self._reserver's cookie automaticallyy
    - login: Student() log in using self._reserver, with the same cookie
        setted in self._reserver when Student call get_login_captchain.This
        is the default behaviour.
    - get_reserve_captcha: return the captcha met when reserve a seat
    - reserve_seat: reserve the seat.
    - query: query available seat according to the given "query_information",
        WARNING: to query avaliable seats needs to log in first, so you need to
        log in first(or you the "_reserver" shouldn't been changed when you
        after log in and before query, the same logic as actions on webpage).
        However, cookies valid only in a certain time, meaning you may relog.

    - collect_captchas: a function to collect captchas to train_pic(dir) 
    """
    def __init__(self, id, password):
        self._id = str(id)
        self._pd = str(password)
        self._reserver = self.__reserver() # whty type should () be?

    def login(self, verification_code):
        """self._reserver log in with verification_code

        Student needs to log in first before reserving seat.
        In fact, this function just set cookie, which will be used later to
        reserve seats later, to "_reserver"  
        
        Args:
            verification_code:

        Returns:
            True if login successfully, False if failed
        """
        req = self.__construct_login_request(verification_code)
        
        # put it in try/except statements in future to deal with exception.
        page = self._reserver.open(req)

        page_returned = page.read().decode('utf-8')
        # print(page_returned)
        if "登录失败: 用户名或密码不正确" in page_returned:
            print("password error")
            return False
        elif "验证码错误"in page_returned:
            print("验证码错误")
            return False
        else:
            print("passwrod right")
            return True
    
    def collect_captchas(self, num=2):
        """Collect captcha images in an interacting way (for training model).


        This function should only be called to retrieve captcha images and
        save them to disk with their labels as file names.

        Args:
            num: the number of captchas to save
        """
        if not os.path.isdir('train_pic'):
            os.mkdir('train_pic')
        if not os.path.isdir('wrong_captcha_dir'):
            os.mkdir('wrong_captcha_dir')
        for n in range(num):
            captcha_dir = 'train_pic'

            self._reserver = self.__reserver()
            captcha_array = self.get_login_captcha()

            plt.imsave('__t.jpg', captcha_array)
            img = Image.open('__t.jpg')
            img.show()

            verification_code = input("please input the code:")

            if not self.__check_verification_code(verification_code):
                captcha_dir = 'wrong_captcha_dir'
                print("The last verification is wrong")
                
            fname = verification_code+'.jpg'
            fname = os.path.join(captcha_dir, fname)

            plt.imsave(fname = fname, arr = captcha_array)
        os.remove('__t.jpg')
    
    def __check_verification_code(self, verification_code):
        """Used to check verification code when collecting captchas"""
        flag = self.login(verification_code)
        return flag
        
    def set_reserve_information(self, seat_information):
        """set reserving seat's information (building, room, seat, time)

        Some logic to process bad information may be added in the future.

        Args:
            seat_information: a dict containing relation information in form
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
                some params are optional and can be added later to 
                _reserving_information
        """
        self._reserving_information = seat_information
    
    def __reserver(self):
        cookie = cookiejar.CookieJar()
        ck_pro = request.HTTPCookieProcessor(cookie)
        return request.build_opener(ck_pro)

    def get_login_captcha(self):
        """Retrieve login captcha and return it's corresponding array"""
        req = self.__construct_captcha_request()
        captcha_array = self.__get_captcha(req)

        return captcha_array

    def get_reserve_captcha(self):
        """Retrieve reservving captcha and return it's corresponding array"""
        req = self.__construct_captcha_request()
        captcha_array = self.__get_captcha(req)

        return captcha_array

    def __get_captcha(self, req):
        """Retrieve captcha image(s) for logging or reserving or traing model

        At present, logging and reserving must using self._reserver as
        cookie needing to be dealt with. But this doesn't apply to training.

        return: the req's captcha's corresponding array.
        """
        response = self._reserver.open(req)
        _t = response.read()
        image_array = Image.open(BytesIO(_t))
        image_array = np.array(image_array)
        image_array.dtype = 'uint8'

        return image_array

    # This can be a decrator?
    def __construct_request(self, url, data=None):
        """Construct some types of requests: log, Reserving, request
        CollCAPT requests.

        
        """
        headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/55.0.2883.87 Mobile Safari/537.36',
        'Referer': r'http://seat.lib.whu.edu.cn/login?targetUri=%2F'
        }
        # Referer has some problem? delete?

        if data is None:
            req = request.Request(url, headers = headers)
        else:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, data = data, headers = headers)
        return req
    
    def __construct_login_request(self, verification_code):
        """"""
        log_data = {
            'username':self._id,
            'password': self._pd,
            'captcha': verification_code
        }
        log_url = r'http://seat.lib.whu.edu.cn/auth/signIn'
        req = self.__construct_request(url = log_url, data = log_data)
        return req

    def __construct_captcha_request(self):
        """construct a request to get captcha"""
        cap_url = r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'
        req = self.__construct_request(url = cap_url)
        return req

    def __construct_reserve_request(self, verification_code):
        """construct a request to reserve seat using _reserving_information"""
        if not hasattr(self, "_reserving_information"):
            raise AttributeError("information of seat to be reserved lost")
        
        res_url = r'http://seat.lib.whu.edu.cn/selfRes'
        self._reserving_information['captcha'] = verification_code
        data = parse.urlencode(self._reserving_information).encode('utf-8')

        req = self.__construct_request(url = res_url, data = data)

        return req

    def __construct_query_request(self, query_information):
        """Construct a query request.
    
        query_information:(dict)
        """
        query_url = r'http://seat.lib.whu.edu.cn/freeBook/ajaxSearch'
        data = query_information

        req = self.__construct_request(url = query_url, data = data)

        return req

    def reserve_seat(self, verification_code):
        """reserve a seat using give information(student, seat, captcha)


        """
        req = self.__construct_reserve_request(verification_code)
        # post(get?) the data 
        response = self._reserver.open(req)
        page = response.read().decode('utf-8')

        if "验证码错误" in page or "预约失败!" in page:
            return False
        elif "系统已经为您预定好了" in page:
            return True
        else:
            raise ValueError("Something wrong happens.")
        # any better ways to check?

    def query(self, query_information):
        """Query available seats using query_information.
        
        Args:
            query_inforamtion: a dict containing query informationl
                which takes the form:
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
        
        Returns:
            Dictionay containng avaliable seats in form: {23: 5645}
            23 is seat number which you can get from the table.
            5645 is the seat's system id needed to reserve the seat.
        """
        req = self.__construct_query_request(query_information)
        response = self._reserver.open(req)
        page = response.read().decode('utf-8')

        page = eval(page)

        query_dict = {}
        if page['seatNum'] == 0:
            return {}
        
        seat_str = page['seatStr']
        soup = BeautifulSoup(seat_str, 'lxml')

        for li in soup.find_all('li'):
            seat_id = int(li['id'][5:])
            seat_num = int(li.dl.dt.contents[0])
            query_dict[seat_num] = seat_id

        return query_dict


if __name__ == '__main__':
    s = Student(20202020202020, 123456)

    seadata = {
        'onDate':'2018-1-11',
        'building':'1',
        'room': '8', # special param
        'hour':'null',
        'startMin':'1245',
        'endMin':'1260',
        'power':'null',
        'window':'null',
        'seat': '5243'  # this is a special param
    }
    s.set_reserve_information(seadata)
    dh = RawDataHandler()
    mh = ModelHandler()
    mh.load_model(clf_or_name)

    cap = s.get_login_captcha()
    feas = dh.captcha_to_feas(cap)

    pred = mh.predict(feas)

    s.login(pred)

    # if OK, we can reserve seat now
    feas = s.get_reserve_captcha()
    pred = mh.predict(feas) 
    s.reserve_seat(pred)
    # finish 1 reserving activity

    # How to query avaliable seats?
    seat_data = {
        'onDate':'2018-1-10',
        'building':'1',
        'room': '7',
        'hour':'null',
        'startMin':'1290',
        'endMin':'1320',
        'power':'null',
        'window':'null'
    }
    available_seats = s.query(seat_data)


        
