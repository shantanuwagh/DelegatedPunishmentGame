import pygame
import pygame_textinput as pt
from pygame_functions import *
from datetime import datetime
from pygame_functions import *
font = pygame.font.SysFont("Arial", 20)
font_bold = pygame.font.SysFont("Arial", 20, bold=True)
class Chat():
    def __init__(self):
        self.message = ''
        self.timestamp = ''
        self.recOuter = pygame.rect.Rect(1300, 540, 620, 1080)

        self.message = ''
        self.recReceiveY = 1000
        self.recReceiveSize = 35
        self.playerHeadersStartCoordinates = (1330, 570)
        self.playerHeaderSize = (93, 30)
        self.playerRectangles = [pygame.rect.Rect(self.playerHeadersStartCoordinates[0] + (self.playerHeaderSize[0] * i), self.playerHeadersStartCoordinates[1], self.playerHeaderSize[0], self.playerHeaderSize[1]) for i in range(7)]
        self.recReceive = pygame.rect.Rect(self.playerHeadersStartCoordinates[0], self.recReceiveY, (len(self.playerRectangles)-1)*self.playerHeaderSize[0], self.recReceiveSize)
        self.selected_recipient_rectangle = 0
        self.selected_recipient = 0
        self.receivecover = pygame.rect.Rect(self.playerHeadersStartCoordinates[0], self.playerHeadersStartCoordinates[1], (len(self.playerRectangles)-1)*self.playerHeaderSize[0], 420)

    def draw_scrolled_receive(self, win, direction, chat_list):
        if direction == 'up':
            if self.recReceiveY < 600:
                self.recReceiveY = min(self.recReceiveY + 35, 600)
        if direction == 'down':
            if self.recReceiveY + self.recReceiveSize > 1000:
                self.recReceiveY = max(self.recReceiveY - 35, 1000-self.recReceiveSize)

        y = self.recReceiveY + 35
        for message in chat_list:
            print(message)
            bold_id = font_bold.render(str(message[1]), 1, (0, 0, 0), 1)
            player_message = font.render(str(message[2]), 1, (0, 0, 0), 1)

            if y < 965 and y > 600:
                win.blit(bold_id, (self.recReceive.x + 5, y))
                win.blit(player_message, (self.recReceive.x + 20, y))

            y += 35


        if self.recReceiveY + self.recReceiveSize == 1000:
            return 0
        else:
            return 1

    def draw_receive(self, win, chat_list, scrolling):
        if not scrolling:
            self.recReceiveSize = (len(chat_list)+1)*35
            self.recReceiveY = 1000-self.recReceiveSize
            y = self.recReceiveY
            for message in chat_list:
                bold_id = font_bold.render(str(message[1]), 1, (0,0,0), 1)
                player_message = font.render(str(message[2]), 1, (0, 0, 0), 1)

                if y<1000 and y>600:
                    win.blit(bold_id, (self.recReceive.x + 5, y))
                    win.blit(player_message, (self.recReceive.x + 20, y))
                    # print("the message that reached draw_receive was ", str(message[2]))
                y+=35


    def draw_chat(self, win, P):
        font_title = pygame.font.SysFont("Arial", 28, bold=True)
        title = font_title.render("CHAT", 1, (0,0,0))
        win.blit(title, (self.receivecover.centerx-(title.get_width()/2), 538))

        pygame.draw.rect(win, (0,0,0), pygame.rect.Rect(1328, 995, 555, 35), 3) # chatbox cover

        pygame.draw.rect(win, (0,0,0), self.recOuter, 4)

        pygame.draw.line(win, (0,0,0), (1300, 0), (1300,1080), 5) # game|chatbox partition

        pygame.draw.rect(win, (204, 204, 204), self.receivecover)



        # chatheading = font.render("CHAT SCREEN", 1, (255,0,0), 1)
        # win.blit(chatheading, (1450,540))
        id_list = [i for i in range(1, 7) if i != P.id]
        id_list.insert(0, 0)

        for i in range(0, 6):

            pygame.draw.rect(win, (255, 255, 255), self.playerRectangles[i])
            pygame.draw.rect(win, (0, 0, 0), self.playerRectangles[i], 1)

            if self.selected_recipient_rectangle == i:
                self.selected_recipient = id_list[i]
                # print("Selected recipient in chat was change to ", self.selected_recipient)
                pygame.draw.rect(win, (204, 204, 204), self.playerRectangles[i])





            grptxt = font.render(str("Group"), 1, (0, 0, 0))
            win.blit(grptxt, (self.playerRectangles[0].centerx - grptxt.get_width() / 2,
                              self.playerRectangles[0].centery - grptxt.get_height() / 2))

            if i:
                maptext = "Player " + str(id_list[i])
                maptext = font.render(maptext, 1, (0, 0, 0))

                win.blit(maptext, (self.playerRectangles[i].centerx - maptext.get_width() / 2,
                                   self.playerRectangles[i].centery - maptext.get_height() / 2))


        pygame.draw.rect(win, (0, 0, 0), self.receivecover, 1)











