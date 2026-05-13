import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.battle import Battle

class Arena:
    def __init__(self, player_deck, enemy_deck):
        self.battle = Battle(player_deck, enemy_deck)
        self.battle.giv_activ_cards(1, 1)
        self.battle_data = self.battle.get_battle_data()
        self.player_turn = True
    
    def status_action(self, status, position_in_activ_cards, position_in_field):
        if self.player_turn:
            match(status):
                case 1:
                    battle_data = self.battle.player_plant_card(position_in_activ_cards, position_in_field)
                case 2:
                    self.player_turn = False
        else:
            while not self.player_turn:
                enemy_data, self.player_turn = buttle.enemy.enemy_move(self.battle_data)
                self.battle_data = self.battle.enemy_plant_card(enemy_data[1], enemy_data[0])
        return self.battle_data

    def start_buttle(self):
        return self.battle_data
