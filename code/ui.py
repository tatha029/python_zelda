import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 35, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # weapon data to list
        self.weapon_graphics = []
        for weapon_i in weapon_data.values():
            path = weapon_i['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        # magic data to list
        self.magic_graphics = []
        for magic_i in magic_data.values():
            path = magic_i['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)
    
    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg bar
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # convert stats to pixels
        ratio = current / max_amount
        cur_width = bg_rect.width * ratio
        cur_rect = bg_rect.copy()
        cur_rect.width = cur_width
        # draw bar
        pygame.draw.rect(self.display_surface, color, cur_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect
    
    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)
    
    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 635, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player, game_over=False):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon) # weapon
        self.magic_overlay(player.magic_index, not player.can_switch_magic) # magic
        
        # Help indicator (only show if not game over)
        if not game_over:
            help_text = self.font.render("Press H for Help", False, TEXT_COLOR)
            help_rect = help_text.get_rect(topleft=(10, HEIGHT - 30))
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, help_rect.inflate(10, 5))
            self.display_surface.blit(help_text, help_rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, help_rect.inflate(10, 5), 2)