import pygame
import math
import sys
from settings import *

class StartScreen:
    def __init__(self):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, 64)
        self.subtitle_font = pygame.font.Font(UI_FONT, 24)
        self.button_font = pygame.font.Font(UI_FONT, 32)
        
        # start screen state
        self.active = True
        self.showing_help = False
        
        # button setup
        self.buttons = {
            'play': pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60),
            'help': pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 60),
            'quit': pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 210, 200, 60)
        }
        
        # selection system
        self.selected_button = 'play'
        self.selection_time = None
        self.can_move = True
        self.selection_cooldown = 200
        
        # background animation
        self.animation_time = 0
        self.animation_speed = 0.02
        
        # try to load background music
        try:
            pygame.mixer.music.load('audio/main.ogg')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(loops=-1)
        except:
            pass  # No background music if file doesn't exist
    
    def handle_input(self):
        """Handle input for the start screen"""
        keys = pygame.key.get_pressed()
        
        if self.showing_help:
            # In help mode, only handle ESC to go back
            if keys[pygame.K_ESCAPE]:
                self.showing_help = False
            return
        
        # Navigation with arrow keys
        if self.can_move:
            if keys[pygame.K_UP]:
                if self.selected_button == 'play':
                    self.selected_button = 'quit'
                elif self.selected_button == 'help':
                    self.selected_button = 'play'
                elif self.selected_button == 'quit':
                    self.selected_button = 'help'
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            
            elif keys[pygame.K_DOWN]:
                if self.selected_button == 'play':
                    self.selected_button = 'help'
                elif self.selected_button == 'help':
                    self.selected_button = 'quit'
                elif self.selected_button == 'quit':
                    self.selected_button = 'play'
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
        
        # Selection with ENTER or SPACE
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            self.handle_button_click()
    
    def selection_cooldowns(self):
        """Handle selection cooldowns"""
        if not self.can_move:
            cur_time = pygame.time.get_ticks()
            if cur_time - self.selection_time >= self.selection_cooldown:
                self.can_move = True
    
    def handle_button_click(self):
        """Handle button clicks"""
        if self.selected_button == 'play':
            self.start_game()
        elif self.selected_button == 'help':
            self.show_help()
        elif self.selected_button == 'quit':
            self.quit_game()
    
    def start_game(self):
        """Start the game"""
        self.active = False
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def show_help(self):
        """Show help information"""
        self.showing_help = True
    
    def quit_game(self):
        """Quit the game"""
        pygame.quit()
        sys.exit()
    
    def draw_animated_background(self):
        """Draw an animated background"""
        self.animation_time += self.animation_speed
        
        # Create a gradient background
        for y in range(HEIGHT):
            # Create a subtle wave effect
            wave = int(20 * math.sin(y * 0.01 + self.animation_time))
            color_value = max(0, min(255, 100 + wave))
            color = (0, color_value // 3, color_value // 2)  # Blue-green gradient
            pygame.draw.line(self.display_surface, color, (0, y), (WIDTH, y))
    
    def draw_title(self):
        """Draw the game title"""
        # Main title
        title_text = self.title_font.render("ZELDA HACK", False, (255, 215, 0))  # Gold color
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        # Add a shadow effect
        shadow_text = self.title_font.render("ZELDA HACK", False, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 3 + 3))
        self.display_surface.blit(shadow_text, shadow_rect)
        self.display_surface.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.subtitle_font.render("A Python Adventure", False, TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 60))
        self.display_surface.blit(subtitle_text, subtitle_rect)
    
    def draw_buttons(self):
        """Draw the menu buttons"""
        button_texts = {
            'play': 'PLAY',
            'help': 'HELP',
            'quit': 'QUIT'
        }
        
        for button_name, button_rect in self.buttons.items():
            # Button background
            if button_name == self.selected_button:
                pygame.draw.rect(self.display_surface, UPGRADE_BG_COLOR_SELECTED, button_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, button_rect, 4)
            else:
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, button_rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, button_rect, 3)
            
            # Button text
            text_color = TEXT_COLOR_SELECTED if button_name == self.selected_button else TEXT_COLOR
            button_text = self.button_font.render(button_texts[button_name], False, text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.display_surface.blit(button_text, text_rect)
    
    def draw_instructions(self):
        """Draw instructions at the bottom"""
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER or SPACE to select"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = self.font.render(instruction, False, TEXT_COLOR)
            instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT - 80 + i * 25))
            self.display_surface.blit(instruction_text, instruction_rect)
    
    def draw_version_info(self):
        """Draw version or author info"""
        version_text = self.font.render("Python Zelda Game", False, TEXT_COLOR)
        version_rect = version_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
        self.display_surface.blit(version_text, version_rect)
    
    def draw_help_overlay(self):
        """Draw the help overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Help content
        help_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, help_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, help_rect, 3)
        
        # Title
        title_text = self.title_font.render("GAME CONTROLS", False, UI_BORDER_COLOR_ACTIVE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        self.display_surface.blit(title_text, title_rect)
        
        # Help content
        help_content = [
            ("Movement", "Arrow Keys - Move your character"),
            ("Attack", "Space - Attack with current weapon"),
            ("Magic", "Left Ctrl - Cast current magic spell"),
            ("Weapon Switch", "Q - Switch between weapons"),
            ("Magic Switch", "E - Switch between magic spells"),
            ("Upgrade Menu", "M - Open/close upgrade menu"),
            ("Help", "H - Open/close help menu"),
            ("", ""),
            ("Objective", "Defeat enemies to gain experience and become stronger!"),
            ("", "Use different weapons and magic to overcome challenges."),
            ("", "Upgrade your stats to survive longer in battle.")
        ]
        
        y_offset = 150
        for title, description in help_content:
            if title:  # Title line
                title_surf = self.subtitle_font.render(title, False, UI_BORDER_COLOR_ACTIVE)
                title_rect = title_surf.get_rect(topleft=(80, y_offset))
                self.display_surface.blit(title_surf, title_rect)
                y_offset += 35
            
            if description:  # Description line
                desc_surf = self.font.render(description, False, TEXT_COLOR)
                desc_rect = desc_surf.get_rect(topleft=(80, y_offset))
                self.display_surface.blit(desc_surf, desc_rect)
                y_offset += 30
            else:
                y_offset += 10
        
        # Back instruction
        back_text = self.font.render("Press ESC to return to menu", False, TEXT_COLOR)
        back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.display_surface.blit(back_text, back_rect)
    
    def display(self):
        """Display the start screen"""
        if not self.active:
            return
        
        self.handle_input()
        self.selection_cooldowns()
        
        # Draw everything
        self.draw_animated_background()
        
        if self.showing_help:
            self.draw_help_overlay()
        else:
            self.draw_title()
            self.draw_buttons()
            self.draw_instructions()
            self.draw_version_info() 