import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, sessionmaker, relationship



Base = declarative_base()


class Clients(Base):
    __tablename__ = 'clients'

    client_id = sq.Column(sq.Integer, primary_key=True)
    client_vk_id = sq.Column(sq.Integer)


class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    user_link = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='users')

    def __str__(self):
        return f'Имя пользователя: {self.user_first_name} {self.user_last_name}, VK id: {self.user_vk_id}, Ссылка на страницу: {self.user_link}'


class Blocked(Base):
    __tablename__ = 'blocked'
    blocked_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='blocked')


    def __str__(self):
        return f'VK id: {self.user_vk_id}, Имя: {self.user_first_name} {self.user_last_name}'


class Favorites(Base):
    __tablename__ = 'favorites'

    favorite_id = sq.Column(sq.Integer, primary_key=True)
    user_vk_id = sq.Column(sq.Integer)
    user_first_name = sq.Column(sq.String)
    user_last_name = sq.Column(sq.String)
    client_id = sq.Column(sq.Integer, sq.ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Clients', backref='favorites')


    def __str__(self):
        return f'VK id: {self.user_vk_id}, Имя: {self.user_first_name} {self.user_last_name}'



class Likes(Base):
    __tablename__ = 'likes'

    like_id = sq.Column(sq.Integer, primary_key=True)
    photo_vk_id = sq.Column(sq.Integer, nullable=False)
    favorite_id = sq.Column(sq.Integer, sq.ForeignKey('favorites.favorite_id'))
    favorite = relationship('Favorites', uselist=False, backref='likes')


    def __str__(self):
        return f'Photo vk id: {self.photo_vk_id}'


#Удаление таблиц
def drop_tables(engine):
    Base.metadata.drop_all(engine)


#Создание таблиц ()
def create_tables(engine):
    Base.metadata.create_all(engine)