from __future__ import annotations

import ctypes
from constants import ALIENFX_DLL_PATH, ALIENFX_LIGHT_MODE, ALIENFX_LIGHT_BRIGHTNESS


class AlienFX:
    def __init__(self, dll_filepath: str = ALIENFX_DLL_PATH):
        self.dll_filepath = dll_filepath
        self.alien_fx = None

    def initialize(self):
        if not self.alien_fx:
            alien_fx = ctypes.CDLL(self.dll_filepath)
            self.alien_fx = alien_fx

        self.alien_fx.LFX_Initialize()
        # print('AlienFX Initialized.')

    def close(self):
        if self.alien_fx:
            # print('AlienFX Released.')
            self.alien_fx.LFX_Release()

    def set_light_color(self, hex_color: int) -> None:
        self.alien_fx.LFX_Light(ALIENFX_LIGHT_MODE, hex_color | (ALIENFX_LIGHT_BRIGHTNESS << 24))
        self.alien_fx.LFX_Update()

    def __enter__(self) -> AlienFX:
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
