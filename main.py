from moving_objects import *
from side_bar import Sidebar


# 384x448
pygame.init()
mainsurf = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
background = Sidebar()
plr = pygame.sprite.GroupSingle(Player(320, 400))
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
FPS = 60
l = 0

while True:
    curtime = round(pygame.time.get_ticks())
    mainsurf.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_g]:
        if curtime - l > 100:
            enemy_bullets.add(EnemyBullet.hedgehog_init(
                init_pos=(192, 200),
                density=4,
                speeds=[3],
                assign=plr.sprite.rect.center))
            l = curtime

    enemy_bullets.draw(mainsurf)
    enemy_bullets.update()
    enemies_group.draw(mainsurf)
    enemies_group.update()
    player_bullets.draw(mainsurf)
    player_bullets.update()
    plr.draw(mainsurf)
    plr.update(player_bullets, curtime, enemy_bullets)
    mainsurf.blits(blit_sequence=((background.surf[0], (-81, 0)),
                                  (background.surf[1], (239, -14)),
                                  (background.surf[1], (239, 461)),
                                  (background.surf[0], (622, 0))))
    clock.tick(FPS)
    pygame.display.update()
