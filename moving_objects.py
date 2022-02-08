import pygame
from pygame.math import Vector2
from math import sin


class Gameobject(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, filename="", image=None):
        pygame.sprite.Sprite.__init__(self)
        if filename: self.image = pygame.image.load(filename).convert_alpha()
        elif image: self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))


#### BULLETS ####


class EnemyBullet(Gameobject):
    def __init__(self, movement_type: str, **kwargs):
        super().__init__(0, 0, "img/enemy_bullet.png")
        self.movement_type = movement_type
        self.params = kwargs
        self.pos = pygame.math.Vector2()
        self.__lifetime = 0
        self.radius = int(min(self.rect.height, self.rect.width) * 0.8)

    @staticmethod
    def hedgehog_init(density: tuple | int, center: (int, int),
                      speeds: tuple, shift: tuple, assignation_pos: (int, int) = None):
        res = []
        for i in range(len(speeds)):
            arr = []
            match (shift[0], density, assignation_pos):
                case (tuple(), tuple(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift[i]])
                case (tuple(), tuple(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(center)).normalize().rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift[i]])
                case (tuple(), int(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density * k) for k in range(density) for j in shift[i]])
                case (tuple(), int(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(center)).normalize().rotate(j + 360 / density * k) for k in range(density) for j in shift[i]])
                case (int(), tuple(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift])
                case (int(), tuple(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(center)).normalize().rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift])
                case (int(), int(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density * k) for k in range(density) for j in shift])
                case (int(), int(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(center)).normalize().rotate(j + 360 / density * k) for k in range(density) for j in shift])
            for j in arr:
                res.append(EnemyBullet("hedgehog", center=center, vec=j, speed=speeds[i]))
        return res

    def hedgehog(self):
        self.rect.center = self.params["center"] + self.params["vec"].normalize() * self.params["speed"] * self.__lifetime

    def horizontal_wave(self):
        self.rect.y = round(sin(self.__lifetime/self.params["vertical_speed"]) * self.params["spread"]) + self.params["center"]
        self.rect.x += self.params["horizontal_speed"]

    def vertical_wave(self):
        self.rect.y += self.params["vertical_speed"]
        self.rect.x = round(sin(self.__lifetime/self.params["horizontal_speed"]) * self.params["spread"]) + self.params["center"]

    def update(self):
        match self.movement_type:
            case "vertical_wave": self.vertical_wave()
            case "horizontal_wave": self.horizontal_wave()
            case "hedgehog": self.hedgehog()
        if (self.rect.x >= 640 or self.rect.y >= 480) or (self.rect.x <= 230 or self.rect.y <= 0):
            self.kill()
        self.__lifetime += 0.1


class PlayerBullet(Gameobject):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, filename="img/player_bullet.png")

    def update(self):
        self.rect.y -= self.rect.height
        if self.rect.y <= 0:
            self.kill()


#### BULLETS ####


class Player(Gameobject):
    def __init__(self, x: int, y: int):
        self.__STRAIGHT_POSE = pygame.image.load("img/reimu_straight.png")
        self.__LEFTRIGHT_POSE = pygame.image.load("img/reimu_leftright.png")
        self.__SHIFT_SPEED = 1.5
        self.__NORMAL_SPEED = 3
        self.true_coords = [x, y]
        self.side_movement = False
        self.last_shot = 0
        self.radius = 1
        super().__init__(x, y, image=self.__STRAIGHT_POSE)

    def move_left(self, shift: bool):
        self.side_movement = True
        if not shift: self.true_coords[0] -= self.__NORMAL_SPEED
        else:         self.true_coords[0] -= self.__SHIFT_SPEED

    def move_right(self, shift: bool):
        self.side_movement = True
        if not shift: self.true_coords[0] += self.__NORMAL_SPEED
        else:         self.true_coords[0] += self.__SHIFT_SPEED

    def move_up(self, shift: bool):
        if not shift: self.true_coords[1] -= self.__NORMAL_SPEED
        else:         self.true_coords[1] -= self.__SHIFT_SPEED

    def move_down(self, shift: bool):
        if not shift: self.true_coords[1] += self.__NORMAL_SPEED
        else:         self.true_coords[1] += self.__SHIFT_SPEED

    def attack(self, bullets_group, curtime):
        if curtime - self.last_shot > 60:
            bullets_group.add(PlayerBullet(self.rect.centerx, self.rect.top))
            self.last_shot = curtime

    def update(self, player_bullets, curtime, enemy_bullets):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 241:
            self.move_left(keys[pygame.K_LSHIFT])
        if keys[pygame.K_RIGHT] and self.rect.x < (620 - self.rect.width):
            self.move_right(keys[pygame.K_LSHIFT])
        if keys[pygame.K_UP] and self.rect.y > 20:
            self.move_up(keys[pygame.K_LSHIFT])
        if keys[pygame.K_DOWN] and self.rect.y < (460 - self.rect.height):
            self.move_down(keys[pygame.K_LSHIFT])
        if keys[pygame.K_z]:
            self.attack(player_bullets, curtime)
        self.rect.topleft = self.true_coords
        if self.side_movement and keys[pygame.K_LEFT] != keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]: self.image = self.__LEFTRIGHT_POSE
            elif keys[pygame.K_RIGHT]: self.image = pygame.transform.flip(self.__LEFTRIGHT_POSE, True, False)
        else:
            self.side_movement = False
            self.image = self.__STRAIGHT_POSE
        pygame.sprite.groupcollide(self.groups()[0], enemy_bullets, False, True, pygame.sprite.collide_circle)


class Enemy(Gameobject):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "img/enemy.png")
