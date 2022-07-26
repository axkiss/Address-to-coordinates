# Address-to-coordinates

Данный скрипт ищет адреса по любой части адреса от региона до квартиры («самара авроры 7 12» → «443017, Самарская обл, г
Самара, ул Авроры, д 7, кв 12»). И определяет координаты долготы и широты по указанному адресу.

## Инструкция запуска

* Установить Git (https://git-scm.com/downloads)
* Установить последнюю версию Python (https://wiki.python.org/moin/BeginnersGuide/Download)
* Клонировать репозиторий `git clone https://github.com/axkiss/Address-to-coordinates.git`
* Перейти в директорию `cd Address-to-coordinates`
* Создать виртуальное окружение `python -m venv venv`
* Активировать его `. venv/bin/activate`
* Установить requirements.txt `pip install -r requirements.txt`
* Запустить скрипт `python script.py`

## Инструкции использования
Для работы необходимо получить API ключ.

Для получения API ключа и секретного ключа Вам необходимо зарегистрироваться в сервисе https://dadata.ru, после чего необходимые данные
будут доступны в Вашем личном кабинете по ссылке: https://dadata.ru/profile/#info

Для изменения настроек скрипта требуется завершить выполнение вводом слова "выйти" и запустить скрипт снова.

## Requirements

- Python 3.10