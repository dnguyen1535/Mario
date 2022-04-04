import pygame as pg
from pygame.sprite import Sprite


class Brick(Sprite):
    BRICK_SIZE = 40

    def __init__(self, screen, settings, block_type):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.block_type = block_type
        self.change_brick = False

        self.sz = Brick.BRICK_SIZE

        self.brick_images = [f'images/brick_{n}.png' for n in range(8)]
        self.image = pg.transform.scale(pg.image.load(self.brick_images[block_type]), (self.sz, self.sz))

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.timer = 0
        self.hit = False

    def change(self):
        self.image = pg.transform.scale(pg.image.load(self.brick_images[4]), (self.sz, self.sz))

    def update(self):
        if self.hit:
            if self.timer <= 5:
                self.rect.y -= 1
            elif self.timer <= 10:
                self.rect.y += 1
            else:
                self.timer = 0
                self.hit = False
            self.timer += 1
