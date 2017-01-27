
import config
from model import pagination
from model.topic import Topic
#from lib import markdown
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
