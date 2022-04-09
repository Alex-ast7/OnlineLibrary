import sqlalchemy
from .db_session import SqlAlchemyBase


books_to_users_marks = sqlalchemy.Table(
    'association_marks',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('books', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('books.id')),
    sqlalchemy.Column('user_marks', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('user_marks.id'))
)


class UserMarks(SqlAlchemyBase):
    __tablename__ = 'user_marks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
