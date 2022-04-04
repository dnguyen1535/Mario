import pygame as pg
from pygame.sprite import Sprite


class Goomba(Sprite):

    def __init__(self, screen, settings, pipes, blocks, ground):
        super(Goomba, self).__init__()
        self.screen = screen
        self.settings = settings
        self.pipes = pipes
        self.blocks = blocks
        self.ground = ground
        self.screen_rect = screen.get_rect()

        self.frames = []
        self.image = pg.Surface((15, 15))
        sheet = pg.image.load(f'images/sprite_sheet.png')

        self.image.set_colorkey((0, 0, 0))
        self.image.blit(sheet, (0, 0), (0, 0, 15, 16))
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.moving_left = False
        self.moving_right = False

        for i in range(0, 4):
            temp_img = pg.Surface((16, 16))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (0, i*20, 16, 16))
            temp = pg.transform.scale(temp_img, (40, 40))
            self.frames.append(temp)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        self.x_change = -0.5
        self.y_change = 0.0

        self.timer = 0
        self.enemy_type = 0

    def update(self, mario): pass

    def move(self): pass

    def falling(self): pass

    def draw(self): pass
