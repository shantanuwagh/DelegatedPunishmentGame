import pygame
import random
pygame.font.init()
from grid import Grid
import pygame_textinput
import pygame.locals as pl
from network import Network
import pickle
from numbers import Number
from datetime import datetime
import time
import csv
##########################################################################################################
import sys
from numbers import Number
from collections import Set, Mapping, deque

try: # Python 2
    zero_depth_bases = (basestring, Number, xrange, bytearray)
    iteritems = 'iteritems'
except NameError: # Python 3
    zero_depth_bases = (str, bytes, Number, range, bytearray)
    iteritems = 'items'

# def getsize(obj_0):
#     """Recursively iterate to sum size of object & members."""
#     _seen_ids = set()
#     def inner(obj):
#         obj_id = id(obj)
#         if obj_id in _seen_ids:
#             return 0
#         _seen_ids.add(obj_id)
#         size = sys.getsizeof(obj)
#         if isinstance(obj, zero_depth_bases):
#             pass # bypass remaining control flow and return
#         elif isinstance(obj, (tuple, list, Set, deque)):
#             size += sum(inner(i) for i in obj)
#         elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
#             size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
#         # Check for custom object instances - may subclass above too
#         if hasattr(obj, '__dict__'):
#             size += inner(vars(obj))
#         if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
#             size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
#         return size
#     return inner(obj_0)

##############################################################################################################

pygame.init()
number = 1
width = 1920
height = 1080
win = pygame.display.set_mode((width,height)) #, pygame.FULLSCREEN)

text_box = pygame_textinput.TextInput(text_color=(32,32,32), repeat_keys_initial_ms=500, repeat_keys_interval_ms=200)
textinputQty = pygame_textinput.TextInput(font_size=25,
                                                      antialias=True,
                                                      text_color=(0, 0, 0),
                                                      cursor_color=(0, 0, 1),
                                                      repeat_keys_initial_ms=400,
                                                      repeat_keys_interval_ms=35,
                                                      box_width=80,
                                                      box_height=25,
                                                      character_limit=4)

pygame.display.set_caption("client")
font_bold = pygame.font.SysFont("Arial", 20, bold=True)


def main1():
    clock = pygame.time.Clock()
    n = Network()
    D, P, S, C, T, W = n.getP()

    textinput = pygame_textinput.TextInput(font_family="timesnewroman", cursor_color=(0,0,0), repeat_keys_initial_ms=10, repeat_keys_interval_ms=10)
    errormade = False
    MainLoop = True
    loopready = True
    loop1 = False
    loop2 = False
    loop3 = False
    loop4 = False
    loop5 = False


    rectangle1_dragging, rectangle2_dragging, rectangle3_dragging, rectangle4_dragging, rectangle5_dragging = False, False, False, False, False
    cross_dragging = [False for i in range(S.numberofstealtokens)]
    defence_dragging = [False for i in range(S.numberofdefencetokens)]
    flag = [0 for i in range(S.numberofstealtokens)]
    selected_rect = 0
    scrolling = 0
    scrolling_log = 0
    menuNumber = 0
    selected_menu_option = [None, None]
    renewal_pending = 0
    punished = 0
    defence_maploc = ['NA' for i in range(S.numberofdefencetokens)]
    while MainLoop:

        def renewal_pending(P, W):
            P.update_fertility(W.round_number)

            global selected_rect, scrolling, scrolling_log, menuNumber, selected_menu_option
            if W.round_number == 1:
                P.experiment_start_time = W.start_time
            rectangle1_dragging, rectangle2_dragging, rectangle3_dragging, rectangle4_dragging, rectangle5_dragging = False, False, False, False, False
            cross_dragging = [False for i in range(S.numberofstealtokens)]
            defence_dragging = [False for i in range(S.numberofdefencetokens)]
            flag = [0 for i in range(S.numberofstealtokens)]
            selected_rect = 0
            scrolling = 0
            scrolling_log = 0
            menuNumber = 0
            defence_maploc = ['NA' for i in range(S.numberofdefencetokens)]
            selected_menu_option = [None, None]


        if loopready:
            response, chat_list = n.send("wait_class")
            W.draw_wait(win)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if W.continue_button.collidepoint(event.pos):
                        W.ready = 1
            if datetime.now() >= W.start_time and datetime.now() <= W.end_time:
                W.started = 0
                W.ready = 0
                if P.type < 2:
                    loopready = False
                    loop1 = True
                else:
                    loopready = False
                    loop2 = True

                renewal_pending(P, W)

            W, P = n.send((W, P))



        if loop1 and P.type < 2:
            if datetime.now() >= W.end_time:
                loopready = True
                loop1 = False
                W.ready = 0
                W.started = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    MainLoop = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if D.rec1.collidepoint(event.pos):
                        selected_rect = 1
                        print("Rec1 selected")
                    elif D.rec2.collidepoint(event.pos):
                        selected_rect = 2
                        print("Rec2 selected")
                    elif D.rec3.collidepoint(event.pos):
                        selected_rect = 3
                        print("Rec3 selected")
                    elif D.rec4.collidepoint(event.pos):
                        selected_rect = 4
                        print("Rec4 selected")
                    elif D.rec5.collidepoint(event.pos):
                        selected_rect = 5
                        print("Rec5 selected")

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_ESCAPE:
                        loop1 = False
                        MainLoop = False

                if event.type == pygame.MOUSEBUTTONUP and D.recSteal.collidepoint(event.pos):
                    loop1 = False
                    loop2 = True
                    loop3 = False


                if event.type == pygame.MOUSEBUTTONUP and C.recOuter.collidepoint(event.pos):
                    loop4 = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if T.recOuter.collidepoint(event.pos):
                        loop5 = True
                        menuNumber = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if D.rec1.collidepoint(event.pos):
                            rectangle1_dragging = True
                            print("Rectangle 1 is being dragged.")
                            mouse_x, mouse_y = event.pos
                            offset_x = D.rec1.x - mouse_x
                            offset_y = D.rec1.y - mouse_y

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if D.rec2.collidepoint(event.pos):
                            rectangle2_dragging = True
                            print("Rectangle 2 is being dragged.")
                            mouse_x, mouse_y = event.pos
                            offset_x = D.rec2.x - mouse_x
                            offset_y = D.rec2.y - mouse_y

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if D.rec3.collidepoint(event.pos):
                            rectangle3_dragging = True
                            print("Rectangle 3 is being dragged.")
                            mouse_x, mouse_y = event.pos
                            offset_x = D.rec3.x - mouse_x
                            offset_y = D.rec3.y - mouse_y

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if D.rec4.collidepoint(event.pos):
                            rectangle4_dragging = True
                            print("Rectangle 4 is being dragged.")
                            mouse_x, mouse_y = event.pos
                            offset_x = D.rec4.x - mouse_x
                            offset_y = D.rec4.y - mouse_y

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if D.rec5.collidepoint(event.pos):
                            rectangle5_dragging = True
                            print("Rectangle 5 is being dragged.")
                            mouse_x, mouse_y = event.pos
                            offset_x = D.rec5.x - mouse_x
                            offset_y = D.rec5.y - mouse_y

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if rectangle1_dragging == True:
                                rectangle1_dragging = False
                                if D.target.collidepoint(event.pos):
                                    D.score[0] = 1
                                    if D.stage == 0:
                                        D.stage = 1
                                D.initialize_rectangles()
                                print("Rectangle 1 is not being dragged.")

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if rectangle2_dragging == True:
                            rectangle2_dragging = False
                            if D.target.collidepoint(event.pos):
                                D.score[1] = 1
                                if D.stage == 1:
                                    D.stage = 2
                            D.initialize_rectangles()
                            print("Rectangle 2 is not being dragged.")

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if rectangle3_dragging == True:
                            rectangle3_dragging = False
                            if D.target.collidepoint(event.pos):
                                D.score[2] = 1
                                if D.stage == 2:
                                    D.stage = 3
                            D.initialize_rectangles()
                            print("Rectangle 3 is not being dragged.")


                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if rectangle4_dragging == True:
                            rectangle4_dragging = False
                            if D.target.collidepoint(event.pos):
                                D.score[3] = 1
                                if D.stage == 3:
                                    D.stage = 4
                            D.initialize_rectangles()
                            print("Rectangle 4 is not being dragged.")


                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if rectangle5_dragging == True:
                            rectangle5_dragging = False
                            if D.target.collidepoint(event.pos):
                                D.score[4] = 1
                                if D.stage == 4:
                                    D.stage = 5
                            D.initialize_rectangles()
                            print("Rectangle 5 is not being dragged.")


                if event.type == pygame.MOUSEMOTION:
                    if rectangle1_dragging:
                        mouse_x, mouse_y = event.pos
                        D.rec1.x = mouse_x + offset_x
                        D.rec1.y = mouse_y + offset_y

                if event.type == pygame.MOUSEMOTION:
                    if rectangle2_dragging:
                        mouse_x, mouse_y = event.pos
                        D.rec2.x = mouse_x + offset_x
                        D.rec2.y = mouse_y + offset_y

                if event.type == pygame.MOUSEMOTION:
                    if rectangle3_dragging:
                        mouse_x, mouse_y = event.pos
                        D.rec3.x = mouse_x + offset_x
                        D.rec3.y = mouse_y + offset_y

                if event.type == pygame.MOUSEMOTION:
                    if rectangle4_dragging:
                        mouse_x, mouse_y = event.pos
                        D.rec4.x = mouse_x + offset_x
                        D.rec4.y = mouse_y + offset_y

                if event.type == pygame.MOUSEMOTION:
                    if rectangle5_dragging:
                        mouse_x, mouse_y = event.pos
                        D.rec5.x = mouse_x + offset_x
                        D.rec5.y = mouse_y + offset_y
            response, chat_list = n.send("drag_class")
            # print("11111 sizeof D", getsize(D), "sizeof P", getsize(P))
            # file = open("logfile.txt", 'a')
            # file.write("\n" + str(datetime.now())+ " BEFORE - sizeof D "+ str(getsize(D)) + " sizeof P " + str(getsize(P)))
            D, P = n.send((D, P))
            # file.write("\n" + str(datetime.now())+ " AFTER - sizeof D "+ str(getsize(D)) + " sizeof P " + str(getsize(P)))
            D.draw_game(win, P)
            C.draw_chat(win, P)
            C.draw_receive(win, chat_list, 0)
            T.draw_trade(win, P, selected_menu_option)
            if scrolling:
                C.draw_scrolled_receive(win, 'neither', chat_list)
            else:
                C.draw_receive(win, chat_list, scrolling)



        if loop2:
            if datetime.now() >= W.end_time:
                loopready = True
                loop2 = False
                W.ready = 0
                W.started = 0

            if len(flag) < S.numberofstealtokens:
                flag.append(0)
                print("had to append one to the flag as flag length was smaller")
            if len(flag) > S.numberofstealtokens:
                flag = flag[:-1]
                print("had to take one from the flag as flag length was larger")
            if len(cross_dragging) < S.numberofstealtokens:
                cross_dragging.append(False)
            if len(cross_dragging) > S.numberofstealtokens:
                cross_dragging = cross_dragging[:-1]
            if len(defence_dragging) < S.numberofdefencetokens:
                defence_dragging.append(False)
            if len(defence_dragging) > S.numberofdefencetokens:
                defence_dragging = defence_dragging[:-1]



            for jdx, j in enumerate(S.stealtoken):
                # print(jdx, (j.x, j.y), "==", S.stealtokenstartcoordinates)
                if (j.x, j.y) == S.stealtokenstartcoordinates:
                    flag[jdx] = 0
                    # print("Flag ", jdx, "was set to zero")
                    P.stealing_from[jdx] = 0
                    # print("flagif=", flag, "stealingfromif=", P.stealing_from)
                else:
                    # print("flagel=", flag, "stealingfromel=", P.stealing_from)
                    pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    MainLoop = False


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:  # or MOUSEBUTTONDOWN depending on what you want.
                        loop2 = False
                        MainLoop = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:

                        if T.recOuter.collidepoint(event.pos):
                            loop5 = True
                            menuNumber = 0

                        if S.recDraw.collidepoint(event.pos):
                            loop1 = True
                            loop2 = False
                            loop3 = False
                            for i in range(len(S.stealtoken)):
                                S.initialize_steal_token(i, "my client place switch to draw")
                                P.stealing_from[i] = 0

                        if C.recOuter.collidepoint(event.pos):
                            loop4 = True

                        # for i in S.stealtoken:
                        #     if i.collidepoint(event.pos):
                        #         selected_rect = "cross"
                        #         break
                        #
                        # for i in S.recDefenceTokens:
                        #     if i.collidepoint(event.pos):
                        #         selected_rect = "defence"
                        #         break



                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for jdx, j in enumerate(S.stealtoken):
                            if j.collidepoint(event.pos):
                                cross_dragging[jdx] = 1
                                flag[jdx] = 0
                                mouse_x, mouse_y = event.pos
                                offset_x = j.x - mouse_x
                                offset_y = j.y - mouse_y
                                break

                        for idx, i in enumerate(S.recDefenceTokens):
                            if i.collidepoint(event.pos):
                                defence_dragging[idx] = 1
                                mouse_x, mouse_y = event.pos
                                offset_x = i.x - mouse_x
                                offset_y = i.y - mouse_y
                                break

                    if S.recLog.collidepoint(event.pos):
                        if event.button == 4:
                            scrolling_log = S.draw_scrolled_log(win, police_log, 'up')
                            print("mouse was scrolled up")
                        if event.button == 5:
                            scrolling_log = S.draw_scrolled_log(win, police_log, 'down')
                            print("mouse was scrolled down")


                if event.type == pygame.MOUSEMOTION:
                        for jdx, j in enumerate(S.stealtoken):
                            if cross_dragging[jdx]:
                                mouse_x, mouse_y = event.pos
                                j.x = mouse_x + offset_x
                                j.y = mouse_y + offset_y
                                break

                        for idx, i in enumerate(S.recDefenceTokens):
                            if defence_dragging[idx]:
                                mouse_x, mouse_y = event.pos
                                i.x = mouse_x + offset_x
                                i.y = mouse_y + offset_y
                                break
                # global number
                # print(number, flag)
                # number += 1

                if event.type == pygame.MOUSEBUTTONUP:
                    for jdx, j in enumerate(S.stealtoken):

                        if cross_dragging[jdx] == True:
                            cross_dragging[jdx] = False
                            for i in range(1, 7):
                                if i != P.id:

                                    if flag[jdx] and not S.maps[i - 1].collidepoint(event.pos):
                                        flag[jdx] = 0
                                    if S.maps[i - 1].collidepoint(event.pos):
                                        S.update_steal_coordinates(jdx)
                                        P.stealing_from[jdx] = i
                                        flag[jdx] = 1
                                        break


                        if flag[jdx]:
                            print("Flag is set")
                            S.steal_start_time[jdx] = datetime.now()

                        if not flag[jdx]:
                            print("flag is not set")
                            S.initialize_steal_token(jdx, "myclient place 1")
                            S.steal_start_time[jdx] = None
                            P.stealing_from[jdx] = 0
                        print("Cross is not being dragged.")


                        try:
                            if defence_dragging[idx]:
                                defence_dragging[idx] = False
                                if S.recDefenceTokens[idx].collidelist(S.maps) == -1 and not S.recDefenceTokens[idx].colliderect(S.recPunishment):
                                    S.initialize_defence_token(idx)
                                    defence_maploc[idx] = 'NA'
                                else:
                                    defence_maploc[idx] = S.recDefenceTokens[idx].collidelist(S.maps) + 1 if S.recDefenceTokens[idx].collidelist(S.maps) + 1 else 7
                                    S.update_defence_coordinates(idx)
                            print("defence maploc ==== ", defence_maploc)
                        except:
                            pass


            for i in range(S.numberofstealtokens):
                if flag[i]:
                    try:
                        if ((datetime.now() - S.steal_start_time[i]).microseconds) >=33333:
                            S.stealoclock[i] = 1
                            S.steal_start_time[i] = datetime.now()
                        else:
                            S.stealoclock[i] = 0
                    except:
                        pass
            response, chat_list  = n.send("steal_class")
            #print(response)
            # print("22222 sizeof S", getsize(S), "sizeof P", getsize(P))
            # file = open("logfile.txt", 'a')
            # file.write("\n" + str(datetime.now())+ " BEFORE - sizeof S "+ str(getsize(S)) + " sizeof P " + str(getsize(P)))
            S, P, police_log, punished, data_storage_punishment = n.send((S, P))
            # file.write("\n" + str(datetime.now())+ " AFTER - sizeof S "+ str(getsize(S)) + " sizeof P " + str(getsize(P)))
            S.draw_steal(win, P)
            C.draw_chat(win, P)
            C.draw_receive(win, chat_list, 0)
            T.draw_trade(win, P, selected_menu_option)

            if scrolling_log:
                S.draw_scrolled_log(win, police_log, 'neither')
            else:
                S.draw_log(win, police_log, scrolling)

            if scrolling:
                C.draw_scrolled_receive(win, 'neither', chat_list)
            else:
                C.draw_receive(win, chat_list, scrolling)


        if loop3:
            if datetime.now() >= W.end_time:
                loopready = True
                loop3 = False
                W.ready = 0
                W.started = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    MainLoop = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:  # or MOUSEBUTTONDOWN depending on what you want.
                        # loop2 = False
                        MainLoop = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # if M.recDraw.collidepoint(event.pos):
                        #     loop1 = True
                        #     loop2 = False
                        #     loop3 = False
                        #
                        #
                        # if M.recSteal.collidepoint(event.pos):
                        #     loop1 = False
                        #     loop2 = True
                        #     loop3 = False
                        loop1 = True
                        loop2 = False
                        loop3 = False


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        pass

        if loop4:
            if datetime.now() >= W.end_time:
                loopready = True
                loop4 = False
                W.ready = 0
                W.started = 0
            if event.type == pygame.MOUSEBUTTONUP and not C.recOuter.collidepoint(event.pos):
                loop4 = False
            response, chat_list = n.send("chat_class")
            # print("the chat_list that reached myclient was ", chat_list)
            C.draw_chat(win, P)
            C.draw_receive(win, chat_list, 0)
            T.draw_trade(win, P, selected_menu_option)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:

                    if T.recOuter.collidepoint(event.pos):
                        loop5 = True
                        menuNumber = 0

                    for i in range(len(C.playerRectangles)):
                        if C.playerRectangles[i].collidepoint(event.pos):
                            C.selected_recipient_rectangle = i
                            C.draw_chat(win, P)
                            C.draw_receive(win, chat_list, 0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if C.recOuter.collidepoint(event.pos):
                        if event.button == 4:
                            scrolling = C.draw_scrolled_receive(win, 'up', chat_list)
                            print("mouse was scrolled up")
                        if event.button == 5:
                            scrolling = C.draw_scrolled_receive(win, 'down', chat_list)
                            print("mouse was scrolled down")

                        else:
                            if scrolling:
                                C.draw_scrolled_receive(win, 'neither', chat_list)
                            else:
                                C.draw_receive(win, chat_list, scrolling)

            win.blit(text_box.get_surface(), (1331, 1000))

            if text_box.update(events):
                C.message = (text_box.get_text())
                if C.message.strip() != '':
                    scrolling = 0
                    C.draw_receive(win, chat_list, scrolling)
                    text_box.clear_text()
                    # print("There was a message and it was ....."+C.message+"....")
            # print("33333 sizeof C", getsize(C), "sizeof P", getsize(P))
            # file = open("logfile.txt", 'a')
            # file.write("\n" + str(datetime.now())+ " BEFORE - sizeof C "+ str(getsize(C)) + " sizeof P " + str(getsize(P)))
            C, P = n.send((C, P))
            # file.write("\n" + str(datetime.now())+ " AFTER - sizeof C "+ str(getsize(C)) + " sizeof P " + str(getsize(P)))

        if loop5:
            if datetime.now() >= W.end_time:
                loopready = True
                loop5 = False
            C.draw_chat(win, P)
            C.draw_receive(win, chat_list, 0)
            win.blit(textinputQty.get_surface(), (T.recHowMuchToSend.x, T.recHowMuchToSend.y))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    MainLoop = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:  # or MOUSEBUTTONDOWN depending on what you want.
                        loop5 = False
                        MainLoop = False

                if event.type == pygame.MOUSEBUTTONUP and not T.recOuter.collidepoint(event.pos):
                    loop5 = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if C.recOuter.collidepoint(event.pos):
                        loop4 = True

                    if T.recWhomToSend.collidepoint(event.pos):
                        menuNumber = 1

                    if T.recWhatToSend.collidepoint(event.pos) and menuNumber != 1:
                        menuNumber = 2

                    if menuNumber == 1:
                        for i in range(len(T.optionrects1)):
                            if T.optionrects1[i].collidepoint(event.pos):
                                T.TryToTrade[0] = T.WhomOptions[i]
                                selected_menu_option[0] = i
                                menuNumber = 0
                                break

                    if menuNumber == 2:
                        for i in range(len(T.optionrects2)):
                            if T.optionrects2[i].collidepoint(event.pos):
                                T.TryToTrade[1] = T.WhatOptions[i]
                                selected_menu_option[1] = i
                                menuNumber = 0
                                break

                if event.type == pygame.MOUSEBUTTONUP:
                    if T.recstealtokenpos.collidepoint(event.pos):
                        print("buy steal")
                        T.buysell[0] += 1
                        print(T.buysell)
                    if T.recstealtokenneg.collidepoint(event.pos):
                        print("sell steal")
                        T.buysell[0] -= 1
                        print(T.buysell)
                    if T.recdefencetokenpos.collidepoint(event.pos):
                        print("buy def")
                        T.buysell[1] += 1
                        print(T.buysell)
                    if T.recdefencetokenneg.collidepoint(event.pos):
                        print("sell def")
                        T.buysell[1] -= 1
                        print(T.buysell)



                if textinputQty.update(events) or (event.type == pygame.MOUSEBUTTONUP and T.recSend.collidepoint(event.pos)):
                    try:
                        T.TryToTrade[2] = int(textinputQty.get_text())
                        if T.TryToTrade[2]:
                            print(T.TryToTrade)
                            selected_menu_option = [None, None]
                            textinputQty.clear_text()
                            T.trade_initiated = True
                    except:
                        errormade = "Invalid number."
                        errortext = font_bold.render(errormade, 1, (255, 0, 0))
                        win.blit(errortext, (1550, 240))




            response, chat_list = n.send("trade_class")
            # print("44444 sizeof T", getsize(T), "sizeof P", getsize(P))
            # file = open("logfile.txt", 'a')
            # file.write("\n" + str(datetime.now())+ " BEFORE - sizeof T "+ str(getsize(T)) + " sizeof P " + str(getsize(P)))
            T, P, response_message = n.send((T, P))
            # file.write("\n" + str(datetime.now())+ " AFTER - sizeof T "+ str(getsize(T)) + " sizeof P " + str(getsize(P)))
            T.draw_trade(win, P, selected_menu_option)
            if menuNumber:
                T.dropdown(win, menuNumber)
            if len(response_message):
                errortext = font_bold.render(response_message, 1, (255, 0, 0))
                win.blit(errortext, (1550, 240))
                pygame.display.update()
                time.sleep(1)
                response_message = ""


        if P.type==0 and not loopready:
            save_steal_token = []
            for i in range(S.numberofstealtokens):
                save_steal_token.append([i+1, S.stealtoken[i].x, S.stealtoken[i].y, P.stealing_from[i] if P.stealing_from[i] else 'NA', "dropped=" + str(flag[i]), S.caught[i][0], S.caught[i][1]+1])

            payment_scheme = [10,20,30,40,50,60] if P.fertility_orientation=='IE' else [10,10,10,10,10,10]
            F = open("session_"+str(n.port)+"_for_civilian_"+str(P.id)+"_"+str(P.experiment_start_time).replace('.', ':').replace(' ', '_').replace(':', '_').replace('-','_')+".csv", 'a')
            F.write(str(P.experiment_start_time)  + '\t' +  str([0.1, 0, 10, 10, 180, "reprimand amount", "reprimand probability"])  + '\t' +  str(n.port)  + '\t' +
              str(payment_scheme)  + '\t' +  str(P.id)  + '\t' +  str(P.type)  + '\t' +
              str(W.round_number)  + '\t' +  str(datetime.now() - W.start_time)  + '\t' +  str(P.resources['Grain'])  + '\t' +  str(loop1)  + '\t' +  str(save_steal_token)  + '\t' +  str(D.score)  + '\t' +  str(punished if punished==P.id else 0))
            # print(P.experiment_start_time, [0.1, 0, 10, 10, 180, "reprimand amount", "reprimand probability"], n.port,
            #       "payment scheme", payment_scheme, P.id, P.type,
            #       W.round_number, datetime.now() - W.start_time, P.resources['Grain'], loop1, save_steal_token, D.score, punished if punished==P.id else 0)
            punished = 0
            S.caught = [[0,0] for i in range(S.numberofstealtokens)]

        if P.type==2 and not loopready:
            save_steal_token = []
            # for i in range(S.numberofstealtokens):
                # save_steal_token.append(
                #     [i + 1, S.stealtoken[i].x, S.stealtoken[i].y, P.stealing_from[i] if P.stealing_from[i] else 'NA',
                #      "dropped=" + str(flag[i]), S.caught[i][0], S.caught[i][1]+1])

            payment_scheme = [10, 20, 30, 40, 50, 60] if P.fertility_orientation == 'IE' else [10, 10, 10, 10, 10, 10]

            save_defence_token = []
            for i in range(S.numberofdefencetokens):
                dropped = 0
                if S.defence_coordinates[i] != S.defencetokenstartcoordinates:
                    dropped = 1
                save_defence_token.append([i+1, S.recDefenceTokens[i].x, S.recDefenceTokens[i].y, S.recDefenceTokens[i].x+S.recDefenceTokens[i].width, S.recDefenceTokens[i].y+S.recDefenceTokens[i].height,
                                           defence_maploc[i], dropped])
            F = open("session_"+str(n.port)+"_for_enforcer_"+str(P.id)+"_"+str(P.experiment_start_time).replace('.', ':').replace(' ', '_').replace(':', '_').replace('-','_')+".csv", 'a')
            F.write('\n' + str(P.experiment_start_time) + '\t' + str([0.1, 0, 10, 10, 180, "reprimand amount", "reprimand probability"]) + '\t' +
                  str(n.port)  + '\t' +
                  str(payment_scheme)  + '\t' +  str(P.id)  + '\t' +  str(P.type)  + '\t' +
                  str(W.round_number)  + '\t' +  str(datetime.now() - W.start_time)  + '\t' +  str(P.resources['Grain'])  + '\t' +  str(loop1)  + '\t' +  str(save_steal_token) + '\t' +  str(D.score) + '\t' +
                  str(punished if punished == P.id else 0) + '\t' +  str(save_defence_token) + '\t' +  str(data_storage_punishment))
            punished = 0
            S.caught = [[0,0] for i in range(S.numberofstealtokens)]
        pygame.display.update()

        clock.tick(30)


    pygame.quit()
main1()