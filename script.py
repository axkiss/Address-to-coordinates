import sys

from sqlalchemy.exc import OperationalError
from services.database import DataBaseManager


def get_settings_from_input() -> dict:
    """Ведет диалог с пользователем для получения настроек"""

    settings = dict()
    print('Чтобы оставить настройку по умолчанию нажимайте "Enter".')

    base_url = input('Введите базовый URL к сервису dadata:').strip()
    if base_url:
        settings['base_url'] = base_url

    while True:
        api_key = input('Введите API ключ для сервиса dadata:').strip()
        if api_key:
            settings['API_key'] = api_key
            break
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


if __name__ == '__main__':
    settings = DataBaseManager('DaData_settings')

    if settings.is_table_exists():
        try:
            settings_from_db = settings.get_values()
            print('Обнаружены настройки!', settings_from_db)
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

    print(settings_from_db)