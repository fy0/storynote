
import config
from model import pagination
from model.topic import Topic
from view import route, AjaxView, AjaxLoginView, url_for


@route('/api/topic/new', name='topic_new')
class TopicNew(AjaxLoginView):
    def post(self):
        title = self.get_argument('title', '').strip()
        content = self.get_argument('content', '').strip()
        if title and config.TITLE_LENGTH_MIN <= len(title) <= config.TITLE_LENGTH_MAX:
            t = Topic.new(title, self.current_user() or 0, content)
            self.redirect(url_for('topic', t.id))
            self.finish({'code': 0, 'topic': {'id': t.id}})
        else:
            # 非标准提交
            self.finish({'code': -1})


@route('/api/topic/(\d+)', name='topic')
class TopicPage(AjaxLoginView):
    def get(self, topic_id):
        topic = Topic.get_by_pk(topic_id)
        if topic:
            topic.view_count_inc()
            #count, user_topics = Topic.get_list_by_user(topic.user)
            #user_topics = user_topics.limit(10)
            self.finish({'code': 0, 'topic': topic.to_dict()})
        else:
            self.finish({'code': -1})


@route('/api/recent', name='recent')
class Recent(AjaxView):
    def get(self):
        page = self.get_argument('p', '1')
        count, query = Topic.get_list()
        pg = pagination(count, query, config.TOPIC_PAGE_SIZE, page)
        pg["items"] = list(map(Topic.to_dict, pg["items"]))
        pg['page_numbers'] = list(pg['page_numbers'])
        self.finish({'code': 0, 'data': pg})
