import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import random
from game.battle import *

move = random.randint(0, 1)
user_energy = 1
enemy_energy = 1
enemy_cards = []
user_cards = []
while True:
    if move:
        print(*enemy_cards)
        print(*user_cards)
    else:
        pass
    move = 0 if move else 1 
