import pygame
from support import import_folder
from settings import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # hitbox should allow overlap
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

        #graphics setup
        self.import_player_assets()
        self.status = 'down'
        
        self.obstacle_sprites = obstacle_sprites

        # attack
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health':100, 'energy':60, 'attack':10, 'magic':4, 'speed':5}
        self.max_stats = {'health':300, 'energy':140, 'attack':20, 'magic':10, 'speed':10}
        self.upgrade_cost = {'health':100, 'energy':100, 'attack':100, 'magic':100, 'speed':100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        # invincibility frames
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_durations = 500

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
                           'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
                           'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):
        if not self.attacking:
            # movement inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.status = 'up'
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.status = 'down'
                self.direction.y = 1
            else:
                self.direction.y =  0
            
            if keys[pygame.K_RIGHT]:
                
                self.status = 'right'
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.status = 'left'
                self.direction.x = -1
            else:
                self.direction.x = 0
            
            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % len(list(weapon_data.keys()))
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength, cost = magic_data[style]['strength'] + self.stats['magic'], magic_data[style]['cost']
                self.create_magic(style, strength, cost)
            
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self.magic_index = (self.magic_index + 1) % len(list(magic_data.keys()))
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        if self.attacking:
            # we dont want attacking and moving
            self.direction.x, self.direction.y = 0, 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    # overwrite idle
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):
        cur_time = pygame.time.get_ticks()
        if self.attacking:
            tot_cooldown = self.attack_cooldown + weapon_data[self.weapon]['cooldown']
            if cur_time - self.attack_time >= tot_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if cur_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        
        if not self.can_switch_magic:
            if cur_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        
        if not self.vulnerable:
            if cur_time - self.hurt_time >= self.invulnerability_durations:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        # set the image
        self.image = animation[int(self.frame_index) % len(animation)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker when hit
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        magic_damage = magic_data[self.magic]['strength']
        return base_damage + magic_damage

    def energy_recovery(self):
        if self.energy <= self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def is_dead(self):
        return self.health <= 0

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.walk(self.stats['speed'])
        self.energy_recovery()