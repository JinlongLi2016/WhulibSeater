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
    """This class represents a student.

    The class represents a student whose main activities are to interacting
    with remote hosts.It contains information of the students, reserving
    seats' information but should never deal with the details of CAPTCHA part.
    All it needs to do is to use APIs of CAPTCHA(model) part.
    """
    def __init__(self, id, password):
        self._id = str(id)
        self._pd = str(password)
        self._reserver = self.__reserver() # whty type should () be?

    def login(self, verification_code):
        req = self.__construct_login_request(verification_code)
        
        # put it in try/except statements in future to deal with exception.
        page = self._reserver.open(req)


        page_returned = page.read().decode('utf-8')
        print(page_returned)
        if "密码与图书馆借书系统密码一致" in page_returned:
            print("password error")
            return False
        else:
            print("passwrod right")
            return True
    
    def collect_captchas(self, num = 2):
        """colloect num of captchas, and save them to disk with with labels"""
        if not os.path.isdir('train_pic'):
            os.mkdir('trian_pic')
        for n in range(num):
            self._reserver = self.__reserver()
            captcha_array = self.get_login_captcha()
            plt.imsave('__t.jpg', captcha_array)
            img = Image.open('__t.jpg')
            img.show()
            verification_code = input("please input the code:")
            fname = verification_code+'.jpg'
            fname = os.path.join('train_pic', fname)

            plt.imsave(fname = fname, arr = captcha_array)
        os.remove('__t.jpg')

    def set_reserve_information(self, seat_information):
        """set reserving seat's information (building, room, seat, time

        Some logic to process bad information may be added in the future.
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
        log_data = {
            'username':self._id,
            'password': self._pd,
            'captcha': verification_code
        }
        log_url = r'http://seat.lib.whu.edu.cn/auth/signIn'
        req = self.__construct_request(url = log_url, data = log_data)
        return req

    def __construct_captcha_request(self):
        cap_url = r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'
        req = self.__construct_request(url = cap_url)
        return req

    def __construct_reserve_request(self, verification_code):
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
        self._reserver.open(req)

    def query(self, query_information):
        """Query available seats

        Query available seats using query_information.

        Return {seat_num: system_seat_id}
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


        
