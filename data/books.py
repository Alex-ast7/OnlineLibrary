import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Books(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    isbn_13 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    isbn_10 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    small_image_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    language = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    total_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    amount_in_library = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f'<Book> {self.id}, {self.title}, {self.author}, {self.isbn_13}, {self.total_amount}, {self.amount_in_library}, {self.image_link}'
