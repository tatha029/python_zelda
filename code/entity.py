import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
    
    def walk(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # self.rect.center += speed * self.direction
        self.hitbox.x += speed * self.direction.x
        self.collisions('hori')
        self.hitbox.y += speed * self.direction.y
        self.collisions('vert')
        
        # image rect should move with the hitbox
        self.rect.center = self.hitbox.center
    
    def collisions(self, direction):
        if direction == 'hori':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'vert':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0