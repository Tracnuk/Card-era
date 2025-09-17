import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game import Game
from helpers.const import *
from models.user_registration import UserRegistrationDTO

game = Game()

while True:
    status = int(input(Register_menu))
    match(status):
        case 1:
            nickname = input('Введите никнэйм: ')
            login = input('Введите логин: ')
            password = input('Введите пророль: ')
            first_name = input('Введите своё имя: ')
            data = UserRegistrationDTO(nickname, login, password, first_name)
            print(game.register(data))
        case 2:
            pass
        case 3:
            pass
        case 4:
            print(game.get_user())
        case 0:
            pass
