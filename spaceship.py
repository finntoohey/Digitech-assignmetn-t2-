import pygame
import game_globals as GAME
import time
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        super().__init__()  # call the init function in pygame.sprite
        self.image = pygame.image.load("images/ptank.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.35), int(self.image.get_height() * 0.35)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.last_shoot_time = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return
    
    def update(self, pressed, mouse_pos, mouse_buttons):

        if pressed[pygame.K_a] == 1:
            self.rect.x = self.rect.x - 6
        if pressed[pygame.K_d] == 1:
            self.rect.x = self.rect.x + 6
       # if pressed[pygame.K_w] == 1:
      #      self.rect.y = self.rect.y - 4
       # if pressed[pygame.K_s] == 1:
       #     self.rect.y = self.rect.y + 4

        if pressed[pygame.K_SPACE] == 1:
            if time.time() - self.last_shoot_time > 0.35:
                direction = pygame.Vector2(0, -1)  # Laser direction upwards
                laser = Laser(self.rect.centerx, self.rect.centery - 30, direction)
                self.last_shoot_time = time.time()
