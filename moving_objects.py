import pygame
from typing import Callable
from pygame.math import Vector2
from gameobject import *
from pattern import *


class EnemyBullet(Gameobject):
    def __init__(self, pattern: Pattern, img: str = "img/enemy_bullet.png"):
        self.pattern = pattern
        self.true_coords = Vector2(self.pattern.init_pos)
        self.lifetime = 0.1
        super().__init__(*self.true_coords, img)
        self.radius = int(min(self.rect.height, self.rect.width) * 0.8)

    def update(self):
        self.pattern.tick(self)
        self.rect.center = self.true_coords
        if (not (230 <= self.rect.x <= 640 or 0 <= self.rect.y <= 480) or self.lifetime >= self.pattern.death_point):
            self.kill()
        self.lifetime += 0.1


class PlayerBullet(Gameobject):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, filename="img/player_bullet.png")

    def update(self):
        self.rect.y -= self.rect.height
        if self.rect.y <= 0:
            self.kill()


class Player(Gameobject):
    def __init__(self, x: int, y: int):
        self.straight_pose = pygame.image.load("img/reimu_straight.png")
        self.leftright_pose = pygame.image.load("img/reimu_leftright.png")
        self.normal_speed = 3
        self.true_coords = [x, y]
        self.last_shot = 0
        self.radius = 1
        super().__init__(x, y, image=self.straight_pose)

    def attack(self, bullets_group, curtime):
        if curtime - self.last_shot > 60:
            bullets_group.add(PlayerBullet(self.rect.centerx, self.rect.top))
            self.last_shot = curtime

    def update(self, player_bullets, curtime, enemy_bullets):
        keys = pygame.key.get_pressed()
        #self.true_coords += pygame.Vector2((self.rect.x < (620 - self.rect.width)) * keys[pygame.K_RIGHT] - (241 < self.rect.x) * keys[pygame.K_LEFT],
        #                                   (self.rect.y < (460 - self.rect.height)) * keys[pygame.K_DOWN] - (20 < self.rect.y) * keys[pygame.K_UP]) / (keys[pygame.K_LSHIFT] + 1) * self.normal_speed
        direction = pygame.Vector2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])
        if direction != pygame.Vector2(0, 0): 
            self.true_coords += direction.normalize() / (keys[pygame.K_LSHIFT] + 1) * self.normal_speed
        self.rect.topleft = self.true_coords
        
        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]: self.image = self.leftright_pose
            elif keys[pygame.K_RIGHT]: self.image = pygame.transform.flip(self.leftright_pose, True, False)
        else:
            self.image = self.straight_pose
        if keys[pygame.K_z]:
            self.attack(player_bullets, curtime)
        pygame.sprite.groupcollide(self.groups()[0], enemy_bullets, False, True, pygame.sprite.collide_circle)


class Enemy(Gameobject):
    def __init__(self, movement_function: Callable[[float], Vector2], speed: float, x: int, y: int):
        self.true_coords = [x, y]
        self.lifetime = 0.1
        self.speed = speed
        self.movement_function = movement_function
        super().__init__(x, y, "img/enemy.png")

    def shoot(self, movement_type: str, **kwargs) -> list:
        return [EnemyBullet(movement_type, init_pos=self.rect.center, **kwargs)]

    def update(self):
        self.true_coords = [self.true_coords[i] + elem for i, elem in enumerate(self.movement_function(self.lifetime).normalize()*self.speed)]
        self.rect.center = self.true_coords
        if not (230 <= self.rect.x <= 640 or 0 <= self.rect.y <= 480):
            self.kill()
        self.lifetime += 0.1
