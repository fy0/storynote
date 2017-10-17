# coding:utf-8

import re
import config
from view import route, AjaxView, AjaxLoginView
from model.user import User


@route('/api/user/userinfo', name='userinfo')
class UserInfo(AjaxLoginView):
    def get(self):
        user = self.current_user()
        self.finish({'code': 0, 'data': user.to_dict()})


@route('/api/user/password_change', name='password_change')
class PasswordChange(AjaxLoginView):
    def post(self):
        user = self.current_user()
        password = self.get_argument("password", '').strip()
        new_password = self.get_argument("new_password", '').strip()

        if password and password == new_password:
            self.finish({'code': -2})
        elif User.password_change(user.username, password, new_password):
            # 重置密码后需要重新登录
            self.clear_cookie('u')
            self.finish({'code': 0})
        else:
            self.finish({'code': -1})


@route('/api/user/signout', name='signout')
class SignOut(AjaxLoginView):
    def post(self):
        self.clear_cookie('u')
        self.finish({'code': 0, 'msg': '您已成功登出'})


@route('/api/user/signin', name='signin')
class SignIn(AjaxView):
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        remember = self.get_argument('remember', False)

        error_info = []
        u = User.auth(username, password)
        if not u:
            error_info.append("帐号或密码错误")

        if not error_info:
            expires = 30 if remember else None
            self.set_secure_cookie("u", u.key, expires_days=expires)
            return self.finish({'code': 0, 'msg': '登陆成功'})

        return self.finish({'code': -1, 'error_msgs': error_info})


@route('/api/user/signup', name='signup')
class SignUp(AjaxView):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        if not config.USER_ALLOW_SIGNUP:
            return self.finish({'code': -2, 'error_msgs': ['注册已关闭']})

        error_info = []
        if not (config.USERNAME_REG_MIN <= len(username) <= config.USERNAME_REG_MAX):
            error_info.append("用户名长度必须在 %d-%d 之间" % (config.USERNAME_REG_MIN, config.USERNAME_REG_MAX))
        if len(password) < config.PASSWORD_MIN:
            error_info.append("密码长度必须大于等于 %d" % config.PASSWORD_MIN)
        if not re.match('^[a-zA-Z][a-zA-Z0-9]+$', username):
            error_info.append("用户名应为英文与数字的组合，同时首字为英文")
        if User.exist(username):
            error_info.append("用户已存在")

        if not error_info:
            u = User.new(username, password)
            self.set_secure_cookie("u", u.key)
            return self.finish({'code': 0, 'msg': '账户创建成功'})

        return self.finish({'code': -1, 'error_msgs': error_info})

