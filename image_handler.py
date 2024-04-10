from io import BytesIO
from PIL import Image
from typing import List, Tuple


Pixel = Tuple[float, float, float]


def get_image_pixels(content: bytes) -> List[Pixel]:
    """Returns the image pixels as a flattened array of RGB tuples, given its content as bytes."""
    buffer = BytesIO(content)
    pillow_image = Image.open(buffer)

    width, height = pillow_image.size
    image_pixels_colors = []

    for y in range(height):
        for x in range(width):
            pixel_color = pillow_image.getpixel((x, y))
            if not isinstance(pixel_color, tuple):
                pixel_color = (pixel_color, pixel_color, pixel_color)
            image_pixels_colors.append(pixel_color)

    return image_pixels_colors


def get_image_average_color(content: bytes) -> Pixel:
    """Returns the image average pixel color, given its content as bytes."""
    image_pixels = get_image_pixels(content=content)

    sum_red = 0
    sum_green = 0
    sum_blue = 0
    for pixel in image_pixels:
        sum_red += pixel[0]
        sum_green += pixel[1]
        sum_blue += pixel[2]

    avg_red = sum_red / len(image_pixels)
    avg_green = sum_green / len(image_pixels)
    avg_blue = sum_blue / len(image_pixels)
    avg_color = (avg_red, avg_green, avg_blue)

    return avg_color
