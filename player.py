import pygame

class Player():
    def __init__(self, id):
        self.type = 0
        self.experiment_start_time = 0
        self.id = id
        self.resources = {"Grain" : 100}
        self.stealing_from = []
        self.fertility = 10
        self.fertility_orientation = ''
        self.stealing_amount_per_30th_of_a_second = 0.1
        self.stealing_fine = 0
        self.enforcer_number_of_defence_tokens = 0

    def update_stealing_from_count(self, n):
        if n>0:
            for i in range(n):
                self.stealing_from.append(0)
        elif n<0:
            self.stealing_from = self.stealing_from[:n]

    def update_fertility(self, round_number):
        print("the two fertility things are", self.fertility_orientation,"and", self.fertility)
        if self.fertility_orientation[0].startswith('I'):
            if round_number<5:
                self.fertility = 10 * self.id
        if self.fertility_orientation[0] == 'E':
            if round_number>4:
                self.fertility = 10 * self.id