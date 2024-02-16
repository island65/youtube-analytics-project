import datetime
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс плейлиста """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlists = self.youtube.playlists().list(id=playlist_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.title = self.playlists['items'][0]['snippet']['title']
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                     id=','.join(self.video_ids)
                                                     ).execute()


    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        max_likes = 0
        max_video = ""
        for video in self.video_response['items']:
            count_likes = video['statistics']['likeCount']
            count_video = video['id']
            if int(count_likes) > int (max_likes):
                max_video = count_video
        return f"https://youtu.be/{max_video}"
