
import json
import config
from config import RETCODE
from model import pagination
from model.comment import Comment
from model.topic import Topic, TOPIC_STATE
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
        return RETCODE.SUCCESS


@route('/api/manage/user/key_reset')
class UserPasswordReset(UserUtil):
    def work_with_user(self, user):
        user.refresh_key()
        return RETCODE.SUCCESS


@route('/api/manage/user/change_level')
class UserChangeLevel(UserUtil):
    def work_with_user(self, user):
        level = int(self.get_argument('level', 0))
        if level in USER_LEVEL.values():
            user.level = level
            user.save()
            return RETCODE.SUCCESS
        else:
            return RETCODE.INVALID_PARAMS


@route('/api/manage/topic')
class TopicAdminView(AjaxAdminView):
    def get(self):
        page = self.get_argument('p', '1')
        count, query = Topic.get_list()
        pg = pagination(count, query, config.TOPIC_PAGE_SIZE, page)
        pg["items"] = list(map(Topic.to_dict, pg["items"]))
        pg['page_numbers'] = list(pg['page_numbers'])
        self.finish({'code': 0, 'data': pg})


@route('/api/manage/topic/change_state')
class TopicChangeLevel(AjaxAdminView):
    def post(self):
        topic_id = self.get_argument('topic_id', None)
        topic = Topic.get_by_pk(topic_id)
        if topic:
            state = int(self.get_argument('state', 0))
            if state in TOPIC_STATE.values():
                topic.state = state
                topic.save()
                code = RETCODE.SUCCESS
            else:
                code = RETCODE.INVALID_PARAMS
        else:
            code = RETCODE.NOT_FOUND
        self.finish(json.dumps({'code': code}))


@route('/api/manage/comment')
class CommentView(AjaxAdminView):
    def get(self):
        page = self.get_argument('p', '1')
        count, query = Comment.get_list()
        pg = pagination(count, query, config.COMMENT_PAGE_SIZE, page)
        pg["items"] = list(map(Comment.to_dict, pg["items"]))
        pg['page_numbers'] = list(pg['page_numbers'])
        self.finish({'code': 0, 'data': pg})


@route('/api/manage/change_state')
class CommentView(AjaxAdminView):
    def get(self):
        page = self.get_argument('p', '1')
        count, query = Comment.get_list()
        pg = pagination(count, query, config.COMMENT_PAGE_SIZE, page)
        pg["items"] = list(map(Comment.to_dict, pg["items"]))
        pg['page_numbers'] = list(pg['page_numbers'])
        self.finish({'code': 0, 'data': pg})

