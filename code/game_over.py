import pygame
import sys
from settings import *

class GameOver:
    def __init__(self):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, 48)
        self.subtitle_font = pygame.font.Font(UI_FONT, 24)
        
        # game over state
        self.game_over = False
        self.fade_alpha = 0
        self.fade_speed = 3
        
        # death sound
        try:
            self.death_sound = pygame.mixer.Sound('audio/death.wav')
            self.death_sound.set_volume(0.8)
        except:
            self.death_sound = None
    
    def trigger_game_over(self):
        """Trigger the game over sequence"""
        self.game_over = True
        if self.death_sound:
            self.death_sound.play()
    
    def handle_input(self):
        """Handle input during game over screen"""
        keys = pygame.key.get_pressed()
        
        # Exit game with ESC or ENTER
        if keys[pygame.K_ESCAPE] or keys[pygame.K_RETURN]:
            pygame.quit()
            sys.exit()
    
    def draw_fade_overlay(self):
        """Draw the fade overlay"""
        if self.fade_alpha < 200:
            self.fade_alpha += self.fade_speed
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(self.fade_alpha)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
    
    def draw_game_over_text(self):
        """Draw the game over text and options"""
        # Game Over title
        title_text = self.title_font.render("GAME OVER", False, (255, 0, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.display_surface.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.subtitle_font.render("You have fallen in battle...", False, TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.display_surface.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        instruction_text = self.font.render("Press ESC or ENTER to exit", False, TEXT_COLOR)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.display_surface.blit(instruction_text, instruction_rect)
        
        # Additional message
        message_text = self.font.render("Your journey ends here, brave warrior", False, TEXT_COLOR)
        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        self.display_surface.blit(message_text, message_rect)
    
    def display(self):
        """Display the game over screen"""
        if not self.game_over:
            return
        
        self.handle_input()
        self.draw_fade_overlay()
        self.draw_game_over_text() 