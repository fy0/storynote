# coding:utf-8

import config
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
            'config': {
                'PAGE_TITLE': config.PAGE_TITLE,
                'TITLE_LENGTH_MIN': config.TITLE_LENGTH_MIN,
                'TITLE_LENGTH_MAX': config.TITLE_LENGTH_MAX,
                'TOPIC_PAGE_SIZE': config.TOPIC_PAGE_SIZE,
                'REPLY_PAGE_SIZE': config.COMMENT_PAGE_SIZE,
            }
        })
