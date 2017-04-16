
import config
from model import pagination
from model.topic import Topic
from datetime import datetime
from view import route, AjaxView, AjaxLoginView, url_for


@route('/api/topic/new', name='topic_new')
class TopicNew(AjaxLoginView):
    def post(self):
        title = self.get_argument('title', '').strip()
        content = self.get_argument('content', '').strip()

        if not (title and config.TITLE_LENGTH_MIN <= len(title) <= config.TITLE_LENGTH_MAX):
            self.finish({'code': -1, 'msg': '标题长度必须在 %d 到 %d 之间' % (config.TITLE_LENGTH_MIN, config.TITLE_LENGTH_MAX)})
        else:
            t = Topic.new(title, self.current_user(), content)
            self.finish({'code': 0, 'data': {'id': t.id}})


@route('/api/topic/edit/(\d+)', name='topic_edit')
class TopicEdit(AjaxLoginView):
    def post(self, topic_id):
        title = self.get_argument('title', '').strip()
        content = self.get_argument('content', '').strip()
        topic = Topic.get_by_pk(topic_id)

        if not topic:
            return self.finish({'code': -1, 'msg': '找不到指定的主题'})

        if not topic.can_edit(self.current_user()):
            return self.finish({'code': -2, 'msg': '你没有编辑该主题的权限'})

        if not (title and config.TITLE_LENGTH_MIN <= len(title) <= config.TITLE_LENGTH_MAX):
            self.finish({'code': -1, 'msg': '标题长度必须在 %d 到 %d 之间' % (config.TITLE_LENGTH_MIN, config.TITLE_LENGTH_MAX)})
        else:
            t = topic.edit({"title":title, "content":content}, self.current_user())
            self.finish({'code': 0, 'data': {'id': t.id}})


@route('/api/topic/del/(\d+)', name='topic_del')
class TopicDel(AjaxLoginView):
    def post(self, topic_id):
        topic = Topic.get_by_pk(topic_id)
        if not topic:
            return self.finish({'code': -1, 'msg': '找不到指定的主题'})
        if not topic.can_edit(self.current_user()):
            return self.finish({'code': -2, 'msg': '你没有编辑该主题的权限'})            
        topic.delete()
        self.finish({'code': 0, 'data': {'id': topic.id}})


@route('/api/topic/(\d+)', name='topic')
class TopicView(AjaxView):
    def get(self, topic_id):
        topic = Topic.get_by_pk(topic_id)
        if topic:
            topic.view_count_inc()
            #count, user_topics = Topic.get_list_by_user(topic.user)
            #user_topics = user_topics.limit(10)
            topic = topic.to_dict()
            #topic['content'] = markdown.render(topic['content'])
            self.finish({'code': 0, 'data': topic})
        else:
            self.finish({'code': -1})


@route('/api/recent', name='recent')
class Recent(AjaxView):
    def get(self):
        self.redirect(url_for('recents', 1))


@route('/api/recent/(\d+)', name='recents')
class Recent(AjaxView):
    def get(self, page):
        count, query = Topic.get_list()
        pg = pagination(count, query, config.TOPIC_PAGE_SIZE, page)
        pg["items"] = list(map(Topic.to_dict, pg["items"]))
        pg['page_numbers'] = list(pg['page_numbers'])
        self.finish({'code': 0, 'data': pg})


@route('/api/timeline/(\d+)', name='timeline')
class Timeline(AjaxView):
    def get(self, page):
        count, query = Topic.get_list_order_by_time()
        pg = pagination(count, query, config.TOPIC_PAGE_SIZE, page)
        pg["items"] = list(map(Topic.to_dict, pg["items"]))
        pg['page_numbers'] = list(pg['page_numbers'])

        timeline = {}
        for i in pg['items']:
            dt = datetime.fromtimestamp(i['time'])
            k = dt.strftime('%Y.%m')
            timeline.setdefault(k, [])
            timeline[k].append(i)

        key_order = list(timeline.keys())
        key_order.sort()
        key_order.reverse()
        self.finish({'code': 0, 'data': pg, 'timeline': timeline, 'key_order': key_order})
