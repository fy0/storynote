# coding:utf-8

import config
from model.topic import Topic
from view import route, url_for, View, AjaxView
from model.reply import Reply


@route('/api/reply/(\d+)', name="reply")
class ReplyView(AjaxView):
    def get(self, relate_id):
        page = self.get_argument('page', '1')
        if not page.isdigit():
            return self.finish({'code': -1})

        offset = (int(page)-1)*config.REPLY_PAGE_SIZE
        reply_count, replies = Reply.get_list(relate_id, offset=offset)
        
        self.finish({'code': 0, 'data': {
            'items': list(replies),
            'count': reply_count,
        }})

    def post(self, relate_id):
        code, msg = self.reply(relate_id)
        if code == 0:
            self.finish({'code': code, 'msg': msg, 'data': {'id': self._r.id}})
        else:
            self.finish({'code': code, 'msg': msg})

    def reply(self, relate_id):
        # 1. 发送评论必须登录
        if not self.current_user():
            return -255, '请先登录后再做此操作'

        content = self.get_argument('content', '').strip()
        send_to_id = self.get_argument('send_to', '').strip()

        # 3. 正文必须存在
        if not content:
            return -3, '请输入内容'

        # 4. 正文不能超过 4096 字
        if len(content) > 4096:
            return -4, '评论不能超过4096字'

        # 5. 如果指定了父级评论，那么父级评论必须存在
        if not send_to_id:
            send_to_id = None

        if send_to_id and not Reply.exists(send_to_id, relate_id):
            return -5, '无法回复一条不存在的评论' # 间接地，只允许一级楼中楼，而不允许楼中楼中楼等

        # 6. relate_id 存在检查
        t = Topic.get_by_pk(relate_id)
        if not t:
            return -6, '你试图评论一个不存在的主题'

        # 7. 存入数据库
        r = Reply.new(relate_id, self.current_user(), content, send_to_id)
        self._r = r
        return 0, '评论发送成功'
