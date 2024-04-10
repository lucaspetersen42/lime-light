import colorsys
from math import sqrt, cos, sin, radians


class RGB:
    # ToDo :: Bugs on data persistency yet
    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b
        self.matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def get_current_color(self, as_int: bool = True):
        if as_int:
            return self.clamp(self.r), self.clamp(self.g), self.clamp(self.b)
        else:
            return self.r, self.g, self.b

    def get_current_color_as_hex(self):
        red, green, blue = self.get_current_color()
        return '0x{:02x}{:02x}{:02x}'.format(red, green, blue)

    @staticmethod
    def clamp(v):
        if v < 0:
            return 0
        if v > 255:
            return 255
        return int(v + 0.5)

    def get_hls(self, nround: int = -1):
        h, l, s = colorsys.rgb_to_hls(self.r / 255.0, self.g / 255.0, self.b / 255.0)
        if nround == -1:
            return h, l, s
        else:
            return round(h, nround), round(l, nround), round(s, nround)

    def change_hue(self, degrees: float):
        cosA = cos(radians(degrees))
        sinA = sin(radians(degrees))

        self.matrix[0][0] = cosA + (1.0 - cosA) / 3.0
        self.matrix[0][1] = 1.0 / 3.0 * (1.0 - cosA) - sqrt(1.0 / 3.0) * sinA
        self.matrix[0][2] = 1.0 / 3.0 * (1.0 - cosA) + sqrt(1.0 / 3.0) * sinA
        self.matrix[1][0] = 1.0 / 3.0 * (1.0 - cosA) + sqrt(1.0 / 3.0) * sinA
        self.matrix[1][1] = cosA + 1.0 / 3.0 * (1.0 - cosA)
        self.matrix[1][2] = 1.0 / 3.0 * (1.0 - cosA) - sqrt(1.0 / 3.0) * sinA
        self.matrix[2][0] = 1.0 / 3.0 * (1.0 - cosA) - sqrt(1.0 / 3.0) * sinA
        self.matrix[2][1] = 1.0 / 3.0 * (1.0 - cosA) + sqrt(1.0 / 3.0) * sinA
        self.matrix[2][2] = cosA + 1.0 / 3.0 * (1.0 - cosA)

        rx = self.r * self.matrix[0][0] + self.g * self.matrix[0][1] + self.b * self.matrix[0][2]
        gx = self.r * self.matrix[1][0] + self.g * self.matrix[1][1] + self.b * self.matrix[1][2]
        bx = self.r * self.matrix[2][0] + self.g * self.matrix[2][1] + self.b * self.matrix[2][2]

        return self.clamp(rx), self.clamp(gx), self.clamp(bx)

    def set_saturation(self, percentage: float):
        h, l, _ = self.get_hls()
        s = percentage
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        rx = r * 255
        gx = g * 255
        bx = b * 255
        self.r = rx
        self.g = gx
        self.b = bx
        return self.clamp(rx), self.clamp(gx), self.clamp(bx)

    def set_lightness(self, percentage: float):
        h, _, s = self.get_hls()
        l = percentage
        r, g, b = colorsys.hls_to_rgb(h, l, s)

        rx = r * 255
        gx = g * 255
        bx = b * 255
        self.r = rx
        self.g = gx
        self.b = bx
        return self.clamp(rx), self.clamp(gx), self.clamp(bx)


if __name__ == '__main__':
    RGB(r=200, g=140, b=100).get_ansi()