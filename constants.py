import os

#
ALIENFX_DLL_PATH = r'C:\Program Files\Alienware\Alienware Command Center\AlienFX SDK\DLLs\x64\LightFX.dll'
ALIENFX_LIGHT_MODE = 0xFF
ALIENFX_LIGHT_BRIGHTNESS = 100
#
SPOTIFY_CLIENT_ID = '43ab55a3bafb463297b4ed113b7b9b23'
SPOTIFY_CLIENT_SECRET = '75a730701292478bb95c056c1c8c02b5'
SPOTIFY_REDIRECT_URI = r'http://localhost:3000'
SPOTIFY_SCOPE = 'user-read-recently-played'
SPOTIFY_LAST_ALBUM_STREAM_URL = 'https://spclient.wg.spotify.com/recently-played/v3/user/22rzppy5nmk7mzhsfhvvexnbq/recently-played'

# ToDo :: Deixar dinâmico.
# curr_stream_token = requests.get(r'https://open.spotify.com/get_access_token/').json()['accessToken']
SPOTIFY_WEB_TOKEN_CACHE_FILE = 'spotify-web-token.cache'
if os.path.isfile(SPOTIFY_WEB_TOKEN_CACHE_FILE):
    with open(SPOTIFY_WEB_TOKEN_CACHE_FILE, 'r') as file:
        SPOTIFY_WEB_TOKEN = file.read().strip()
        file.close()
else:
    SPOTIFY_WEB_TOKEN = input('Spotify Web Token: ').strip()
    with open(SPOTIFY_WEB_TOKEN_CACHE_FILE, 'w') as file:
        file.write(SPOTIFY_WEB_TOKEN)
        file.close()
    print()

#
HUE_BALANCE_POINT = 0.5
HUE_DELTA_UP = 15  # degrees
HUE_DELTA_DOWN = 355  # degrees
#
SATURATION_BALANCE_POINT = 0.03
OPTIMAL_SATURATION = 1.0
#
LIGHTNESS_BALANCE_POINT = 0.5
MIN_LIGHTNESS = 0.0
MAX_LIGHTNESS = 1.0
OPTIMAL_LIGHTNESS = 0.5
#
TIME_TO_UPDATE_IN_SECONDS = 5
