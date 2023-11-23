import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, sessionmaker, relationship



Base = declarative_base()


class Clients(Base):
    __tablename__ = 'clients'

    client_id = sq.Column(sq.Integer, primary_key=True)
    client_vk_id = sq.Column(sq.String)


class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.String)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    user_link = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='users')




class Photos(Base):
    __tablename__ = 'photos'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    photo_vk_id = sq.Column(sq.String)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)
    user = relationship('Users', backref='photos')


class Blocked(Base):
    __tablename__ = 'blocked'

    blocked_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    user = relationship('Clients', backref='blocked')


class Favorites(Base):
    __tablename__ = 'favorites'

    favorite_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='favorites')


class LikedDisliked(Base):
    __tablename__ = 'likesdislikes'

    like_dislike_id = sq.Column(sq.Integer, primary_key=True)
    reaction = sq.Column(sq.Integer)
    user_vk_id = sq.Column(sq.String, nullable=False)
    photo_vk_id = sq.Column(sq.String, nullable=False)
    favorite_id = sq.Column(sq.Integer, sq.ForeignKey('favorites.favorite_id'))
    blocked_id = sq.Column(sq.Integer, sq.ForeignKey('blocked.blocked_id'))
    favorite = relationship('Favorites', uselist=False, backref='likesdislikes')
    blocked = relationship('Blocked', uselist=False, backref='likesdislikes')


#Создание таблиц
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)