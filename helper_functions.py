from constants import HUE_BALANCE_POINT, SATURATION_BALANCE_POINT, LIGHTNESS_BALANCE_POINT
from constants import HUE_DELTA_DOWN, HUE_DELTA_UP
from constants import MIN_LIGHTNESS, MAX_LIGHTNESS, OPTIMAL_LIGHTNESS
from constants import OPTIMAL_SATURATION

from spotify_handler import SpotifyRequester
from alienfx_handler import AlienFX
from image_handler import get_image_average_color
from color_handler import RGB


def get_album_color(spotify_requester: SpotifyRequester, album: dict) -> RGB:
    # Getting the album cover.
    curr_streaming_album_cover = spotify_requester.get_album_cover(album=album)

    # Getting the album average color.
    album_average_color = get_image_average_color(content=curr_streaming_album_cover)
    album_rgb_color_model = RGB(*album_average_color)

    return album_rgb_color_model


def set_cpu_lights(rgb: RGB) -> None:
    # Fixing the color to be compatible with the CPU lights.
    hue, lightness, saturation = rgb.get_hls()

    # Changing Hue slightly up or down, based on the current value.
    if hue > HUE_BALANCE_POINT:
        rgb.change_hue(degrees=HUE_DELTA_UP)
    else:
        rgb.change_hue(degrees=HUE_DELTA_DOWN)

    # Changing the Lightness, based on the current value.
    if saturation < SATURATION_BALANCE_POINT:
        if lightness < LIGHTNESS_BALANCE_POINT:
            rgb.set_lightness(percentage=MIN_LIGHTNESS)  # If the color is not so bright, turn off (black).
        else:
            rgb.set_lightness(percentage=MAX_LIGHTNESS)  # If it is bright enough, set to max (white-ish).
    else:
        rgb.set_lightness(percentage=OPTIMAL_LIGHTNESS)  # If saturated enough, set to max keeping color.

    # Changing the Saturation to max value.
    rgb.set_saturation(percentage=OPTIMAL_SATURATION)

    # Setting the CPU lights.
    with AlienFX() as alien_fx:
        hex_color = rgb.get_current_color_as_hex()
        alien_fx.set_light_color(hex_color=eval(hex_color))
