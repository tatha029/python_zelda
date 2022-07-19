from tkinter.tix import TEXT
import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // (self.attribute_nr + 1)
        self.create_items()

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.selection_cooldown = 300
    
    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_LEFT] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)
    
    def selection_cooldowns(self):
        if not self.can_move:
            cur_time = pygame.time.get_ticks()
            if cur_time - self.selection_time >= self.selection_cooldown:
                self.can_move = True
    
    def create_items(self):
        self.item_list = []
        for item in range(self.attribute_nr):
            # horizontal and vertical positions
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2
            top = self.display_surface.get_size()[1] * 0.1
            # create item
            item = Item(left, top, self.width, self.height, item, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldowns()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.stats[name]
            max_value = self.player.max_stats[name]
            cost = self.player.upgrade_cost[name]
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
    
    def display_names(self, surface, name, cost, selected):
        text_color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        title_surf = self.font.render(name, False, text_color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop+pygame.math.Vector2(0,20))

        cost_surf = self.font.render(f'{int(cost)}', False, text_color)
        cost_rect = title_surf.get_rect(midbottom=self.rect.midbottom+pygame.math.Vector2(0,-20))

        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)
    
    def display_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attr = list(player.stats.keys())[self.index]
        # print(upgrade_attr)

        if player.exp >= player.upgrade_cost[upgrade_attr] and player.stats[upgrade_attr] < player.max_stats[upgrade_attr]:
            player.exp -= player.upgrade_cost[upgrade_attr]
            player.stats[upgrade_attr] = min(player.stats[upgrade_attr] * 1.1, player.max_stats[upgrade_attr])
            player.upgrade_cost[upgrade_attr] *= 1.4

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR_ACTIVE, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index==selection_num)
        self.display_bar(surface, value, max_value, self.index==selection_num)