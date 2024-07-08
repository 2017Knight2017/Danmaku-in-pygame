from typing import Callable
from pygame.math import Vector2
from gameobject import *
from moving_objects import *


def hedgehog_formation(init_pos: tuple[int, int],
                       density: list[int] | int,
                       speeds: list[float],
                       shift: list[list[float]] | list[float] = [0],
                       speed_script: dict[float, Callable[[float], float]] = {},
                       vec_script: dict[float, Callable[[Vector2], Vector2]] = {},
                       assign: tuple[int, int] = None,
                       death_point: float | int = 200):
    res = []
    for i in range(len(speeds)):
        arr = []
        match (shift[0], density, assign):
            case (list(), list(), None):
                arr.extend([Vector2(0, 1).rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift[i]])
            case (list(), list(), _):
                arr.extend([(Vector2(assign) - Vector2(init_pos)).normalize().rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift[i]])
            case (list(), int(), None):
                arr.extend([Vector2(0, 1).rotate(j + 360 / density * k) for k in range(density) for j in shift[i]])
            case (list(), int(), _):
                arr.extend([(Vector2(assign) - Vector2(init_pos)).normalize().rotate(j + 360 / density * k) for k in range(density) for j in shift[i]])
            case (float() | int(), list(), None):
                arr.extend([Vector2(0, 1).rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift])
            case (float() | int(), list(), _):
                arr.extend([(Vector2(assign) - Vector2(init_pos)).normalize().rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift])
            case (float() | int(), int(), None):
                arr.extend([Vector2(0, 1).rotate(j + 360 / density * k) for k in range(density) for j in shift])
            case (float() | int(), int(), _):
                arr.extend([(Vector2(assign) - Vector2(init_pos)).normalize().rotate(j + 360 / density * k) for k in range(density) for j in shift])
        for j in arr:
            res.append(EnemyBullet(Pattern(init_pos, j, speed=speeds[i], vec_script=vec_script, speed_script=speed_script, death_point=death_point)))
    return res