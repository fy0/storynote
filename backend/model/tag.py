# coding:utf-8

from peewee import *
from model import BaseModel


class Tag(BaseModel):
    name = CharField(index=True, unique=True, max_length=40)
    time = BigIntegerField(index=True)
    desc = CharField(max_length=255)

    class Meta:
        db_table = 'tag'


class TopicTag(BaseModel):
    topic_id = BigIntegerField(index=True)
    tag_id = BigIntegerField(index=True)
    user_id = BigIntegerField(index=True)
    time = BigIntegerField(index=True)

    class Meta:
        db_table = 'topic_tag'
