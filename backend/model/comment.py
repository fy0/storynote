# coding:utf-8

import time
import config
from lib.jsdict import JsDict
from peewee import *
from lib.state_obj import StateObject
from model import BaseModel
from model.user import User


class COMMENT_STATE(StateObject):
    DEL = 0
    HIDE = 10
    NORMAL = 50

COMMENT_STATE.init()


class Comment(BaseModel):
    related_id = BigIntegerField(index=True)  # 被评论文章
    related_type = IntegerField(index=True, default=0)  # 被评论文章的类型
    extra_id = BigIntegerField(index=True, null=True)  # 关联ID
    user = ForeignKeyField(User)  # 发布用户
    time = BigIntegerField(index=True)  # 发布时间
    state = IntegerField(default=COMMENT_STATE.NORMAL)  # 当前状态
    content = CharField(max_length=4096)  # 文本，varchar(4096)

    class Meta:
        db_table = 'comments'

    @classmethod
    def get_list(cls, related_id=0, offset=0):
        if related_id:
            q = cls.select().where(cls.state > COMMENT_STATE.HIDE, cls.related_id == related_id)
            return q.count(), q.offset(offset).limit(config.COMMENT_PAGE_SIZE)
        else:
            q = cls.select().where(cls.state > COMMENT_STATE.HIDE)
            return q.count(), q.offset(offset).limit(config.COMMENT_PAGE_SIZE)

    @classmethod
    def get_list_by_user(cls, user, offset=0, limit=config.COMMENT_PAGE_SIZE):
        """ 获取指定用户的回复 """
        q = cls.select().where(cls.state > COMMENT_STATE.HIDE, cls.user == user)
        return q.count(), q.offset(offset).limit(limit)

    @classmethod
    def get_count(cls, related_id):
        q = cls.select().where(cls.state > COMMENT_STATE.HIDE, cls.related_id == related_id)
        return q.count()

    @classmethod
    def exists(cls, pk_id, related_id):
        return cls.select().where(cls._meta.primary_key == pk_id, cls.related_id == related_id).exists()

    @classmethod
    def new(cls, relate_id, user, content, extra_id=None):
        return cls.create(related_id=relate_id, user=user, content=content,
                          time=int(time.time()), extra_id=extra_id)

    def can_edit(self, user):
        if self.user == user:
            return True

    def delete(self):
        self.state = COMMENT_STATE.DEL
        self.save()
