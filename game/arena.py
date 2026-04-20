import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.battle import Battle

class Arena:
    def __init__(self):
        self.leave = False
        self.battle = Battle()
        self.battle.giv_activ_cards(1, 1)
        return battle.get_battle_data()
    
    def status_action(self, status, position_in_activ_cards, position_in_field):
        match(status):
            case 1:
                battle_data = self.battle.plant_player_card(position_in_activ_cards,
                                                   position_in_field)
            case 2:
                # ход бота
                battle_data = battle.attak_cards()
            case 3:
                self.leave = True
        return (battle_data, self.leave)
