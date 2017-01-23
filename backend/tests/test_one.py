# coding:utf-8

import re
import os
import sys

import time
import unittest
import requests

WEB_PORT = 9000

def uescape(text):
    return str(bytes(text, 'utf-8'), 'unicode-escape')


class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_about(self):
        #resp = requests.get('http://127.0.0.1:%s/about' % WEB_PORT)
        #self.assertEqual(resp.status_code, 200)
        pass

    def test_logout_without_login(self):
        #resp = requests.get('http://127.0.0.1:%s/signout' % WEB_PORT)
        #self.assertEqual(resp.history[0].status_code, 302)
        pass

    def test_sign_up(self):
        url = 'http://127.0.0.1:%s/api/signup' % WEB_PORT

        # length of username must not be less than 2
        resp = requests.post(url, {'username': 'a', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名长度必须在 2-15 之间' in uescape(resp.text))

        # length of username must not be more than 15
        resp = requests.post(url, {'username': 'a' * 16, 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名长度必须在 2-15 之间' in uescape(resp.text))

        # success
        resp = requests.post(url, {'username': 'ab', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'账户创建成功' in uescape(resp.text))

        # user exists
        resp = requests.post(url, {'username': 'ab', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户已存在' in uescape(resp.text))


if __name__ == '__main__':
    unittest.main()
