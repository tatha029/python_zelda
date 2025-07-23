import pygame
from support import *
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from particles import AnimationPlayer
from enemy import Enemy
from magic import MagicPlayer
from upgrade import Upgrade
from help import Help
from game_over import GameOver

from random import choice, randint

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.help_active = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.help = Help()
        self.game_over = GameOver()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player= MagicPlayer(self.animation_player)
    
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('map/map_FloorBlocks.csv'),
            'grass' : import_csv_layout('map/map_Grass.csv'),
            'object' : import_csv_layout('map/map_LargeObjects.csv'),
            'entities' : import_csv_layout('map/map_Entities.csv')
        }

        graphics = {
            'grass' : import_folder('graphics/grass'), 
            'objects' : import_folder('graphics/objects')
        }
        for style, layout in layouts.items():
            for row_idx, row in enumerate(layout):
                for col_idx, col in enumerate(row):
                    if col != '-1':
                        x, y = col_idx * TILESIZE, row_idx * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            # create grass tile
                            img = choice(graphics['grass'])
                            Tile((x,y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                img)
                        if style == 'object':
                            # create object tile
                            img = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', img)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x,y), 
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                elif col == '393': monster_name = 'squid'
                                Enemy(monster_name,
                                      (x,y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_exp)

        #         if col == 'x':
        #             Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
        #         elif col == 'p':
        #             self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
    
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
    
    def create_magic(self, style, strength, cost):
        # print(style, cost, strength)
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                # add more leaf breaking particles
                                self.animation_player.create_grass_particles(pos-offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
            
            # Check if player is dead
            if self.player.is_dead():
                self.game_over.trigger_game_over()

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def toggle_help(self):
        self.help_active = not self.help_active

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player, self.game_over.game_over)
        
        # Check if player is dead (in case health goes below 0 from other sources)
        if self.player.is_dead() and not self.game_over.game_over:
            self.game_over.trigger_game_over()
        
        if self.game_over.game_over:
            # display game over screen
            self.game_over.display()
        elif self.help_active:
            # display help menu
            self.help.display()
        elif self.game_paused:
            # display upgrade menu
            self.upgrade.display()
        else:
            # display game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

class YSortCameraGroup(pygame.sprite.Group):
    # name is such that the sprite having higher y pos elements is on top
    def __init__(self):
        super().__init__()

        # we want our player to be within the centre of screen
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # the camera variable that'll control the display rect
        self.offset = pygame.math.Vector2()

        # creating background (floors)
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
    
    def custom_draw(self, player):
        # getting the camera offset depending on current player position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
        # we want the sprites having higher y rendered later
        # this is to have the player and enemies appear ahead or before the rocks and trees
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)