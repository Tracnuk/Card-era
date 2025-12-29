import sys
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game import Game

#energy = 0
hp = 40

area = [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]

class Battle:
    def __init__(self):
        self.deck_of_cards = Game.import_deck_of_cards()[1:]
        self.activ_cards = []

    def get_battle_data(self):
        return [area, self.activ_cards]
        
    def attak_card(self):
        pass

    def plant_card(self, position, nam):
        if self.activ_cards[nam] == None:
            return "Выбрана несуществующяя карта"
        elif area[1][position] != None:
            return "Поле занято"
        area[1][position] = self.activ_cards.pop[nam]
        return None
    
    def get_cards_in_hand(self):
        return

    def giv_activ_cards(self, count):
        for _ in range(count):
            self.activ_cards.append(deck_of_cards[random.randint(0, 4)])
