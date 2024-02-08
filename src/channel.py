import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    _api_key: str = os.getenv('YT_API_KEY')
    _channel_data: dict = None
    # создаём специальный объект для работы с API
    _youtube = build('youtube', 'v3', developerKey=_api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    @classmethod
    def get_service(cls):
        return cls._youtube

    def _get_info_from_channel(self) -> dict:
        """Метод для получения информации о канале"""
        if self._channel_data is None:
            self._channel_data = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return self._channel_data

    @property
    def title(self) -> str:
        self._get_info_from_channel()
        return self._channel_data['items'][0]['snippet']['title']

    @property
    def description(self) -> str:
        self._get_info_from_channel()
        return self._channel_data['items'][0]['snippet']['description']

    @property
    def url(self) -> str:
        self._get_info_from_channel()
        return f"https://www.youtube.com/channel/{self.__channel_id}"

    @property
    def subscriber_count(self) -> int:
        self._get_info_from_channel()
        return self._channel_data['items'][0]['statistics']['subscriberCount']

    @property
    def video_count(self) -> int:
        self._get_info_from_channel()
        return self._channel_data['items'][0]['statistics']['videoCount']

    @property
    def view_count(self) -> int:
        self._get_info_from_channel()
        return self._channel_data['items'][0]['statistics']['viewCount']

    def _to_json(self, file_name) -> None:
        """Метод, сохраняющий в файл значения атрибутов экземпляра Channel"""
        with open(file_name, 'w', encoding='utf8') as file:
            data = {'channel_id': self.__channel_id,
                    'title': self.title,
                    'description:': self.description,
                    'url': self.url,
                    'subscriberCount': self.subscriber_count,
                    'videoCount': self.video_count,
                    'viewCount': self.view_count
                    }
            json.dump(data, file, ensure_ascii=False, indent=2)

    @property
    def _new_channel_data(self) -> dict:
        """Метод для возвращения информации о канале"""
        if self._channel_data is None:
            data = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
            self._to_json('moscowpython.json')
        return self._channel_data

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self._get_info_from_channel(), indent=2, ensure_ascii=False))

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other) -> int:
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other) -> bool:
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other) -> bool:
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other) -> bool:
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other) -> bool:
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other) -> bool:
        return int(self.subscriber_count) == int(other.subscriber_count)