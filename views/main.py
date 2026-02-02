import sys
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game import Game
from helpers.const import *
from models.user_registration import UserRegistrationDTO

game = Game()
flag_register = False
flag_exit_menu = False
while not flag_exit_menu:
    try:
        menu_status = int(input(Register_menu))
        match(menu_status):
            case 1:
                nickname = input('Введите никнэйм: ')
                login = input('Введите логин: ')
                password = input('Введите пророль: ')
                first_name = input('Введите своё имя: ')
                data = UserRegistrationDTO(nickname, login, password, first_name)
                query_result = game.register(data)
                flag_register = query_result[0]
                print(query_result[1])
            case 2:
                login = input('Введите логин: ')
                password = input('Введите пророль: ')
                print(game.login(login, password))
            case 3:
                print(game.delete_user())
            case 4:
                if flag_register:
                    flag_exit_game = False
                    while not flag_exit_game:
                        try:
                            status = int(input(Register_menu))
                            match(status):
                                flag_exit_buttle = False
                                case 1: #битва
                                    while not flag_exit_battle:
                                        try:
                                            battle_status = int(input())
                                            if battle_status == 1:
                                                position_in_activ_cards = int(input())
                                                position_in_fiel = int(input())
                                                
                                            else:
                                                
                                        except:
                                            print("Ошибка ввода")
                                case 2: #магазин
                                    pass
                                case 3: #инвентарь
                                    pass
                                case 4:
                                    flag_exit_game = True
                        except:
                            print("Ошибка ввода")
            case 5:
                print(*game.get_current_user())
            case 6:
                for users in game.get_all_users():
                    for user in users:
                        print(user)
                        print('_' * 10)
            case 0:
                print('\nДо свидания!')
                flag_exit_menu = True
            case _:
                print('Некорректный ввод, попробуйте ещё раз')
    except:
        print("Ошибка ввода")
