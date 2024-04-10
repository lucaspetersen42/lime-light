import os
import time
from tabulate import tabulate

from constants import TIME_TO_UPDATE_IN_SECONDS

from spotify_handler import SpotifyRequester
from helper_functions import get_album_color, set_cpu_lights


def main():
    spotify_requester = SpotifyRequester()
    last_curr_streaming_album = spotify_requester.get_curr_streaming_album()

    running = True
    first_time_running = True
    while running:
        try:
            os.system('title 🍋 LimeLight - Updating...')
            curr_streaming_album = spotify_requester.get_curr_streaming_album()
            if (curr_streaming_album != last_curr_streaming_album) or first_time_running:
                first_time_running = False

                album_name = curr_streaming_album["name"]
                album_artists = ", ".join([art["name"] for art in curr_streaming_album["artists"]])
                album_display_name = f'\x1b[38;5;117m"{album_name}"\x1b[0m \x1b[38;5;225mby {album_artists} \x1b[0m'
                print(f'💿 New Album Playing :: {album_display_name}')

                album_color = get_album_color(spotify_requester=spotify_requester, album=curr_streaming_album)
                album_color_rgb = album_color.get_current_color()
                album_color_hex = album_color.get_current_color_as_hex()
                album_color_hls = album_color.get_hls(nround=4)

                color_data = {
                    'RGB': album_color_rgb,
                    'Hexadecimal': album_color_hex,
                    'HLS': album_color_hls
                }
                colors_data_ascii = tabulate([[k, v] for k, v in color_data.items()], tablefmt='grid', showindex=False)
                print(colors_data_ascii + '\n')

                set_cpu_lights(rgb=album_color)
                last_curr_streaming_album = curr_streaming_album

            os.system('title 🍋 LimeLight')
            time.sleep(TIME_TO_UPDATE_IN_SECONDS)

        except Exception as e:
            print(f'\x1b[38;5;214mError:\x1b[0m \x1b[38;5;196m{e}\x1b[0m')
            running = False
            quit()

        except KeyboardInterrupt:
            print(f'\x1b[38;5;214mExecution ended by user.\x1b[0m')
            running = False
            quit()


if __name__ == '__main__':
    os.system('cls')
    print('''\x1b[38;5;190m
888     🍋🍋                        888      🍋🍋         888      888    
888     🍋🍋                        888      🍋🍋         888      888    
888                                 888                   888      888    
888      888 88888b.d88b.   .d88b.  888      888  .d88b.  88888b.  888888 
888      888 888 "888 "88b d8P  Y8b 888      888 d88P"88b 888 "88b 888    
888      888 888  888  888 88888888 888      888 888  888 888  888 888    
888      888 888  888  888 Y8b.     888      888 Y88b 888 888  888 Y88b.  
88888888 888 888  888  888  "Y8888  88888888 888  "Y88888 888  888  "Y888 
                                                      888                 
                                                 Y8b d88P                 
                                                  "Y88P"                  
\x1b[0m
══════════════════════════════════════════════════════════════════════════════
══════════════════════════════════════════════════════════════════════════════
''')
    main()
