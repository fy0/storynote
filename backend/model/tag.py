# coding:utf-8

import time
from peewee import *
from model import BaseModel
from playhouse.gfk import GFKField


class TagDefine(BaseModel):
    name = CharField(index=True, unique=True, max_length=40)
    time = BigIntegerField(index=True)
    desc = CharField(max_length=4096)

    class Meta:
        db_table = 'tag_define'

    @classmethod
    def new(cls, name, desc):
        return cls.create(name=name, desc=desc, time=int(time.time()))


class Tag(BaseModel):
    tag = ForeignKeyField(TagDefine, index=True)
    obj_type = CharField()
    obj_id = BigIntegerField()
    object = GFKField('obj_type', 'obj_id')
    time = BigIntegerField(index=True)

    class Meta:
        db_table = 'tag'
        indexes = (
            (('obj_type', 'obj_id'), True),
        )

    @classmethod
    def new_by_topic(cls, topic, tag_define):
        try:
            return cls.create(object=topic, tag=tag_define, time=int(time.time()))
        except IntegrityError:
            # 违反唯一性约束
            # 使用异常而不是先行 exists 检查是因为原子性上的优势
            pass
