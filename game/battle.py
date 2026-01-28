import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.player import Player
from models.enemy import Enemy

class Battle:
    def __init__(self):
        self.player_deck = game.import_deck_of_cards()
        self.enemy_deck = game.import_deck_of_cards()
        self.player = Player()
        self.enemy = Enemy()
        self.player_area = [0, 0, 0, 0, 0]
        self.enemy_area = [0, 0, 0, 0, 0]

    def check_result_buttle(self):
        result = [False, False] 
        if player.hp <= 0:
            result[0] = True
        elif enemy.hp <= 0:
            result[1] = True
        return result
    
    def get_battle_data(self):
        return {'player_area': self.player_area,
                'enemy_area': self.enemy_area,
                'player_activ_cards': self.player.activ_cards,
                'player_energy': self.player.energy,
                'enemy_energy': self.enemy.energy,
                'remaining_player_energy': self.player.energy - self.player.wasted_energy,
                'remaining_enemy_energy': self.enemy.energy - self.enemy.wasted_energy,
                'enemy_hp': self.enemy.hp,
                'player_hp': self.player.hp}

    def attak_cards(self):
        for position in range(5):
            player_card = self.player_area[position]
            enemy_card = self.enemy_area[position]
            if player_card == None and enemy_card == None:
                pass
            elif player_card == None:
                player.hp -= enemy_card.damage
            elif enemy_card == None:
                enemy.hp -= player_card.damage
            else:
                player_card.hp -= enemy_card.damage
                enemy_card.hp -= player_card.damage
            if enemy_card.hp <= 0:
                del self.enemy_area[position]
            if player_card.hp <= 0:
                del self.player_area[position]

    def player_plant_card(self, position, nam):
        if self.player.activ_cards[nam] == None:
            return "Выбрана несуществующяя карта"
        elif self.player.area[position] != None:
            return "Поле занято"
        elif self.player.activ_cards[nam].energy  + self.player.wasted_energy > self.player.energy:
            return "Нехвотает энергии"
        self.player.wasted_energy += self.player.activ_cards[nam].energy
        self.player.area[position] = self.player.activ_cards.pop(nam)
        return None

    def enemy_plant_card(self, position, nam):
        self.enemy.wasted_energy += self.enemy.activ_cards[nam].energy
        self.enemy.area[position] = self.enemy.activ_cards.pop(nam)
        
    def giv_activ_cards(self, count_p, count_e):
        for _ in range(count_p):
            self.player.activ_cards.append(self.player_deck[random.randint(0, 4)])
        for _ in range(count_e):
            self.enemy.activ_cards.append(self.enemy_deck[random.randint(0, 4)])
