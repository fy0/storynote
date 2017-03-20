# coding:utf-8

from model import db
from model.user import User
from model.topic import Topic
from model.comment import Comment

db.connect()
db.create_tables([User, Topic, Comment], safe=True)
