import os
import requests
from typing import Optional
from spotipy.oauth2 import SpotifyOAuth
from constants import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SCOPE,
    SPOTIFY_LAST_ALBUM_STREAM_URL,
    SPOTIFY_WEB_TOKEN,
    SPOTIFY_WEB_TOKEN_CACHE_FILE
)


class SpotifyRequester:
    URL = r'https://api.spotify.com'

    def __init__(self):
        self._oauth_manager = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SPOTIFY_SCOPE
        )

    def _get_token(self) -> str:
        """Returns authentication token."""
        response = self._oauth_manager.get_access_token()
        token = response.get('access_token')
        return token

    def _build_headers(self, headers: Optional[dict]) -> dict:
        """Returns request headers with authentication token."""
        if not headers:
            headers = dict()
        token = self._get_token()
        headers['Authorization'] = f'Bearer {token}'
        return headers

    def _build_url(self, endpoint: str) -> str:
        """Returns a complete API URL after the given endpoint."""
        url = f'{self.URL}{endpoint}'
        return url

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Makes an authenticated request."""
        headers = self._build_headers(kwargs.get('headers'))
        kwargs['headers'] = headers
        response = requests.request(method=method, url=url, **kwargs)
        return response

    def _get(self, url: str, **kwargs) -> requests.Response:
        """Makes an authenticated GET request."""
        return self._request(method='GET', url=url, **kwargs)

    def _post(self, url: str, **kwargs) -> requests.Response:
        """Makes an authenticated POST request."""
        return self._request(method='POST', url=url, **kwargs)

    @staticmethod
    def get_album_cover(album: dict) -> bytes:
        cover_url = album.get('images')[1].get('url')
        cover_image_response = requests.get(cover_url)
        return cover_image_response.content

    def get_last_listened_song(self):  # ToDo :: Entender comportamento pra talvez usar futuramente.
        # url = self._build_url(endpoint='/v1/me/player/recently-played')
        # params = dict(limit=1, offset=0, market='from_token')
        # response = self._get(url, params=params)
        # r = response.json()
        # last_song = r['items'][0]['track']
        # song_name = last_song['name']
        # song_artists = ", ".join([art['name'] for art in last_song['artists']])
        # song_display_name = f'"{song_name}"  by    {song_artists}\n'
        # print(f'{datetime.now().strftime("%H:%M:%S")} :: {song_display_name}')
        raise NotImplemented()

    def get_curr_streaming_album(self):
        params_curr_stream = dict(limit=1, offset=0, market='from_token', format='json')

        headers_curr_stream = {'Authorization': f'Bearer {SPOTIFY_WEB_TOKEN}'}
        response_curr_stream = requests.get(SPOTIFY_LAST_ALBUM_STREAM_URL, params=params_curr_stream,
                                            headers=headers_curr_stream)

        if not response_curr_stream.ok:
            print('\x1b[38;5;214mToken Inválido! Tente novamente.\x1b[0m')
            if os.path.isfile(SPOTIFY_WEB_TOKEN_CACHE_FILE):
                os.remove(SPOTIFY_WEB_TOKEN_CACHE_FILE)
            quit()

        r_curr_stream = response_curr_stream.json()
        curr_stream_raw = r_curr_stream['playContexts'][0]['uri']

        url_album = self._build_url(endpoint=f'/v1/albums/{curr_stream_raw.split(":")[-1]}')
        response_album = self._get(url_album)
        r_album = response_album.json()

        return r_album
