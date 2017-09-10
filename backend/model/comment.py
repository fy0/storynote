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
    user = ForeignKeyField(User, null=True)  # 发布用户
    time = BigIntegerField(index=True)  # 发布时间
    state = IntegerField(default=COMMENT_STATE.NORMAL)  # 当前状态
    content = TextField()  # 内容文本

    is_visitor = BooleanField(index=True, default=False)  # 是否游客评论
    visitor_name = TextField(null=True, default=None)  # 评论者名字，注意限长，必选
    visitor_ip = BlobField(null=True, default=None)  # 评论者 IP，自动
    visitor_website = TextField(null=True, default=None)  # 评论者网站，注意限长，可选
    visitor_email = TextField(null=True, default=None)  # 评论者邮箱，注意限长，可选
    visitor_useragent = TextField(null=True, default=None)  # 评论者UA，注意限长，自动

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
