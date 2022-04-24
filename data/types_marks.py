import sqlalchemy
from .db_session import SqlAlchemyBase


class TypesMarks(SqlAlchemyBase):
    __tablename__ = 'types_of_marks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
