import sqlalchemy
from .db_session import SqlAlchemyBase


class UserMarks(SqlAlchemyBase):
    __tablename__ = 'user_marks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    book_id = sqlalchemy.Column(sqlalchemy.Integer)
