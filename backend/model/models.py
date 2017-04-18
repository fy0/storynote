# coding:utf-8

from model import db
from model.user import User
from model.topic import Topic
from model.comment import Comment
from model.tag import TagDefine, Tag

db.connect()
db.create_tables([User, Topic, Comment, TagDefine, Tag], safe=True)
