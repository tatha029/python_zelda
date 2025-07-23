import pygame
from settings import *

class Help:
    def __init__(self):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(UI_FONT, 14)
        self.title_font = pygame.font.Font(UI_FONT, 24)
        
        # help sections
        self.sections = ['Controls', 'Story', 'World', 'Combat', 'Magic']
        self.current_section = 0
        
        # selection system
        self.selection_time = None
        self.can_move = True
        self.selection_cooldown = 300
        
        # help content
        self.help_content = {
            'Controls': [
                ('Movement', 'Arrow Keys - Move your character'),
                ('Attack', 'Space - Attack with current weapon'),
                ('Magic', 'Left Ctrl - Cast current magic spell'),
                ('Weapon Switch', 'Q - Switch between weapons'),
                ('Magic Switch', 'E - Switch between magic spells'),
                ('Upgrade Menu', 'M - Open/close upgrade menu'),
                ('Help', 'H - Open/close this help menu'),
                ('', ''),
                ('Weapons Available:', 'Sword, Lance, Axe, Rapier, Sai'),
                ('Magic Available:', 'Flame, Heal')
            ],
            'Story': [
                ('The Legend of Zelda Hack', ''),
                ('', 'You are a brave warrior in the mystical land of Hyrule.'),
                ('', 'Dark forces have corrupted the once peaceful realm,'),
                ('', 'turning innocent creatures into dangerous monsters.'),
                ('', ''),
                ('Your Quest:', ''),
                ('', '- Defeat the corrupted monsters'),
                ('', '- Collect experience to grow stronger'),
                ('', '- Master different weapons and magic'),
                ('', '- Restore peace to the land'),
                ('', ''),
                ('The monsters you face:', ''),
                ('', '- Squid: Quick but weak'),
                ('', '- Spirit: Fast and elusive'),
                ('', '- Bamboo: Stealthy leaf attacker'),
                ('', '- Raccoon: Strong and dangerous')
            ],
            'World': [
                ('The World of Hyrule', ''),
                ('', 'You find yourself in a mysterious forest clearing'),
                ('', 'surrounded by ancient ruins and corrupted nature.'),
                ('', ''),
                ('Environment:', ''),
                ('', '- Grass patches can be destroyed for resources'),
                ('', '- Large objects block your path'),
                ('', '- Invisible boundaries keep you in the area'),
                ('', ''),
                ('Day and Night:', ''),
                ('', 'The world exists in perpetual twilight,'),
                ('', 'with the water reflecting the sky above.'),
                ('', ''),
                ('Survival Tips:', ''),
                ('', '- Watch your health and energy bars'),
                ('', '- Use cover from objects during combat'),
                ('', '- Destroy grass for potential resources'),
                ('', '- Keep moving to avoid being surrounded')
            ],
            'Combat': [
                ('Combat System', ''),
                ('', 'Combat in this world is fast-paced and strategic.'),
                ('', ''),
                ('Weapon Types:', ''),
                ('', '- Sword: Balanced damage and speed'),
                ('', '- Lance: High damage, slow attack'),
                ('', '- Axe: Medium damage, medium speed'),
                ('', '- Rapier: Low damage, very fast'),
                ('', '- Sai: Medium damage, fast attack'),
                ('', ''),
                ('Combat Tips:', ''),
                ('', '- Different enemies have different weaknesses'),
                ('', '- Use hit-and-run tactics against groups'),
                ('', '- Watch enemy attack patterns'),
                ('', '- Use terrain to your advantage'),
                ('', '- Upgrade your stats to become stronger'),
                ('', ''),
                ('Enemy Behavior:', ''),
                ('', '- Enemies will chase you when close'),
                ('', '- They have attack cooldowns like you'),
                ('', '- Some are faster, some are stronger')
            ],
            'Magic': [
                ('Magic System', ''),
                ('', 'Magic requires energy to cast and can be powerful.'),
                ('', ''),
                ('Available Spells:', ''),
                ('', 'Flame:'),
                ('', '  - Creates fire particles in a line'),
                ('', '  - Costs energy but deals magic damage'),
                ('', '  - Effective against most enemies'),
                ('', ''),
                ('Heal:'),
                ('', '  - Restores your health'),
                ('', '  - Costs energy but keeps you alive'),
                ('', '  - Use when health is low'),
                ('', ''),
                ('Magic Tips:', ''),
                ('', '- Energy regenerates over time'),
                ('', '- Magic damage scales with magic stat'),
                ('', '- Use heal strategically in combat'),
                ('', '- Flame is great for crowd control'),
                ('', ''),
                ('Energy Management:', ''),
                ('', '- Don\'t waste energy on weak enemies'),
                ('', '- Keep some energy for healing'),
                ('', '- Upgrade magic stat for more energy')
            ]
        }
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.current_section < len(self.sections) - 1:
                self.current_section += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_LEFT] and self.current_section > 0:
                self.current_section -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
    
    def selection_cooldowns(self):
        if not self.can_move:
            cur_time = pygame.time.get_ticks()
            if cur_time - self.selection_time >= self.selection_cooldown:
                self.can_move = True
    
    def draw_text_wrapped(self, surface, text, font, color, rect, line_spacing=5):
        """Draw text with automatic word wrapping"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, False, color)
            
            if test_surface.get_width() <= rect.width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        y = rect.top
        for line in lines:
            if y + font.get_height() > rect.bottom:
                break
            text_surface = font.render(line, False, color)
            text_rect = text_surface.get_rect(topleft=(rect.left, y))
            surface.blit(text_surface, text_rect)
            y += font.get_height() + line_spacing
    
    def display_section_tabs(self):
        """Display the section tabs at the top"""
        tab_width = WIDTH // len(self.sections)
        tab_height = 40
        
        for i, section in enumerate(self.sections):
            tab_rect = pygame.Rect(i * tab_width, 0, tab_width, tab_height)
            
            # Background
            if i == self.current_section:
                pygame.draw.rect(self.display_surface, UPGRADE_BG_COLOR_SELECTED, tab_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, tab_rect, 3)
            else:
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, tab_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, tab_rect, 2)
            
            # Text
            text_color = TEXT_COLOR_SELECTED if i == self.current_section else TEXT_COLOR
            text_surf = self.font.render(section, False, text_color)
            text_rect = text_surf.get_rect(center=tab_rect.center)
            self.display_surface.blit(text_surf, text_rect)
    
    def display_content(self):
        """Display the content of the current section"""
        content_rect = pygame.Rect(20, 60, WIDTH - 40, HEIGHT - 80)
        
        # Background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, content_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, content_rect, 3)
        
        # Display content
        current_content = self.help_content[self.sections[self.current_section]]
        
        y_offset = 80
        for title, description in current_content:
            if title:  # Title line
                title_surf = self.title_font.render(title, False, UI_BORDER_COLOR_ACTIVE)
                title_rect = title_surf.get_rect(topleft=(40, y_offset))
                self.display_surface.blit(title_surf, title_rect)
                y_offset += 35
            
            if description:  # Description line
                desc_rect = pygame.Rect(40, y_offset, WIDTH - 80, 25)
                self.draw_text_wrapped(self.display_surface, description, self.font, TEXT_COLOR, desc_rect)
                y_offset += 30
            else:
                y_offset += 10
    
    def display_navigation_hint(self):
        """Display navigation hints at the bottom"""
        hint_rect = pygame.Rect(20, HEIGHT - 40, WIDTH - 40, 30)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, hint_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, hint_rect, 2)
        
        hint_text = "Use LEFT/RIGHT arrows to navigate sections • Press H to close help"
        hint_surf = self.small_font.render(hint_text, False, TEXT_COLOR)
        hint_text_rect = hint_surf.get_rect(center=hint_rect.center)
        self.display_surface.blit(hint_surf, hint_text_rect)
    
    def display(self):
        self.input()
        self.selection_cooldowns()
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        self.display_section_tabs()
        self.display_content()
        self.display_navigation_hint() 