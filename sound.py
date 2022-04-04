import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        self.track = [pg.mixer.Sound(f'sounds/bg_music.wav'), pg.mixer.Sound(f'sounds/block_bump.wav'),
                      pg.mixer.Sound(f'sounds/brick_break.wav'), pg.mixer.Sound(f'sounds/coin.wav'),
                      pg.mixer.Sound(f'sounds/death.wav'), pg.mixer.Sound(f'sounds/extra_life.wav'),
                      pg.mixer.Sound(f'sounds/fireball.wav'), pg.mixer.Sound(f'sounds/jump.wav'),
                      pg.mixer.Sound(f'sounds/kill.wav'),
                      pg.mixer.Sound(f'sounds/pipe.wav'), pg.mixer.Sound(f'sounds/power_spawn.wav'),
                      pg.mixer.Sound(f'sounds/powerup.wav'), pg.mixer.Sound(f'sounds/stage_clear.wav'),
                      pg.mixer.Sound(f'sounds/star.wav')]

    def play_bg(self): self.play_music('sounds/bg_music.wav')

    def play_music(self, music, volume=0.3):
        pg.mixer.music.unload()  # stop previous music playing before beginning another
        pg.mixer.music.load(music)
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.play(-1, 0.0)

    def play_sound(self, num): pg.mixer.Sound.play(self.track[num])

    def stop_bg(self): pg.mixer.music.stop()
