import os
from googleapiclient.discovery import build


class Video:
    """Класс для видео"""
    api_key: str = os.getenv('YT_API_KEY')
    _video: dict = None
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_title: str = self.video_response()['items'][0]['snippet']['title']
        self.url: str = f"https://www.youtube.com/channel/{self.video_id}"
        self.view_count: int = self.video_response()['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response()['items'][0]['statistics']['likeCount']
        self.comment_count: int = self.video_response()['items'][0]['statistics']['commentCount']

    def video_response(self) -> dict:
        """Если информации в словаре нет, то возвращает информацию о видеоролике"""
        if self._video is None:
            self._video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id).execute()
        return self._video

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    """Класс для плейлиста"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self. playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
