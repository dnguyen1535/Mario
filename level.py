import pygame as pg


class Level:
    def __init__(self, screen, settings, pipes, lvl_map, bricks, upgrades, enemies, flags, poles):
        self.screen = screen
        self.settings = settings
        self.bricks = bricks
        self.lvl_map = lvl_map
        self.pipes = pipes
        self.upgrades = upgrades
        self.enemies = enemies
        self.flags = flags
        self.poles = poles
        self.image = pg.image.load(f'images/level_bg.png')
        self.image = pg.transform.scale(self.image, (10910, self.settings.screen_height))  # 8300
        self.rect = self.image.get_rect()

        self.shift_world = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def camera(self, shifting_x):
        self.shift_world += shifting_x

        self.rect.x += shifting_x
        for flag in self.flags:
            flag.rect.x += shifting_x
        for pole in self.poles:
            pole.rect.x += shifting_x

        for brick in self.bricks:
            brick.rect.x += shifting_x
        for pipe in self.pipes:
            pipe.rect.x += shifting_x
        for upgrade in self.upgrades:
            upgrade.rect.x += shifting_x
        for enemy in self.enemies:
            enemy.x += shifting_x
