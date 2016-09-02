# coding:utf-8

from view import route, url_for, AjaxView


@route('/', name='index')
class Index(AjaxView):
    def get(self):
        a = self.get_body_argument('username')
        print(a)
        self.finish({'code': 0, 'status': 'ready'})

    def post(self):
        #print(self.request.body_arguments)
        a = self.get_argument('username')
        print(a)
        self.finish({'code': 0, 'status': 'ready'})
