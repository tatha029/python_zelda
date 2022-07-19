import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        y_offset = HITBOX_OFFSET[sprite_type]
        if sprite_type == 'object':
            # object is larger than 64x64 size so offset is needed
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        # we want the hitbox to be little smaller than the image
        self.hitbox = self.rect.inflate(0,y_offset)