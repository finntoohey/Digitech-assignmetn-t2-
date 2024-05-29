import pygame
import game_globals as GAME

class Laser(pygame.sprite.Sprite):
 
    def __init__(self, x, y, direction):
        super().__init__()  # call the init function in pygame.sprite
        self.image = pygame.Surface((3, 15))
        self.image = pygame.image.load("images/bullet1.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.15), int(self.image.get_height() * 0.15)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.sound = pygame.mixer.Sound("sounds/laser.mp3")
        self.sound.play(0)

        self.direction = direction.normalize()  # Ensure the direction is normalized
        self.speed = 5

        GAME.BULLET_GROUP.add(self)
  
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if (self.rect.y < 0 or self.rect.y > GAME.SCREEN.get_height() or
                self.rect.x < 0 or self.rect.x > GAME.SCREEN.get_width()):
            self.kill()
