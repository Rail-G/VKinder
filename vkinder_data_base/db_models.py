import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from config import DIALECT, USERNAME, PASSWORD, HOST, DATABASE


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    user_vk = sq.Column(sq.String)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    user_link = sq.Column(sq.String)


class Photos(Base):
    __tablename__ = 'photos'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    photo_vk_id = sq.Column(sq.String)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)
    user = relationship('Users', backref='photos')


class Blocked(Base):
    __tablename__ = 'blocked'

    blocked_id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)
    user = relationship('Users', backref='blocked')


class Favorites(Base):
    __tablename__ = 'favorites'

    favorite_id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)
    user = relationship('Users', backref='favorites')


class LikedDisliked(Base):
    __tablename__ = 'likesdislikes'

    like_dislike_id = sq.Column(sq.Integer, primary_key=True)
    reaction = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)
    photo_id = sq.Column(sq.Integer, sq.ForeignKey('photos.photo_id'), nullable=False)
    user = relationship('Users', uselist=False, backref='likesdislikes')
    photo = relationship('Photos', uselist=False, backref='likesdislikes')


#Создание таблиц
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)