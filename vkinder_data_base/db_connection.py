import os

from config import DIALECT, USERNAME, PASSWORD, HOST, DATABASE
import sqlalchemy as sq

from sqlalchemy.orm import sessionmaker, scoped_session
from vkinder_data_base.db_models import Clients, Users, Blocked, Favorites, Likes
from dotenv import load_dotenv


def connect_to_db():
    # eng = f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
    load_dotenv()
    eng = os.getenv('MY_DSN')
    engine = sq.create_engine(eng)
    return engine

sessions = sessionmaker(bind=connect_to_db())
Session = scoped_session(sessions)


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
def add_user(user_info: dict, client_id: int):
    session = Session()
    if not check_users(user_info['user_vk_id']):
        new_user = Users(**user_info, client_id=client_id)
        session.add(new_user)


#Дропаем таблицу users
@dbconnect
def drop_users():
    session = Session
    session.query(Users).delete()


#Функция нового поиска
def search():
    drop_users()


#Получение инфо пользователя по его vk_id
@dbconnect
def get_user(user_id: int):
    session = Session
    users = session.query(Users).filter(Users.user_id==user_id).all()
    if not users:
        print(f'Такой пользователь не найден')
    else:
        for user in users:
            print(user)


#Проверка на наличие в таблице Favorites
def check_favorites(check_id: int):
    session = Session()
    check_user = session.query(Favorites).filter_by(user_vk_id=check_id).first()
    return check_user is not None


#Добавление в таблицу Favorites
@dbconnect
def add_user_to_favorites(user_info: dict, client_id: int):
    session = Session()
    if not check_favorites(user_info['user_vk_id']):
        new_favorite_user = Favorites(user_vk_id=user_info['user_vk_id'], user_first_name=user_info['user_first_name'], user_last_name=user_info['user_last_name'], client_id=client_id)
        session.add(new_favorite_user)


#Удаление из таблицы Favorites
@dbconnect
def delete_from_favorites(user_vk_id: int):
    session = Session()
    session.query(Favorites).filter_by(user_vk_id=user_vk_id).delete()


#Вывод всех пользователей из избранного
def all_favorites(client_id: int):
    session = Session()
    users = session.query(Favorites).filter_by(client_id=client_id).all()
    if not users:
        print('У вас ещё нет избранных пользователей')
    else:
        for user in users:
            print(user)


#Добавление фото в лайкнутые
@dbconnect
def add_liked_photos(photo_vk_id: int, favorite_id: int):
    session = Session
    like = Likes(photo_vk_id=photo_vk_id, favorite_id=favorite_id)
    session.add(like)


#Удаление фото из лайкнутых
@dbconnect
def del_liked_photo(photo_vk_id: int):
    session = Session
    session.query(Likes).filter_by(photo_vk_id=photo_vk_id).delete()


#Вывод всех понравившихся фотографий
@dbconnect
def show_liked_photos(user_id: int):
    session = Session
    photos = session.query(Likes, Favorites).join(Favorites, Likes.favorite_id==Favorites.favorite_id).filter(Favorites.user_vk_id==user_id).all()
    for photo in photos:
        print(photo)


#Проверка на наличие в таблице Blocked
def check_blocked(check_id: int):
    session = Session()
    check_users = session.query(Blocked).filter_by(user_vk_id=check_id).first()
    return check_users is not None


#Добавление в таблицу Blocked
@dbconnect
def add_to_blocked(user_info: dict, client_id: int):
    session = Session()
    if check_favorites(user_info['user_vk_id']):
        delete_from_favorites(user_info['user_vk_id'])
    if not check_blocked(user_info['user_vk_id']):
        new_blocked_user = Blocked(user_vk_id=user_info['user_vk_id'], user_first_name=user_info['user_first_name'], user_last_name=user_info['user_last_name'], client_id=client_id)
        session.add(new_blocked_user)


#Вывод всех заблокированных пользователей
@dbconnect
def all_blocked(client_id: int):
    session = Session
    blocked_users = session.query(Blocked).filter_by(client_id=client_id).all()
    if not blocked_users:
        print('Ваш список заблокированных пользователей пуст')
    else:
        for user in blocked_users:
            print(user)


#Удаление из таблицы Blocked
@dbconnect
def delete_from_blocked(user_vk_id: int):
    session = Session()
    session.query(Blocked).filter_by(user_vk_id=user_vk_id).delete()

