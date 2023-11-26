import os

import sqlalchemy as sq

from sqlalchemy.orm import sessionmaker
from vkinder_data_base.db_models import Clients, Users, Favorites, Blocked, Likes, create_tables, drop_tables
from dotenv import load_dotenv
from vkinder_data_base import db_connection as db
load_dotenv()
engine = sq.create_engine(os.getenv('MY_DSN'))
sessions = sessionmaker(bind=engine)

# drop_tables(engine)
# create_tables(engine)
#
# db.add_client(1)


info = [
    {
    'user_vk_id': 1,
    'user_first_name': 'Dmitriy',
    'user_last_name': 'Kovalev'
},
    {'user_vk_id': 2,
    'user_first_name': 'Dmitri',
    'user_last_name': 'Kovalec'
     }
]
#
# for user in info:
#     db.add_user(user, 1)
# db.get_user(1)
# db.get_user(2)
#
# for user in info:
#     db.add_user_to_favorites(user, 1)
#
# db.all_favorites(1)
# db.add_liked_photos(77, 1)
# db.del_liked_photo(77)
# db.show_liked_photos(1)

# db.del_liked_photo(77)
# db.delete_from_favorites(1)
# for user in info:
#     db.add_to_blocked(user, 1)
# db.all_blocked(1)
# db.delete_from_blocked(1)

# db.search()