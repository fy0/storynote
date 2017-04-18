# coding:utf-8
import time
import config
from peewee import *
from model import db, BaseModel
from model.tag import Tag
from model.user import User
from lib.state_obj import StateObject
from playhouse.gfk import ReverseGFK


class TOPIC_STATE(StateObject):
    DEL = 0
    HIDE = 10
    CLOSE = 30 # 禁止回复
    NORMAL = 50

    txt = {DEL: "删除", HIDE: "隐藏", CLOSE:"关闭", NORMAL:"正常"}

TOPIC_STATE.init()


class Topic(BaseModel):
    title = CharField(index=True, max_length=255)
    user = ForeignKeyField(User, index=True)
    time = BigIntegerField(index=True)
    state = IntegerField(default=TOPIC_STATE.NORMAL, index=True)

    edit_time = BigIntegerField(index=True, null=True)
    last_edit_user = ForeignKeyField(User, related_name="last_edit_user_id", null=True)
    view_count = IntegerField(default=0)
    brief = CharField(max_length=500)
    content = CharField(max_length=50000)
    tags = ReverseGFK(Tag, 'obj_type', 'obj_id')

    sticky_weight = IntegerField(index=True, default=0)  # 置顶权重
    weight = IntegerField(index=True, default=0) # 排序权值，越大越靠前，默认权重与id相同

    class Meta:
        db_table = 'topics'

    def can_edit(self, user):
        if self.user == user:
            return True

    def edit(self, data, user):
        if 'title' in data:
            self.title = data['title']
        if 'content' in data:
            self.content = data['content']
            self.brief = data['content'][:config.TOPIC_BRIEF_LENGTH]
        self.last_edit_user = user
        self.edit_time = int(time.time())
        self.save()
        return self

    def delete(self):
        self.state = TOPIC_STATE.DEL
        self.save()

    @property
    def reply_count(self):
        from model.comment import Comment
        return Comment.get_count(self.id)

    @classmethod
    def new(cls, title, user, content=None):
        with db.atomic():
            ret = cls.create(title=title, user=user, time=int(time.time()), content=content, brief=content[:config.TOPIC_BRIEF_LENGTH])
            ret.weight = ret.id
            ret.save()
        return ret

    @classmethod
    def get_list(cls):
        q = cls.select().where(cls.state>TOPIC_STATE.HIDE).order_by(cls.weight.desc(), cls.time.desc())
        return q.count(), q

    @classmethod
    def get_list_order_by_time(cls, state=-1):
        if state == -1:
            q = cls.select().where(cls.state>TOPIC_STATE.HIDE).order_by(cls.time.desc())
        else:
            q = cls.select().where(cls.state==state).order_by(cls.time.desc())
        return q.count(), q

    @classmethod
    def get_list_by_board(cls, board):
        q = cls.select().where(cls.board==board, cls.state>TOPIC_STATE.HIDE)\
                .order_by(cls.sticky_weight.desc(), cls.weight.desc(), cls.time.desc())
        return q.count(), q

    @classmethod
    def get_list_by_user(cls, user):
        q = cls.select().where(cls.user==user, cls.state>TOPIC_STATE.HIDE)
        return q.count(), q

    def view_count_inc(self):
        cls = Topic
        cls.update(view_count=cls.view_count + 1).where(cls.id == self.id).execute()

    def to_dict(self):
        ret = super().to_dict()
        ret['user'] = self.user.to_dict()
        if self.last_edit_user:
            ret['last_edit_user'] = self.last_edit_user.to_dict()
        return ret
