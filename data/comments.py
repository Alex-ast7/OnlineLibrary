import sqlalchemy
from .db_session import SqlAlchemyBase


books_to_users_comments = sqlalchemy.Table(
    'association_comments',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('books', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('books.id')),
    sqlalchemy.Column('comments', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('comments.id'))
)


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    date_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
