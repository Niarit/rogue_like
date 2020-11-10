from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # the unicode value of the character we want to show on the screen
        ("fg", "3B"),  # foreground color represented by 3 empty bites, which will be converted to RGB
        ("bg", "3B"),  # background, it does the same as foreground
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # a parameter describing that the tile can be walked on or not, represented by a boolean
        ("transparent", np.bool),  # this parameter describing if the tile blocks the FOV or not, boolean value
        ("dark", graphic_dt),  # the character we want to print, it is of type graphic_dt which holds it's specific data
        ("light", graphic_dt)  # Graphics for a tile which in FOV
    ]
)


def new_tile(
        *,
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents the fields what we can't see and not explored
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (58, 26, 74)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50))
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("#"), (255, 255, 255), (20, 14, 23)),
    light=(ord("#"), (255, 255, 255), (130, 110, 500))
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
    light=(ord(">"), (255, 255, 255), (200, 180, 50))
)
