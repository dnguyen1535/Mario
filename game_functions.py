import sys
import pygame as pg


def update_screen(screen, mario, settings, level, pipes, display, stats, bricks, upgrades, enemies, flags,
                  poles, sound, secret_bricks, secret_pipes):
    screen.fill(settings.bg_color)
    if stats.flag_reach_bot and stats.timer <= 100:
        mario.move_right()
        stats.timer += 1
    if stats.timer >= 100:
        mario.move_stop()
    mario.update(stats, level, sound)
    flags.update()
    upgrades.update()
    for enemy in enemies:
        enemy.update(mario)
    bricks.update()
    mario.check_collision(screen, stats, display)
    if not stats.secret_level:
        level.draw()
        enemies.draw(screen)
        bricks.draw(screen)
        pipes.draw(screen)
        poles.draw(screen)
        flags.draw(screen)

    mario.draw()
    upgrades.draw(screen)
    display.draw(screen, stats)
    stats.update_time(sound)
    stats.update_txt()

    if stats.game_over is True:
        screen.fill((0, 0, 0))
        display.over_rect(screen)

    pg.display.flip()


def check_events(mario, stats, sound):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                sys.exit()
            elif event.key == pg.K_LEFT:
                # Stops player control when Mario has collided with the flag pole
                if not stats.reached_pole:
                    if mario.rect.left >= 20:
                        mario.move_left()
            elif event.key == pg.K_RIGHT:
                # Stops player control when Mario has collided with the flag pole
                if not stats.reached_pole:
                    mario.move_right()
            elif event.key == pg.K_DOWN:
                mario.crouch = True
            elif event.key == pg.K_SPACE:
                # Stops player control when Mario has collided with the flag pole
                if not stats.reached_pole:
                    if mario.y_change == 0:
                        sound.play_sound(7)
                        mario.move_jump()

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                mario.move_stop()
            elif event.key == pg.K_RIGHT:
                mario.move_stop()
