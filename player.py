import pygame

class Player():
    def __init__(self, id):
        self.type = 0
        self.connected = 0
        self.id = id
        self.resources = {"Grain" : 0}
        self.stealing_from = []

    def update_stealing_from_count(self, n):
        if n>0:
            for i in range(n):
                self.stealing_from.append(0)
        elif n<0:
            self.stealing_from = self.stealing_from[:n]
