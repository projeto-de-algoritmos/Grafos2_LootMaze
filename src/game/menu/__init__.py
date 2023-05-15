import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.start_button = pygame.Rect(0, 0, 200, 80)
        self.quit_button = pygame.Rect(0, 100, 200, 80)
        self.game_scene = False

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.collidepoint(event.pos):
                self.running = False
                self.game_scene = False
            elif self.start_button.collidepoint(event.pos):
                self.running = False
                self.game_scene = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            # Draw everything for the menu
            self.screen.fill((0,0,0))
            
            # Draw start button
            pygame.draw.rect(self.screen, (255, 0, 0), self.start_button)
            # Draw quit button
            pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button)
            
            pygame.display.flip()
        
        return self.running, self.game_scene