import os

from config import DIALECT, USERNAME, PASSWORD, HOST, DATABASE
import sqlalchemy as sq

from sqlalchemy.orm import sessionmaker, scoped_session
from vkinder_data_base.db_models import Clients, Users, Blocked, Favorites, Likes
from vkinder_data_base.db_models import create_tables
from dotenv import load_dotenv

def connect_to_db():
    load_dotenv()
    eng = os.getenv('MY_DSN')
    engine = sq.create_engine(eng)
    return engine

sessions = sessionmaker(bind=connect_to_db())
Session = scoped_session(sessions)

def create_table():
    create_tables(connect_to_db())

#Декоратор для sessionmaker
def dbconnect(func):
    def _dbconnect(*args, **kwargs):
        session = Session()
        try:
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            print(f'Ошибка {e}')
            session.rollback()
        finally:
            Session.remove()

    return _dbconnect


#Проверка наличия клиента в таблице Clients
def check_client(client_check_id: int):
    session = Session()
    checking_client = session.query(Clients).filter(Clients.client_id==client_check_id).first()
    return checking_client is not None


#Проверка PK клиента
def client_pk_id(client_vk_id: int) -> None:
    session = Session()
    client_pk_id = session.query(Clients.client_id).filter(Clients.client_vk_id==client_vk_id).first()
    return client_pk_id[0]

#Добавление нового клиента в таблицу Clients
@dbconnect
def add_client(client_vk_id: int):
    session = Session()
    if not check_client(client_vk_id):
        new_client = Clients(client_vk_id=client_vk_id)
        session.add(new_client)


#Проверка пользователя в таблице Users
def check_users(check_id: str):
    session = Session()
    checking_user = session.query(Users).filter(Users.user_vk_id==check_id).first()
    return checking_user is not None


#Добавление пользователя в список Users
@dbconnect
def add_user(user_info: dict, client_vk_id: int):
    session = Session()
    if not check_users(user_info['user_vk_id']):
        client_id = client_pk_id(client_vk_id)
        new_user = Users(**user_info, client_id=client_id)
        session.add(new_user)


#Дропаем таблицу users
@dbconnect
def drop_users(client_vk_id):
    session = Session
    client_id = client_pk_id(client_vk_id)
    session.query(Users).filter(Users.client_id==client_id).delete()


# #Функция нового поиска
# def search():
#     drop_users()


#Получение инфо пользователя по его vk_id
@dbconnect
def get_user(pk_user: int):
    session = Session
    users = session.query(Users.user_vk_id, Users.user_first_name, Users.user_last_name).filter(Users.user_id==pk_user).first()
    return users


#Проверка на наличие в таблице Favorites
def check_favorites(check_id: int):
    session = Session()
    check_user = session.query(Favorites).filter_by(user_vk_id=check_id).first()
    return check_user is not None


#Добавление в таблицу Favorites
@dbconnect
def add_user_to_favorites(user_info: dict, client_vk_id: int):
    session = Session()
    if not check_favorites(user_info['user_vk_id']):
        client_id = client_pk_id(client_vk_id)
        new_favorite_user = Favorites(user_vk_id=user_info['user_vk_id'], user_first_name=user_info['user_first_name'], user_last_name=user_info['user_last_name'], client_id=client_id)
        session.add(new_favorite_user)


#Удаление из таблицы Favorites
@dbconnect
def delete_from_favorites(user_vk_id: int):
    session = Session()
    session.query(Favorites).filter_by(user_vk_id=user_vk_id).delete()

#Вывод всех пользователей из избранного
@dbconnect
def all_favorites(client_vk_id: int):
    session = Session()
    client_id = client_pk_id(client_vk_id)
    users = session.query(Favorites.user_vk_id, Favorites.user_first_name, Favorites.user_last_name).filter_by(client_id=client_id).all()
    return users


#Добавление фото в лайкнутые
@dbconnect
def add_liked_photos(photo_vk_id: int, user_vk_id: int, client_vk_id: int):
    session = Session
    client_id = client_pk_id(client_vk_id)
    like = Likes(photo_vk_id=photo_vk_id, user_vk_id=user_vk_id, client_id=client_id)
    session.add(like)


#Удаление фото из лайкнутых
@dbconnect
def del_liked_photo(photo_vk_id: int):
    session = Session
    session.query(Likes).filter_by(photo_vk_id=photo_vk_id).delete()


#Вывод всех понравившихся фотографий
@dbconnect
def show_liked_photos(client_vk_id: int):
    session = Session
    client_id = client_pk_id(client_vk_id)
    photos = session.query(Likes.photo_vk_id, Likes.user_vk_id).filter_by(client_id=client_id).all()
    return photos

#Проверка на наличие в таблице Blocked
def check_blocked(check_id: int):
    session = Session()
    check_users = session.query(Blocked).filter_by(user_vk_id=check_id).first()
    return check_users is not None


#Добавление в таблицу Blocked
@dbconnect
def add_to_blocked(user_info: dict, client_vk_id: int):
    session = Session()
    if check_favorites(user_info['user_vk_id']):
        delete_from_favorites(user_info['user_vk_id'])
    if not check_blocked(user_info['user_vk_id']):
        client_id = client_pk_id(client_vk_id)
        new_blocked_user = Blocked(user_vk_id=user_info['user_vk_id'], user_first_name=user_info['user_first_name'], user_last_name=user_info['user_last_name'], client_id=client_id)
        session.add(new_blocked_user)


#Вывод всех заблокированных пользователей
@dbconnect
def all_blocked(client_vk_id: int):
    session = Session()
    client_id = client_pk_id(client_vk_id)
    blocked_users = session.query(Blocked.user_vk_id, Blocked.user_first_name, Blocked.user_last_name).filter_by(client_id=client_id).all()
    return blocked_users


#Удаление из таблицы Blocked
@dbconnect
def delete_from_blocked(user_vk_id: int):
    session = Session()
    session.query(Blocked).filter_by(user_vk_id=user_vk_id).delete()


def delete_all(client_vk_id):
    client_id = client_pk_id(client_vk_id)
    session = Session()
    session.query(Users).filter_by(client_id=client_id).delete()
    session.query(Likes).filter_by(client_id=client_id).delete()
    session.query(Blocked).filter_by(client_id=client_id).delete()
    session.query(Favorites).filter_by(client_id=client_id).delete()