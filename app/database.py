from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from config import DatabaseConfig


engine = create_engine(f'postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s'
                                                                % DatabaseConfig.get_data_database(),
                                                                                            echo=False)
base = declarative_base()


def init_database():
    '''In it func import your models'''

    from app.auth.models import User

    base.metadata.create_all(bind=engine)