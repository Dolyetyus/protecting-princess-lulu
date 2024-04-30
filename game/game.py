import pygame
import sys
import os
import random
import math
import webbrowser

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

pygame.init()
pygame.mixer.init()

map = pygame.image.load("img/map.png")
menu = pygame.image.load("img/mainmenu.png")
gameover_img = pygame.image.load("img/gameover.jpg")
instructions = pygame.image.load("img/instructions.png")
settingsbg = pygame.image.load("img/settings.jpg")
creditsbg = pygame.image.load("img/credits.png")
storybg = pygame.image.load("img/storybg.png")
pause = pygame.image.load("img/pause.png")
menu_cursor = pygame.image.load("img/menucursor.png")
ingame_cursor = pygame.image.load("img/ingamecursor.png")

enemy_image_right = pygame.image.load("img/enemyright.png")
enemy_image_left = pygame.image.load("img/enemyleft.png")

knight_right = pygame.image.load("img/knightright.png")
knight_left = pygame.image.load("img/knightleft.png")
knight_up = pygame.image.load("img/knightup.png")
knight_down = pygame.image.load("img/knightdown.png")
knight_damage_right = pygame.image.load("img/knightdamageright.png")
knight_damage_left = pygame.image.load("img/knightdamageleft.png")
knight_damage_up = pygame.image.load("img/knightdamageup.png")
knight_damage_down = pygame.image.load("img/knightdamagedown.png")
knight_attack_right = pygame.image.load("img/knightattackright.png")
knight_attack_left = pygame.image.load("img/knightattackleft.png")
knight_attack_up = pygame.image.load("img/knightattackup.png")
knight_attack_down = pygame.image.load("img/knightattackdown.png")
knight_shoot_right = pygame.image.load("img/knightshootright.png")
knight_shoot_left = pygame.image.load("img/knightshootleft.png")

princess_right = pygame.image.load("img/luluright.png")
princess_left = pygame.image.load("img/lululeft.png")
princess_damage_right = pygame.image.load("img/luludamageright.png")
princess_damage_left = pygame.image.load("img/luludamageleft.png")
princess_shoot_right = pygame.image.load("img/lulushootright.png")
princess_shoot_left = pygame.image.load("img/lulushootleft.png")
player_boost_img = pygame.image.load("img/playerboost.png")
princess_boost_img = pygame.image.load("img/princessboost.png")
arrow_stack_img = pygame.image.load("img/arrowstack.png")
bow_boost_img = pygame.image.load("img/bowboost.png")
speed_boost_img = pygame.image.load("img/speedboost.png")

main_menu_sound = pygame.mixer.Sound("audio/mainmenu.mp3")
story_sound = pygame.mixer.Sound("audio/story.mp3")
story_sound.set_volume(2)
gameover_sound = pygame.mixer.Sound("audio/gameover.mp3")
gameover_sound.set_volume(0.7)
ingame_sound = pygame.mixer.Sound("audio/ingame.mp3")
ingame_sound.set_volume(0.7)

button_sound = pygame.mixer.Sound("audio/button.wav")
button_sound.set_volume(0.7)
musdeath_sound = pygame.mixer.Sound("audio/musdeath.wav")
mushurt1 = pygame.mixer.Sound("audio/mushurt1.wav")
mushurt2 = pygame.mixer.Sound("audio/mushurt2.wav")
mushurt3 = pygame.mixer.Sound("audio/mushurt3.wav")
mushurt4 = pygame.mixer.Sound("audio/mushurt4.wav")
attack1 = pygame.mixer.Sound("audio/attack1.wav")
attack2 = pygame.mixer.Sound("audio/attack2.wav")
attack3 = pygame.mixer.Sound("audio/attack3.wav")
attack4 = pygame.mixer.Sound("audio/attack4.wav")
luluhurt1 = pygame.mixer.Sound("audio/luluhurt1.wav")
luluhurt2 = pygame.mixer.Sound("audio/luluhurt2.wav")
killing1 = pygame.mixer.Sound("audio/killing1.wav")
killing2 = pygame.mixer.Sound("audio/killing2.wav")
arrow_shoot = pygame.mixer.Sound("audio/arrowshoot.wav")
arrow_kill1 = pygame.mixer.Sound("audio/arrowkill1.wav")
arrow_kill2 = pygame.mixer.Sound("audio/arrowkill2.wav")
arrow_kill3 = pygame.mixer.Sound("audio/arrowkill3.wav")
bow_short = pygame.mixer.Sound("audio/bowaudioshort.wav")
bow_long = pygame.mixer.Sound("audio/bowaudio.wav")
enemy_die1 = pygame.mixer.Sound("audio/enemydie1.wav")
enemy_die2 = pygame.mixer.Sound("audio/enemydie2.wav")
enemy_die3 = pygame.mixer.Sound("audio/enemydie3.wav")
enemy_die4 = pygame.mixer.Sound("audio/enemydie4.wav")
enemy_die5 = pygame.mixer.Sound("audio/enemydie5.wav")
enemy_die6 = pygame.mixer.Sound("audio/enemydie6.wav")

enemy_die_sounds = [enemy_die1, enemy_die2, enemy_die3, enemy_die4, enemy_die5, enemy_die6]
for sound in enemy_die_sounds:
    sound.set_volume(0.5)

def set_difficulty(difficulty):
    global player_speed_multiplier, player_health, princess_health, princess_arrows, enemy_speed, enemy_spawn, arrow_speed, boost_multiplier
    
    difficulties = {
        0: (1.1, 12, 6, 15, 0.9, 0.9, 1.2, 1.2),
        1: (1, 10, 5, 10, 1, 1, 1, 1),
        2: (1, 8, 4, 5, 1.1, 1.1, 1, 1)
    }
    
    settings = difficulties.get(difficulty, difficulties[1])
    player_speed_multiplier, player_health, princess_health, princess_arrows, enemy_speed, enemy_spawn, arrow_speed, boost_multiplier = settings

with open("misc/savegame.txt", "r") as file:
    file_lines = file.readlines()
    high_score = int(file_lines[0])
    friendly_fire = int(file_lines[1])
    display_story = int(file_lines[2])
    story_displayed = False
    difficulty = int(file_lines[3])
    set_difficulty(difficulty)

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed_multiplier = 1
        self.player_speed = 1.5 * self.speed_multiplier * player_speed_multiplier
        self.current_shape = 'right'
        self.aim_direction = ''
        self.character_img = knight_right
        self.player_x = (screen_width // 2) - 50
        self.player_y = screen_height // 2
        self.init_time = pygame.time.get_ticks()

        self.attack = False
        self.attack_duration = 300
        self.attack_start_time = 0
        self.attack_cooldown = 1200
        self.last_attack_time = 0

        self.collision_cooldown = 2000
        self.last_collision_time = 0
        self.health = player_health

        self.score = 0
        self.arrow_list = []
        self.arrow_cooldown = 4100
        self.last_arrow_time = 0
        self.freeze_duration = 900
        self.freeze_start_time = 0
        self.is_frozen = False
        self.arrow_fire = False
        self.bow_shoot = True
        self.bow_audio = bow_long

        self.shoot_boosted = False
        self.shoot_boost_start_time = 0
        self.speed_boosted = False
        self.speed_boost_start_time = 0
        self.boost_duration = 13000 * boost_multiplier
        self.time = 0

    def update(self, keys, mouse_pos, mouse_click):
        current_time = pygame.time.get_ticks()

        if self.is_frozen:
            if current_time - self.freeze_start_time > self.freeze_duration:
                self.arrow_fire = True
                self.is_frozen = False
                self.bow_shoot = True
            else:
                if (self.bow_shoot): 
                    pygame.mixer.Channel(6).play(self.bow_audio)
                    self.bow_shoot = False

                if self.aim_direction == 'left':
                    self.character_img = knight_shoot_left
                if self.aim_direction == 'right':
                    self.character_img = knight_shoot_right

            return (self.player_x - 34 // 2, self.player_y - 34 // 2, 34, 34), self.character_img

        if self.arrow_fire:
            self.last_arrow_time = current_time
            target_x, target_y = mouse_pos
            arrow = Arrow(self.player_x, self.player_y, target_x, target_y, 'player')
            self.arrow_list.append(arrow)
            pygame.mixer.Channel(4).play(arrow_shoot)
            self.arrow_fire = False

        if mouse_click[0] == 1 and current_time - self.last_arrow_time > self.arrow_cooldown and not current_time - self.init_time < 4000:
            self.is_frozen = True
            self.freeze_start_time = current_time
            target_x, target_y = mouse_pos

            if target_x > self.player_x:
                self.aim_direction = 'right'
            else:
                self.aim_direction = 'left'

        if self.shoot_boosted and current_time - self.shoot_boost_start_time > self.boost_duration:
            self.shoot_boosted = False
            self.arrow_cooldown = 4100
            self.freeze_duration = 900
            self.bow_audio = bow_long

        if self.speed_boosted and current_time - self.speed_boost_start_time > self.boost_duration:
            self.speed_boosted = False
            self.speed_multiplier = 1

        if (keys[pygame.K_w] and keys[pygame.K_a]) or \
           (keys[pygame.K_w] and keys[pygame.K_d]) or \
           (keys[pygame.K_s] and keys[pygame.K_a]) or \
           (keys[pygame.K_s] and keys[pygame.K_d]):
            self.player_speed = 1.06 * self.speed_multiplier * player_speed_multiplier
        else:
            self.player_speed = 1.5 * self.speed_multiplier * player_speed_multiplier

        if keys[pygame.K_w] and self.player_y - self.player_speed > 17:         # 17 because player rectangle size is 34px
            self.current_shape = 'up'
            self.player_y -= self.player_speed
            self.character_img = knight_up
        if keys[pygame.K_s] and self.player_y + self.player_speed < self.screen_height-17:
            self.current_shape = 'down'
            self.player_y += self.player_speed
            self.character_img = knight_down
        if keys[pygame.K_a] and self.player_x - self.player_speed > 17:
            self.current_shape = 'left'
            self.player_x -= self.player_speed
            self.character_img = knight_left
        if keys[pygame.K_d] and self.player_x + self.player_speed < self.screen_width-17:
            self.current_shape = 'right'
            self.player_x += self.player_speed
            self.character_img = knight_right
        if keys[pygame.K_SPACE] and current_time - self.last_attack_time > self.attack_cooldown:
            self.attack = True
            random_attack = random.choice([attack1, attack2, attack3, attack4])
            pygame.mixer.Channel(2).play(random_attack)
            self.attack_start_time = current_time
            self.last_attack_time = current_time

        if self.attack:
            if current_time - self.attack_start_time < self.attack_duration:
                if self.current_shape == 'left':
                    self.character_img = knight_attack_left
                if self.current_shape == 'right':
                    self.character_img = knight_attack_right
                if self.current_shape == 'up':
                    self.character_img = knight_attack_up
                if self.current_shape == 'down':
                    self.character_img = knight_attack_down
            else:
                self.attack = False
                if self.current_shape == 'left':
                    self.character_img = knight_left
                if self.current_shape == 'right':
                    self.character_img = knight_right
                if self.current_shape == 'up':
                    self.character_img = knight_up
                if self.current_shape == 'down':
                    self.character_img = knight_down

        elif current_time - self.last_collision_time <= 250:
            if self.current_shape == 'left':
                self.character_img = knight_damage_left
            if self.current_shape == 'right':
                self.character_img = knight_damage_right
            if self.current_shape == 'up':
                self.character_img = knight_damage_up
            if self.current_shape == 'down':
                self.character_img = knight_damage_down
        else:
            if self.current_shape == 'left':
                self.character_img = knight_left
            if self.current_shape == 'right':
                self.character_img = knight_right
            if self.current_shape == 'up':
                self.character_img = knight_up
            if self.current_shape == 'down':
                self.character_img = knight_down

        if self.character_img == knight_attack_left:
            return (self.player_x - 68 // 2, self.player_y - 34 // 2, 34, 34), self.character_img
        elif self.character_img == knight_attack_up:
            return (self.player_x - 34 // 2, self.player_y - 56 // 2, 34, 34), self.character_img
        else:
            return (self.player_x - 34 // 2, self.player_y - 34 // 2, 34, 34), self.character_img
    
    def get_health(self):
        return self.health
    
    def update_arrows(self, enemy_list, player, princess):
        for arrow in self.arrow_list:
            arrow.update()
            arrow.handle_collision(enemy_list, player, princess)

        self.arrow_list = [arrow for arrow in self.arrow_list if arrow.on_screen(self.screen_width, self.screen_height)]

    def draw_arrows(self, screen):
        for arrow in self.arrow_list:
            arrow.draw(screen)
    
    def handle_collision(self, enemy, current_time):
        if current_time - self.last_collision_time > self.collision_cooldown:
            for enemy_pos in enemy.enemy_list:
                dist = ((self.player_x - enemy_pos[0]) ** 2 + (self.player_y - enemy_pos[1]) ** 2) ** 0.5
                if dist <= 16:
                    if self.health > 0:
                        self.health -= 1
                        self.last_collision_time = current_time

                        random_mushurt = random.choice([mushurt1, mushurt2, mushurt3, mushurt4])
                        if not self.health <= 0:
                            pygame.mixer.Channel(1).play(random_mushurt)

                        dx = self.player_x - enemy_pos[0]
                        dy = self.player_y - enemy_pos[1]
                        dist = (dx ** 2 + dy ** 2) ** 0.5
                        if dist != 0:
                            dx /= dist
                            dy /= dist
                        self.player_x += dx * self.player_speed
                        self.player_y += dy * self.player_speed

            dist_to_princess = ((self.player_x - princess.princess_x) ** 2 + (self.player_y - princess.princess_y) ** 2) ** 0.5
            if dist_to_princess <= 24:
                dx = self.player_x - princess.princess_x
                dy = self.player_y - princess.princess_y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist != 0:
                    dx /= dist
                    dy /= dist
                self.player_x += dx * self.player_speed
                self.player_y += dy * self.player_speed

    def attack_collision(self, enemy, princess):
        random_killing = random.choice([killing1, killing2])
        enemy_kill_effects = random.choice(enemy_die_sounds)

        for enemy_pos in enemy.enemy_list[:]:
            dist = ((self.player_x - enemy_pos[0]) ** 2 + (self.player_y - enemy_pos[1]) ** 2) ** 0.5
            if dist <= 32 and self.attack:
                relative_pos = (enemy_pos[0] - self.player_x, enemy_pos[1] - self.player_y)

                valid_directions = {
                    'right': relative_pos[0] > 0,
                    'left': relative_pos[0] < 0,
                    'up': relative_pos[1] < 0,
                    'down': relative_pos[1] > 0
                }

                for direction, condition in valid_directions.items():
                    if self.current_shape == direction and condition:
                        text_pos = enemy_pos
                        pygame.mixer.Channel(2).play(random_killing)
                        pygame.mixer.Channel(7).play(enemy_kill_effects)
                        enemy.enemy_list.remove(enemy_pos)
                        self.score += 1
                        princess.arrow_loot(text_pos[0], text_pos[1])
                        break

    def shoot_boost_player(self):
        current_time = pygame.time.get_ticks()
        self.time = current_time

        if current_time - self.shoot_boost_start_time > self.boost_duration:
            self.shoot_boosted = True
            self.shoot_boost_start_time = current_time
            self.arrow_cooldown = 1600
            self.freeze_duration = 350
            self.bow_audio = bow_short

    def speed_boost_player(self):
        current_time = pygame.time.get_ticks()
        self.time = current_time

        if current_time - self.speed_boost_start_time > self.boost_duration:
            self.speed_boosted = True
            self.speed_boost_start_time = current_time
            self.speed_multiplier *= 1.4

    def remaining_boost_time(self):
        current_time = pygame.time.get_ticks()
        if self.shoot_boosted:
            time_remaining = self.boost_duration - (current_time - self.shoot_boost_start_time)
            return time_remaining
        if self.speed_boosted:
            time_remaining = self.boost_duration - (current_time - self.speed_boost_start_time)
            return time_remaining
        return 0

    def get_score(self):
        return self.score

class Princess:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.shapes = ['left', 'right']
        self.current_shape = 'left'
        self.last_position_change = pygame.time.get_ticks()

        self.princess_x = screen_width // 2
        self.princess_y = screen_height // 2
        self.triangle_color = (255, 192, 203)

        self.health = princess_health
        self.collision_cooldown = 2000
        self.last_collision_time = 0

        self.arrow_list = []
        self.start_shoot = False
        self.arrow_cooldown = 4250
        self.last_arrow_time = 0
        self.arrow_capacity = princess_arrows
        self.used_arrows = 0
        self.bow_used = True

    def update_position(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_position_change > 2500:
            self.current_shape = random.choice(self.shapes)
            self.last_position_change = current_time

    def draw_princess(self, screen):
        current_time = pygame.time.get_ticks()
        princess_rect = pygame.Rect(self.princess_x - 34 // 2, self.princess_y - 34 // 2, 34, 34)

        if current_time - self.last_collision_time <= 250:
            if self.current_shape == 'left':
                screen.blit(princess_damage_left, princess_rect.topleft)
            else:
                screen.blit(princess_damage_right, princess_rect.topleft)
        else:
            if (3350 < current_time - self.last_arrow_time < 4250) and (self.used_arrows < self.arrow_capacity) and (self.start_shoot):
                if self.bow_used:
                    pygame.mixer.Channel(6).play(bow_long)
                    self.bow_used = False

                if self.current_shape == 'left':
                    screen.blit(princess_shoot_left, princess_rect.topleft)
                else:
                    screen.blit(princess_shoot_right, princess_rect.topleft)
            else:
                self.bow_used = True
                if self.current_shape == 'left':
                    screen.blit(princess_left, princess_rect.topleft)
                else:
                    screen.blit(princess_right, princess_rect.topleft)

    def get_health(self):
        return self.health
    
    def get_capacity(self):
        return self.arrow_capacity - self.used_arrows

    def handle_collision(self, enemy, current_time):
        if current_time - self.last_collision_time > self.collision_cooldown:
            for enemy_pos in enemy.enemy_list:
                dist = ((self.princess_x - enemy_pos[0]) ** 2 + (self.princess_y - enemy_pos[1]) ** 2) ** 0.5
                if dist <= 22:
                    if self.health > 0:
                        self.health -= 1
                        self.last_collision_time = current_time
                        pygame.mixer.Channel(3).play(luluhurt1)

    def shoot_arrow(self, enemy_list):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_arrow_time > self.arrow_cooldown and self.used_arrows < self.arrow_capacity:
            self.last_arrow_time = current_time
            if enemy_list:
                target_enemy = random.choice(enemy_list)
                target_x, target_y, _ = target_enemy
                target_x += random.randint(-25, 25)
                target_y += random.randint(-25, 25)
                arrow = Arrow(self.princess_x, self.princess_y, target_x, target_y, 'princess')
                self.arrow_list.append(arrow)
                pygame.mixer.Channel(4).play(arrow_shoot)
                self.used_arrows += 1

    def update_arrows(self, enemy_list, player):
        for arrow in self.arrow_list:
            arrow.update()
            arrow.handle_collision(enemy_list, player, self)

        self.arrow_list = [arrow for arrow in self.arrow_list if arrow.on_screen(self.screen_width, self.screen_height)]
    
    def arrow_loot(self, text_position_x, text_position_y):
        if random.random() < 0.125:
            self.arrow_capacity += 1
            curr_time = pygame.time.get_ticks()
            print_power_up('loot', pygame.Rect(text_position_x, text_position_y, 24, 24), False, curr_time)
            
    def draw_arrows(self, screen):
        for arrow in self.arrow_list:
            arrow.draw(screen)

class Enemy:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_timer = pygame.time.get_ticks()
        self.enemy_list = []
        self.spawn_delay = 4000 * enemy_spawn
        self.speed = 0.25 * enemy_speed
        self.facing_direction = 'right'

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = current_time

            margin = 100
            restricted_rect = pygame.Rect(margin, margin, self.screen_width - 2 * margin, self.screen_height - 2 * margin)

            enemy_rect = None
            while enemy_rect is None or enemy_rect.colliderect(restricted_rect):
                enemy_x = random.randint(0, self.screen_width - 24)
                enemy_y = random.randint(0, self.screen_height - 24)
                enemy_rect = pygame.Rect(enemy_x - 12, enemy_y - 12, 24, 24)

            self.enemy_list.append((enemy_x, enemy_y, 'right'))

    def draw_enemies(self, screen):
        for enemy_pos in self.enemy_list:
            enemy_x, enemy_y, facing_direction = enemy_pos
            enemy_rect = pygame.Rect(enemy_x - 12, enemy_y - 12, 24, 24)

            if facing_direction == 'left':
                screen.blit(enemy_image_left, enemy_rect.topleft)
            else:
                screen.blit(enemy_image_right, enemy_rect.topleft)

    def move_towards_player_or_lulu(self, player, center_x, center_y, princess):
        for idx, enemy_pos in enumerate(self.enemy_list):
            enemy_x, enemy_y, _ = enemy_pos
            player_x, player_y = player.player_x, player.player_y

            dist_to_player = ((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2) ** 0.5
            dist_to_center = ((center_x - enemy_x) ** 2 + (center_y - enemy_y) ** 2) ** 0.5

            if dist_to_player <= dist_to_center:
                dx = player_x - enemy_x
                dy = player_y - enemy_y
            else:
                dx = center_x - enemy_x
                dy = center_y - enemy_y

            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                dx /= dist
                dy /= dist

            facing_direction = 'right' if dx >= 0 else 'left'
            new_position = (enemy_x + dx * self.speed, enemy_y + dy * self.speed, facing_direction)

            dist_to_princess = ((enemy_x - princess.princess_x) ** 2 + (enemy_y - princess.princess_y) ** 2) ** 0.5
            if dist_to_princess <= 18:
                dx = enemy_x - princess.princess_x
                dy = enemy_y - princess.princess_y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist != 0:
                    dx /= dist
                    dy /= dist
                new_position = (enemy_x + dx * self.speed, enemy_y + dy * self.speed, facing_direction)

            for other_idx, other_pos in enumerate(self.enemy_list):
                if idx != other_idx:
                    other_x, other_y, _ = other_pos
                    dist_to_other = ((new_position[0] - other_x) ** 2 + (new_position[1] - other_y) ** 2) ** 0.5
                    if dist_to_other <= 15:
                        dx = new_position[0] - other_x
                        dy = new_position[1] - other_y
                        dist = (dx ** 2 + dy ** 2) ** 0.5
                        if dist != 0:
                            dx /= dist
                            dy /= dist
                        new_position = (new_position[0] + dx * self.speed, new_position[1] + dy * self.speed, facing_direction)

            dist_to_player = ((enemy_x - player.player_x) ** 2 + (enemy_y - player.player_y) ** 2) ** 0.5
            if dist_to_player <= 15: 
                dx = enemy_x - player.player_x
                dy = enemy_y - player.player_y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist != 0:
                    dx /= dist
                    dy /= dist
                new_position = (enemy_x + dx * self.speed, enemy_y + dy * self.speed, facing_direction)

            self.enemy_list[idx] = new_position

class HealthBar:
    def __init__(self, max_health, width, height):
        self.max_health = max_health
        self.width = width
        self.height = height
        self.current_health = max_health

    def update_health(self, new_health):
        self.current_health = new_health

    def draw(self, screen, x, y):
        remaining_health_width = int((self.current_health / self.max_health) * self.width)
        remaining_color = (0, 255, 0)
        
        remaining_health_rect = pygame.Rect(x, y, remaining_health_width, self.height)
        pygame.draw.rect(screen, remaining_color, remaining_health_rect)

        health_bar_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), health_bar_rect, 1)

class Arrow:
    def __init__(self, start_x, start_y, target_x, target_y, shooter):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 4.5 * arrow_speed
        self.hit_enemy = False
        self.source = shooter
        self.rect = pygame.Rect(start_x, start_y, 1, 1)

    def update(self):
        if not self.hit_enemy:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                dx /= dist
                dy /= dist
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.rect.center = (self.x, self.y)

            if dist <= self.speed:
                self.hit_enemy = True

    def handle_collision(self, enemy_list, player, princess):
        for enemy_pos in enemy_list[:]:
            dist = ((self.x - enemy_pos[0]) ** 2 + (self.y - enemy_pos[1]) ** 2) ** 0.5
            if dist <= 12:
                text_pos = enemy_pos
                enemy_list.remove(enemy_pos)
                random_kill = random.choice([arrow_kill1, arrow_kill2, arrow_kill3])
                enemy_kill_effects = random.choice(enemy_die_sounds)
                pygame.mixer.Channel(5).play(random_kill)
                pygame.mixer.Channel(7).play(enemy_kill_effects)
                self.hit_enemy = True
                player.score += 1
                princess.arrow_loot(text_pos[0], text_pos[1])

        if friendly_fire:
            princess_hitbox = pygame.Rect(princess.princess_x - 34 // 2, princess.princess_y - 34 // 2, 34, 34)
            player_hitbox = pygame.Rect(player.player_x - 34 // 2, player.player_y - 34 // 2, 34, 34)

            if self.rect.colliderect(princess_hitbox) and princess.health > 0 and self.source != 'princess':
                self.hit_enemy = True
                princess.health -= 1
                princess.last_collision_time = pygame.time.get_ticks()
                pygame.mixer.Channel(3).play(luluhurt1)

            if self.rect.colliderect(player_hitbox) and player.health > 0 and self.source != 'player':
                self.hit_enemy = True
                player.health -= 1
                player.last_collision_time = pygame.time.get_ticks()
                random_mushurt = random.choice([mushurt1, mushurt2, mushurt3, mushurt4])
                if not player.health <= 0:
                    pygame.mixer.Channel(1).play(random_mushurt)

    def on_screen(self, screen_width, screen_height):
        return not self.hit_enemy and 0 <= self.x <= screen_width and 0 <= self.y <= screen_height

    def draw(self, screen):
        if not self.hit_enemy:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                dx /= dist
                dy /= dist

            arrow_length = 15
            arrowhead_size = 5

            arrowhead1 = (self.x + arrowhead_size * math.cos(math.atan2(dy, dx) + math.pi / 6),
                          self.y + arrowhead_size * math.sin(math.atan2(dy, dx) + math.pi / 6))
            arrowhead2 = (self.x + arrowhead_size * math.cos(math.atan2(dy, dx) - math.pi / 6),
                          self.y + arrowhead_size * math.sin(math.atan2(dy, dx) - math.pi / 6))
            base_point = (self.x + arrow_length * dx, self.y + arrow_length * dy)

            pygame.draw.line(screen, (205, 133, 63), (self.x, self.y), base_point, 2)
            pygame.draw.polygon(screen, (169, 169, 169), [arrowhead1, arrowhead2, base_point])

class PowerUp:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.power_up_list = []
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = random.randint(20000, 25000)

    def spawn_power_up(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = current_time

            margin = 210
            power_up_type = random.choice(['extra_arrow', 'player_boost', 'princess_boost', 'faster_shoot', 'speed_boost'])
            restricted_rect = pygame.Rect(margin, margin // 2, self.screen_width - 2 * margin, self.screen_height - margin)

            power_up_rect = None
            while power_up_rect is None or power_up_rect.colliderect(restricted_rect):
                power_up_x = random.randint(0, self.screen_width - 24)
                power_up_y = random.randint(0, self.screen_height - 24)
                power_up_rect = pygame.Rect(power_up_x, power_up_y, 24, 24)

            spawn_time = pygame.time.get_ticks()
            self.power_up_list.append((power_up_type, power_up_rect, spawn_time))

    def draw_power_ups(self, screen):
        for power_up_type, power_up_rect, _ in self.power_up_list:
            if power_up_type == 'extra_arrow':
                screen.blit(arrow_stack_img, power_up_rect.topleft)
            elif power_up_type == 'player_boost':
                screen.blit(player_boost_img, power_up_rect.topleft)
            elif power_up_type == 'princess_boost':
                screen.blit(princess_boost_img, power_up_rect.topleft)
            elif power_up_type == 'faster_shoot':
                screen.blit(bow_boost_img, power_up_rect.topleft)
            elif power_up_type == 'speed_boost':
                screen.blit(speed_boost_img, power_up_rect.topleft)

    def check_collision(self, player, player_rect, princess):
        for power_up_type, power_up_rect, spawn_time in self.power_up_list:
            if power_up_rect.colliderect(player_rect):
                self.apply_power_up(player, princess, power_up_type, power_up_rect)
                self.power_up_list.remove((power_up_type, power_up_rect, spawn_time))
            elif current_time - spawn_time > 10000:
                self.power_up_list.remove((power_up_type, power_up_rect, spawn_time))

    def apply_power_up(self, player, princess, power_up_type, power_up_rect):
        curr_time = pygame.time.get_ticks()
        applied = False

        if power_up_type == 'extra_arrow':
            princess.arrow_capacity += 5
            applied = True
        elif power_up_type == 'player_boost':
            if player.get_health() < player_health:
                player.health += 1
                applied = True
        elif power_up_type == 'princess_boost':
            if princess.get_health() < princess_health:
                princess.health += 1
                applied = True
        elif power_up_type == 'faster_shoot':
            player.shoot_boost_player()
            applied = True
        elif power_up_type == 'speed_boost':
            player.speed_boost_player()
            applied = True

        print_power_up(power_up_type, power_up_rect, applied, curr_time)

def print_power_up(power_up_type, power_up_rect, isapplied, activation_time):
    font = pygame.font.SysFont('papyrus', 14, bold=True)

    lines = []
    boost_type = ''

    if power_up_type == 'extra_arrow':
        lines.append("Arrows looted!")
    elif power_up_type == 'player_boost':
        if isapplied:
            lines.append("Player health boosted!")
        else:
            lines.extend(["Your health", "is already full!"])
    elif power_up_type == 'princess_boost':
        if isapplied:
            lines.append("Princess health boosted!")
        else:
            lines.extend(["Princess health", "is already full!"])
    elif power_up_type == 'faster_shoot':
        boost_type = 'shoot'
        lines.extend(["Player archery", "speed boosted!"])
    elif power_up_type == 'speed_boost':
        boost_type = 'speed'
        lines.extend(["Player movement", "speed boosted!"])
    elif power_up_type == 'loot':
        lines.append("Arrow looted!")

    text_surfaces = [font.render(line, True, (0, 255, 0)) for line in lines]

    total_height = sum(surface.get_height() for surface in text_surfaces)
    y_position = power_up_rect.centery - total_height // 2

    for surface in text_surfaces:
        text_rect = surface.get_rect(center=(power_up_rect.centerx, y_position))
        power_up_display_list.append((surface, text_rect, activation_time + 2000, boost_type))
        y_position += surface.get_height()

menu_font = pygame.font.Font("misc/menufont.ttf", 54)
health_font = pygame.font.Font("misc/menufont.ttf", 30)
capacity_font = pygame.font.Font("misc/menufont.ttf", 25)
score_font = pygame.font.Font("misc/menufont.ttf", 24)
high_score_font = pygame.font.Font("misc/menufont.ttf", 20)
boost_font = pygame.font.Font("misc/menufont.ttf", 28)

WIDTH, HEIGHT = 1200, 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Protect Princess Lulu')

clock = pygame.time.Clock()
running = True
progress_reset = False
stop_clicking = False
ingame = False

def display_menu(mouse_pos):
    text_color = (189, 152, 5)
    hover_color = (160, 160, 160)
    border_color = (0, 0, 0)

    start_text = menu_font.render('Start', True, text_color)
    ins_text = menu_font.render('Instructions', True, text_color)
    settings_text = menu_font.render('Settings', True, text_color)
    credits_text = menu_font.render('Credits', True, text_color)
    exit_text = menu_font.render('Exit', True, text_color)
    supp_text = menu_font.render('Support us?', True, text_color)

    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    ins_rect = ins_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25))
    settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    credits_rect = credits_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 175))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
    supp_rect = supp_text.get_rect(center=(WIDTH - 175, HEIGHT // 2 + 300))

    if start_rect.collidepoint(mouse_pos):
        start_text = menu_font.render('Start', True, hover_color)
    if ins_rect.collidepoint(mouse_pos):
        ins_text = menu_font.render('Instructions', True, hover_color)
    if settings_rect.collidepoint(mouse_pos):
        settings_text = menu_font.render('Settings', True, hover_color)
    if credits_rect.collidepoint(mouse_pos):
        credits_text = menu_font.render('Credits', True, hover_color)
    if exit_rect.collidepoint(mouse_pos):
        exit_text = menu_font.render('Exit', True, hover_color)
    if supp_rect.collidepoint(mouse_pos):
        supp_text = menu_font.render('Support us?', True, hover_color)

    start_text_border = menu_font.render('Start', True, border_color)
    ins_text_border = menu_font.render('Instructions', True, border_color)
    settings_text_border = menu_font.render('Settings', True, border_color)
    credits_text_border = menu_font.render('Credits', True, border_color)
    exit_text_border = menu_font.render('Exit', True, border_color)
    supp_text_border = menu_font.render('Support us?', True, border_color)

    text_with_shadow(start_text, start_text_border, start_rect)
    text_with_shadow(ins_text, ins_text_border, ins_rect)
    text_with_shadow(settings_text, settings_text_border, settings_rect)
    text_with_shadow(credits_text, credits_text_border, credits_rect)
    text_with_shadow(exit_text, exit_text_border, exit_rect)
    text_with_shadow(supp_text, supp_text_border, supp_rect)
    screen.blit(menu_cursor, cursor_menu_rect)

def check_menu_click(pos):
    start_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 70, 100, 45)
    ins_rect = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 5, 230, 45)
    settings_rect = pygame.Rect(WIDTH // 2 - 65, HEIGHT // 2 + 80, 140, 45)
    credits_rect = pygame.Rect(WIDTH // 2 - 55, HEIGHT // 2 + 155, 120, 45)
    exit_rect = pygame.Rect(WIDTH // 2 - 40, HEIGHT // 2 + 230, 80, 40)
    supp_rect = pygame.Rect(WIDTH - 285 , HEIGHT // 2 + 280, 222, 45)

    if start_rect.collidepoint(pos):
        button_sound.play()
        return "Start"
    elif ins_rect.collidepoint(pos):
        button_sound.play()
        return "Instructions"
    elif settings_rect.collidepoint(pos):
        button_sound.play()
        return "Settings"
    elif credits_rect.collidepoint(pos):
        button_sound.play()
        return "Credits"
    elif exit_rect.collidepoint(pos):
        button_sound.play()
        return "Exit"
    elif supp_rect.collidepoint(pos):
        button_sound.play()
        return "Support"
    else:
        return None
    
def display_instructions(screen, mouse_pos, background):
    screen.blit(background, (0, 0))
    text_color = (189, 152, 5)
    hover_color = (160, 160, 160)
    border_color = (0, 0, 0)

    back_text = menu_font.render('Back to Menu', True, text_color)
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 85))

    if back_rect.collidepoint(mouse_pos):
        back_text = menu_font.render('Back to Menu', True, hover_color)

    back_text_border = menu_font.render('Back to Menu', True, border_color)
    text_with_shadow(back_text, back_text_border, back_rect)
    
    screen.blit(menu_cursor, cursor_menu_rect)

def check_instructions_click(pos):
    back_rect = pygame.Rect(WIDTH // 2 - 115, HEIGHT - 105, 240, 40)
    if back_rect.collidepoint(pos):
        button_sound.play()
        return "Back"
    else:
        return None

def display_settings(screen, mouse_pos, background):
    screen.blit(background, (0, 0))
    text_color = (189, 152, 5)
    hover_color = (160, 160, 160)
    border_color = (0, 0, 0)
    green = (15, 153, 24)
    orange = (204, 135, 31)
    red = (212, 38, 38)
    whiteish = (235, 208, 155)

    difficulty_texts = {
        0: ('Easy', green),
        1: ('Normal', orange),
        2: ('Hard', red)
    }

    difficulty_level, difficulty_color = difficulty_texts.get(difficulty, ('Hard', red))

    ff_status = 'On' if friendly_fire else 'Off'
    ff_color = green if friendly_fire else red

    difficulty_text = menu_font.render('Difficulty:', True, text_color)
    diff_level_text = menu_font.render(difficulty_level, True, difficulty_color)
    friendly_fire_text = menu_font.render('Friendly Fire:', True, text_color)
    ff_text = menu_font.render(ff_status, True, ff_color)
    reset_text = menu_font.render('Reset Progress', True, text_color)
    is_reset_text = capacity_font.render('Progress has been reset!', True, whiteish if stop_clicking else red)
    reset_info_text1 = high_score_font.render('(For now, resetting progress only resets', True, text_color)
    reset_info_text2 = high_score_font.render('the highscore since there is no story yet)', True, text_color)
    back_text = menu_font.render('Back to Menu', True, text_color)

    difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2 - 55, HEIGHT // 2 - 120))
    friendly_fire_rect = friendly_fire_text.get_rect(center=(WIDTH // 2 - 20, HEIGHT // 2 - 45))
    ff_rect = ff_text.get_rect(center=(WIDTH // 2 + 136 if friendly_fire else WIDTH // 2 + 140, HEIGHT // 2 - 45))
    reset_rect = reset_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    is_reset_rect = is_reset_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
    reset_info_rect1 = reset_info_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70 if not progress_reset else HEIGHT // 2 + 110))
    reset_info_rect2 = reset_info_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 85 if not progress_reset else HEIGHT // 2 + 125))
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 85))
    diff_level_rect = diff_level_text.get_rect(center=(WIDTH // 2 + 103 if difficulty != 1 else WIDTH // 2 + 111, HEIGHT // 2 - 120))
    screen.blit(diff_level_text, diff_level_rect)

    screen.blit(ff_text, ff_rect)
    screen.blit(reset_info_text1, reset_info_rect1)
    screen.blit(reset_info_text2, reset_info_rect2)

    if progress_reset:
        screen.blit(is_reset_text, is_reset_rect)

    if difficulty_rect.collidepoint(mouse_pos):
        difficulty_text = menu_font.render('Difficulty:', True, hover_color)
    if friendly_fire_rect.collidepoint(mouse_pos):
        friendly_fire_text = menu_font.render('Friendly Fire:', True, hover_color)
    if reset_rect.collidepoint(mouse_pos):
        reset_text = menu_font.render('Reset Progress', True, hover_color)
    if back_rect.collidepoint(mouse_pos):
        back_text = menu_font.render('Back to Menu', True, hover_color)

    difficulty_text_border = menu_font.render('Difficulty:', True, border_color)
    friendly_fire_text_border = menu_font.render('Friendly Fire: ', True, border_color)
    reset_text_border = menu_font.render('Reset Progress', True, border_color)
    back_text_border = menu_font.render('Back to Menu', True, border_color)

    text_with_shadow(difficulty_text, difficulty_text_border, difficulty_rect)
    text_with_shadow(friendly_fire_text, friendly_fire_text_border, friendly_fire_rect)
    text_with_shadow(reset_text, reset_text_border, reset_rect)
    text_with_shadow(back_text, back_text_border, back_rect)

    screen.blit(menu_cursor, cursor_menu_rect)

def check_settings_click(pos):
    difficulty_rect = pygame.Rect(WIDTH // 2 - 135, HEIGHT // 2 - 135, 165, 40)
    friendly_fire_rect = pygame.Rect(WIDTH // 2 - 135, HEIGHT // 2 - 60, 240, 40)
    reset_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 15, 275, 40)
    back_rect = pygame.Rect(WIDTH // 2 - 115, HEIGHT - 105, 240, 45)
    if difficulty_rect.collidepoint(pos):
        button_sound.play()
        return "Difficulty"
    if friendly_fire_rect.collidepoint(pos):
        button_sound.play()
        return "Friendly Fire"
    if reset_rect.collidepoint(pos):
        button_sound.play()
        return "Reset"
    if back_rect.collidepoint(pos):
        button_sound.play()
        return "Back"
    else:
        return None
    
def text_with_shadow(text, text_border, rect):
    offset = 1
    screen.blit(text_border, (rect.x - offset, rect.y))
    screen.blit(text_border, (rect.x + offset, rect.y))
    screen.blit(text_border, (rect.x, rect.y - offset))
    screen.blit(text_border, (rect.x, rect.y + offset))
    screen.blit(text, rect)

def print_death_message(message, size, y_offset):
    death_font = pygame.font.Font("misc/menufont.ttf", size)
    death_text = death_font.render(message, True, (255, 255, 255))
    death_rect = death_text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) - 170 + y_offset))
    screen.blit(death_text, death_rect)

def start_game():
    global player, player_health_bar, enemy, princess, princess_health_bar, power_up, new_high, current_score, arrow_capacity, power_up_display_list
    
    main_menu_sound.set_volume(1)
    main_menu_sound.stop()
    story_sound.stop()
    gameover_sound.stop()
    pygame.mouse.set_visible(False)

    player = Player(WIDTH, HEIGHT)
    player_health_bar = HealthBar(player.get_health(), 40, 5)
    enemy = Enemy(WIDTH, HEIGHT)
    princess = Princess(WIDTH, HEIGHT)
    princess_health_bar = HealthBar(princess.get_health(), 40, 5)
    power_up = PowerUp(WIDTH, HEIGHT)
    ingame_sound.play(-1)
    current_score = 0
    new_high = False
    arrow_capacity = 50
    power_up_display_list = []

def init_game():
    global menu_displayed, game_started, game_over, mus_died, lulu_died, instructions_displayed, settings_displayed, credits_displayed, print_speed, print_shoot, is_paused

    menu_displayed = True
    instructions_displayed = False
    settings_displayed = False
    credits_displayed = False
    game_started = False
    game_over = False
    print_shoot = False
    print_speed = False
    is_paused = False
    mus_died = False
    lulu_died = False

def adjust_difficulty(score, enemy):
    if score >= 4 and score < 8:
        enemy.spawn_delay = 3000 * enemy_spawn
    elif score >= 8 and score < 14:
        enemy.speed = 0.40 * enemy_speed
    elif score >= 14 and score < 30:
        enemy.spawn_delay = 2500 * enemy_spawn
    elif score >= 30 and score < 50:
        enemy.speed = 0.5 * enemy_speed
    elif score >= 50 and score < 70:
        enemy.spawn_delay = 2000 * enemy_spawn
    elif score >= 70 and score < 90:
        enemy.speed = 0.65 * enemy_speed
    elif score >= 90 and score < 120:
        enemy.spawn_delay = 1500 * enemy_spawn
    elif score >= 120 and score < 150:
        enemy.speed = 0.8 * enemy_speed
    elif score >= 150 and score < 180:
        enemy.speed = 1 * enemy_speed
    elif score >= 180:
        enemy.speed = 1.2 * enemy_speed

init_game()

if menu_displayed or instructions_displayed:
    main_menu_sound.play(-1)

while running:
    current_time = pygame.time.get_ticks()
    screen.blit(menu, (0,0))

    mouse_pos = pygame.mouse.get_pos()
    cursor_ing_rect = ingame_cursor.get_rect()
    cursor_ing_rect.center = pygame.mouse.get_pos()
    cursor_menu_rect = menu_cursor.get_rect()
    cursor_menu_rect.center = pygame.mouse.get_pos()

    if menu_displayed:
        ingame = False
        pygame.mouse.set_visible(False)
        display_menu(mouse_pos)
    elif instructions_displayed:
        pygame.mouse.set_visible(False)
        display_instructions(screen, mouse_pos, instructions)
    elif settings_displayed:
        pygame.mouse.set_visible(False)
        display_settings(screen, mouse_pos, settingsbg)
    elif credits_displayed:
        pygame.mouse.set_visible(False)
        display_instructions(screen, mouse_pos, creditsbg)
    elif story_displayed:
        ingame = False
        pygame.mouse.set_visible(False)
        screen.blit(storybg, (0, 0))
    elif not game_over:
        ingame = True
        screen.blit(map, (0, 0))
        keys = pygame.key.get_pressed()

        mouse_click = pygame.mouse.get_pressed()

        player_rectangle, knight_img = player.update(keys, mouse_pos, mouse_click)
        screen.blit(knight_img, player_rectangle)

        princess.update_position()
        princess.draw_princess(screen)
        princess.handle_collision(enemy, current_time)
        princess_health_bar.update_health(princess.get_health())
        princess_health_bar.draw(screen, (princess.princess_x - princess_health_bar.width // 2), princess.princess_y - 25)

        for power_up_text, power_up_rect, end_time, boost in power_up_display_list[:]:
            if boost == 'shoot':
                print_shoot = True
            elif boost == 'speed':
                print_speed = True

            if current_time < end_time:
                screen.blit(power_up_text, power_up_rect)
            else:
                power_up_display_list.remove((power_up_text, power_up_rect, end_time, boost))

        if print_shoot or print_speed:
            time_remaining = player.remaining_boost_time()
            seconds_remaining = time_remaining / 1000 
            formatted_seconds = "{:.1f}".format(seconds_remaining)

            if print_shoot:
                countdown_text = boost_font.render(f"Archery speed boost for: {formatted_seconds}s", True, (255, 255, 255))
            if print_speed:
                countdown_text = boost_font.render(f"Movement speed boost for: {formatted_seconds}s", True, (255, 255, 255))
            countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, 40))
            screen.blit(countdown_text, countdown_rect)

            if time_remaining < 0.5:
                print_speed = False
                print_shoot = False

        if (player.get_health() <= player_health//2) or (princess.get_health() <= princess_health//2):
            if not princess_fire:
                princess.last_arrow_time = pygame.time.get_ticks()-2500
                princess_fire = True
            princess.start_shoot = True
            princess.shoot_arrow(enemy.enemy_list)
            princess.update_arrows(enemy.enemy_list, player)
            princess.draw_arrows(screen)
        else:
            princess_fire = False

        if (current_time - player.init_time > 10000):
            power_up.spawn_power_up()
            power_up.draw_power_ups(screen)
            power_up.check_collision(player, player_rectangle, princess)

        capacity_text = capacity_font.render(f'Princess Arrows: {princess.get_capacity()}', True, (124,252,0))
        if (princess.get_capacity() == 0): 
            capacity_text = capacity_font.render(f'Princess Arrows: {princess.get_capacity()}', True, (255, 0, 0))
            princess_fire = False
        capacity_rect = capacity_text.get_rect()
        capacity_rect.topright = (WIDTH - 20, 42)
        screen.blit(capacity_text, capacity_rect)

        player.attack_collision(enemy, princess)
        player.handle_collision(enemy, current_time)
        player_health_bar.update_health(player.get_health())
        player_health_bar.draw(screen, (player.player_x - player_health_bar.width // 2), player.player_y - 27)
        player.update_arrows(enemy.enemy_list, player, princess)
        player.draw_arrows(screen)

        enemy.spawn_enemy()
        enemy.move_towards_player_or_lulu(player, WIDTH // 2, HEIGHT // 2, princess)
        enemy.draw_enemies(screen)

        screen.blit(ingame_cursor, cursor_ing_rect)

        current_score = player.get_score()
        adjust_difficulty(current_score, enemy)

        health_text = health_font.render(f'Player Health: {player.get_health()}', True, (219, 157, 11))
        health_rect = health_text.get_rect()
        health_rect.topright = (WIDTH - 20, 15)
        screen.blit(health_text, health_rect)

        score_text = score_font.render(f'Score: {current_score}', True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topright = (WIDTH - 20, 68)
        screen.blit(score_text, score_rect)

        high_score_text = high_score_font.render(f'High Score: {high_score}', True, (235, 208, 155))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.topright = (WIDTH - 20, 92)
        screen.blit(high_score_text, high_score_rect)

        if is_paused:
            screen.blit(pause, (WIDTH//2 - 198, HEIGHT//2 - 200))

        if player.get_health() <= 0:
            mus_died = True
            game_over = True
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(musdeath_sound))
        if princess.get_health() <= 0:
            lulu_died = True
            game_over = True
            pygame.mixer.Channel(3).play(luluhurt2)

    if game_over:
        ingame = False
        pygame.mouse.set_visible(False)
        screen.blit(gameover_img, (0, 0))
        gameover_menu_font = pygame.font.Font("misc/menufont.ttf", 40)

        ingame_sound.stop()
        gameover_sound.play(-1)
        is_paused = False

        game_over_font = pygame.font.Font("misc/menufont.ttf", 68)
        game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) - 210))

        offset = 1
        game_over_text_border = gameover_menu_font.render('Game Over', True, (0, 0, 0))
        text_with_shadow(game_over_text, game_over_text_border, game_over_rect)
        
        printed = False
        if mus_died and not printed:
            print_death_message('You Died', 30, offset)
            printed = True

        if lulu_died and not printed:
            print_death_message('Princess Lulu Died', 30, offset)
            printed = True

        if current_score > high_score:
            high_score = current_score
            new_high = True
            file_lines[0] = str(high_score) + "\n"
            with open("misc/savegame.txt", "w") as file:
                file.writelines(file_lines)

        if new_high:
            high_score_text = score_font.render(f'New highscore: {high_score}!', True, (30, 250, 48))
            high_score_rect = high_score_text.get_rect()
            high_score_rect.center = (WIDTH // 2, (HEIGHT // 2) - 140)
        else:
            score_game_over_text = score_font.render(f'Score: {player.get_score()}', True, (255, 255, 255))
            score_game_over_rect = score_game_over_text.get_rect()
            score_game_over_rect.center = (WIDTH // 2, (HEIGHT // 2) - 140)
            screen.blit(score_game_over_text, score_game_over_rect)

            high_score_text = high_score_font.render(f'High Score: {high_score}', True, (230, 202, 147))
            high_score_rect = high_score_text.get_rect()
            high_score_rect.center = (WIDTH // 2, (HEIGHT // 2) - 113)

        screen.blit(high_score_text, high_score_rect)

        play_again_text = gameover_menu_font.render('Play Again', True, (189, 152, 5))
        play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) - 10))

        back_to_menu_text = gameover_menu_font.render('Back to Menu', True, (189, 152, 5))
        back_to_menu_rect = back_to_menu_text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 55))

        if play_again_rect.collidepoint(mouse_pos):
            play_again_text = gameover_menu_font.render('Play Again', True, (160, 160, 160))
        if back_to_menu_rect.collidepoint(mouse_pos):
            back_to_menu_text = gameover_menu_font.render('Back to Menu', True, (160, 160, 160))

        play_again_text_border = gameover_menu_font.render('Play Again', True, (0, 0, 0))
        back_to_menu_text_border = gameover_menu_font.render('Back to Menu', True, (0, 0, 0))
        highscore_text_border = high_score_font.render(f'High Score: {high_score}', True, (0, 0, 0))

        text_with_shadow(play_again_text, play_again_text_border, play_again_rect)
        text_with_shadow(back_to_menu_text, back_to_menu_text_border, back_to_menu_rect)
        text_with_shadow(high_score_text, highscore_text_border, high_score_rect)

        screen.blit(menu_cursor, cursor_menu_rect)

        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] == 1:
            if play_again_rect.collidepoint(mouse_pos):
                button_sound.play()
                start_game()
                game_over = False
            elif back_to_menu_rect.collidepoint(mouse_pos):
                menu_displayed = True
                game_over = False
                gameover_sound.stop()
                button_sound.play()
                main_menu_sound.play(-1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_displayed:
                clicked = check_menu_click(mouse_pos)
                if clicked == "Start":
                    if display_story:
                        story_displayed = True
                        main_menu_sound.set_volume(0.25)
                        story_sound.play()
                        menu_displayed = False
                    else:
                        start_game()
                        menu_displayed = False
                        game_started = True
                elif clicked == "Exit":
                    running = False
                elif clicked == "Instructions":
                    menu_displayed = False
                    instructions_displayed = True
                elif clicked == "Settings":
                    menu_displayed = False
                    settings_displayed = True
                elif clicked == "Credits":
                    menu_displayed = False
                    credits_displayed = True
                elif clicked == "Support":
                    webbrowser.open("https://www.buymeacoffee.com/musabdoli")

            elif instructions_displayed:
                clicked = check_instructions_click(mouse_pos)
                if clicked == "Back":
                    instructions_displayed = False
                    menu_displayed = True

            elif settings_displayed:
                clicked = check_settings_click(mouse_pos)
                if clicked == "Difficulty":
                    difficulty += 1
                    if difficulty > 2:
                        difficulty = 0
                if clicked == "Friendly Fire":
                    friendly_fire = not friendly_fire
                    file_lines[1] = str(int(friendly_fire)) + "\n"
                    with open("misc/savegame.txt", "w") as file:
                        file.writelines(file_lines)
                if clicked == "Reset":
                    progress_reset = True
                    stop_clicking = not stop_clicking
                    high_score = 0
                    display_story = 1
                    file_lines[0] = str(high_score) + "\n"
                    file_lines[2] = str(1) + "\n"
                    with open("misc/savegame.txt", "w") as file:
                        file.writelines(file_lines)
                if clicked == "Back":
                    progress_reset = False
                    stop_clicking = False
                    set_difficulty(difficulty)
                    file_lines[3] = str(difficulty)
                    with open("misc/savegame.txt", "w") as file:
                        file.writelines(file_lines)
                    settings_displayed = False
                    menu_displayed = True

            elif credits_displayed:
                clicked = check_instructions_click(mouse_pos)
                if clicked == "Back":
                    credits_displayed = False
                    menu_displayed = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and ingame:
                is_paused = not is_paused
            elif event.key == pygame.K_y and is_paused:
                menu_displayed = True
                game_over = False
                ingame_sound.stop()
                main_menu_sound.play(-1)
                is_paused = False
            if event.key == pygame.K_RETURN and story_displayed:
                display_story = 0
                story_displayed = False
                file_lines[2] = str(display_story) + "\n"
                with open("misc/savegame.txt", "w") as file:
                        file.writelines(file_lines)
                        
                start_game()
                menu_displayed = False
                game_started = True

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()