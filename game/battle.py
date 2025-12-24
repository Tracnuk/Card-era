import sys
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from game.game import Game
from models.batle_data import Data
from models.area import Area

class Battle:
    def __init__(self):
        self.deck_of_cards = game.import_deck_of_cards()
        self.activ_cards = []
        self.activ_cards = []
        self.user_wasted_energy = 0
        self.enemy_wasted_energy = 0
        self.user_energy = 2
        self.enemy_energy = 2
        self.enemy_hp = 40
        self.user_hp = 40
        self.area = [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]

    def get_battle_data(self):
        return [self.area, self.activ_cards,
                self.user_energy,
                self.enemy_energy,
                self.user_energy - self.user_wasted_energy,
                self.enemy_energy - self.enemy_wasted_energy,
                self.enemy_hp, self.user_hp]
        
    def attak_cards(self):
        for position in range(5):
            user_card = area[1][position]
            enemy_card = area[0][position]
            if user_card == None and enemy_card == None:
                pass
            elif user_card == None:
                self.user_hp -= enemy_card.damage
            elif enemy_card == None:
                self.enemy_hp -= user_card.damage
            else:
                user_card.hp -= enemy_card.damage
                enemy_card.hp -= user_card.damage
            if enemy_card.hp <= 0:
                del self.area[0][position]
            if user_card.hp <= 0:
                del self.area[1][position]
            self.enemy_energy += 1
            self.user_energy += 1
                
    def plant_card(self, position, nam):
        if self.activ_cards[nam] == None:
            return "Выбрана несуществующяя карта"
        elif self.area[1][position] != None:
            return "Поле занято"
        elif self.activ_cards[nam].energy  + self.user_wasted_energy > self.user_energy:
            return "Нехвотает энергии"
        self.user_wasted_energy += self.activ_cards[nam].energy
        self.area[1][position] = self.activ_cards.pop(nam)
        return None

    def giv_activ_cards(self, count):
        for _ in range(count):
            self.activ_cards.append(deck_of_cards[random.randint(0, 4)])
