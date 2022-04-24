import datetime

import sqlalchemy
from sqlalchemy import func

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    date_time = sqlalchemy.Column(sqlalchemy.Date, nullable=True, default=datetime.datetime.today())
    stars = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    book_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('books.id'))
