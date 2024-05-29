import pygame

# Global game objects and variables
SCREEN = None
BULLET_GROUP = None
ENEMY_GROUP = None
MID_ENEMY_GROUP = None
BIG_ENEMY_GROUP = None
BOSS_ENEMY_GROUP = None
PLAYER = None
EXIT = False
STATE = "Ready"
MUSIC = None
SCORE = 0
STARTTIME = 0
ENDTIME = 0
ENEMY = None

def is_sprite_outside_rectangle(sprite, rectangle, wrap=False, align=False):
    if sprite.rect.top < rectangle.top:
        if align:
            sprite.rect.top = rectangle.top
        elif wrap:
            sprite.rect.bottom = rectangle.bottom
        sprite.position = pygame.Vector2(sprite.rect.center)
        return True
    elif sprite.rect.bottom > rectangle.bottom:
        if align:
            sprite.rect.bottom = rectangle.bottom
        elif wrap:
            sprite.rect.top = rectangle.top
        sprite.position = pygame.Vector2(sprite.rect.center)
        return True
    elif sprite.rect.left < rectangle.left:
        if align:
            sprite.rect.left = rectangle.left
        elif wrap:
            sprite.rect.right = rectangle.right
            sprite.angle = -sprite.angle
        sprite.position = pygame.Vector2(sprite.rect.center)
        return True
    elif sprite.rect.right > rectangle.right:
        if align:
            sprite.rect.right = rectangle.right
        elif wrap:
            sprite.rect.left = rectangle.left
            sprite.angle = -sprite.angle
        sprite.position = pygame.Vector2(sprite.rect.center)
        return True
    else:
        return False
