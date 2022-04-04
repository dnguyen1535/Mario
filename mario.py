import pygame as pg
from pygame.sprite import Sprite
from upgrade import Upgrade
from map import Map


class Mario(Sprite):

    def __init__(self, screen, settings, pipes, bricks, upgrades, stats, enemies, poles, sound,
                  secret_bricks, secret_pipes, ground):
        super(Mario, self).__init__()
        self.sound = sound
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.pipes = pipes
        self.ground = ground
        self.secret_pipes = secret_pipes
        self.bricks = bricks
        self.secret_bricks = secret_bricks
        self.upgrades = upgrades
        self.enemies = enemies
        self.poles = poles
        self.screen_rect = screen.get_rect()

        self.mario_states = []
        self.small_mario = []
        self.small_star_mario = []
        self.mush_mario = []
        self.flower_mario = []
        self.star_mario = []
        self.image = pg.Surface((16, 16))
        sheet = pg.image.load(f'images/sprite_sheet.png')

        self.image.set_colorkey((0, 0, 0))
        self.image.blit(sheet, (0, 0), (59, 0, 17, 16))
        self.image = pg.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.facing_right = True
        self.crouch = False

        for i in range(0, 13):
            # base mario
            temp_img = pg.Surface((17, 16))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (60, i * 20, 17, 16))
            temp = pg.transform.scale(temp_img, (40, 40))
            self.small_mario.append(temp)
            
            # small star mario
            temp_img = pg.Surface((17, 16))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (80, i * 20, 17, 16))
            temp = pg.transform.scale(temp_img, (40, 40))
            self.small_star_mario.append(temp)
            
            # self.mario_states.append(temp)
            temp_img = pg.Surface((17, 16))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (100, i * 20, 17, 16))
            temp = pg.transform.scale(temp_img, (40, 40))
            self.small_star_mario.append(temp)
            
            # mush mario
            temp_img = pg.Surface((17, 32))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (120, i * 40, 17, 32))
            temp = pg.transform.scale(temp_img, (40, 60))
            self.mush_mario.append(temp)
            
            # flower mario
            temp_img = pg.Surface((17, 32))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (140, i * 40, 17, 32))
            temp = pg.transform.scale(temp_img, (40, 60))
            self.flower_mario.append(temp)
            self.star_mario.append(temp)
            
            # star mario
            temp_img = pg.Surface((17, 32))
            temp_img.set_colorkey((0, 0, 0))
            temp_img.blit(sheet, (0, 0), (160, i * 40, 17, 32))
            temp = pg.transform.scale(temp_img, (40, 60))
            self.star_mario.append(temp)

        temp_img = pg.Surface((17, 16))
        temp_img.set_colorkey((0, 0, 0))
        temp_img.blit(sheet, (0, 0), (59, 260, 17, 16))
        temp = pg.transform.scale(temp_img, (40, 40))
        self.small_mario.append(temp)

        self.image = self.small_mario[0]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.x_change = 0
        self.y_change = 0

        self.timer = 0
        self.flash_frame = 0
        self.star_timer = 0
        self.invinc_length = 0
        self.count = 0

        self.invinc = False
        self.dead = False
        self.mush = False
        self.fired = False
        self.star_pow = False

    def update(self, stats, level, sound):
        self.invincible()
        if self.dead:
            self.image = self.small_mario[12]
            self.die_animate(stats, level, sound)
        else:
            if not self.mush and not self.star_pow:
                self.update_small(sound)
            elif self.star_pow and not self.mush:
                self.update_star(sound)
            elif self.mush and not self.fired and not self.star_pow:
                self.update_mush(sound)
            elif self.fired and not self.star_pow:
                self.update_flowered(sound)
            elif self.mush and self.star_pow:
                self.update_big_star(sound)

        if self.star_pow:
            if self.star_timer <= 750:
                self.star_timer += 1
            else:
                self.star_timer = 0
                self.star_pow = False

    def update_small(self, sound):
        self.move(sound)
        if self.rect.y == self.settings.base_level - self.rect.height:
            self.jump = False

        if not self.moving_right and not self.moving_left and not self.jump:
            if self.facing_right:
                self.image = self.small_mario[0]
            else:
                self.image = self.small_mario[6]
        if self.moving_right and not self.jump:
            self.right_animate()
        if self.facing_right and self.jump:
            self.image = self.small_mario[5]
        if self.moving_left and not self.jump:
            self.left_animate()
        if not self.facing_right and self.jump:
            self.image = self.small_mario[11]

    def update_mush(self, sound):
        self.move(sound)
        if self.rect.y == self.settings.base_level - self.rect.height:
            self.jump = False

        if not self.moving_right and not self.moving_left and not self.jump:
            if self.facing_right:
                self.image = self.mush_mario[0]
            else:
                self.image = self.mush_mario[6]
        if self.moving_right and not self.jump:
            self.big_right_animate()
        if self.facing_right and self.jump:
            self.image = self.mush_mario[5]
        if self.moving_left and not self.jump:
            self.big_left_animate()
        if not self.facing_right and self.jump:
            self.image = self.mush_mario[11]

    def update_flowered(self, sound):
        self.move(sound)
        if self.rect.y == self.settings.base_level - self.rect.height:
            self.jump = False

        if not self.moving_right and not self.moving_left and not self.jump:
            if self.facing_right:
                self.image = self.flower_mario[0]
            else:
                self.image = self.flower_mario[6]
        if self.moving_right and not self.jump:
            self.flower_right_animate()
        if self.facing_right and self.jump:
            self.image = self.flower_mario[5]
        if self.moving_left and not self.jump:
            self.flower_left_animate()
        if not self.facing_right and self.jump:
            self.image = self.flower_mario[11]

    def update_star(self, sound):
        self.move(sound)
        if self.rect.y == self.settings.base_level - self.rect.height:
            self.jump = False

        if not self.moving_right and not self.moving_left and not self.jump:
            self.star_flash()
        if self.moving_right and not self.jump:
            self.right_star_flash()
        if self.facing_right and self.jump:
            self.right_star_jump()
        if self.moving_left and not self.jump:
            self.left_star_flash()
        if not self.facing_right and self.jump:
            self.left_star_jump()

    def update_big_star(self, sound):
        self.move(sound)
        if self.rect.y == self.settings.base_level - self.rect.height:
            self.jump = False

        if not self.moving_right and not self.moving_left and not self.jump:
            self.big_star_flash()
        if self.moving_right and not self.jump:
            self.big_right_star_flash()
        if self.facing_right and self.jump:
            self.big_right_star_jump()
        if self.moving_left and not self.jump:
            self.big_left_star_flash()
        if not self.facing_right and self.jump:
            self.big_left_star_jump()

    def star_flash(self):
        if self.timer <= 50:
            if self.facing_right:
                self.image = self.small_star_mario[0]
            else:
                self.image = self.small_star_mario[12]
        elif self.timer <= 100:
            if self.facing_right:
                self.image = self.small_star_mario[1]
            else:
                self.image = self.small_star_mario[13]
        elif self.timer <= 150:
            if self.facing_right:
                self.image = self.small_mario[0]
            else:
                self.image = self.small_mario[6]
        else:
            self.timer = 0
        self.timer += 4

    def right_star_jump(self):
        if self.timer <= 50:
            self.image = self.small_star_mario[10]
        elif self.timer <= 100:
            self.image = self.small_star_mario[11]
        elif self.timer <= 150:
            self.image = self.small_mario[5]
        else:
            self.timer = 0
        self.timer += 4

    def right_star_flash(self):
        if self.timer <= 50:
            self.image = self.small_star_mario[2]
        elif self.timer <= 100:
            self.image = self.small_star_mario[5]
        elif self.timer <= 150:
            self.image = self.small_mario[3]
        else:
            self.timer = 0
        self.timer += 4

    def right_animate(self):
        if self.timer <= 50:
            self.image = self.small_mario[1]
        elif self.timer <= 100:
            self.image = self.small_mario[2]
        elif self.timer <= 150:
            self.image = self.small_mario[3]
        else:
            self.timer = 0
        self.timer += 4

    def left_star_jump(self):
        if self.timer <= 50:
            self.image = self.small_star_mario[22]
        elif self.timer <= 100:
            self.image = self.small_star_mario[23]
        elif self.timer <= 150:
            self.image = self.small_mario[11]
        else:
            self.timer = 0
        self.timer += 4

    def left_star_flash(self):
        if self.timer <= 50:
            self.image = self.small_star_mario[14]
        elif self.timer <= 100:
            self.image = self.small_star_mario[17]
        elif self.timer <= 150:
            self.image = self.small_mario[9]
        else:
            self.timer = 0
        self.timer += 4

    def left_animate(self):
        if self.timer <= 50:
            self.image = self.small_mario[7]
        elif self.timer <= 100:
            self.image = self.small_mario[8]
        elif self.timer <= 150:
            self.image = self.small_mario[9]
        else:
            self.timer = 0
        self.timer += 4

    def big_star_flash(self):
        if self.timer <= 50:
            if self.facing_right:
                self.image = self.star_mario[0]
            else:
                self.image = self.star_mario[12]
        elif self.timer <= 100:
            if self.facing_right:
                self.image = self.star_mario[1]
            else:
                self.image = self.star_mario[13]
        elif self.timer <= 150:
            if self.facing_right:
                self.image = self.mush_mario[0]
            else:
                self.image = self.mush_mario[6]
        else:
            self.timer = 0
        self.timer += 4

    def big_right_star_jump(self):
        if self.timer <= 50:
            self.image = self.star_mario[10]
        elif self.timer <= 100:
            self.image = self.star_mario[11]
        elif self.timer <= 150:
            self.image = self.mush_mario[5]
        else:
            self.timer = 0
        self.timer += 4

    def big_right_star_flash(self):
        if self.timer <= 50:
            self.image = self.star_mario[2]
        elif self.timer <= 100:
            self.image = self.star_mario[5]
        elif self.timer <= 150:
            self.image = self.mush_mario[3]
        else:
            self.timer = 0
        self.timer += 4

    def big_right_animate(self):
        if self.timer <= 50:
            self.image = self.mush_mario[1]
        elif self.timer <= 100:
            self.image = self.mush_mario[2]
        elif self.timer <= 150:
            self.image = self.mush_mario[3]
        else:
            self.timer = 0
        self.timer += 4

    def big_left_star_jump(self):
        if self.timer <= 50:
            self.image = self.star_mario[22]
        elif self.timer <= 100:
            self.image = self.star_mario[23]
        elif self.timer <= 150:
            self.image = self.mush_mario[11]
        else:
            self.timer = 0
        self.timer += 4

    def big_left_star_flash(self):
        if self.timer <= 50:
            self.image = self.star_mario[14]
        elif self.timer <= 100:
            self.image = self.star_mario[17]
        elif self.timer <= 150:
            self.image = self.mush_mario[9]
        else:
            self.timer = 0
        self.timer += 4

    def big_left_animate(self):
        if self.timer <= 50:
            self.image = self.mush_mario[7]
        elif self.timer <= 100:
            self.image = self.mush_mario[8]
        elif self.timer <= 150:
            self.image = self.mush_mario[9]
        else:
            self.timer = 0
        self.timer += 4

    def flower_right_animate(self):
        if self.timer <= 50:
            self.image = self.flower_mario[1]
        elif self.timer <= 100:
            self.image = self.flower_mario[2]
        elif self.timer <= 150:
            self.image = self.flower_mario[3]
        else:
            self.timer = 0
        self.timer += 4

    def flower_left_animate(self):
        if self.timer <= 50:
            self.image = self.flower_mario[7]
        elif self.timer <= 100:
            self.image = self.flower_mario[8]
        elif self.timer <= 150:
            self.image = self.flower_mario[9]
        else:
            self.timer = 0
        self.timer += 4

    def move(self, sound):
        self.sound = sound
        if pg.sprite.spritecollide(self, self.poles, False):
            self.stats.reached_pole = True
            self.timer = 0
            if self.rect.y != 508:
                self.rect.y += 1
            self.rect.x += self.x_change
        else:
            self.falling()

            if self.rect.left > 20:
                self.rect.x += self.x_change
            else:
                self.rect.x = 22
            if not self.stats.secret_level:
                pipe_collide = pg.sprite.spritecollide(self, self.pipes, False)
                for pipe in pipe_collide:
                    if self.x_change > 0:
                        self.rect.right = pipe.rect.left
                    if self.x_change < 0:
                        self.rect.left = pipe.rect.right

                self.rect.y += self.y_change
                pipe_collide = pg.sprite.spritecollide(self, self.pipes, False)
                for pipe in pipe_collide:
                    if self.y_change > 0:
                        self.rect.bottom = pipe.rect.top
                        if pipe.num == 3 and self.crouch:
                            self.stats.activate_secret = True
                            self.stats.secret_level = True
                    elif self.y_change < 0:
                        self.rect.top = pipe.rect.bottom
                    self.y_change = 0

                # Mario collides with side of bricks
                brick_collide = pg.sprite.spritecollide(self, self.bricks, False)
                for brick in brick_collide:
                    if self.rect.right >= brick.rect.left and brick.rect.bottom == self.rect.bottom:
                        self.x_change = 0
                    if self.rect.left <= brick.rect.right and brick.rect.bottom == self.rect.bottom:
                        self.x_change = 0

                brick_collide = pg.sprite.spritecollide(self, self.bricks, False)
                for brick in brick_collide:
                    if self.y_change > 0:
                        self.rect.bottom = brick.rect.top
                    elif self.y_change < 0:
                        self.rect.top = brick.rect.bottom
                    self.y_change = 0

                    if brick.rect.x - 20 < self.rect.x < brick.rect.x + 20 and brick.rect.y < self.rect.y \
                            and brick.block_type == 5 and not brick.change_brick:
                        brick.change_brick = True
                        upgrade = Upgrade(self.screen, self.settings, self.pipes, self.bricks,
                                          brick.rect.x, brick.rect.y - 20, 3)
                        self.upgrades.add(upgrade)
                        brick.change()

                    if brick.rect.x - 20 < self.rect.x < brick.rect.x + 20 and brick.rect.y < self.rect.y \
                            and brick.block_type == 6 and not brick.change_brick:
                        brick.change_brick = True
                        upgrade = Upgrade(self.screen, self.settings, self.pipes, self.bricks,
                                          brick.rect.x, brick.rect.y - 20, 2)
                        self.upgrades.add(upgrade)
                        brick.change()

                    if brick.rect.x - 20 < self.rect.x < brick.rect.x + 20 and brick.rect.y < self.rect.y \
                            and brick.block_type == 2:
                        brick.change()

                        if brick.block_type == 2 and not brick.change_brick and brick.rect.y < self.rect.y \
                                and not self.mush:
                            brick.change_brick = True
                            upgrade = Upgrade(self.screen, self.settings, self.pipes, self.bricks,
                                              brick.rect.x, brick.rect.y - 20, 0)
                            self.upgrades.add(upgrade)
                        # spawns a fire flower
                        if brick.block_type == 2 and not brick.change_brick and brick.rect.y < self.rect.y \
                                and self.mush:
                            brick.change_brick = True
                            upgrade = Upgrade(self.screen, self.settings, self.pipes, self.bricks,
                                              brick.rect.x, brick.rect.y - 40, 1)
                            self.upgrades.add(upgrade)
                    #  draws a coin for item block
                    if brick.rect.x - 20 < self.rect.x < brick.rect.x + 20 and brick.rect.y < self.rect.y \
                            and brick.block_type == 1:
                        brick.change()
                        self.stats.coins += 1

                    if brick.rect.x - 20 < self.rect.x < brick.rect.x + 20 and brick.rect.y < self.rect.y \
                            and brick.block_type == 9 and not brick.change_brick:
                        if self.count != 4:
                            self.stats.coins += 1
                            self.count += 1
                        else:
                            brick.change_brick = True
                            brick.change()

                    # Check if Mario is big and below the block and if he is and hits it the brick is removed
                    if brick.rect.x - 20 < self.rect.x < brick.rect.x + 20 and brick.rect.y < self.rect.y \
                            and brick.block_type == 0 and self.mush:
                        self.bricks.remove(brick)
                        self.sound.play_sound(2)
                    elif brick.rect.x - 20 < self.rect.x < brick.rect.x + 20 and brick.rect.y < self.rect.y \
                            and brick.block_type == 0 and not self.mush:
                        brick.bouncing = True
                        self.sound.play_sound(1)

                brick_collide = pg.sprite.spritecollide(self, self.secret_bricks, False)
                for brick in brick_collide:
                    if self.rect.right >= brick.rect.left and brick.rect.bottom == self.rect.bottom:
                        self.x_change = 0
                    if self.rect.left <= brick.rect.right and brick.rect.bottom == self.rect.bottom:
                        self.x_change = 0

                brick_collide = pg.sprite.spritecollide(self, self.secret_bricks, False)
                for brick in brick_collide:
                    if self.y_change > 0:
                        self.rect.bottom = brick.rect.top
                    elif self.y_change < 0:
                        self.rect.top = brick.rect.bottom
                    self.y_change = 0

    def check_collision(self, screen, stats, display):
        upgrade_collide = pg.sprite.spritecollide(self, self.upgrades, True)
        for upgrade in upgrade_collide:
            if upgrade.up_type == 0:
                self.mush = True
                self.sound.play_sound(11)
                display.give_score(screen, stats, upgrade.rect.x, upgrade.rect.y, 1000)
            if upgrade.up_type == 1 and self.mush:
                self.fired = True
                self.sound.play_sound(11)
                display.give_score(screen, stats, upgrade.rect.x, upgrade.rect.y, 1000)
            if upgrade.up_type == 2:
                self.stats.lives += 1
                self.sound.play_sound(5)
                display.give_score(screen, stats, upgrade.rect.x, upgrade.rect.y, 1000)
            if upgrade.up_type == 3:
                self.star_pow = True
                self.sound.stop_bg()
                self.sound.play_sound(2)
                display.give_score(screen, stats, upgrade.rect.x, upgrade.rect.y, 1000)
            if upgrade.up_type == 4:
                self.stats.coins += 1
                self.stats.score += 200

        enemy_collide = pg.sprite.spritecollide(self, self.enemies, False)
        for enemy in enemy_collide:
            if self.star_pow:
                self.enemies.remove(enemy)
            if enemy.enemy_type == 0 and not self.star_pow and not self.invinc:
                if enemy.rect.y > self.rect.y and not self.mush:
                    self.enemies.remove(enemy)
                    self.sound.play_sound(8)
                    display.give_score(screen, stats, enemy.rect.x, enemy.rect.y, 100)
                if enemy.rect.y > self.rect.y + 3 and self.mush:
                    self.enemies.remove(enemy)
                    self.sound.play_sound(8)
                    display.give_score(screen, stats, enemy.rect.x, enemy.rect.y, 100)
            # Koopa into shell
            if enemy.enemy_type == 1 and not self.star_pow and not self.invinc:
                if enemy.rect.y > self.rect.y and not self.mush:
                    enemy.stunned = True
                    self.sound.play_sound(8)
                    display.give_score(screen, stats, enemy.rect.x, enemy.rect.y, 100)
                if enemy.rect.y > self.rect.y + 3 and self.mush:
                    enemy.stunned = True
                    self.sound.play_sound(8)
                    display.give_score(screen, stats, enemy.rect.x, enemy.rect.y, 100)
            if enemy.enemy_type == 1 and enemy.stunned:
                enemy.kicked = True
                self.sound.play_sound(8)
                display.give_score(screen, stats, enemy.rect.x, enemy.rect.y, 100)
            elif enemy.enemy_type == 0 and enemy.rect.y - 5 <= self.rect.y and not \
                    self.star_pow and not self.invinc:
                if not self.mush and not self.fired:
                    self.sound.stop_bg()
                    self.sound.play_sound(4)
                    self.dead = True
                    self.timer = 0
                if self.mush or self.fired:
                    self.mush = False
                    self.fired = False
                    self.invinc = True
            elif enemy.enemy_type == 1 and enemy.rect.y - 5 <= self.rect.y and not \
                    self.star_pow and not self.invinc:
                if not self.mush and not self.fired:
                    self.sound.stop_bg()
                    self.sound.play_sound(4)
                    self.dead = True
                    self.timer = 0
                if self.mush or self.fired:
                    self.mush = False
                    self.invinc = True

    def invincible(self):

        if self.invinc_length < 100 and self.invinc:
            self.invinc_length += 1
        else:
            self.invinc = False
            self.invinc_length = 0

    def falling(self):
        if self.y_change == 0:
            self.y_change = 1
        else:
            self.y_change += .1

    def move_left(self):
        if self.rect.left <= 20:
            self.x_change = 0
        else:
            self.x_change = -1
        self.moving_left = True
        self.facing_right = False

    def move_right(self):
        self.x_change = 1
        self.moving_right = True
        self.facing_right = True

    def move_stop(self):
        self.x_change = 0
        self.moving_left = False
        self.moving_right = False

    def move_jump(self):
        self.y_change = -6
        self.jump = True

    def draw(self):
        if self.stats.reached_pole and self.timer <= 100:
            self.timer += 5
            self.screen.blit(self.small_mario[13], self.rect)
        else:
            if not self.mush:
                self.screen.blit(self.image, self.rect)
            elif self.mush:
                big_rect = pg.Rect(self.rect.x, self.rect.y-20, self.rect.width, self.rect.height)
                self.screen.blit(self.image, big_rect)

    def die_animate(self, stats, level, sound):
        self.image = self.small_mario[12]
        if self.timer <= 100:
            self.rect.y -= 2
        elif self.timer <= 200:
            self.rect.y += 2
        else:
            if stats.lives > 1:
                self.dead = False
                self.reset_mario(level, sound)
                stats.lives -= 1
            else:
                stats.game_over = True
                if self.timer >= 400:
                    stats.game_over = False
                    stats.reset_stats()

        self.timer += 1

    def reset_mario(self, level, sound):
        self.enemies.empty()
        self.bricks.empty()
        level.camera(-level.shift_world)
        lvl_map = Map(self.screen, self.settings, self.bricks, self.pipes, self,
                      self.enemies, self.ground, self.upgrades, self.stats, self.secret_bricks)
        lvl_map.build_brick()
        self.rect.x = 100
        self.rect.y = 100
        sound.play_bg()
