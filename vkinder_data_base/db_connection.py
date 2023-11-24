import os

from config import DIALECT, USERNAME, PASSWORD, HOST, DATABASE
import sqlalchemy as sq

from sqlalchemy.orm import sessionmaker, scoped_session
from vkinder_data_base.db_models import Clients, Users, Photos, Blocked, Favorites, LikedDisliked
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
def check_client(client_check_id: str):
    session = Session()
    checking_client = session.query(Clients).filter(Clients.client_id==client_check_id).first()
    return checking_client is not None

#Добавление нового клиента в таблицу Clients
@dbconnect
def add_client(client_vk_id: str):
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
def add_user(user_info: dict):
    session = Session()
    if not check_users(user_info['user_vk_id']):
        new_user = Users(**user_info)
        session.add(new_user)


@dbconnect
def get_user(user_vk_id: str):
    session = Session
    users = session.query(Users).filter(Users.user_vk_id==user_vk_id).all()
    if not users:
        print(f'Такой пользователь не найден')
    else:
        for user in users:
            print(user)


#Добавление id фото в таблицу Photo
@dbconnect
def add_photo(photo_info: dict):
    session = Session()
    user_photo = Photos(**photo_info)
    session.add(user_photo)


#Проверка на наличие в таблице Favorites
def check_favorites(check_id: str):
    session = Session()
    check_user = session.query(Favorites).filter_by(user_vk_id=check_id).first()
    return check_user is not None


#Добавление в таблицу Favorites
@dbconnect
def add_user_to_favorites(user_info: dict):
    session = Session()
    if not check_favorites(user_info['user_vk_id']):
        new_favorite_user = Favorites(user_vk_id=user_info['user_vk_id'], client_id=user_info['client_id'])
        session.add(new_favorite_user)


#Удаление из таблицы Favorites
@dbconnect
def delete_from_favorites(user_vk_id: str):
    session = Session()
    session.query(Favorites).filter_by(user_vk_id=user_vk_id).delete()


#Проверка на наличие в таблице Blocked
def check_blocked(check_id: str):
    session = Session()
    check_users = session.query(Blocked).filter_by(user_vk_id=check_id).first()
    return check_users is not None


#Добавление в таблицу Blocked
@dbconnect
def add_to_blocked(user_info: dict):
    session = Session()
    if check_favorites(user_info['user_vk_id']):
        delete_from_favorites(user_info['user_vk_id'])
    if not check_blocked(user_info['user_vk_id']):
        new_favorite_user = Blocked(user_vk_id=user_info['user_vk_id'], client_id=user_info['client_id'])
        session.add(new_favorite_user)


def all_favorites(client_id: int):
    session = Session()
    users = session.query(Favorites).filter_by(client_id=client_id).all()
    if not users:
        print('У вас ещё нет избранных пользователей')
    else:
        for user in users:
            print(user)


@dbconnect
def like_or_not(reaction: int, user_vk_id: str, photo_vk_id: str):
    session = Session()
    try:
        photo_excists = session.query(LikedDisliked).filter_by(user_vk_id=user_vk_id, photo_vk_id=photo_vk_id).first()
        if photo_excists:
            photo_excists.reaction = reaction
        else:
            new_reaction = LikedDisliked(user_vk_id=user_vk_id, photo_vk_id=photo_vk_id, reaction=reaction)
            session.add(new_reaction)
    except Exception as e:
        print(f'Ошибка добавления реакции: {e}')
        session.rollback()
