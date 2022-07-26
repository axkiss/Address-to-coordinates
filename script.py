import sys
import re

from sqlalchemy.exc import OperationalError

from services.database import DataBaseManager
from services.utils import input_or_exit as input
from services.dadata_API import SuggestClient


def get_settings_from_input() -> dict:
    """Ведет диалог с пользователем для получения настроек"""

    settings = dict()
    print('-' * 15)
    print('   НАСТРОЙКА   ')
    print('-' * 15)
    print('Чтобы оставить настройку по умолчанию нажимайте "Enter".')

    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    while True:
        base_url = input('Введите базовый URL к сервису dadata:').strip()
        if base_url:
            if re.fullmatch(url_pattern, base_url):
                settings['base_url'] = base_url
                break
            else:
                print("Введите URL вида 'https://suggestions.dadata.ru/'")
        else:
            break

    while True:
        api_key = input('Введите API ключ для сервиса dadata:').strip()
        if api_key:
            if re.fullmatch('^[A-Za-z0-9]+$', api_key):
                settings['API_key'] = api_key
                break
            else:
                print('API ключ должен содержать только цифры и буквы a-z')
        else:
            print('API ключ не имеет значения по умолчанию!')

    while True:
        print('Выберете язык, на котором должен возвращаться ответ от dadata:')
        print("""1. ru - по умолчанию\n2. en""")
        language = input('Ваш выбор:').strip()
        if not language: break
        if language.isdecimal():
            int_language = int(language)
            if int_language in (1, 2):
                settings['language'] = ('ru', 'en')[int_language - 1]
                break
        print('Введите 1, или 2, или оставьте поле пустым.')

    return settings


def print_settings(dict_settings: dict) -> None:
    """Печатает переданные настройки"""

    print('-' * 15)
    for key, value in dict_settings.items():
        print(key + ' : ' + value)
    print('-' * 15)


def main():
    # Подключаем базу данных для хранения настроек
    settings = DataBaseManager('DaData_settings')

    # Используем найденные настройки или запрашиваем новые
    if settings.is_table_exists():
        try:
            settings_from_db = settings.get_values()
            print('Обнаружены настройки!')
            print_settings(settings_from_db)
            ans = input('Использовать? (Да/Нет):').strip().lower()
            while ans not in ('да', 'нет'):
                print('Введите "Да" или "Нет"')
                ans = input('Использовать? (Да/Нет):').strip().lower()

            if ans.strip().lower() == 'нет':
                settings.create_table()
                settings.insert_values(get_settings_from_input())
                settings_from_db = settings.get_values()
        except (AttributeError, OperationalError):
            settings.create_table()
            settings.insert_values(get_settings_from_input())
            settings_from_db = settings.get_values()
        except Exception as err:
            print('Непредвиденная ошибка!')
            print(err)
            sys.exit(1)

    else:
        settings.create_table()
        settings.insert_values(get_settings_from_input())
        settings_from_db = settings.get_values()

    print_settings(settings_from_db)


if __name__ == '__main__':
    print('Привет, User!\n'
          'Данный скрипт поможет найти координаты (долгота, широта) введенного адреса.\n'
          'Если захочешь закрыть скрипт, то напиши "Выйти"\n')
    main()
