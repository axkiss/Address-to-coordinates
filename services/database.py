import sys

from sqlalchemy import create_engine, inspect, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Setting(Base):
    """Таблица настроек"""
    __tablename__ = 'Setting'

    id = Column(Integer, primary_key=True)
    base_url = Column(String, nullable=False,
                      default='https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address')
    API_key = Column(String, nullable=False)
    language = Column(String, nullable=False, default='ru')

    def __repr__(self):
        return f'{self.base_url} - {self.API_key} - {self.language}'

    def get_dict(self):
        return {'base_url': self.base_url, 'API_key': self.API_key, 'language': self.language}


class DataBaseManager:
    """Взаимодействует с базой SQLite"""

    def __init__(self, dbname):
        self.dbname = dbname
        self.engine = self._get_engine()

    def _get_engine(self):
        """Подключение к базе данных"""

        try:
            return create_engine(f'sqlite:///{self.dbname}.sqlite')
        except Exception as err:
            print(f"Не удалось подключиться к базе данных с настройками: {self.dbname}")
            print(err)
            sys.exit(1)

    def insert_values(self, values: dict) -> None:
        """Вставка данных в таблицу"""

        try:
            Session = sessionmaker(bind=self.engine)
            with Session.begin() as session:
                session.add(Setting(**values))
            print(f'Настройки успешно сохранены.')
            print('-' * 15)
        except Exception as err:
            print(err)
            print(f'Не удалось добавить настройки')
            print('Попробуйте перезапустить скрипт и заново произвести настройку.')
            sys.exit(1)

    def create_table(self) -> None:
        """Создание таблицы"""

        if not self.is_table_exists():
            Base.metadata.create_all(self.engine)
        else:
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)

    def is_table_exists(self) -> bool:
        """Проверка наличия таблицы в базе данных"""

        return inspect(self.engine).has_table(Setting.__tablename__)

    def get_values(self) -> dict:
        """Возвращает словарь из данных первой записи таблицы"""

        Session = sessionmaker(bind=self.engine)
        with Session.begin() as session:
            settings = session.query(Setting).first()
            return settings.get_dict()