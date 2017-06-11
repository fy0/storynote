
import json
import config
from config import RETCODE
from model import pagination
from view import route, AjaxView, AjaxLoginView
from model.user import User, USER_LEVEL
from view.authview import AjaxAdminView


@route('/api/manage/user')
class UserAdminView(AjaxAdminView):
    def get(self):
        keyword = self.get_argument('keyword', '').strip()
        page = self.get_argument('p', '1')
        if keyword:
            count, query = User.get_list_search(keyword)
        else:
            count, query = User.get_list()
        pg = pagination(count, query, config.TOPIC_PAGE_SIZE, page)

        pg["items"] = list(map(User.to_dict, pg["items"]))
        pg['page_numbers'] = list(pg['page_numbers'])
        self.finish({'code': RETCODE.SUCCESS, 'data': pg})


class UserUtil(AjaxAdminView):
    def post(self):
        user_id = self.get_argument('user_id', None)
        user = User.get_by_pk(user_id)
        if user:
            code = self.work_with_user(user)
        else:
            code = RETCODE.NOT_FOUND
        self.finish(json.dumps({'code': code}))

    def work_with_user(self, user):
        return RETCODE.SUCCESS


@route('/api/manage/user/password_reset')
class UserPasswordReset(UserUtil):
    def work_with_user(self, user):
        password = self.get_argument('new_password', None)
        if not password:
            return RETCODE.INVALID_PARAMS
        elif len(password) < config.PASSWORD_MIN:
            return RETCODE.TOO_SHORT
        else:
            user.set_password(password)
            self.clear_cookie('u')
        return RETCODE.SUCCESS


@route('/api/manage/user/key_reset')
class UserPasswordReset(UserUtil):
    def work_with_user(self, user):
        user.refresh_key()
        return RETCODE.SUCCESS


@route('/api/manage/user/change_level/del')
class UserDel(UserUtil):
    def work_with_user(self, user):
        user.level = USER_LEVEL.DEL
        user.save()
        return RETCODE.SUCCESS


@route('/api/manage/user/change_level/ban')
class UserBan(UserUtil):
    def work_with_user(self, user):
        user.level = USER_LEVEL.BAN
        user.save()
        return RETCODE.SUCCESS


@route('/api/manage/user/change_level/normal')
class UserNormal(UserUtil):
    def work_with_user(self, user):
        user.level = USER_LEVEL.NORMAL
        user.save()
        return RETCODE.SUCCESS


@route('/api/manage/user/change_level/writer')
class UserWriter(UserUtil):
    def work_with_user(self, user):
        user.level = USER_LEVEL.WRITER
        user.save()
        return RETCODE.SUCCESS


@route('/api/manage/user/change_level/admin')
class UserAdmin(UserUtil):
    def work_with_user(self, user):
        user.level = USER_LEVEL.ADMIN
        user.save()
        return RETCODE.SUCCESS

