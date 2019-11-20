import pygame
import pygame_textinput
from rounded_rect import Rounded_Rect
class Trade():
    def __init__(self, id):
        self.optionrect1alignment = (1450, 120)
        self.optionrect2alignment = (1450, 200)
        self.optionrect3alignment = (1450, 280)
        self.optionrectsize = [80, 25]
        self.recWhomToSend = pygame.rect.Rect(self.optionrect1alignment[0], self.optionrect1alignment[1], self.optionrectsize[0], self.optionrectsize[1])
        self.recWhatToSend = pygame.rect.Rect(self.optionrect2alignment[0], self.optionrect2alignment[1], self.optionrectsize[0], self.optionrectsize[1])
        self.recHowMuchToSend = pygame.rect.Rect(self.optionrect3alignment[0], self.optionrect3alignment[1], self.optionrectsize[0], self.optionrectsize[1])

        self.WhomOptions = []
        for i in range(1,7):
            if id != i:
                self.WhomOptions.append(i)
        self.WhatOptions = ["Grain"]
        self.TryToTrade = [0, "", 0]
        self.trade_initiated = False
        self.recOuter = pygame.rect.Rect(1300, 0, 620, 540)
        self.recSend = pygame.rect.Rect(1450, 360, self.optionrectsize[0], self.optionrectsize[1])
        self.optionrects1 = [pygame.rect.Rect(self.optionrect1alignment[0], self.optionrect1alignment[1]+(25*i), self.optionrectsize[0], self.optionrectsize[1]) for i in range(1,6)]

        self.optionrects2 = [pygame.rect.Rect(self.optionrect2alignment[0], self.optionrect2alignment[1]+25, self.optionrectsize[0], self.optionrectsize[1])]

        self.stealtokenoffer = 0
        self.defencetokenoffer = 0


        self.recstealtokenneg = pygame.rect.Rect(1675, 120, 35, 35)
        self.recstealtokenpos = pygame.rect.Rect(1800, 120, 35, 35)

        self.recdefencetokenneg = pygame.rect.Rect(1675, 280, 35, 35)
        self.recdefencetokenpos = pygame.rect.Rect(1800, 280, 35, 35)

        self.stealtokenbuycost = 50
        self.stealtokensellcost = 50
        self.defencetokenbuycost = 50
        self.defencetokensellcost = 50

        self.buysell = [0,0]

    def draw_trade(self, win, P, selected_menu_option):
        font = pygame.font.SysFont("Arial", 20)
        font_bold = pygame.font.SysFont("Arial", 24, bold=True)

        totext = font.render("To:", 1, (0,0,0))
        win.blit(totext, (self.optionrect1alignment[0]-totext.get_width()-20, self.optionrect1alignment[1]))
        pygame.draw.rect(win, (0,0,0), self.recWhomToSend, 1)
        if selected_menu_option[0] is not None:
            selectedtext = font.render("Player " + str(self.WhomOptions[selected_menu_option[0]]), 1, (0, 0, 0))
            win.blit(selectedtext, (self.recWhomToSend.centerx - selectedtext.get_width()/2, self.recWhomToSend.centery - selectedtext.get_height()/2))

        itemtext = font.render("Item:", 1, (0,0,0))
        win.blit(itemtext, (self.optionrect2alignment[0]-itemtext.get_width()-20, self.optionrect2alignment[1]))
        pygame.draw.rect(win, (0, 0, 0), self.recWhatToSend, 1)
        if selected_menu_option[1] is not None:
            selectedtext = font.render(str(self.WhatOptions[selected_menu_option[1]]), 1, (0, 0, 0))
            win.blit(selectedtext, (self.recWhatToSend.centerx - selectedtext.get_width() / 2, self.recWhatToSend.centery - selectedtext.get_height() / 2))

        qtytext = font.render("Amount:", 1, (0,0,0))
        win.blit(qtytext, (self.optionrect3alignment[0]-qtytext.get_width()-20, self.optionrect3alignment[1]))
        pygame.draw.rect(win, (0, 0, 0), self.recHowMuchToSend, 1)

        font_title = pygame.font.SysFont("Arial", 28, bold=True)
        punishheading = font_title.render("TRADE", 1, (0, 0, 0))
        win.blit(punishheading, (self.optionrect1alignment[0]+self.optionrectsize[0]/2 - (punishheading.get_width() / 2), 30))

        pygame.draw.rect(win, (204,204,204), self.recSend)
        pygame.draw.rect(win, (0, 0, 0), self.recSend, 1)
        sendtext = font_bold.render("SEND", 1, (0,0,0))
        win.blit(sendtext, ((self.recSend.centerx - sendtext.get_width()/2), (self.recSend.centery - sendtext.get_height()/2)))

        pygame.draw.line(win, (0,0,0), (1610,0), (1610,540), 1)

        punishheading = font_title.render("TRADE", 1, (0, 0, 0))
        win.blit(punishheading, (self.optionrect1alignment[0] + self.optionrectsize[0] / 2 - (punishheading.get_width() / 2), 30))

        text = font.render("Steal tokens", 1, (0, 0, 0))
        win.blit(text, (1725, 70))

        text = font.render("Defend tokens", 1, (0, 0, 0))
        win.blit(text, (1720, 230))


        pygame.draw.rect(win, (0, 0, 0), self.recstealtokenneg, 2)
        text = font.render("-", 1, (0,0,0))
        win.blit(text, (self.recstealtokenneg.centerx - text.get_width()/2, self.recstealtokenneg.centery - text.get_height()/2))
        pygame.draw.rect(win, (0, 0, 0), self.recstealtokenpos, 2)
        text = font.render("+", 1, (0, 0, 0))
        win.blit(text, (self.recstealtokenpos.centerx - text.get_width() / 2, self.recstealtokenpos.centery - text.get_height() / 2))
        text = font.render("BUY for " + str(self.stealtokenbuycost), 1, (0, 0, 0))
        win.blit(text, (self.recstealtokenpos.centerx - text.get_width() / 2, self.recstealtokenpos.centery + 30))
        text = font.render("SELL for " + str(self.stealtokensellcost), 1, (0, 0, 0))
        win.blit(text, (self.recstealtokenneg.centerx - text.get_width() / 2, self.recstealtokenneg.centery +30))


        pygame.draw.rect(win, (0, 0, 0), self.recdefencetokenneg, 2)
        text = font.render("-", 1, (0, 0, 0))
        win.blit(text, (self.recdefencetokenneg.centerx - text.get_width() / 2, self.recdefencetokenneg.centery - text.get_height() / 2))
        pygame.draw.rect(win, (0, 0, 0), self.recdefencetokenpos, 2)
        text = font.render("+", 1, (0, 0, 0))
        win.blit(text, (self.recdefencetokenpos.centerx - text.get_width() / 2, self.recdefencetokenpos.centery - text.get_height() / 2))
        text = font.render("BUY for " + str(self.defencetokenbuycost), 1, (0, 0, 0))
        win.blit(text, (self.recdefencetokenpos.centerx - text.get_width() / 2, self.recdefencetokenpos.centery + 30))
        text = font.render("SELL for " + str(self.defencetokensellcost), 1, (0, 0, 0))
        win.blit(text, (self.recdefencetokenneg.centerx - text.get_width() / 2, self.recdefencetokenneg.centery + 30))

        text = font_bold.render("Grain Available = " + str(int(P.resources["Grain"])), 1, (0, 0, 0))
        win.blit(text, (1665, 400))

    def dropdown(self, win, menuNumber):
        font = pygame.font.SysFont("Arial", 15)
        if menuNumber == 1:

            for i in range(len(self.WhomOptions)):
                pygame.draw.rect(win, (0, 0, 0), self.optionrects1[i])
                optiontext = font.render("Player " + str(self.WhomOptions[i]), 1, (255,255,255))
                win.blit(optiontext, (self.optionrects1[i].centerx - optiontext.get_width()/2, self.optionrects1[i].centery - optiontext.get_height()/2))


        if menuNumber == 2:

            for i in range(len(self.WhatOptions)):
                pygame.draw.rect(win, (0, 0, 0), self.optionrects2[i])
                optiontext = font.render(str(self.WhatOptions[i]), 1, (255,255,255))
                win.blit(optiontext, (self.optionrects2[i].centerx - optiontext.get_width()/2, self.optionrects2[i].centery - optiontext.get_height()/2))
