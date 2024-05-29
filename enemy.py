import pygame
import game_globals as GAME
from laser import Laser

class Enemy(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/baddietank.png")
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Initial speed and spawn time settings
        self.base_speed = 1
        self.base_spawn_time = 1500  # milliseconds
        self.direction = pygame.Vector2(0, 1)  # Moving downwards initially
        self.speed = self.base_speed
        self.spawn_time = self.base_spawn_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.direction.y * self.speed

        screen_rect = pygame.Rect((0, 0), GAME.SCREEN.get_size())
        if GAME.is_sprite_outside_rectangle(self, screen_rect, align=True):
            self.direction.y = 0  # Stop moving if outside the screen

        if self.rect.y >= 550:
            self.kill()
            GAME.STATE = 'Game Over'

    def increase_difficulty(self, level):
        # Adjust enemy speed and spawn time based on level
        self.speed = self.base_speed + 0.1 * level
        self.spawn_time = max(self.base_spawn_time - 200 * level, 500)  # Minimum spawn time of 500ms

