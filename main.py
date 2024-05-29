''' Main Game Code '''
import pygame
import random
import pygame.locals as CONSTANTS
import os, sys, random, time, math
import game_globals as GAME
from spaceship import Spaceship
from enemy import Enemy
from midenemy import MidEnemy
from bigenemy import BigEnemy
from bossenemy import BossEnemy

'''----------------------- Initialisation --------------------------'''
pygame.init()
pygame.mixer.init()
pygame.font.init()

# window
pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Asteroids') 

# Initialize the background
screen_rect = pygame.display.get_surface().get_rect()
BACKGROUND_IMAGE = pygame.image.load("images/1.webp")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, screen_rect.size)

# Global game objects and variables
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont('Impact', 60)
FONT2 = pygame.font.SysFont('Ariel', 30)

GAME.SCREEN = pygame.display.get_surface()
GAME.EXIT = False
GAME.STATE = "Start Game"
GAME.PLAYER = None
GAME.ENEMY_GROUP = pygame.sprite.Group()
GAME.MID_ENEMY_GROUP = pygame.sprite.Group()
GAME.BIG_ENEMY_GROUP = pygame.sprite.Group()
GAME.BOSS_ENEMY_GROUP = pygame.sprite.Group()
GAME.BULLET_GROUP = pygame.sprite.Group()
create_enemy_event = pygame.USEREVENT + 1
create_mid_enemy_event = pygame.USEREVENT + 2
create_big_enemy_event = pygame.USEREVENT + 3

# Define levels and their respective scores
LEVEL_SCORES = {1: 10, 2: 15, 3: 20, 4: 25, 5: 30}
current_level = 1

'''-------------------------- Game Loop --------------------------'''
while not GAME.EXIT:

    CLOCK.tick(60)

    for event in pygame.event.get():
        t = random.randint(0, 1000)
        if event.type == CONSTANTS.QUIT:
            GAME.EXIT = True
        elif event.type == create_enemy_event:
            if current_level != 4:
                e = Enemy(t, 100)
                GAME.ENEMY_GROUP.add(e)
                pygame.time.set_timer(create_enemy_event, e.spawn_time)
        elif event.type == create_mid_enemy_event and current_level in [2, 3]:
            e = MidEnemy(t, 100)
            GAME.MID_ENEMY_GROUP.add(e)
            pygame.time.set_timer(create_mid_enemy_event, e.spawn_time)
        elif event.type == create_big_enemy_event and current_level == 4:
            e = BigEnemy(t, 100)
            GAME.BIG_ENEMY_GROUP.add(e)
            pygame.time.set_timer(create_big_enemy_event, e.spawn_time)

    pressed = pygame.key.get_pressed()
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    mouse_buttons = pygame.mouse.get_pressed()

    GAME.SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

    if GAME.STATE == "Start Game" or GAME.STATE == "Start Game Level " + str(current_level):
        GAME.SCORE = 0
        text = FONT.render("Press SPACE to Start Level " + str(current_level), True, (255, 0, 0))
        GAME.SCREEN.blit(text, (280, 320))

        x = mouse_pos.x
        y = mouse_pos.y
        position_text = "X: " + str(x) + " Y: " + str(y)
        text = FONT2.render(position_text, True, (255, 255, 255))
        GAME.SCREEN.blit(text, (10, 10))

        if pressed[pygame.K_SPACE] == 1:
            GAME.STATE = "Running"
            GAME.MUSIC = pygame.mixer.Sound("sounds/sunsetreverie.mp3")
            GAME.MUSIC.play(-1)
            GAME.PLAYER = Spaceship(512, 500)
            if current_level == 2 or current_level == 3:
                pygame.time.set_timer(create_mid_enemy_event, 2000)
            elif current_level == 4:
                pygame.time.set_timer(create_big_enemy_event, 2000)
            else:
                pygame.time.set_timer(create_enemy_event, 2000)

    elif GAME.STATE == "Running":
        text = FONT2.render("Score: " + str(GAME.SCORE), True, (255, 0, 0))
        GAME.SCREEN.blit(text, (10, 10))

        for enemy in GAME.ENEMY_GROUP:
            enemy.increase_difficulty(current_level)
        for enemy in GAME.MID_ENEMY_GROUP:
            enemy.increase_difficulty(current_level)
        for enemy in GAME.BIG_ENEMY_GROUP:
            enemy.increase_difficulty(current_level)
        for enemy in GAME.BOSS_ENEMY_GROUP:
            enemy.increase_difficulty(current_level)

        GAME.PLAYER.update(pressed, mouse_pos, mouse_buttons)
        GAME.ENEMY_GROUP.update()
        GAME.MID_ENEMY_GROUP.update()
        GAME.BIG_ENEMY_GROUP.update()
        GAME.BOSS_ENEMY_GROUP.update()
        GAME.BULLET_GROUP.update()

        if pygame.sprite.groupcollide(GAME.ENEMY_GROUP, GAME.BULLET_GROUP, True, True):
            GAME.SCORE += 1
        if pygame.sprite.groupcollide(GAME.MID_ENEMY_GROUP, GAME.BULLET_GROUP, True, True):
            GAME.SCORE += 2
        if pygame.sprite.groupcollide(GAME.BIG_ENEMY_GROUP, GAME.BULLET_GROUP, True, True):
            GAME.SCORE += 3

        if pygame.sprite.spritecollide(GAME.PLAYER, GAME.ENEMY_GROUP, True):
            GAME.STATE = "Game Over"
        if pygame.sprite.spritecollide(GAME.PLAYER, GAME.MID_ENEMY_GROUP, True):
            GAME.STATE = "Game Over"
        if pygame.sprite.spritecollide(GAME.PLAYER, GAME.BIG_ENEMY_GROUP, True):
            GAME.STATE = "Game Over"
        if pygame.sprite.spritecollide(GAME.PLAYER, GAME.BOSS_ENEMY_GROUP, True):
            GAME.STATE = "Game Over"

        GAME.PLAYER.draw(GAME.SCREEN)
        GAME.ENEMY_GROUP.draw(GAME.SCREEN)
        GAME.MID_ENEMY_GROUP.draw(GAME.SCREEN)
        GAME.BIG_ENEMY_GROUP.draw(GAME.SCREEN)
        GAME.BOSS_ENEMY_GROUP.draw(GAME.SCREEN)
        GAME.BULLET_GROUP.draw(GAME.SCREEN)

        if GAME.SCORE >= LEVEL_SCORES[current_level]:
            if current_level == 4 and not GAME.BIG_ENEMY_GROUP:
                current_level += 1
                GAME.STATE = "Start Game Level " + str(current_level)
                GAME.ENEMY_GROUP.empty()
                GAME.MID_ENEMY_GROUP.empty()
                GAME.BIG_ENEMY_GROUP.empty()
                GAME.BOSS_ENEMY_GROUP.empty()
                GAME.BULLET_GROUP.empty()
                GAME.PLAYER.kill()
                GAME.MUSIC.stop()
            elif current_level == 5:
                if not GAME.BOSS_ENEMY_GROUP:
                    GAME.STATE = "Start Game Level 5"
                    if len(GAME.BOSS_ENEMY_GROUP) < 3:
                        boss_enemy = BossEnemy(512, 100)
                        GAME.BOSS_ENEMY_GROUP.add(boss_enemy)
            else:
                current_level += 1
                GAME.STATE = "Start Game Level " + str(current_level)
                GAME.ENEMY_GROUP.empty()
                GAME.MID_ENEMY_GROUP.empty()
                GAME.BULLET_GROUP.empty()
                GAME.PLAYER.kill()
                GAME.MUSIC.stop()

    elif GAME.STATE == "Game Over":
        GAME.ENEMY_GROUP.empty()
        GAME.MID_ENEMY_GROUP.empty()
        GAME.BIG_ENEMY_GROUP.empty()
        GAME.BOSS_ENEMY_GROUP.empty()
        GAME.BULLET_GROUP.empty()
        GAME.PLAYER.kill()
        GAME.MUSIC.stop()

        text = FONT.render("Game Over", True, (255, 0, 0))
        GAME.SCREEN.blit(text, (280, 320))

        if pressed[pygame.K_SPACE] == 1:
            GAME.STATE = "Start Game"

    pygame.display.flip()

print("Exiting")
pygame.quit()
sys.exit(0)
