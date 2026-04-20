import sys
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game import Game
from helpers.const import *
from models.user_registration import UserRegistrationDTO

game = Game()
flag_registration_auntification = False
while not flag_exit_menu:
    try:
        menu_status = int(input(Register_menu))
        while not flag_registration_auntification:
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
                    flag_registration_auntification = True
                case 2:
                    login = input('Введите логин: ')
                    password = input('Введите пророль: ')
                    print(game.authentication(login, password))
                    flag_registration_auntification = True
                case 0:
                    print('\nДо свидания!')
                    flag_registration_auntification = True
                case _:
                    print('Некорректный ввод, попробуйте ещё раз')
                    flag_registration_auntification = True
                    flag_exit_game = True
        menu_status = int(input(Main_menu))
        if not flag_exit_game:
            match(menu_status):
                case 1:
                    flag_exit_game = False
                    while not flag_exit_game:
                        try:
                            status = int(input(Register_menu))
                            match(status):
                                flag_exit_buttle = False
                                case 1: #битва
                                    while not flag_exit_battle:
                                        battle_status = int(input())
                                        match battle_status:# Прочитать и доделать
                                            case 1: # установить карту
                                                position_in_activ_cards = int(input())
                                                position_in_field = int(input())
                                                game_data = game.get_battle_next_step(battle_status, position_in_activ_cards, position_in_field)
                                            case 2: # закончить ход
                                                game_data = game.get_battle_next_step(battle_status)
                                            case 3: # выйти
                                                flag_exit_battle = True
                                case 2: #магазин
                                    pass
                                case 3: #инвентарь
                                    pass
                                case 4:
                                    flag_exit_game = True
                        except:
                            print("Ошибка ввода")
                case 2: #сделать обновление данных пользователя
                    
                case 3:
                    print(game.delete_user())
                case 4:
                    print(*game.get_current_user())
                case 5:
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
