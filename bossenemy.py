import pygame
import game_globals as GAME
#UFJDBSAIGUFB
class BossEnemy(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/baddietank.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = 5
        
        self.base_speed = 1
        self.base_spawn_time = 1500
        self.direction = 1
        self.speed = self.base_speed
        self.spawn_time = self.base_spawn_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.direction * self.speed

        screen_rect = pygame.Rect((0, 0), GAME.SCREEN.get_size())
        if GAME.is_sprite_outside_rectangle(self, screen_rect, align=True):
            self.direction *= 0
            self.rect.y += 0
            self.speed += 0

        if self.rect.y == 550:
            self.kill()
            GAME.STATE = 'Game Over'

    def increase_difficulty(self, level):
        self.speed = self.base_speed + 0.1 * level
        self.spawn_time = max(self.base_spawn_time - 200 * level, 500)
