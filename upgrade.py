import pygame as pg
from pygame.sprite import Sprite


class Upgrade(Sprite):
    UPGRADE_SIZE = 40

    def __init__(self, screen, settings, pipes, bricks, x, y, up_type):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.bricks = bricks
        self.pipes = pipes
        self.up_type = up_type

        self.sz = Upgrade.UPGRADE_SIZE

        self.powerUps_images = [f'images/collect_{n}.png' for n in range(5)]
        self.image = pg.transform.scale(pg.image.load(self.powerUps_images[up_type]), (self.sz, self.sz))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen_rect = screen.get_rect()

        self.y_change = 0
        self.x_change = 0

        self.stop_left = True
        self.stop_right = False

    def update(self):
        if self.up_type == 0 or self.up_type == 2 or self.up_type == 3:
            self.falling()
            self.rect.x += self.x_change
            pipe_collide = pg.sprite.spritecollide(self, self.pipes, False)
            for pipe in pipe_collide:
                if self.x_change > 0:
                    self.stop_right = True
                    self.stop_left = False
                    self.rect.right = pipe.rect.left
                if self.x_change < 0:
                    self.stop_left = True
                    self.stop_right = False
                    self.rect.left = pipe.rect.right

            self.rect.y += self.y_change
            pipe_collide = pg.sprite.spritecollide(self, self.pipes, False)
            for pipe in pipe_collide:
                if self.y_change > 0:
                    self.rect.bottom = pipe.rect.top
                elif self.y_change < 0:
                    self.rect.top = pipe.rect.bottom
                self.y_change = 0
            brick_collide = pg.sprite.spritecollide(self, self.bricks, False)
            for brick in brick_collide:
                if self.y_change > 0:
                    self.rect.bottom = brick.rect.top
                elif self.y_change < 0:
                    self.rect.top = brick.rect.bottom
                self.y_change = 0

            if not self.stop_right:
                self.move_right()

            if not self.stop_left:
                self.move_left()

    def move_right(self):
        self.x_change = 1

    def move_left(self):
        self.x_change = -1

    def falling(self):
        if self.y_change == 0:
            self.y_change = 1
        else:
            self.y_change += .05
        if self.rect.y >= self.settings.base_level - self.rect.height and self.y_change >= 0:
            self.y_change = 0
            self.rect.y = self.settings.base_level - self.rect.height

    def draw(self):
        self.screen.blit(self.image, self.rect)
