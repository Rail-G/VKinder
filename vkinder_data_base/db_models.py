import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, sessionmaker, relationship



Base = declarative_base()


class Clients(Base):
    __tablename__ = 'clients'

    client_id = sq.Column(sq.Integer, primary_key=True)
    client_vk_id = sq.Column(sq.Integer, unique=True)


    def __int__(self):
        return f'PK_client_id: {self.client_id}, vk_id: {self.client_vk_id}'


class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, unique=True)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='users')

    def __str__(self):
        return f'Имя пользователя: {self.user_first_name} {self.user_last_name}'


    def __int__(self):
        return f'PK_user_id: {self.user_id}, vk_id: {self.user_vk_id}'


class Blocked(Base):
    __tablename__ = 'blocked'
    blocked_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, unique=True)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='blocked')


    def __str__(self):
        return f'Имя: {self.user_first_name} {self.user_last_name}'

    def __int__(self):
        return f'PK_blocked_id: {self.blocked_id}, vk_id: {self.user_vk_id}'


class Favorites(Base):
    __tablename__ = 'favorites'

    favorite_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer, unique=True)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='favorites')


    def __str__(self):
        return f'Имя: {self.user_first_name} {self.user_last_name}'

    def __int__(self):
        return f'PK_favorite_id: {self.favorite_id}, vk_id: {self.user_vk_id}'



class Likes(Base):
    __tablename__ = 'likes'

    like_id = sq.Column(sq.Integer, primary_key=True)
    photo_vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    user_vk_id = sq.Column(sq.Integer, nullable=False)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'))
    client = relationship('Clients', uselist=False, backref='likes')


    def __int__(self):
        return f'PK_like_id: {self.like_id}, Photo vk id: {self.photo_vk_id}'


# #Удаление таблиц
# def drop_tables(engine):
#     Base.metadata.drop_all(engine)


#Создание таблиц ()
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)