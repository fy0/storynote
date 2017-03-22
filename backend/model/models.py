# coding:utf-8

from model import db
from model.user import User
from model.topic import Topic
from model.comment import Comment
from model.tag import Tag, TopicTag

db.connect()
db.create_tables([User, Topic, Comment, Tag, TopicTag], safe=True)
