import sys


def input_or_exit(*args, **kwargs):
    """Кастомизированный стандартный input() с возможностью выйти по стоп слову"""

    STOP_WORD = 'выйти'
    user_input = input(*args, **kwargs)
    if user_input.strip().lower() == STOP_WORD:
        print('Завершение скрипта.')
        sys.exit(0)

    return user_input
