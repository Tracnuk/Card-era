import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.battle import Battle

class arena:
    def __init__(self):
        self.leave = False
        battle = Battle()
        battle.giv_activ_cards(1)
        return battle.get_battle_data()
    
    def batle(self, status):
        massage = ''
        match(status):
            case 1:
                massage = battle.plant_player_card(int(input()), int(input()))
            case 2:
                # ход бота
                battle.attak_cards()
            case 3:
                self.leave = True
        return (butle.get_battle_data(), self.leave, massage)
