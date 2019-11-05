import pygame
import random


class DragDrop():
    def initialize_rectangles(self):
        self.rec1.center = (100, 100)
        self.rec2.center = (375, 100)
        self.rec3.center = (650, 100)
        self.rec4.center = (925, 100)
        self.rec5.center = (1200, 100)


    def __init__(self):
        self.rec1 = pygame.rect.Rect(50, 50, 100, 100)
        self.rec2 = pygame.rect.Rect(50, 50, 100, 100)
        self.rec3 = pygame.rect.Rect(50, 50, 100, 100)
        self.rec4 = pygame.rect.Rect(50, 50, 100, 100)
        self.rec5 = pygame.rect.Rect(50, 50, 100, 100)
        self.target = pygame.rect.Rect(0, 540, 1300, 540)
        self.recSteal = pygame.rect.Rect(1080, 500, 220, 25)
        self.score = [0,0,0,0,0]
        self.stage = 0
        self.bgs = ["plainbg.jpg", "seedbg.jpg", "fertibg.jpg", "waterbg.jpg", "plantsbg.jpg"]
        self.initialize_rectangles()
        self.log_last_message = []


    def draw_game(self, win, P):
        win.fill((255,255,255))


        win.blit(pygame.image.load(self.bgs[self.stage]), (0,0))
        font = pygame.font.SysFont("Arial", 20)
        font_bold = pygame.font.SysFont("Arial", 20, bold=True)
        text = font_bold.render(str("GRAIN"), 1, (0,0,0))
        win.blit(text, (1200, 960))
        text = font_bold.render(str(P.resources["Grain"]), 1, (0, 0, 0))
        win.blit(text, (1200, 980))

        font_title = pygame.font.SysFont("Arial", 28, bold=True)
        punishheading = font_title.render("PRODUCE", 1, (0, 0, 0))
        win.blit(punishheading, (650 - (punishheading.get_width() / 2), 10))

        pygame.draw.rect(win, (255, 255, 255), self.rec1)
        pygame.draw.rect(win, (0,0,0), self.rec1, 1)
        rec1text = "SEED"
        rec1text = font.render(rec1text, 1, (0, 0, 0))
        win.blit(rec1text, (self.rec1.centerx - rec1text.get_width() / 2, self.rec1.centery - rec1text.get_height() / 2))

        pygame.draw.rect(win, (255, 255, 255), self.rec2)
        pygame.draw.rect(win, (0, 0, 0), self.rec2, 1)
        rec2text = "FERTILIZER"
        rec2text = font.render(rec2text, 1, (0, 0, 0))
        win.blit(rec2text, (self.rec2.centerx - rec2text.get_width() / 2, self.rec2.centery - rec2text.get_height() / 2))

        pygame.draw.rect(win, (255, 255, 255), self.rec3)
        pygame.draw.rect(win, (0, 0, 0), self.rec3, 1)
        rec3text = "WATER"
        rec3text = font.render(rec3text, 1, (0, 0, 0))
        win.blit(rec3text, (self.rec3.centerx - rec3text.get_width() / 2, self.rec3.centery - rec3text.get_height() / 2))

        pygame.draw.rect(win, (255, 255, 255), self.rec4)
        pygame.draw.rect(win, (0, 0, 0), self.rec4, 1)
        rec4text = "SUNLIGHT"
        rec4text = font.render(rec4text, 1, (0, 0, 0))
        win.blit(rec4text, (self.rec4.centerx - rec4text.get_width() / 2, self.rec4.centery - rec4text.get_height() / 2))

        pygame.draw.rect(win, (255, 255, 255), self.rec5)
        pygame.draw.rect(win, (0, 0, 0), self.rec5, 1)
        rec5text = "HARVEST"
        rec5text = font.render(rec5text, 1, (0, 0, 0))
        win.blit(rec5text, (self.rec5.centerx - rec5text.get_width() / 2, self.rec5.centery - rec5text.get_height() / 2))

        pygame.draw.rect(win, (0,0,0), self.target, 1)

        pygame.draw.rect(win, (0,0,0), self.recSteal)
        recStealtext = "STEAL/DEFEND/PUNISH ->"
        recStealtext = font_bold.render(recStealtext, 1, (255,255,255))

        font_bold_underline = pygame.font.SysFont("Arial", 20, bold=True)
        font_bold_underline.set_underline(1)

        if len(self.log_last_message):
            log_text1 = font_bold.render(self.log_last_message[0], 1, (0, 0, 0))
            log_text2 = font_bold.render(self.log_last_message[1], 1, (0, 0, 0))
            log_text3 = font_bold.render(self.log_last_message[2], 1, (0, 0, 0))
            heading1 = font_bold_underline.render("Time", 1, (0, 0, 0))
            heading2 = font_bold_underline.render("Player Punished", 1, (0, 0, 0))
            heading3 = font_bold_underline.render("Victim", 1, (0, 0, 0))

            win.blit(heading1, (80 - heading1.get_width()/2, 960))
            win.blit(heading2, (206 - heading2.get_width()/2, 960))
            win.blit(heading3, (322 - heading3.get_width()/2, 960))
            win.blit(log_text1, (80 - log_text1.get_width()/2, 980))
            win.blit(log_text2, (206 - log_text2.get_width()/2, 980))
            win.blit(log_text3, (322 - log_text3.get_width()/2, 980))

        win.blit(recStealtext, (self.recSteal.centerx - recStealtext.get_width() / 2, self.recSteal.centery - recStealtext.get_height() / 2))


