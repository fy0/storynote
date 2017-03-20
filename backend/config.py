# coding:utf-8

PORT = 9000
DEBUG = True
PAGE_TITLE = 'single'
TEMPLATE = 'mako'  # jinja2/mako/tornado
DATABASE_URI = "sqlite:///database.db"
COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"
ORIGIN_DOMAIN = 'http://localhost:8080'

USER_ALLOW_SIGNUP = True

TITLE_LENGTH_MIN = 3  # 发表主题的标题最短长度，最少为2
TITLE_LENGTH_MAX = 50  # 发表主题的标题最长长度，最大允许值255

TOPIC_PAGE_SIZE = 20  # 每页主题数量
COMMENT_PAGE_SIZE = 5  # 每页评论数量

TOPIC_BRIEF_LENGTH = 500  # 文章短介绍

try:
    from private import *
except:
    pass
