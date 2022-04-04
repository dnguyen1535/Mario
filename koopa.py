import pygame as pg
from pygame.sprite import Sprite


class Koopa(Sprite):

    def __init__(self, screen, settings, pipes, blocks, enemies, mario):
        super(Koopa, self).__init__()
        self.screen = screen
        self.settings = settings
        self.pipes = pipes
        self.blocks = blocks
        self.screen_rect = screen.get_rect()
        self.enemies = enemies
        self.mario = mario

        self.frames = []
        self.image = pg.Surface((15, 15))
        sheet = pg.image.load(f'images/sprite_sheet.png')

        self.image.set_colorkey((0, 0, 0))
        self.image.blit(sheet, (0, 0), (19, 0, 16, 23))
        self.image = pg.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        self.moving_left = True
        self.kicked = False

        for i in range(0, 5):
            temp_img = pg.Surface((16, 23))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (19, i * 30, 16, 23))
            temp = pg.transform.scale(temp_img, (40, 60))
            self.frames.append(temp)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.x_change = -0.5
        self.y_change = 0.0
        self.x = self.rect.x
        self.y = self.rect.y

        self.timer = 0
        self.stunned = False
        self.set_direction = False

        self.enemy_type = 1

    def update(self, mario): pass

    def move(self):
        pass

    def falling(self):
        pass

    def draw(self):
        pass

    def swap_bool(self):
        pass
