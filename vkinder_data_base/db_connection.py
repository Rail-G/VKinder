from config import DIALECT, USERNAME, PASSWORD, HOST, DATABASE
import sqlalchemy as sq

from sqlalchemy.orm import sessionmaker, scoped_session
from vkinder_data_base.db_models import Users, Photos, Blocked, Favorites, LikedDisliked


def connect_to_db():
    eng = f"{DIALECT}://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
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

#Проверка пользователя в таблице Users
def check_users(check_id: str):
    session = Session()
    checking_user = session.query(Users).filter(Users.user_vk==check_id).first()
    return checking_user is not None


#Добавление пользователя в список Users
@dbconnect
def add_user(user_info):
    session = Session()
    if not check_users(user_info['user_vk']):
        new_user = Users(**user_info)
        session.add(new_user)


#Добавление id фото в таблицу Photo
@dbconnect
def add_photo(photo_id):
    session = Session()
    user_photo = Photos(**photo_id)
    session.add(user_photo)


#Обновление реакции на фото в таблице LikedDisliked
@dbconnect
def rection_update(update_reaction: int, user_id: int):
    session = Session()
    new_reaction = session.query(LikedDisliked).filter_by(user_id=user_id).update({'reaction': update_reaction})
    session.commit()


#Достаем vk_id из таблицы Users
@dbconnect
def get_user_id(user_id: str) -> type[Users] | None:
    session = Session()
    user = session.query(Users).filter(Users.user_vk == user_id).first()
    return user


#Проверка на наличие в таблице Favorites
def check_favorites(check_id: str):
    session = Session()
    check_user = session.query(Favorites).filter_by(favorite_user_id=check_id).first()
    return check_user is not None


#Добавление в таблицу Favorites
@dbconnect
def add_user_to_favorites(user_info, matched_user_info):
    session = Session()
    if not check_users(matched_user_info['user_id']):
        add_user(matched_user_info)
    if not check_favorites(matched_user_info['user_id']):
        new_favorite_user = Favorites(user_id=user_info['user_id'], favorite_user_id=matched_user_info['user_id'])
        session.add(new_favorite_user)


#Удаление из таблицы Favorites
@dbconnect
def delete_from_favorites(user_id: str):
    session = Session()
    session.query(Favorites).filter_by(favorite_user_id=user_id).delete()


#Проверка на наличие в таблице Blocked
def check_blocked(check_id: str):
    session = Session()
    check_users = session.query(Blocked).filter_by(blocked_list_id=check_id).first()
    return check_users is not None


#Добавление в таблицу Blocked
@dbconnect
def add_to_blocked(user_info, matched_user_info):
    session = Session()
    if not check_users(matched_user_info['user_id']):
        add_user(matched_user_info)
    if check_favorites(matched_user_info['user_id']):
        delete_from_favorites(matched_user_info['user_id'])
    if not check_blocked(matched_user_info['user_id']):
        new_blocked_user = Blocked(user_id=user_info['user_id'], blocked_list_id=matched_user_info['user_id'])
        session.add(new_blocked_user)


def all_favorites(user_id):
    session = Session()
    users = session.query(Users).join(Favorites(Favorites.favorite_id == Users.user_id).filter(Favorites.user_id == user_id)).all()
    favorites_list = []
    for user in users:
        favorites_list.append({'id': user.user_id,
                               'first_name': user.user_first_name,
                               'last_name': user.last_name,
                               'user_vk_id': user.user_vk
                               })

    return favorites_list


@dbconnect
def like_or_not(reaction: str):
    session = Session()
    react = LikedDisliked(reaction=reaction, user_id=Users.user_id, photo_id=Photos.photo_id)
    session.add(react)



