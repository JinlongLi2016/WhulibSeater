# coding: utf-8
# 
# this script tests Student log-in and query seats ability.
# If pass this test, then Student can log and querey.

import matplotlib.pyplot as plt
from studenter import Student
import pd as _pd
if __name__ == '__main__':
    s = Student(_pd.my_info['id'], _pd.my_info['pd'])

    seadata = {
        'onDate':'2018-1-10',
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

    cap = s.get_login_captcha()
    print(type(cap), cap.shape)# cap: ndarray (70, 160, 4)
    plt.imshow(cap)
    plt.show()
    ver_code = input("input code")

    s.login(ver_code)

    # seadata :waiting
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
    s.query(seat_data)