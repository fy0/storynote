# coding:utf-8

from view import route, url_for, View


@route('/', name='index')
class Index(View):
    def get(self):
        self.render()
