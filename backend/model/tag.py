# coding:utf-8

import time
from peewee import *
from model import BaseModel
from lib.state_obj import StateObject
from playhouse.gfk import GFKField


class TAG_DEFINE_STATE(StateObject):
    DEL = 0
    HIDE = 10
    NORMAL = 50

    txt = {DEL: "删除", HIDE: "隐藏", NORMAL:"正常"}

TAG_DEFINE_STATE.init()


class TagDefine(BaseModel):
    name = CharField(max_length=40, primary_key=True)
    time = BigIntegerField(index=True)
    desc = CharField(max_length=4096)
    state = IntegerField(default=TAG_DEFINE_STATE.NORMAL, index=True)

    class Meta:
        db_table = 'tag_define'

    @classmethod
    def new(cls, name, desc):
        try:
            return cls.create(name=name, desc=desc, time=int(time.time()), state=TAG_DEFINE_STATE.NORMAL)
        except IntegrityError:
            pass

    @classmethod
    def get_by_name(cls, name):
        return cls.get_by_pk(name)

    @classmethod
    def get_list(cls):
        return TagDefine.select().where(cls.state > TAG_DEFINE_STATE.NORMAL)


class Tag(BaseModel):
    tag = ForeignKeyField(TagDefine, index=True)
    obj_type = CharField()
    obj_id = BigIntegerField()
    object = GFKField('obj_type', 'obj_id')
    time = BigIntegerField(index=True)

    class Meta:
        db_table = 'tag'
        indexes = (
            (('obj_type', 'obj_id', 'tag'), True),
        )

    @classmethod
    def new_by_topic(cls, topic, tag_define):
        try:
            return cls.create(object=topic, tag=tag_define, time=int(time.time()))
        except IntegrityError:
            # 违反唯一性约束
            # 使用异常而不是先行 exists 检查是因为原子性上的优势
            pass

    @classmethod
    def get_by_topic_and_tag_define(cls, topic, tag_define):
        try:
            return cls.get(cls.object == topic, cls.tag == tag_define)
        except DoesNotExist:
            pass
