import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.player_DTO import Player
from models.enemy import Enemy
from models.battle_status import BattleStatus

class Battle:
    def __init__(self, player_deck, enemy_deck):
        enemy = Enemy(enemy_deck)
        player = Player(player_deck)
        self.battle = BattleStatus(player, player.energy, 
                                   enemy, enemy.energy)

'''    def check_result_buttle(self):
        result = (False, False) 
        if player.hp <= 0:
            result[0] = True
        elif enemy.hp <= 0:
            result[1] = True
        return result'''

    def attak_cards(self):
        for position in range(5):
            player_card = self.battle.player_area[position]
            enemy_card = self.battle.enemy_area[position]
            if player_card == None and enemy_card == None:
                pass
            elif player_card == None:
                self.battle.player_data.hp -= enemy_card.damage
                if self.battle.player_data.hp <= 0:
                    
            elif enemy_card == None:
                self.battle.enemy_data.hp -= player_card.damage
                if self.battle.enemy_data.hp <= 0:
                    
            else:
                player_card.hp -= enemy_card.damage
                enemy_card.hp -= player_card.damage
            if enemy_card.hp <= 0:
                del self.enemy_area[position]
            if player_card.hp <= 0:
                del self.player_area[position]
        return self.battle

    def player_plant_card(self, position_in_field, position_in_activ_cards):
        if self.player.activ_cards[position_in_activ_cards] == None:
            return "Выбрана несуществующяя карта"
        elif self.player.area[position_in_field] != None:
            return "Поле занято"
        elif self.player.activ_cards[position_in_activ_cards].energy  + self.player.wasted_energy > self.player.energy:
            return "Нехвотает энергии"
        self.player.wasted_energy += self.player.activ_cards[position_in_activ_cards].energy
        self.player.area[position_in_field] = self.player.activ_cards.pop(position_in_activ_cards)
        return self.battle

    def enemy_plant_card(self, position_in_field, position_in_activ_cards):
        self.enemy.wasted_energy += self.enemy.activ_cards[position_in_activ_cards].energy
        self.enemy.area[position_in_field] = self.enemy.activ_cards.pop(position_in_activ_cards)
        
    def giv_activ_cards(self, count_player_cards, count_enemy_cards):
        for _ in range(count_player_cards):
            self.player.activ_cards.append(self.player_deck[random.randint(0, 4)])
        for _ in range(count_enemy_cards):
            self.enemy.activ_cards.append(self.enemy_deck[random.randint(0, 4)])
