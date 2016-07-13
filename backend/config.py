# coding:utf-8

PORT = 9000
DEBUG = True
TITLE = 'single'
TEMPLATE = 'mako'  # jinja2/mako/tornado
DATABASE_URI = "sqlite:///database.db"
COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

TITLE_LENGTH_MIN = 5  # 发表主题的标题最短长度
TITLE_LENGTH_MAX = 50  # 发表主题的标题最长长度

TOPIC_PAGE_SIZE = 20  # 每页主题数量
REPLY_PAGE_SIZE = 30  # 每页评论数量

try:
    from private import *
except:
    pass
