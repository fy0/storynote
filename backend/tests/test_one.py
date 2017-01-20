# coding:utf-8

import re
import os
import sys

import time
import unittest
import requests

WEB_PORT = 9000

class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_about(self):
        resp = requests.get('http://127.0.0.1:%s/about' % WEB_PORT)
        self.assertEqual(resp.status_code, 200)

    def test_logout_without_login(self):
        resp = requests.get('http://127.0.0.1:%s/signout' % WEB_PORT)
        self.assertEqual(resp.history[0].status_code, 302)

    def test_sign_up(self):
        url = 'http://127.0.0.1:%s/signup' % WEB_PORT
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

        session = requests.Session()

        # length of username must not be less than 3
        resp = session.get(url)
        xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
        resp = session.post(url, {'username': 'ab', 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
        self.assertTrue(u'用户名长度必须在 3-15 之间' in resp.text)

        # length of username must not be more than 15
        resp = session.get(url)
        xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
        resp = session.post(url, {'username': 'a' * 16, 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
        self.assertTrue(u'用户名长度必须在 3-15 之间' in resp.text)

        # password not same
        resp = session.get(url)
        xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
        resp = session.post(url, {'username': 'abc', 'password': '1234', 'password_again': '12345', '_xsrf': xsrf})
        self.assertTrue(u'两次输入的密码不一致！' in resp.text)

        # success
        resp = session.get(url)
        xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
        resp = session.post(url, {'username': 'abc', 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
        self.assertTrue(u'账户创建成功！' in resp.text)

        # user exists
        resp = session.get(url)
        xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
        resp = session.post(url, {'username': 'abc', 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
        self.assertTrue(u'用户已存在！' in resp.text)


if __name__ == '__main__':
    unittest.main()
