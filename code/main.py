import pygame, sys
from settings import *
from level import Level
from start_screen import StartScreen


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Zelda_Hack')

        # Initialize start screen and level
        self.start_screen = StartScreen()
        self.level = None
        self.game_started = False

        # sound
        # ogg files may not be working
        # main_sound = pygame.mixer.Sound('audio/main.ogg')
        # main_sound.set_volume(0.5)
        # main_sound.play(loops=-1)
    
    def start_game(self):
        """Initialize the game level when starting"""
        self.level = Level()
        self.game_started = True
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.game_started:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    if event.key == pygame.K_h:
                        self.level.toggle_help()
            
            # Clear screen
            self.screen.fill(WATER_COLOR)
            
            # Show start screen or game
            if not self.game_started:
                self.start_screen.display()
                if not self.start_screen.active:
                    self.start_game()
            else:
                self.level.run()
            
            pygame.display.update()
            self.clock.tick(FPS)
            

if __name__ == '__main__':
    game = Game()
    game.run()