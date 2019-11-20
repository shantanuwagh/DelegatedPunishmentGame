import pygame
from datetime import datetime, timedelta

class Wait():
    def __init__(self):
        self.continue_button = pygame.rect.Rect(1000, 100, 100, 50)
        self.ready = 0
        self.start_time = datetime.now() + timedelta(days=1)
        self.end_time = datetime.now() - timedelta(days=1)
        self.started = 0
        self.round_number = 1
    
    def draw_wait(self, win):
        win.fill((255,255,255))

        pygame.draw.rect(win, (0, 0, 0), self.continue_button)
        # pygame.draw.rect(win, (0, 0, 0), self.continue_button, 1)
        
        font_bold = pygame.font.SysFont("Arial", 24, bold=True)
        text = font_bold.render("Ready", 1, (255,0,0))
        win.blit(text, (
        self.continue_button.centerx - text.get_width() / 2, self.continue_button.centery - text.get_height() / 2))

        if self.started:
            font_bold = pygame.font.SysFont("Arial", 24, bold=True)
            text = font_bold.render("starting in " + str((self.start_time - datetime.now()).seconds)  + "...", 1, (0, 0, 0))
            win.blit(text, (
                self.continue_button.centerx - text.get_width() / 2,
                self.continue_button.centery + 130 - text.get_height() / 2))
            if (self.start_time - datetime.now()).seconds <= 1:
                self.started = 0

        elif self.ready == 1:
            font_bold = pygame.font.SysFont("Arial", 24, bold=True)
            text = font_bold.render("Waiting for other players to get ready...", 1, (0, 0, 0))
            win.blit(text, (
            self.continue_button.centerx - text.get_width() / 2, self.continue_button.centery + 100 - text.get_height() / 2))
