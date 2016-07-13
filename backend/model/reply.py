# coding:utf-8

import time
import config
from lib.jsdict import JsDict
from peewee import *
from lib.state_obj import StateObject
from model import BaseModel
from model.user import User


class REPLY_STATE(StateObject):
    DEL = 0
    HIDE = 10
    NORMAL = 50

REPLY_STATE.init()


class Reply(BaseModel):
    related_id = BigIntegerField(index=True)  # 被评论文章
    extra_id = BigIntegerField(index=True, null=True)  # 关联ID
    user = ForeignKeyField(User)  # 发布用户
    send_to_id = BigIntegerField(null=True)  # 是否是回复某个评论
    time = BigIntegerField(index=True)  # 发布时间
    state = IntegerField(default=REPLY_STATE.NORMAL)  # 当前状态
    content = CharField(max_length=4096)  # 文本，varchar(4096)

    @classmethod
    def get_list(cls, related_id, offset=0):
        q = cls.select().where(cls.state > REPLY_STATE.HIDE, cls.related_id == related_id)
        return q.count(), q.offset(offset).limit(config.REPLY_PAGE_SIZE)

    @classmethod
    def get_list_by_user(cls, user, offset=0, limit=config.REPLY_PAGE_SIZE):
        """ 获取指定用户的回复 """
        q = cls.select().where(cls.state > REPLY_STATE.HIDE, cls.user == user)
        return q.count(), q.offset(offset).limit(limit)

    @classmethod
    def get_count(cls, related_id):
        q = cls.select().where(cls.state > REPLY_STATE.HIDE, cls.related_id == related_id)
        return q.count()

    @classmethod
    def exists(cls, pk_id, related_id):
        return cls.select().where(cls._meta.primary_key == pk_id, cls.related_id == related_id).exists()

    @classmethod
    def new(cls, relate_id, user, content, send_to_id=None, extra_id=None):
        return cls.create(related_id=relate_id, user=user, content=content,
                          send_to_id=send_to_id, time=int(time.time()), extra_id=extra_id)
