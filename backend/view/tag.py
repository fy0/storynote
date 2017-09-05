import config
from config import RETCODE
from model import pagination
from model.topic import Topic
from view import route, AjaxView, AjaxLoginView
from model.tag import TagDefine, Tag
from view.authview import AjaxWriterView


@route('/api/tag/define')
class TagDefineView(AjaxWriterView):
    def post(self):
        name = self.get_argument('name')
        desc = self.get_argument('desc', '').strip()
        td = TagDefine.new(name, desc)
        if td:
            self.finish({'code': RETCODE.SUCCESS})
        else:
            self.finish({'code': RETCODE.ALREADY_EXISTS})


@route('/api/tag/list')
class TagListView(AjaxView):
    def get(self):
        self.finish({'code': RETCODE.SUCCESS, 'data': list(map(TagDefine.to_dict, TagDefine.get_list()))})


@route('/api/tag/get_topics_by_tag')
class TagListView(AjaxView):
    def get(self):
        tag_name = self.get_argument('tag_name')
        count, query = Tag.get_topics_by_tagname(tag_name)

        if not query:
            return self.finish({'code': RETCODE.NOT_FOUND})

        pg = pagination(count, query, config.TOPIC_PAGE_SIZE, 1)
        items = []
        for i in pg["items"]:
            items.append({
                'time': i.time,
                'data': i.object.to_dict()
            })

        pg["items"] = items
        self.finish({'code': RETCODE.SUCCESS, 'data': pg})


@route('/api/tag/add_to_topic')
class TagAddTo(AjaxWriterView):
    def post(self):
        tag_name = self.get_argument('tag_name')
        topic_id = self.get_argument('topic_id')
        add_tag_if_not_exist = self.get_argument('add_tag_if_not_exist', False)

        td = TagDefine.get_by_pk(tag_name)
        topic = Topic.get_by_pk(topic_id)

        # 文章存在检测
        if not topic:
            return self.finish({'code': RETCODE.NOT_FOUND})

        # 自动创建标签的一种情况
        if not td and add_tag_if_not_exist:
            td = TagDefine.new(tag_name, '')

        # 标签不存在
        if not td:
            return self.finish({'code': RETCODE.NOT_FOUND})

        if not topic.can_edit(self.current_user()):
            return self.finish({'code': RETCODE.PERMISSION_DENIED})

        tag = Tag.new_by_topic(topic, td)
        if tag:
            self.finish({'code': RETCODE.SUCCESS, 'data': tag.to_dict()})
        else:
            self.finish({'code': RETCODE.ALREADY_EXISTS})


@route('/api/tag/remove_from_topic')
class TagRemoveFrom(AjaxWriterView):
    def post(self):
        tag_name = self.get_argument('tag_name')
        topic_id = self.get_argument('topic_id')

        td = TagDefine.get_by_pk(tag_name)
        topic = Topic.get_by_pk(topic_id)

        if not td or not topic:
            return self.finish({'code': RETCODE.NOT_FOUND})

        if not topic.can_edit(self.current_user()):
            return self.finish({'code': RETCODE.PERMISSION_DENIED})

        tag = Tag.get_by_topic_and_tag_define(topic, td)
        if tag:
            tag.delete_instance()
            self.finish({'code': RETCODE.SUCCESS})
        else:
            self.finish({'code': RETCODE.NOT_FOUND})


@route('/api/tag/remove_from_post_by_id')
class TagRemoveById(AjaxWriterView):
    def post(self):
        tid = self.get_argument('id')
        tag = Tag.get_by_pk(tid)

        if tag:
            if type(tag.object) == Topic:
                if tag.object.can_edit(self.current_user()):
                    tag.delete_instance()
                    self.finish({'code': RETCODE.SUCCESS})
                else:
                    return self.finish({'code': RETCODE.PERMISSION_DENIED})
            else:
                self.finish({'code': RETCODE.PERMISSION_DENIED})
        else:
            self.finish({'code': RETCODE.NOT_FOUND})

