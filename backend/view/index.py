# coding:utf-8

import config
from model.user import USER_LEVEL
from view import route, url_for, AjaxView


@route('/', name='index')
class IndexView(AjaxView):
    def get(self):
        self.finish({'code': 0, 'status': 'ready'})

    def post(self):
        self.finish({'code': 0, 'status': 'ready'})


@route('/api/misc', name='misc')
class MiscView(AjaxView):
    def get(self):
        self.finish({
            'code': 0,
            'data': {
                'PAGE_TITLE': config.PAGE_TITLE,
                'TITLE_LENGTH_MIN': config.TITLE_LENGTH_MIN,
                'TITLE_LENGTH_MAX': config.TITLE_LENGTH_MAX,
                'TOPIC_PAGE_SIZE': config.TOPIC_PAGE_SIZE,
                'COMMENT_PAGE_SIZE': config.COMMENT_PAGE_SIZE,
                'USERNAME_MIN': config.USERNAME_MIN,
                'USERNAME_MAX': config.USERNAME_MAX,
                'USERNAME_REG_MIN': config.USERNAME_REG_MIN,
                'USERNAME_REG_MAX': config.USERNAME_REG_MAX,
                'PASSWORD_MIN': config.PASSWORD_MIN,
                'PASSWORD_MAX': config.PASSWORD_MAX,
                'PASSWORD_REG_MIN': config.PASSWORD_REG_MIN,
                'PASSWORD_REG_MAX': config.PASSWORD_REG_MAX,
                'USER_LEVEL': USER_LEVEL.txt,
            }
        })
