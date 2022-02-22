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
        self.__lifetime = 0.1
        self.radius = int(min(self.rect.height, self.rect.width) * 0.8)

    @staticmethod
    def hedgehog_init(init_pos: (int, int), density: tuple | int,
                      speeds: tuple, shift: tuple, assignation_pos: (int, int) = None):
        res = []
        for i in range(len(speeds)):
            arr = []
            match (shift[0], density, assignation_pos):
                case (tuple(), tuple(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift[i]])
                case (tuple(), tuple(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(init_pos)).normalize().rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift[i]])
                case (tuple(), int(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density * k) for k in range(density) for j in shift[i]])
                case (tuple(), int(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(init_pos)).normalize().rotate(j + 360 / density * k) for k in range(density) for j in shift[i]])
                case (int(), tuple(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift])
                case (int(), tuple(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(init_pos)).normalize().rotate(j + 360 / density[i] * k) for k in range(density[i]) for j in shift])
                case (int(), int(), None):
                    arr.extend([Vector2(0, 1).rotate(j + 360 / density * k) for k in range(density) for j in shift])
                case (int(), int(), _):
                    arr.extend([(Vector2(assignation_pos) - Vector2(init_pos)).normalize().rotate(j + 360 / density * k) for k in range(density) for j in shift])
            for j in arr:
                res.append(EnemyBullet("hedgehog", init_pos=init_pos, vec=j, speed=speeds[i]))
        return res

    @staticmethod
    def wave_init(init_pos: tuple[int, int], speed: float, spread: float, init_angle: float = 0, assignation_pos: (int, int) = None):
        return [EnemyBullet("wave", init_pos=init_pos, vec=(Vector2(assignation_pos) - Vector2(init_pos)).normalize(), speed=speed, spread=spread, init_angle=init_angle)]

    def hedgehog(self):
        self.rect.center = self.params["init_pos"] + self.params["vec"].normalize() * self.params["speed"] * self.__lifetime

    def wave(self):
        self.rect.center = self.params["init_pos"] + self.params["vec"].rotate(sin(self.__lifetime + self.params["init_angle"]) * self.params["spread"]/self.__lifetime) * self.params["speed"] * self.__lifetime

    def update(self):
        match self.movement_type:
            case "hedgehog": self.hedgehog()
            case "wave": self.wave()
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
    def __init__(self, movement_function, speed: float, x: int, y: int):
        self.true_coords = [x, y]
        self.__lifetime = 0.1
        self.speed = speed
        self.movement_function = movement_function
        super().__init__(x, y, "img/enemy.png")

    def shoot(self, movement_type: str, **kwargs) -> list:
        return [EnemyBullet(movement_type, init_pos=self.rect.center, **kwargs)]

    def update(self):
        self.true_coords = [self.true_coords[i] + elem for i, elem in enumerate(self.movement_function(self.__lifetime).normalize()*self.speed)]
        self.rect.center = self.true_coords
        if (self.rect.x >= 640 or self.rect.y >= 480) or (self.rect.x <= 230 or self.rect.y <= 0):
            self.kill()
        self.__lifetime += 0.1
