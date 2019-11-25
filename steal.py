import pygame
from player import Player
class Cross():
    def __init__(self, x, y, width, height, color, lineThickness):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lineThickness = lineThickness
        self.centerx = (x+width)/2
        self.centery = (y+height)/2

    def draw_cross(self, win):
        points1 = [(self.x, self.y), (self.x+self.width, self.y+self.height)]
        points2 = [(self.x+self.width, self.y), (self.x, self.y+self.width)]
        pygame.draw.lines(win, self.color, False, points1, self.lineThickness)
        pygame.draw.lines(win, self.color, False, points2, self.lineThickness)

    def collidepoint(self, pos):
        imaginary_rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        if imaginary_rect.collidepoint(pos[0], pos[1]):
            return 1
        else:
            return 0


class Steal():

    def __init__(self, player_no):
        self.maps = [pygame.rect.Rect(50, 50, 180, 180),
                     pygame.rect.Rect(250, 50, 180, 180),
                     pygame.rect.Rect(450, 50, 180, 180),
                     pygame.rect.Rect(650, 50, 180, 180),
                     pygame.rect.Rect(850, 50, 180, 180),
                     pygame.rect.Rect(1050, 50, 180, 180)]
        self.stealtokenstartcoordinates = (350, 375)
        self.numberofstealtokens = 0 if player_no == 1 else 1
        self.stealtokensize = (10, 10)
        self.stealtoken = [Cross(self.stealtokenstartcoordinates[0], self.stealtokenstartcoordinates[1], self.stealtokensize[0], self.stealtokensize[1], (255, 0, 0), 2) for i in range(self.numberofstealtokens)]
        self.defencetokenstartcoordinates = (380, 425)
        self.numberofdefencetokens = 10 if player_no == 1 else 0
        self.recDraw = pygame.rect.Rect(0, 500, 150, 25)
        self.defencetokensize = (40, 40)
        self.recDefenceTokens = [pygame.rect.Rect(self.defencetokenstartcoordinates[0], self.defencetokenstartcoordinates[1], self.defencetokensize[0], self.defencetokensize[1]) for i in range(self.numberofdefencetokens)] if player_no==1 else []

        self.stealing_from = [0 for i in range(self.numberofstealtokens)]
        self.stealoclock = [0 for i in range(self.numberofstealtokens)]
        self.detectoclockS = 0
        self.detectoclockD = 0
        self.steal_start_time = [None for i in range(self.numberofstealtokens)]

        self.P_innocent = 0
        self.P_culprit = 0

        self.defence_coordinates = []
        self.steal_coordinates = []
        for i in range(self.numberofdefencetokens):
            self.defence_coordinates.append((self.defencetokenstartcoordinates[0], self.defencetokenstartcoordinates[1]))
        for i in range(self.numberofstealtokens):
            self.steal_coordinates.append((self.stealtokenstartcoordinates[0], self.stealtokenstartcoordinates[1]))
        self.caught = [[0,0] for i in range(self.numberofstealtokens)]
        self.recLogY = 600
        self.recLogsize = 420
        self.recLog = pygame.rect.Rect(0, self.recLogY, 650, self.recLogsize)
        self.ranking = []
        self.recPunishment = pygame.rect.Rect(885, 450, 180, 180)

    def initialize_steal_token(self, n, text):
        self.stealtoken[n].x = self.stealtokenstartcoordinates[0]
        self.stealtoken[n].y = self.stealtokenstartcoordinates[1]
        self.steal_coordinates[n] = (self.stealtokenstartcoordinates[0], self.stealtokenstartcoordinates[1])
        print(text)

    def initialize_defence_token(self, n):
        self.recDefenceTokens[n].x = self.defencetokenstartcoordinates[0]
        self.recDefenceTokens[n].y = self.defencetokenstartcoordinates[1]
        self.defence_coordinates[n] = (self.defencetokenstartcoordinates[0], self.defencetokenstartcoordinates[1])
        # print("defence coords have been updated to = ", self.defence_coordinates)

    def update_steal_coordinates(self, n):
        self.steal_coordinates[n] = (self.stealtoken[n].x+self.stealtokensize[0]/2, self.stealtoken[n].y+self.stealtokensize[1]/2)
        self.detectoclockS = 1
        # print("steal coords have been updates to = ", self.steal_coordinates)

    def update_defence_coordinates(self, n):
        self.defence_coordinates[n] = (self.recDefenceTokens[n].x, self.recDefenceTokens[n].y)
        self.detectoclockD = 1
        # print("defence coords have been updates to = ", self.defence_coordinates)

    def update_token_count(self):
        if len(self.stealtoken) != self.numberofstealtokens:
            if len(self.stealtoken) > self.numberofstealtokens:
                self.stealtoken = self.stealtoken[:-1]
            if len(self.stealtoken) < self.numberofstealtokens:
                self.stealtoken.append(Cross(self.stealtokenstartcoordinates[0], self.stealtokenstartcoordinates[1], self.stealtokensize[0], self.stealtokensize[1], (255, 0, 0), 2))
            if len(self.steal_coordinates) < self.numberofstealtokens:
                while len(self.steal_coordinates) < self.numberofstealtokens:
                    self.steal_coordinates.append(self.stealtokenstartcoordinates)
            if len(self.steal_coordinates) > self.numberofstealtokens:
                while len(self.steal_coordinates) > self.numberofstealtokens:
                    self.steal_coordinates = self.steal_coordinates[:-1]
            print(self.numberofstealtokens, self.steal_coordinates)
            self.steal_start_time = [None for i in range(self.numberofstealtokens)]
            self.stealing_from = [0 for i in range(self.numberofstealtokens)]
            self.stealoclock = [0 for i in range(self.numberofstealtokens)]

            if len(self.steal_start_time) < self.numberofstealtokens:
                while len(self.steal_start_time) < self.numberofstealtokens:
                    self.steal_start_time.append(None)
            if len(self.steal_start_time) > self.numberofstealtokens:
                while len(self.steal_start_time) > self.numberofstealtokens:
                    self.steal_start_time = self.steal_start_time[:-1]


        if len(self.recDefenceTokens) != self.numberofdefencetokens:
            if len(self.recDefenceTokens) > self.numberofdefencetokens:
                self.recDefenceTokens = self.recDefenceTokens[:-1]
            if len(self.recDefenceTokens) < self.numberofdefencetokens:
                self.recDefenceTokens.append(pygame.rect.Rect(self.defencetokenstartcoordinates[0], self.defencetokenstartcoordinates[1], self.defencetokensize[0], self.defencetokensize[1]))
            if len(self.defence_coordinates) < self.numberofdefencetokens:
                while len(self.defence_coordinates) < self.numberofdefencetokens:
                    self.defence_coordinates.append(self.defencetokenstartcoordinates)
            if len(self.defence_coordinates) > self.numberofdefencetokens:
                while len(self.defence_coordinates) > self.numberofdefencetokens:
                    self.defence_coordinates = self.defence_coordinates[:-1]
            print(self.numberofdefencetokens, self.defence_coordinates)


    def draw_steal(self, win, P):
        # print(self.numberofstealtokens, len(self.stealtoken))
        win.fill((255, 255, 255))
        font = pygame.font.SysFont("Arial", 20)
        font_bold = pygame.font.SysFont("Arial", 20, bold=True)
        font_small = pygame.font.SysFont("Arial", 10)

        pygame.draw.line(win, (0,0,0), (0,300), (1300, 300), 1)
        pygame.draw.line(win, (0,0,0), (0, 540), (650, 540), 1)
        pygame.draw.line(win, (0,0,0), (650, 300), (650, 1080), 1)

        pygame.draw.rect(win, (204, 229, 255), self.recPunishment)
        pygame.draw.rect(win, (0,0,0), self.recPunishment, 1)
        punishment_text = font.render(str("Drag your officer tokens here to increase punishment probabilities."), 1, (0,0,0))
        win.blit(punishment_text, (self.recPunishment.centerx - punishment_text.get_width()/2, self.recPunishment.y - 60))

        font_bold_underline = pygame.font.SysFont("Arial", 25, bold=True)
        font_bold_underline.set_underline(1)
        heading1 = font_bold_underline.render("Time", 1, (0, 0, 0))
        heading2 = font_bold_underline.render("Player Punished", 1, (0, 0, 0))
        heading3 = font_bold_underline.render("Victim", 1, (0, 0, 0))

        win.blit(heading1, (104, 585))
        win.blit(heading2, (260, 585))
        win.blit(heading3, (525, 585))

        font_title = pygame.font.SysFont("Arial", 28, bold=True)
        punishheading = font_title.render("PUNISH", 1, (0,0,0))
        win.blit(punishheading, (975-(punishheading.get_width()/2), 310))

        punishheading = font_title.render("POLICE LOG", 1, (0, 0, 0))
        win.blit(punishheading, (320 - (punishheading.get_width() / 2), 540))

        punishheading = font_title.render("STEAL/DEFEND", 1, (0, 0, 0))
        win.blit(punishheading, (650 - (punishheading.get_width() / 2), 10))

        punishheading = font_title.render("BUDGET", 1, (0, 0, 0))
        win.blit(punishheading, (325 - (punishheading.get_width() / 2), 310))


        for i in range(1,7):
            if i not in [1,6]:
                if i != P.id:
                    pygame.draw.rect(win, (240, 240, 240), self.maps[i-1])
                    maptext = "Player "+ str(i)
                    maptext = font.render(maptext, 1, (0, 0, 0))
                    win.blit(maptext, (self.maps[i-1].centerx - maptext.get_width() / 2, self.maps[i-1].y+self.maps[i-1].height+20))
                    ranktext = font.render("Rank " + str(self.ranking.index(i)+1), 1, (0,0,0))
                    win.blit(ranktext, (self.maps[i-1].centerx - maptext.get_width() / 2, self.maps[i-1].y+self.maps[i-1].height+40))

                    pygame.draw.rect(win, (0, 0, 0), self.maps[i - 1], 1)
                else:
                    pygame.draw.rect(win, (180, 180, 180), self.maps[i - 1])
                    maptext = "Player "+ str(i) + " (Your Map)"
                    maptext = font.render(maptext, 1, (0, 0, 0))
                    win.blit(maptext, (self.maps[i - 1].centerx - maptext.get_width() / 2, self.maps[i-1].y+self.maps[i-1].height+20))
                    ranktext = font.render("Rank " + str(self.ranking.index(i) + 1), 1, (0, 0, 0))
                    win.blit(ranktext, (self.maps[i - 1].centerx - maptext.get_width() / 2, self.maps[i-1].y+self.maps[i - 1].height + 40))

                    pygame.draw.rect(win, (0,0,0), self.maps[i - 1], 1)


                    pygame.draw.rect(win, (0,0,0), self.recDraw)
                    recDrawtext = "<- PRODUCE"
                    recDrawtext = font_bold.render(recDrawtext, 1, (255,255,255))
                    win.blit(recDrawtext, (
                        self.recDraw.centerx - recDrawtext.get_width() / 2,
                        self.recDraw.centery - recDrawtext.get_height() / 2))

        available_steals = self.numberofstealtokens
        for i in self.stealtoken:
            i.draw_cross(win)
            if i.x != self.stealtokenstartcoordinates[0] or i.y != self.stealtokenstartcoordinates[1]:
                available_steals -= 1
        stealtext = font.render("Available steal tokens (" +str(available_steals)+ ")", 1, (0,0,0))
        win.blit(stealtext, (self.stealtokenstartcoordinates[0] - stealtext.get_width() - 30, self.stealtokenstartcoordinates[1] - 5))
        recProbabilityCulprit = pygame.rect.Rect(700, 700, 500, 30)

        recProbabilityCulpritFilling = pygame.rect.Rect(recProbabilityCulprit.x, recProbabilityCulprit.y,
                                                        recProbabilityCulprit.width*(self.P_culprit),
                                                        recProbabilityCulprit.height)
        pygame.draw.rect(win, (204, 229, 255), recProbabilityCulpritFilling)
        pygame.draw.rect(win, (0, 0, 0), recProbabilityCulprit, 1)

        culprit_text = font.render("Probability of you being punished if you are the culprit is ≈" + str(round(self.P_culprit * 100)) + "%", 1, (0,0,0))
        win.blit(culprit_text, (recProbabilityCulprit.x, recProbabilityCulprit.y - 30))

        for i in range(11):
            pygame.draw.line(win, (0,0,0), (recProbabilityCulprit.x + (recProbabilityCulprit.width*i/10), recProbabilityCulprit.y+recProbabilityCulprit.height), (recProbabilityCulprit.x + (recProbabilityCulprit.width*i/10), recProbabilityCulprit.y+recProbabilityCulprit.height+5))
            t = font_small.render(str(i*10), 1, (0,0,0))
            win.blit(t, (recProbabilityCulprit.x + (recProbabilityCulprit.width*i/10), recProbabilityCulprit.y+recProbabilityCulprit.height+5))

        recProbabilityInnocent = pygame.rect.Rect(700, 850, 500, 30)

        recProbabilityInnocentFilling = pygame.rect.Rect(recProbabilityInnocent.x, recProbabilityInnocent.y,
                                                        recProbabilityInnocent.width * (self.P_innocent),
                                                        recProbabilityInnocent.height)
        pygame.draw.rect(win, (204, 229, 255), recProbabilityInnocentFilling)
        pygame.draw.rect(win, (0, 0, 0), recProbabilityInnocent, 1)
        innocent_text = font.render(
            "Probability of you being punished if you are innocent ≈" + str(round(self.P_innocent * 100)) + "%", 1, (0, 0, 0))
        win.blit(innocent_text, (recProbabilityInnocent.x, recProbabilityInnocent.y - 30))

        for i in range(11):
            pygame.draw.line(win, (0,0,0), (recProbabilityInnocent.x + (recProbabilityInnocent.width*(i/10)), recProbabilityInnocent.y+recProbabilityInnocent.height), (recProbabilityInnocent.x + (recProbabilityInnocent.width*(i/10)), recProbabilityInnocent.y+recProbabilityInnocent.height+5))
            t = font_small.render(str(i*10), 1, (0,0,0))
            win.blit(t, (recProbabilityInnocent.x + (recProbabilityInnocent.width*i/10), recProbabilityInnocent.y+recProbabilityInnocent.height+5))



        available_defences = self.numberofdefencetokens
        for i in self.recDefenceTokens:
            pygame.draw.rect(win, (0,153,0), i)
            if i.x != self.defencetokenstartcoordinates[0] or i.y != self.defencetokenstartcoordinates[1]:
                available_defences -= 1
        defencetext = font.render("Available defence tokens (" + str(available_defences) + ")", 1, (0,0,0))
        win.blit(defencetext, (self.defencetokenstartcoordinates[0]-defencetext.get_width() - 30, self.defencetokenstartcoordinates[1]-5))

    def draw_log(self, win, police_log, scrolling):
        font = pygame.font.SysFont("Arial", 20)
        if not scrolling:
            self.recLogsize = (len(police_log)+1) * 35
            self.recLogY = 1020 - self.recLogsize
            y = self.recLogY + 35
            for message in police_log:
                post1 = font.render(str(message[0]), 1, (0, 0, 0), 1)
                post2 = font.render(str(message[1]), 1, (0, 0, 0), 1)
                post3 = font.render(str(message[2]), 1, (0, 0, 0), 1)


                if y < 1020 and y > 600:
                    win.blit(post1, (self.recLog.x + 108, y))
                    win.blit(post2, (self.recLog.x + 324, y))
                    win.blit(post3, (self.recLog.x + 540, y))

                y += 35


    def draw_scrolled_log(self, win, police_log, direction):
        font = pygame.font.SysFont("Arial", 20)
        self.recLogsize = (len(police_log) + 1) * 35
        if direction == 'up':
            if self.recLogY < 600:
                self.recLogY = min(self.recLogY + 35, 600)
        if direction == 'down':
            if self.recLogY + self.recLogsize > 1020:
                self.recLogY = max(self.recLogY - 35, 1020-self.recLogsize)

        y = self.recLogY + 35
        for message in police_log:
            print(message)
            post1 = font.render(str(message[0]), 1, (0, 0, 0), 1)
            post2 = font.render(str(message[1]), 1, (0, 0, 0), 1)
            post3 = font.render(str(message[2]), 1, (0, 0, 0), 1)

            if y < 1020 and y > 600: #######################################################
                win.blit(post1, (self.recLog.x + 108, y))
                win.blit(post2, (self.recLog.x + 324, y))
                win.blit(post3, (self.recLog.x + 540, y))

            y += 35

        if self.recLogY + self.recLogsize == 1020:
            return 0
        else:
            return 1


