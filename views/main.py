import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.battle import *
from game.game import Game
from helpers.const import *
from models.user_registration import UserRegistrationDTO

game = Game()

while True:
    try:
        status = int(input(Register_menu))
    except:
        print("Ошибка ввода")
    match(status):
        case 1:
            nickname = input('Введите никнэйм: ')
            login = input('Введите логин: ')
            password = input('Введите пророль: ')
            first_name = input('Введите своё имя: ')
            data = UserRegistrationDTO(nickname, login, password, first_name)
            print(game.register(data))
        case 2:
            login = input('Введите логин: ')
            password = input('Введите пророль: ')
            print(game.login(login, password))
        case 3:
            print(game.delete_user())
        case 4:
            if game.verification():
                while True:
                    try:
                        n = int(input(Game_menu))
                    except:
                        print("Ошибка ввода")
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
                            input('Вы уверены, что хотите выйти?\n1 - ДА\n2 - НЕТ')
                            if int(input()) == 1:
                                break
                        case _:
                            print('Некорректный ввод, попробуйте ещё раз')
            else:
                print('Вы не вошли в аккаунт')
        case 5:
            print(*game.get_current_user())
        case 6:
            for users in game.get_all_users():
                for user in users:
                    print(user)
                    print('_' * 10)
        case 0:
            pass
        case _:
            print('Некорректный ввод, попробуйте ещё раз')
