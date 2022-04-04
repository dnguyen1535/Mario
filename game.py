import pygame as pg
from pygame.sprite import Group
from stats import Stats
import game_functions as gf
from mario import Mario
from settings import Settings
from level import Level
from pipe import Pipe
from scoreboard import Scoreboard
from map import Map
from flag import Flag
from pole import Pole
from sound import Sound


class Game:
    def __init__(self):
        pg.init()

        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.pipes = Group()
        self.secret_pipes = Group()
        self.bricks = Group()
        self.secret_bricks = Group()
        self.upgrades = Group()
        self.enemies = Group()
        self.poles = Group()
        self.flags = Group()
        self.ground = Group()
        self.sound = Sound()
        self.stats = Stats()
        for i in range(6, 8):
            pipe = Pipe(self.screen, self.settings, i)
            self.secret_pipes.add(pipe)

        self.flag = Flag(self.screen, self.settings, self.stats)
        self.flags.add(self.flag)
        self.pole = Pole(self.screen, self.settings)
        self.poles.add(self.pole)

        self.mario = Mario(self.screen, self.settings, self.pipes, self.bricks, self.upgrades, self.stats, self.enemies,
                           self.poles, self.sound, self.secret_bricks,
                           self.secret_pipes, self.ground)
        self.lvl_map = None
        self.level = Level(self.screen, self.settings, self.pipes, self.lvl_map, self.bricks, self.upgrades,
                           self.enemies, self.flags, self.poles)
        self.display = Scoreboard(self.screen, self.stats)
        lvl_map = Map(self.screen, self.settings, self.bricks, self.pipes, self.mario, self.enemies, self.ground,
                      self.upgrades, self.stats, self.secret_bricks)
        lvl_map.build_brick()

        for i in range(0, 6):
            pipe = Pipe(self.screen, self.settings, i)
            self.pipes.add(pipe)
        flag = Flag(self.screen, self.settings, self.stats)
        self.flags.add(flag)
        pole = Pole(self.screen, self.settings)
        self.poles.add(pole)

    def update(self):
        if self.stats.game_active:
            gf.check_events(self.mario, self.stats, self.sound)

            if self.mario.rect.right >= 600 and self.stats.main_level:
                diff = self.mario.rect.right - 600
                self.mario.rect.right = 600
                self.level.camera(-diff)

            gf.update_screen(self.screen, self.mario, self.settings, self.level, self.pipes, self.display, self.stats,
                             self.bricks, self.upgrades, self.enemies, self.flags, self.poles, self.sound,
                             self.secret_bricks, self.secret_pipes)
            pg.display.flip()

    def play(self):
        self.sound.play_bg()
        while True:
            self.update()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
