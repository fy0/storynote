# coding:utf-8

import re
import os
import sys

import time
import unittest
import requests

HOST = '127.0.0.1'
WEB_PORT = 9000

def uescape(text):
    return str(bytes(text, 'utf-8'), 'unicode-escape')


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # register first account (admin account)
        url = 'http://%s:%s/api/signup' % (HOST, WEB_PORT)
        resp = requests.post(url, {'username': 'test', 'password': '1234'})

    @classmethod
    def tearDownClass(cls):
        pass

    def test_about(self):
        #resp = requests.get('http://%s:%s/about' % (HOST, WEB_PORT))
        #self.assertEqual(resp.status_code, 200)
        pass

    def test_logout_without_login(self):
        #resp = requests.get('http://%s:%s/signout' % (HOST, WEB_PORT))
        #self.assertEqual(resp.history[0].status_code, 302)
        pass

    def test_sign_up(self):
        url = 'http://%s:%s/api/signup' % (HOST, WEB_PORT)

        # length of username must not be less than 2
        resp = requests.post(url, {'username': 'a', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名长度必须在 2-15 之间' in uescape(resp.text))

        # length of username must not be more than 15
        resp = requests.post(url, {'username': 'a' * 16, 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名长度必须在 2-15 之间' in uescape(resp.text))
        
        # username matches '^[a-zA-Z][a-zA-Z0-9]+$'
        resp = requests.post(url, {'username': '测试', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名应为英文与数字的组合，同时首字为英文' in uescape(resp.text))      

        resp = requests.post(url, {'username': '12', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名应为英文与数字的组合，同时首字为英文' in uescape(resp.text))        

        # success
        resp = requests.post(url, {'username': 'ab', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'账户创建成功' in uescape(resp.text))

        # user exists
        resp = requests.post(url, {'username': 'ab', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户已存在' in uescape(resp.text))

    def test_sign_in(self):
        url = 'http://%s:%s/api/signin' % (HOST, WEB_PORT)
        
        # wrong password
        resp = requests.post(url, {'username': 'test', 'password': '123*'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['code'], -1)
        self.assertTrue('帐号或密码错误' in data['error_msgs'])

        # username too short
        resp = requests.post(url, {'username': 'u', 'password': '123*'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['code'], -1)
        self.assertTrue('帐号或密码错误' in data['error_msgs'])

        # user isn't exists
        resp = requests.post(url, {'username': 'unotexist', 'password': '123*'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['code'], -1)
        self.assertTrue('帐号或密码错误' in data['error_msgs'])
        
        # lost parameters
        resp = requests.post(url, {})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['code'], -1)
        self.assertTrue('帐号或密码错误' in data['error_msgs'])        

        # right user
        resp = requests.post(url, {'username': 'test', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['msg'], '登陆成功')

    def test_userinfo(self):
        url_signin = 'http://%s:%s/api/signin' % (HOST, WEB_PORT)
        url_userinfo = 'http://%s:%s/api/userinfo' % (HOST, WEB_PORT)

        # without signin
        resp = requests.get(url_userinfo)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -255)

        # signin and check again
        session = requests.Session()
        resp = session.post(url_signin, {'username': 'test', 'password': '1234'})
        resp = session.get(url_userinfo)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['user']['username'], 'test')

    def test_signout(self):
        url_signin = 'http://%s:%s/api/signin' % (HOST, WEB_PORT)
        url_signout = 'http://%s:%s/api/signout' % (HOST, WEB_PORT)
        url_userinfo = 'http://%s:%s/api/userinfo' % (HOST, WEB_PORT)
        session = requests.Session()

        resp = session.post(url_signin, {'username': 'test', 'password': '1234'})
        resp = session.get(url_userinfo)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

        resp = session.post(url_signout)
        resp = session.get(url_userinfo)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -255)

    def test_password_change(self):
        url_signin = 'http://%s:%s/api/signin' % (HOST, WEB_PORT)
        url_pwchange = 'http://%s:%s/api/password_change' % (HOST, WEB_PORT)
        url_userinfo = 'http://%s:%s/api/userinfo' % (HOST, WEB_PORT)
        session = requests.Session()

        # without signin
        resp = requests.post(url_pwchange, {'password': '1234', 'new_password': '1230'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -255)

        # sign in
        resp = session.post(url_signin, {'username': 'test', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

        # change with wrong password
        resp = session.post(url_pwchange, {'password': '123', 'new_password': '123.'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -1)

        # change without params
        resp = session.post(url_pwchange, {})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -1)

        # change with same old and new password
        resp = session.post(url_pwchange, {'password': '1234', 'new_password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -2)

        # change
        resp = session.post(url_pwchange, {'password': '1234', 'new_password': '123X'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

        # already signout
        resp = session.get(url_userinfo)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -255)
        
        # signin and change password back
        resp = session.post(url_signin, {'username': 'test', 'password': '123X'})
        resp = session.post(url_pwchange, {'password': '123X', 'new_password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)


if __name__ == '__main__':
    unittest.main()
