import socket
from _thread import *
import sys
import pygame
from drag import DragDrop
from player import Player
from steal import Steal
from waitforstart import Wait
import pickle
from pygame import *
from chat import Chat
from trade import Trade
from datetime import datetime
import random
import numpy as np
from datetime import datetime, timedelta
import csv

# import pdb
# pdb.set_trace()
#######################################################################################################################
import sys
from numbers import Number
# from collections import Set, Mapping, deque

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

#########################################################################################################################

player_no = 0
enforcer_random = random.randint(0,6)

chat_lists = {
    "0" : [],
    "12" : [],
    "13" : [],
    "14" : [],
    "15" : [],
    "16" : [],

    "23" : [],
    "24" : [],
    "25" : [],
    "26" : [],

    "34" : [],
    "35" : [],
    "36" : [],

    "45" : [],
    "46" : [],

    "56" : []
}
trades_list = []
server = "192.168.1.15"
port = 5556

fertility_orientation = "IE"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(6)
print("Waiting for a connection, Server Started")

draganddrops = [DragDrop(), DragDrop(), DragDrop(), DragDrop(), DragDrop(), DragDrop()]
players = [Player(1), Player(2), Player(3), Player(4), Player(5), Player(6)]
steals = [Steal(1), Steal(2), Steal(3), Steal(4), Steal(5), Steal(6)]
chats = [Chat(), Chat(), Chat(), Chat(), Chat(), Chat()]
trades = [Trade(1), Trade(2), Trade(3), Trade(4), Trade(5), Trade(6)]
waits = [Wait(), Wait(), Wait(), Wait(), Wait(), Wait()]

def renew_classes(round_number):
    global draganddrops, players, steals, chats, trades, waits
    draganddrops = [DragDrop(), DragDrop(), DragDrop(), DragDrop(), DragDrop(), DragDrop()]
    players = [Player(1), Player(2), Player(3), Player(4), Player(5), Player(6)]
    steals = [Steal(1), Steal(2), Steal(3), Steal(4), Steal(5), Steal(6)]
    chats = [Chat(), Chat(), Chat(), Chat(), Chat(), Chat()]
    trades = [Trade(1), Trade(2), Trade(3), Trade(4), Trade(5), Trade(6)]
    waits = [Wait(), Wait(), Wait(), Wait(), Wait(), Wait()]
    players[0].type = 2


renew_classes(0)
all_defences = {
                1:[],
                2:[],
                3:[],
                4:[],
                5:[],
                6:[]
                }
all_steals = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: []
}
police_log = [['11:14:02 AM', 4, 3],
['11:14:05 AM', 2, 3],
['11:14:09 AM', 5, 3],
['11:14:11 AM', 5, 3],
['11:14:13 AM', 4, 3],
['11:14:15 AM', 4, 3],
['11:14:16 AM', 4, 3],
['11:14:19 AM', 2, 3],
['11:14:21 AM', 2, 3],
              ['11:14:02 AM', 4, 3],
              ['11:14:05 AM', 2, 3],
              ['11:14:09 AM', 5, 3],
              ['11:14:11 AM', 5, 3],
              ['11:14:13 AM', 4, 3],
              ['11:14:15 AM', 4, 3],
              ['11:14:16 AM', 4, 3],
              ['11:14:19 AM', 2, 3],
              ['11:14:21 AM', 2, 3]
              ]
log_length = len(police_log)
updater = []
tokens_allocated = 0
frame_number = 0
new_chat_row = []



round_constants = {
    'round_time':300,
    'round_number': 0
                   }
# ready = [0,0,0,0,0]
# for p in players:
    # if p.id == enforcer_random:
        # p.type = 2


# def my_punishment(culprit, victim):
#     n_punishable = 5 if enforcer_random == victim else 4
#
#     if tokens_allocated == 0 or enforcer_random == culprit:
#         punishment_vector = [1,0,0,0,0,0,0]
#         arrange = [0,1,2,3,4,5,6]
#     else:
#         P_nobody = 0
#         P_victim = 0
#         P_innocent = (1 / n_punishable) * (1 - (tokens_allocated / 10))
#         P_culprit = (1 / n_punishable) * (tokens_allocated / 10) * (n_punishable - 1)
#         P_enforcer = 0
#
#         if enforcer_random == victim:
#             punishment_vector = [P_nobody, P_enforcer, P_culprit, P_innocent, P_innocent, P_innocent, P_innocent]
#             arrange = [0, enforcer_random, culprit]
#         else:
#             punishment_vector = [P_nobody, P_enforcer, P_victim, P_culprit, P_innocent, P_innocent, P_innocent]
#             arrange = [0, enforcer_random, victim, culprit]
#
#         for i in range(1,7):
#             if i not in arrange:
#                 arrange.append(i)
#     # print("mypunishment", arrange, punishment_vector)
#     chosen = random.choices(arrange, punishment_vector)
#     # print("mypunishment", chosen)
#     return chosen


def ranking():
    data = []
    for pl in players:
        try:
            data.append((pl.id, pl.resources['Grain']))
        except:
            data.append((pl.id, 0))
    data.sort(key=lambda tup:tup[1], reverse=True)
    data1 = [d[0] for d in data]
    return [d[0] for d in data]

def probability():
    n_punishable = 4
    if tokens_allocated:
        return (1 / n_punishable) * (1 - (tokens_allocated / 10)), (1 / n_punishable)  + ((n_punishable - 1)/n_punishable)* (tokens_allocated / 10)
    else:
        return 0,0
punish_counter = 0
# np.random.seed(seed=5)
def punishment(culprit, victim, enforcer):

    print("tokens_allocated", tokens_allocated)
    n_punishable = 3
    # if enforcer_random != victim:
    #     n_punishable = 3

    if tokens_allocated: # and enforcer != culprit
        P_nobody = 0
        P_victim = 0
        abar = 10
        P_innocent = (abar - tokens_allocated)/(n_punishable*abar)
        P_culprit = (abar + (n_punishable-1)*tokens_allocated)/(n_punishable*abar)
        P_enforcer = 0
        punishment_vector = [P_nobody]
        global punish_counter

        for player in players[0:-1]:

            if player.id == enforcer:
                punishment_vector.append(P_enforcer)
            elif player.id == victim:
                punishment_vector.append(P_victim)
            elif player.id == culprit:
                punishment_vector.append(P_culprit)
            else:
                punishment_vector.append(P_innocent)

    else:
        punishment_vector = [1,0,0,0,0,0]

    list_punishment = list(np.random.multinomial(1, punishment_vector))
    print("punishmentvector=", punishment_vector, "list_pun=", list_punishment, punish_counter)
    punish_counter += 1
    return list_punishment.index(1)


def threaded_client(conn, player_no):
    player_no -= 1
    players[player_no].stealing_from = [0 for i in range(steals[player_no].numberofstealtokens)]
    players[player_no].fertility_orientation = fertility_orientation
    tell_the_officer_data_store_punishment = ['NA' for i in range(steals[0].numberofdefencetokens)]
    conn.send(pickle.dumps((draganddrops[player_no], players[player_no], steals[player_no], chats[player_no], trades[player_no], waits[player_no])))
    round_change_flag = {
                         '0': {'drag': 0, 'chat': 0, 'steal': 0, 'trade': 0, 'player': 0},
                         '1': {'drag': 0, 'chat': 0, 'steal': 0, 'trade': 0, 'player': 0},
                         '2': {'drag': 0, 'chat': 0, 'steal': 0, 'trade': 0, 'player': 0},
                         '3': {'drag': 0, 'chat': 0, 'steal': 0, 'trade': 0, 'player': 0},
                         '4': {'drag': 0, 'chat': 0, 'steal': 0, 'trade': 0, 'player': 0},
                         '5': {'drag': 0, 'chat': 0, 'steal': 0, 'trade': 0, 'player': 0},
    }

    #conn.send(pickle.dumps())
    while True:


        # for S in all_steals:
        #     if S[2]:
        #         victims[S[2] - 1] = 1

        # for i in range(victims):
        #     players[i].being_stolen_from = victims[i]
        steals[player_no].ranking = ranking()

        data_type = pickle.loads(conn.recv(3*4096))
        if chats[player_no].selected_recipient == 0:
            # print("I am sending 0 because chats" + str(player_no) + "=" + str(chats[player_no].selected_recipient))

            conn.send(pickle.dumps((data_type + " active", chat_lists["0"])))

        else:
            if chats[player_no].selected_recipient < players[player_no].id:
                # print("I am sending ", str(chats[player_no].selected_recipient) + str(player.id))

                conn.send(pickle.dumps(
                    (data_type + " active", chat_lists[str(chats[player_no].selected_recipient) + str(player.id)])))

            else:
                # print("I am sending ", str(player.id) + str(chats[player_no].selected_recipient))

                    conn.send(pickle.dumps(
                    (data_type + " active", chat_lists[str(player.id) + str(chats[player_no].selected_recipient)])))

        if data_type == "wait_class":
            wait, player = pickle.loads(conn.recv(3*4096))
            # print("wait player grain", player.resources['Grain'])
            wait.start_time = waits[player_no].start_time
            wait.end_time = waits[player_no].end_time
            wait.started = waits[player_no].started
            sum_of_ready = int()
            # print(player_no, "wait.ready", wait.ready, "wait.started", wait.started)

            if wait.ready and not wait.started:
                waits[player_no].ready = wait.ready
                sum_of_ready = 0
                for i in range(6):
                    sum_of_ready += waits[i].ready
            if sum_of_ready >= 2:
                print("Because sum_of_ready was ", sum_of_ready, "we could now start says player", player_no,". Look what waits[i].ready looks like.", "A", waits[0].ready, "B", waits[1].ready, "C", waits[2].ready, "D", waits[3].ready, "E", waits[4].ready, "F", waits[5].ready)
                wait.started = 1
                round_constants['round_number'] += 1
                wait.round_number = round_constants['round_number']
                waits[player_no].round_number = round_constants['round_number']

                for i in range(6):
                    waits[i].start_time = datetime.now() + timedelta(seconds=5)
                    waits[i].end_time = waits[i].start_time + timedelta(seconds=round_constants['round_time'])
                    waits[i].ready = 0
                    waits[i].started = wait.started
                    round_change_flag[str(i)] = {
                        'drag': 1,
                        'chat': 1,
                        'steal': 1,
                        'trade': 1,
                        'player': 1
                    }
                    players[i] = Player(i+1)
                    steals[i] = Steal(i+1)
                    if round_constants['round_number'] == 1:
                        players[i].experiment_start_time = wait.start_time
                    if i == 0:
                        players[i].type = 2
                        print(steals[0].numberofdefencetokens)
                    players[i].enforcer_number_of_defence_tokens = steals[0].numberofdefencetokens
                    players[player_no].stealing_from = [0 for i in range(steals[player_no].numberofstealtokens)]
                    players[player_no].fertility_orientation = fertility_orientation

                    if fertility_orientation == 'EI':
                        if round_constants['round_number'] >= 5:
                            players[i].fertility = players[i].id * 10
                            players[i].fertility = players[i].id * 10
                    elif fertility_orientation == 'IE':
                        if round_constants['round_number'] <= 4:
                            players[i].fertility = players[i].id * 10
                            players[i].fertility = players[i].id * 10

            if datetime.now() > wait.start_time and datetime.now() < wait.end_time:
                for i in range(6):
                    waits[i].started = 0
            conn.send(pickle.dumps((wait, player)))

        if data_type == "chat_classs":

            chat, player = pickle.loads(conn.recv(3*4096))
            # print("round_change_flag on chat", round_change_flag[str(player_no)], player_no)
            if round_change_flag[str(player_no)]['chat']:
                chat = Chat()
                chats[player_no] = Chat()
                round_change_flag[str(player_no)]['chat'] = 0

            # if round_change_flag[str(player_no)]['player']:
            #     player = Player(player_no+1)
            #     players[player_no] = Player(player_no+1)
            #     # print("special chat player grain", player.resources['Grain'], "player number is", player_no)
            #     # print("special chat player grain", players[player_no].resources['Grain'], "player number is", player_no)
            #     if fertility_orientation == 'EI':
            #         if round_constants['round_number'] >= 5:
            #             player.fertility = player.id * 10
            #             players[player_no].fertility = player.id * 10
            #     elif fertility_orientation == 'IE':
            #         if round_constants['round_number'] <=4:
            #             player.fertility = player.id * 10
            #             players[player_no].fertility = player.id * 10
            #     round_change_flag[str(player_no)]['player'] = 0

            global new_chat_row
            if chat.message != '':
                if chat.selected_recipient == 0:
                    chat_lists['0'].append([str(datetime.now()), player.id, chat.message])

                else:
                    if chat.selected_recipient < player.id:
                        chat_lists[str(chat.selected_recipient) + str(player.id)].append([str(datetime.now()), player.id, chat.message])
                    else:
                        chat_lists[str(player.id) + str(chat.selected_recipient)].append([str(datetime.now()), player.id, chat.message])
                new_chat_row = [str(datetime.now()), player.id, chat.selected_recipient, chat.message]
                chat.message = ''
            chats[player_no] = chat

            conn.send(pickle.dumps((chat, player)))

        if data_type == "trade_classs":

            response_message = ''
            trade, player = pickle.loads(conn.recv(3*4096))
            # print("round_change_flag on trade", round_change_flag[str(player_no)], player_no)
            if round_change_flag[str(player_no)]['trade']:
                trade = Trade(player_no)
                trades[player_no] = Trade(player_no)
                round_change_flag[str(player_no)]['trade'] = 0

            # if round_change_flag[str(player_no)]['player']:
            #     player = Player(player_no+1)
            #     players[player_no] = Player(player_no+1)
            #     # print("special trade player grain", player.resources['Grain'], "player number is", player_no)
            #     # print("special trade player grain", players[player_no].resources['Grain'], "player number is", player_no)
            #     if fertility_orientation == 'EI':
            #         if round_constants['round_number'] >= 5:
            #             player.fertility = player.id * 10
            #             players[player_no].fertility = player.id * 10
            #     elif fertility_orientation == 'IE':
            #         if round_constants['round_number'] <=4:
            #             player.fertility = player.id * 10
            #             players[player_no].fertility = player.id * 10
            #     round_change_flag[str(player_no)]['player'] = 0

            if not trade:
                print("disconnected")
                break

            elif trade.trade_initiated:
                print("Player number ", player_no, "is trying to send ", trade.TryToTrade[0] - 1, ", ",
                      trade.TryToTrade[1], " of quantity ", trade.TryToTrade[2])
                trade.trade_initiated = False
                if player.resources[trade.TryToTrade[1]] >= trade.TryToTrade[2]:

                    player.resources[trade.TryToTrade[1]] -= trade.TryToTrade[2]
                    players[trade.TryToTrade[0]-1].resources[trade.TryToTrade[1]] += trade.TryToTrade[2]
                    players[player.id - 1] = player
                    trades_list.append([str(datetime.now()), player.id, trade.TryToTrade[0], trade.TryToTrade[1], trade.TryToTrade[2]])
                    print(trades_list)
                    response_message = "Success!!"

                else:
                    response_message = "You have insufficient " + str(trade.TryToTrade[1]) + "."

            if trade.buysell[0] > 0:
                if players[player_no].resources["Grain"] >= trade.buysell[0]*trade.stealtokenbuycost:
                    steals[player_no].numberofstealtokens += trade.buysell[0]
                    players[player_no].resource_change -= trade.buysell[0]*trade.stealtokenbuycost
                    trade.buysell[0] = 0

            elif trade.buysell[0] < 0:
                steals[player_no].numberofstealtokens += trade.buysell[0]
                players[player_no].resource_change -= trade.buysell[0]*trade.stealtokensellcost
                trade.buysell[0] = 0

            if trade.buysell[1] > 0:
                if player.resources["Grain"] >= trade.buysell[1] * trade.defencetokenbuycost:
                    steals[player_no].numberofdefencetokens += trade.buysell[1]
                    players[player_no].resource_change -= trade.buysell[1]*trade.defencetokenbuycost
                    trade.buysell[1] = 0

            elif trade.buysell[1] < 0:
                steals[player_no].numberofdefencetokens += trade.buysell[1]
                players[player_no].resource_change -= trade.buysell[1]*trade.defencetokensellcost
                trade.buysell[1] = 0

            player.resources['Grain'] += players[player_no].resource_change
            players[player_no].resource_change = 0
            conn.send(pickle.dumps((trade, player, response_message)))

        if data_type == "drag_class":
            draganddrop, player = pickle.loads(conn.recv(3*4096))
            # if player_no == 1:
            #     print("round_change_flag on drag class", round_change_flag[str(player_no)], player_no)
            if round_change_flag[str(player_no)]['drag']:
                draganddrop = DragDrop()
                draganddrops[player_no] = DragDrop()
                round_change_flag[str(player_no)]['drag'] = 0

                # player = Player(player_no+1)
                # players[player_no] = Player(player_no+1)
                # # if player_no == 1:
                #     # print("special drag player grain", player.resources['Grain'], "player number is", player_no)
                #     # print("special drag player grain", players[player_no].resources['Grain'], "player number is", player_no)
                # if fertility_orientation == 'EI':
                #     if round_constants['round_number'] >= 5:
                #         player.fertility = player.id * 10
                #         players[player_no].fertility = player.id * 10
                # elif fertility_orientation == 'IE':
                #     if round_constants['round_number'] <=4:
                #         player.fertility = player.id * 10
                #         players[player_no].fertility = player.id * 10
                # round_change_flag[str(player_no)]['player'] = 0
            # print("drag player grain", player.resources['Grain'], "for player_no", player_no)
            # print("player.fertility of", player_no, "is", player.fertility)
            try:
                draganddrop.log_last_message = [str(police_log[-1][0]), str(police_log[-1][1]), str(police_log[-1][2])]
            except:
                draganddrop.log_last_message = []

            player.resources["Grain"] = players[player_no].resources["Grain"]
            #print(draganddrop.score)
            if not draganddrop:
                print("disconnected")
                break
            else:
                if draganddrop.stage == 5:
                    players[player_no].resource_change += player.fertility
                    draganddrop.stage = 0
                    draganddrop.score = [0,0,0,0,0]
                players[player_no].resources["Grain"] = max(0, player.resources['Grain'] + players[player_no].resource_change)
                player.resources['Grain'] = max(0, player.resources['Grain'] + players[player_no].resource_change)
                players[player_no].resource_change = 0

                conn.send(pickle.dumps((draganddrop, player)))

        if data_type == "steal_class":
            steal, player = pickle.loads(conn.recv(100*4096))

            if round_change_flag[str(player_no)]['steal']:
                steal = Steal(player.id)
                steals[player_no] = Steal(player.id)
                steals[player_no].ranking = ranking()
                round_change_flag[str(player_no)]['steal'] = 0

            # if round_change_flag[str(player_no)]['player']:
            #     player = Player(player_no+1)
            #     players[player_no] = Player(player_no+1)
            #     # if player_no == 1:
            #         # print("special steal player grain", player.resources['Grain'], "player number is", player_no)
            #         # print("special steal player grain", players[player_no].resources['Grain'], "player number is", player_no)
            #     if fertility_orientation == 'EI':
            #         if round_constants['round_number'] >= 5:
            #             player.fertility = player.id * 10
            #             players[player_no].fertility = player.id * 10
            #     elif fertility_orientation == 'IE':
            #         if round_constants['round_number'] <=4:
            #             player.fertility = player.id * 10
            #             players[player_no].fertility = player.id * 10
            #
            #     round_change_flag[str(player_no)]['player'] = 0

            player.update_stealing_from_count(steal.numberofstealtokens - len(player.stealing_from))
            global updater, tokens_allocated
            for update in updater:
                try:
                    if update[0] == player.id:
                        steal.initialize_steal_token(update[1], "myserver place 1")
                        update[0] = 0
                except:
                    pass
            updater = [i for i in updater if i[0] != 0]
            if player.type == 2:
                tokens_allocated = len(steal.recPunishment.collidelistall(steal.recDefenceTokens))
            steal.ranking = steals[player_no].ranking

            players[player_no].resources["Grain"] = max(0, player.resources['Grain'] + players[player_no].resource_change)
            player.resources['Grain'] = max(0, player.resources['Grain'] + players[player_no].resource_change)
            players[player_no].resource_change = 0
            if not steal:
                print("disconnected")
                break
            else:

                for i in range(steal.numberofstealtokens):

                    if player.stealing_from[i]:
                        #print("reached first if")
                        if steal.stealoclock[i]:
                            #print("reached 2 if")
                            # if players[player.stealing_from[i]-1].connected:
                                #print(player.stealing_from[i]-1)
                                #print("reached 3 if")
                                if players[player.stealing_from[i]-1].resources["Grain"]:
                                    players[player_no].resource_change += player.stealing_amount_per_30th_of_a_second
                                    players[player.stealing_from[i]-1].resource_change -= player.stealing_amount_per_30th_of_a_second
                                # else:
                                #     steal.initialize_steal_token(i, "myserver place 2")
                                # print("player "+ str(player.id) +" has ", str(player.resources["Grain"]) + ". He is stealing from player " + str(player.stealing_from[i]) + ". Victim now has "+ str(players[player.stealing_from[i]-1].resources["Grain"]))
                                steal.stealoclock[i] = 0

                all_defences[player.id] = [pygame.rect.Rect(i[0], i[1], steal.defencetokensize[0], steal.defencetokensize[1]) for i in steal.defence_coordinates if i != steal.defencetokenstartcoordinates]
                all_steals[player.id] = [(i[0], i[1], player.stealing_from[steal.steal_coordinates.index(i)]) for i in steal.steal_coordinates]
                # print(all_steals, updater)


                if steal.detectoclockD:
                    print("D=", steal.detectoclockD)
                    steal.detectoclockD = 0
                    for j in all_steals.keys():  # see all players steal tokens
                        if j != player.id:  # except the players own
                            for stoken_no, stoken in enumerate(all_steals[
                                                                   j]):  # in which steal token number = stoken_no  and  stoken is the steal token itself
                                for defence_no, defence in enumerate(all_defences[player.id]):  # get players own
                                    if defence.collidepoint((stoken[0], stoken[1])):
                                        print("player ", j, "was found stealing from", stoken[2])

                                        # print(stoken_no)
                                        punished = punishment(j, stoken[2], 1)
                                        print("punished up", punished)
                                        players[punished-1].resource_change -= 17
                                        players[0].resource_change += 25
                                        if punished != j:
                                            if np.random.randint(low=1, high=100, size=1)[0]>30:
                                                players[0].resource_change -= 15
                                        # chosen = my_punishment(j, stoken[2])
                                        tell_the_officer_data_store_punishment[defence_no] = [j, stoken_no, punished, "reprimanded"]
                                        if punished:
                                            police_log.append([datetime.now().strftime("%H:%M:%S %p"), punished, stoken[2]])
                                        # my_punishment(j, stoken[2])
                                        updater.append([j, stoken_no])

                data_store_punishment = ['NA' for i in range(steals[0].numberofdefencetokens)]
                if player.type == 2:
                    data_store_punishment = tell_the_officer_data_store_punishment
                    tell_the_officer_data_store_punishment = ['NA' for i in range(steal.numberofdefencetokens)]
                if steal.detectoclockS:
                    print("S=", steal.detectoclockS)
                    steal.detectoclockS = 0
                    for i in all_defences.keys():  # all_defences has keys and values as player.id:rects made from deence coordinates
                        if i != player.id:  # we dont want to check the player's own defences matching with his steal tokens
                            for defence_no, defence in enumerate(all_defences[i]):  # check all the defence rects in one of the values
                                for coords_no, coords in enumerate(all_steals[
                                                                       player.id]):  # coords_no is which steal token it is, and coords are the steal token coords.
                                    if defence.collidepoint((coords[0], coords[
                                        1])):  # if defence rect collides with player's steal token and not found anything before
                                        print("Player ", player.id, "was found stealing from ", coords[2])

                                        punished = punishment(player.id, coords[2], 1)
                                        print("punished", punished)
                                        players[punished-1].resource_change -= 17
                                        # chosen = my_punishment(player.id, coords[2])
                                        players[0].resource_change += 25
                                        if punished != player.id:
                                            if np.random.randint(low=1, high=100, size=1)[0]>30:
                                                players[0].resource_change -= 15
                                        print("defence_no ===== ", defence_no)
                                        data_store_punishment[defence_no] = [player.id, coords_no, punished, "reprimanded"]
                                        if punished:
                                            police_log.append([datetime.now().strftime(
                                                "%H:%M:%S %p"), punished, coords[2]])
                                        # my_punishment(player.id, coords[2])
                                        steal.caught[coords_no] = [1, defence_no]
                                        steal.initialize_steal_token(coords_no, "myserver place 3")

                try:
                    punished = punished if punished else 0
                except:
                    punished = 0

                steal.numberofstealtokens = steals[player_no].numberofstealtokens
                steal.numberofdefencetokens = steals[player_no].numberofdefencetokens
                steal.update_token_count()
                player.update_stealing_from_count(steal.numberofstealtokens-len(player.stealing_from))
                players[player_no].stealing_from = player.stealing_from
                steal.P_innocent, steal.P_culprit = probability()
                # players[player_no].resources["Grain"] = player.resources["Grain"] ##############################################################################################################
                steals[player_no] = steal

                conn.send(pickle.dumps((steal, player, police_log, punished, data_store_punishment)))
            # Write data to file
            # if len(new_chat_row):
            #     with open('chats.csv', 'a', newline='') as csvfile:
            #         chatwriter = csv.writer(csvfile, delimiter=',',
            #                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #         chatwriter.writerow(new_chat_row)
            #         print(new_chat_row)
            #         new_chat_row = []

            # file = open(r'C:\Users\Shantanu\PycharmProjects\desipun\venv\storage\important'+str(frame_number), 'wb')
            # dump information to that file
            # pickle.dump((players, draganddrops, steals, trades, all_defences, all_steals, trades_list), file)
            # close the file
            # file.close()



            #except:
                #print("break at except")
                #break
    print("lost connection")
    player_no -= 1
    conn.close()

while True:
    conn, adr = s.accept()
    print("Connected to ", adr)
    player_no += 1
    start_new_thread(threaded_client, (conn, player_no))











