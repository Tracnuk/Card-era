import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.battle import *
from helpers.const import *

while True:
    n = int(input(Game_menu))
    match(n):
        case 1:
            arena()
        case 2:
            inventory()
        case 3:
            settings()
        case 4:
            shop()
        case 0:
            input('Вы уверены, что хотите выйти?) \n1 - ДА\n2 - НЕТ')
            if int(input()) == 1:
                break
        case _:
            print('Некорректный ввод, попробуйте ещё раз')