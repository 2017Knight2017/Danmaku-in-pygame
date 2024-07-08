import pygame
from typing import Callable
from pygame.math import Vector2


class Pattern:
    def __init__(self,
                 init_pos: tuple[int, int],
                 vec: Vector2,
                 speed: float = 3.0,
                 speed_script: dict[float, Callable[[float], float]] = None,
                 vec_script: dict[float, Callable[[Vector2], Vector2]] = None,
                 death_point: float = 200):
        self.init_pos = init_pos
        self.vec = vec
        self.speed = speed
        self.speed_script = speed_script or {}
        self.speed_script[0.0] = lambda x: 0
        self.speed_script_keylist = sorted(self.speed_script.keys())
        self.vec_script = vec_script or {}
        self.vec_script[0.0] = lambda vec, t, pos: vec
        self.vec_script_keylist = sorted(self.vec_script.keys())
        self.death_point = death_point

    def tick(self, object):
        if object.lifetime > self.speed_script_keylist[-1]:
            if object.lifetime > self.vec_script_keylist[-1]:
                object.true_coords += (self.vec_script[self.vec_script_keylist[-1]](self.vec, object.lifetime, object.rect.center).normalize()
                                     * (self.speed + self.speed_script[self.speed_script_keylist[-1]](object.lifetime)))
            else:
                for j in range(1, len(self.vec_script)):
                    if self.vec_script_keylist[j - 1] < object.lifetime < self.vec_script_keylist[j]:
                        object.true_coords += (self.vec_script[self.vec_script_keylist[j - 1]](self.vec, object.lifetime, object.rect.center).normalize()
                                             * (self.speed + self.speed_script[self.speed_script_keylist[-1]](object.lifetime)))
                        break
        else:
            if object.lifetime > self.vec_script_keylist[-1]:
                for i in range(1, len(self.speed_script)):
                    if self.speed_script_keylist[i - 1] < object.lifetime < self.speed_script_keylist[i]:
                        object.true_coords += (self.vec_script[self.vec_script_keylist[-1]](self.vec, object.lifetime, object.rect.center).normalize()
                                             * (self.speed + self.speed_script[self.speed_script_keylist[i - 1]](object.lifetime)))
                        break
            else:
                for i in range(1, len(self.speed_script)):
                    for j in range(1, len(self.vec_script)):
                        if (self.speed_script_keylist[i - 1] < object.lifetime < self.speed_script_keylist[i]
                                and self.vec_script_keylist[j - 1] < object.lifetime < self.vec_script_keylist[j]):
                            object.true_coords += (self.vec_script[self.vec_script_keylist[j - 1]](self.vec, object.lifetime, object.rect.center).normalize()
                                                * (self.speed + self.speed_script[self.speed_script_keylist[i - 1]](object.lifetime)))
