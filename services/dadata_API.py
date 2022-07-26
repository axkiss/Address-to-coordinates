import sys
import requests

HTTP_codes = {
    200: 'Запрос успешно обработан',
    400: 'Некорректный запрос (невалидный JSON или XML)',
    401: 'В запросе отсутствует API-ключ',
    403: 'В запросе указан несуществующий API-ключ \nИли не подтверждена почта \nИли исчерпан дневной лимит по количеству запросов',
    404: 'Неверный базовый URL к сервису dadata',
    405: 'Запрос сделан с методом, отличным от POST',
    413: 'Слишком большая длина запроса или слишком много условий',
    429: 'Слишком много запросов в секунду или новых соединений в минуту',
    500: 'Произошла внутренняя ошибка сервиса'
}


class SuggestClient:
    """Dadata Suggestions API client"""

    TIMEOUT_SEC = 10

    def __init__(self, base_url, token: str):
        self.base_url = base_url
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {token}",
        }

    def suggest(self, query: str, language: str = 'ru', count: int = 10) -> list[dict]:
        """Список похожих адресов с подробными данными"""

        body = {"query": query,
                "count": count,
                "language": language}
        response = self._post(self.base_url, json=body, headers=self.headers)
        suggestions = response.json()['suggestions']
        return suggestions

    def address_list(self, query: str, language: str = 'ru', count: int = 10) -> list[str]:
        """Список похожих адресов"""

        suggestions = self.suggest(query, language, count)
        return [suggest['value'] for suggest in suggestions]

    def get_coordinates(self, query: str) -> tuple:
        """Координаты запроса (долгота, широта)"""

        suggestions = self.suggest(query, count=1)
        if suggestions:
            data = suggestions[0]['data']
            coordinates = (data['geo_lat'], data['geo_lon'])
        else:
            coordinates = (None, None)

        return coordinates

    def _post(self, url, json, headers):
        """Выполнения метода POST"""
        response = requests.post(url, json=json, headers=headers, timeout=self.TIMEOUT_SEC)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            code = 500 if response.status_code >= 500 else response.status_code
            print('Произошла ошибка!')
            print('-' * 15)
            print(HTTP_codes.get(code, f'Неизвестная ошибка: {response.status_code}'))
            print('-' * 15)
            print('Попробуйте перезапустить скрипт и заново произвести настройку.')
            sys.exit(1)
        return response
