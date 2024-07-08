import pygame


def normalize_coords(x: int, y: int) -> tuple[int, int]:
    """Used in most of cases"""
    return x + 239, y + 19

def realize_coords(x: int, y: int) -> tuple[int, int]:
    """Used only for getting the true_coords"""
    return x - 239, y - 19


class Gameobject(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, filename="", image=None):
        pygame.sprite.Sprite.__init__(self)
        if filename: self.image = pygame.image.load(filename).convert_alpha()
        elif image: self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))