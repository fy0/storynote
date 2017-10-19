# coding:utf-8

import config
from model.topic import TOPIC_STATE
from model.user import USER_LEVEL
from view import route, url_for, AjaxView
from qiniu_lite import Cow

from view.authview import AjaxWriterView

cow = Cow(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
policy = cow.get_put_policy(config.QINIU_BUCKET)


@route('/api/qn', name='upload_key')
class UploadTokenView(AjaxWriterView):
    def get(self):
        self.finish({'code': 0, 'data': policy.token()})


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
                'USER_LEVEL': dict(USER_LEVEL.items()),
                'USER_LEVEL_TXT': USER_LEVEL.txt,
                'TOPIC_STATE': dict(TOPIC_STATE.items()),
                'TOPIC_STATE_TXT': TOPIC_STATE.txt,
            }
        })
