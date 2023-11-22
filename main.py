import os

import sqlalchemy

from vkinder_data_base.db_models import Users, Photos, Favorites, Blocked, LikedDisliked, create_tables
from dotenv import load_dotenv

load_dotenv()

engine = sqlalchemy.create_engine(os.getenv('MY_DSN'))

create_tables(engine)