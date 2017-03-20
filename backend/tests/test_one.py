# coding:utf-8

import re
import os
import sys

import time
import unittest
import requests

config = {}
HOST = '127.0.0.1'
WEB_PORT = 9000

url_misc = 'http://%s:%s/api/misc' % (HOST, WEB_PORT)
url_signin = 'http://%s:%s/api/user/signin' % (HOST, WEB_PORT)
url_signup = 'http://%s:%s/api/user/signup' % (HOST, WEB_PORT)
url_signout = 'http://%s:%s/api/user/signout' % (HOST, WEB_PORT)
url_userinfo = 'http://%s:%s/api/user/userinfo' % (HOST, WEB_PORT)
url_pwchange = 'http://%s:%s/api/user/password_change' % (HOST, WEB_PORT)

url_topic = 'http://%s:%s/api/topic/%%s' % (HOST, WEB_PORT)
url_topic_new = 'http://%s:%s/api/topic/new' % (HOST, WEB_PORT)
url_topic_edit = 'http://%s:%s/api/topic/edit/%%s' % (HOST, WEB_PORT)
url_topic_del = 'http://%s:%s/api/topic/del/%%s' % (HOST, WEB_PORT)

url_comment = 'http://%s:%s/api/comment/%%s' % (HOST, WEB_PORT)
url_comment_del = 'http://%s:%s/api/comment/del/%%s' % (HOST, WEB_PORT)

url_recent = 'http://%s:%s/api/recent/%%s' % (HOST, WEB_PORT)
url_recent2 = 'http://%s:%s/api/recent' % (HOST, WEB_PORT)


def uescape(text):
    return str(bytes(text, 'utf-8'), 'unicode-escape')


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # register first account (admin account)
        resp = requests.post(url_signup, {'username': 'test', 'password': '1234'})
        resp = requests.post(url_signup, {'username': 'test2', 'password': '1234'})

        global config
        config = requests.get(url_misc).json()['config']

    @classmethod
    def tearDownClass(cls):
        pass

    def test_index(self):
        resp = requests.get('http://%s:%s/' % (HOST, WEB_PORT))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)

    def test_sign_up(self):
        # length of username must not be less than 2
        resp = requests.post(url_signup, {'username': 'a', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名长度必须在 2-15 之间' in uescape(resp.text))

        # length of username must not be more than 15
        resp = requests.post(url_signup, {'username': 'a' * 16, 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名长度必须在 2-15 之间' in uescape(resp.text))

        # username matches '^[a-zA-Z][a-zA-Z0-9]+$'
        resp = requests.post(url_signup, {'username': '测试', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名应为英文与数字的组合，同时首字为英文' in uescape(resp.text))

        resp = requests.post(url_signup, {'username': '12', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户名应为英文与数字的组合，同时首字为英文' in uescape(resp.text))

        # success
        resp = requests.post(url_signup, {'username': 'ab', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'账户创建成功' in uescape(resp.text))

        # user exists
        resp = requests.post(url_signup, {'username': 'ab', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(u'用户已存在' in uescape(resp.text))

    def test_sign_in(self):
        # wrong password
        resp = requests.post(url_signin, {'username': 'test', 'password': '123*'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -1)
        self.assertTrue('帐号或密码错误' in info['error_msgs'])

        # username too short
        resp = requests.post(url_signin, {'username': 'u', 'password': '123*'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -1)
        self.assertTrue('帐号或密码错误' in info['error_msgs'])

        # user isn't exists
        resp = requests.post(url_signin, {'username': 'unotexist', 'password': '123*'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -1)
        self.assertTrue('帐号或密码错误' in info['error_msgs'])

        # lost parameters
        resp = requests.post(url_signin, {})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -1)
        self.assertTrue('帐号或密码错误' in info['error_msgs'])

        # right user
        resp = requests.post(url_signin, {'username': 'test', 'password': '1234'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertEqual(info['msg'], '登陆成功')

    def test_userinfo(self):
        # without signin
        resp = requests.get(url_userinfo)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -255)

        # signin and check again
        session = requests.Session()
        resp = session.post(url_signin, {'username': 'test', 'password': '1234'})
        resp = session.get(url_userinfo)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertEqual(info['data']['username'], 'test')

    def test_signout(self):
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

    def test_misc(self):
        resp = requests.get(url_misc)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertTrue(info['config']['PAGE_TITLE'])
        self.assertTrue(info['config']['TITLE_LENGTH_MIN'])
        self.assertTrue(info['config']['TITLE_LENGTH_MAX'])
        self.assertTrue(info['config']['TOPIC_PAGE_SIZE'])
        self.assertTrue(info['config']['REPLY_PAGE_SIZE'])

    def test_topic(self):
        # get config
        config = requests.get(url_misc).json()['config']

        # sign in
        session = requests.Session()
        resp = session.post(url_signin, {'username': 'test', 'password': '1234'})

        # too short topic title
        resp = session.post(url_topic_new, {'title': 'a' * (config['TITLE_LENGTH_MIN'] - 1), 'content': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -1)

        # too long topic title
        resp = session.post(url_topic_new, {'title': 'a' * (config['TITLE_LENGTH_MAX'] + 1), 'content': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -1)

        # new topic
        resp = session.post(url_topic_new, {'title': 'a' * (config['TITLE_LENGTH_MIN']), 'content': 'topic 1'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        topic1 = info['data']['id']

        val = int((config['TITLE_LENGTH_MIN'] + config['TITLE_LENGTH_MAX']) / 2)
        resp = session.post(url_topic_new, {'title': 'a' * val, 'content': 'topic 2'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        topic2 = info['data']['id']

        resp = session.post(url_topic_new, {'title': 'a' * (config['TITLE_LENGTH_MAX']), 'content': 'topic 3'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        topic3 = info['data']['id']

        # read topic
        resp = requests.get(url_topic % topic1)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertEqual(info['data']['id'], topic1)
        self.assertTrue(info['data']['title'])
        self.assertEqual('topic 1', info['data']['content'])

        resp = requests.get(url_topic % topic2)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertEqual(info['data']['id'], topic2)
        self.assertTrue(info['data']['title'])
        self.assertEqual('topic 2', info['data']['content'])

        resp = requests.get(url_topic % topic3)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertEqual(info['data']['id'], topic3)
        self.assertTrue(info['data']['title'])
        self.assertEqual('topic 3', info['data']['content'])

        resp = requests.get(url_topic % 0)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -1)

        # topic edit
        resp = session.post(url_topic_edit % topic3,
                            {'title': 'a' * (config['TITLE_LENGTH_MIN']), 'content': 'topic 233'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)

        # edit - success
        resp = requests.get(url_topic % topic3)
        info = resp.json()
        self.assertEqual('a' * config['TITLE_LENGTH_MIN'], info['data']['title'])
        self.assertEqual('topic 233', info['data']['content'])

        # edit - topic not found
        resp = session.post(url_topic_edit % 0, {'title': 'a' * (config['TITLE_LENGTH_MIN']), 'content': 'topic 233'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -1)

        # edit - others
        session2 = requests.Session()
        resp = session2.post(url_signup, {'username': 'author', 'password': '5678'})
        resp = session2.post(url_topic_new, {'title': 'a' * (config['TITLE_LENGTH_MAX']), 'content': 'topic 3'})
        info = resp.json()
        topic_other = info['data']['id']

        resp = session.post(url_topic_edit % topic_other,
                            {'title': 'a' * (config['TITLE_LENGTH_MIN']), 'content': 'topic 233'})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -2)

        # recent
        resp = requests.get(url_recent % 1)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertTrue(info['data']['page_numbers'])
        self.assertTrue(len(info['data']['items']) > 0)

        resp = requests.get(url_recent2)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertTrue(info['data']['page_numbers'])
        self.assertTrue(len(info['data']['items']) > 0)

        resp = requests.get(url_recent % 2)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        self.assertTrue(info['data']['page_numbers'])
        self.assertTrue(len(info['data']['items']) == 0)

        resp = requests.get(url_recent % 'test')
        self.assertEqual(resp.status_code, 404)

        # delete - not found
        resp = session.post(url_topic_del % 0)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -1)

        # delete - others
        resp = session2.post(url_topic_del % topic3)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], -2)

        # delete - success
        resp = session.post(url_topic_del % topic3)
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)

        # 40 topics
        for i in range(1, 41):
            resp = session.post(url_topic_new, {'title': '文章标题 %d' % i, 'content': ('topic %d\n\n' % i) * 100})

    def test_comment(self):
        # signin and send topic
        session = requests.Session()
        resp = session.post(url_signin, {'username': 'test', 'password': '1234'})
        resp = session.post(url_topic_new, {'title': 'a' * config['TITLE_LENGTH_MIN'], 'content': 'topic test'})
        topic_id = resp.json()['data']['id']

        # without signin
        resp = requests.post(url_comment % topic_id, {'content': '123'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -255)

        # empty content
        resp = session.post(url_comment % topic_id, {'content': '  \n '})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -3)

        # too long comment (4096)
        resp = session.post(url_comment % topic_id, {'content': '测' * 4097})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -4)

        # wrong topic id
        resp = session.post(url_comment % 0, {'content': '123'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -6)

        # success
        resp = session.post(url_comment % topic_id, {'content': '测' * 4096})
        self.assertEqual(resp.status_code, 200)
        info = resp.json()
        self.assertEqual(info['code'], 0)
        rid = info['data']['id']

        # reply a comment which not exists
        # resp = session.post(url_reply % rid, {'content': '123', 'send_to_id': 0})
        # self.assertEqual(resp.status_code, 200)
        # self.assertEqual(resp.json()['code'], -5)

        # resp = session.post(url_reply % rid, {'content': '123', 'send_to_id': 'test'})
        # self.assertEqual(resp.status_code, 404)

        # success
        # resp = session.post(url_reply % 0, {'content': '123', 'send_to_id': rid})
        # self.assertEqual(resp.status_code, 200)
        # info = resp.json()
        # self.assertEqual(info['code'], 0)

        # delete
        resp = session.post(url_comment_del % 0)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -1)

        session2 = requests.Session()
        resp = session2.post(url_signin, {'username': 'test2', 'password': '1234'})
        resp = session2.post(url_comment_del % rid)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], -2)

        resp = session.post(url_comment_del % rid)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 0)


if __name__ == '__main__':
    unittest.main()
