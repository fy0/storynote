# coding:utf-8

from view import route, AjaxView, AjaxLoginView
from model.user import User


@route('/api/signin', name='signin')
class SignIn(AjaxView):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        remember = self.get_argument('remember', False)

        error_info = []
        u = User.auth(username, password)
        if not u:
            error_info.append("帐号或密码错误！")

        if not error_info:
            expires = 30 if remember else None
            self.set_secure_cookie("u", u.key, expires_days=expires)
            return self.finish({'code': 0, 'msg': '登陆成功！'})

        return self.finish({'code': -1, 'error_msgs': error_info})


@route('/api/userinfo', name='userinfo')
class SignOut(AjaxView):
    def post(self):
        user = self.current_user()
        return self.finish({'code': 0, 'user': user.to_dict() if user else None})


@route('/api/signout', name='signout')
class SignOut(AjaxLoginView):
    def get(self):
        self.clear_cookie('u')
        return self.finish({'code': 0, 'msg': '您已成功登出！'})


@route('/api/signup', name='signup')
class SignUp(AjaxView):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        error_info = []
        if not (2 <= len(username) <= 15):
            error_info.append("用户名长度必须在 2-15 之间")
        if len(password) < 3:
            error_info.append("密码长度必须大于等于3")
        if User.exist(username):
            error_info.append("用户已存在")

        if not error_info:
            u = User.new(username, password)
            return self.finish({'code': 0, 'msg': '账户创建成功'})

        print(error_info)
        return self.finish({'code': -1, 'error_msgs': error_info})
