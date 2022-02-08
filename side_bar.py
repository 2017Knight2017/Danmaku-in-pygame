import pygame


class Sidebar:
    def __init__(self):
        self.surf = Sidebar.__createBackground(pygame.image.load("img/tile.png").convert())

    @staticmethod
    def __createBackground(tile):
        res = []
        a = pygame.surface.Surface((32*10, 32*15))
        for i in range(10):
            for j in range(15):
                a.blit(tile, (i*32, j*32))
        res.append(a)
        b = pygame.surface.Surface((32*13, 32))
        for i in range(13):
            b.blit(tile, (i*32, 0))
        res.append(b)
        return res
