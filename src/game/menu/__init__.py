import os

import pygame

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, SPRITES_DIR


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.start_button = pygame.Rect(0, 100, 200, 80)
        self.quit_button = pygame.Rect(0, 200, 200, 80)
        self.game_scene = False
        self.button_tile = pygame.transform.scale(
            self.load_tile("button.png"), (200, 80)
        )

    @staticmethod
    def load_tile(image_file):
        tile_image = pygame.image.load(os.path.join(SPRITES_DIR, image_file)).convert()
        tile_image.set_colorkey((0, 0, 0))
        return tile_image

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
            self.screen.blit(self.button_tile, (0, 100))
            # Write start text
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Start', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (100, 140)
            self.screen.blit(text, textRect)

            # Draw quit button
            pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button)
            self.screen.blit(self.button_tile, (0, 200))
            # Write quit text
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Quit', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (100, 240)
            self.screen.blit(text, textRect)
            
            pygame.display.flip()
        
        return self.running, self.game_scene