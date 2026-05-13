import sys
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game import Game
from helpers.const import *
from models.user_registration import UserRegistrationDTO

game = Game()
flag_registration_authentication = False
flag_exit_menu = False

while not flag_exit_menu:
    while not flag_registration_authentication:
        #try:
        menu_status = int(input(Register_menu))
        match menu_status:
            case 1:
                nickname = input('Введите никнейм: ')
                login = input('Введите логин: ')
                password = input('Введите пароль: ')
                first_name = input('Введите своё имя: ')
                data = UserRegistrationDTO(nickname, login, password, first_name)
                query_result = game.register(data)
                if isinstance(query_result, int):
                    print('\nВы создали аккаунт!\n')
                    flag_registration_authentication = True
                else:
                    print(query_result)
            case 2:
                login = input('Введите логин: ')
                password = input('Введите пароль: ')
                answer = game.authentication(login, password)
                print(answer[0])
                if answer[1]:
                    flag_registration_authentication = True
            case 0:
                print('\nДо свидания!')
                flag_registration_authentication = True
                flag_exit_menu = True
            case _:
                print('Некорректный ввод!')
        '''except ValueError:
            print("Ошибка ввода: введите число!")
        except Exception as e:
            print(f"Ошибка регистрации: {str(e)}")'''
    if (not flag_exit_menu) and game.verification():  # проверка авторизации перед основным меню
        menu_status = int(input(Main_menu))
        match menu_status:
            case 1:  # игра
                flag_exit_game = False
                while not flag_exit_game:
                    #try:
                    status = int(input(Game_menu))
                    match status:
                        case 1:  # начать битву
                            game_data = game.start_battle()
                            print('', '□ ' * 5, '\n', '□ ' * 5, '\n' * 2,
                                  *list(map(lambda x: '□' if x == None else x, game_data.player_data.activ_cards)), '\n',
                                  game_data.player_data.hp, game_data.remaining_player_energy)
                            flag_exit_battle = False
                            while not flag_exit_battle:
                                #try:
                                battle_status = int(input(Buttle_menu))
                                match battle_status:
                                    case 1:  # установить карту
                                        position_in_activ_cards = int(input("Позиция в активных картах: ")) - 1
                                        position_in_field = int(input("Позиция на поле: ")) - 1
                                        game_data = game.get_battle_next_step(battle_status, position_in_field, position_in_activ_cards)
                                    case 2:  # закончить ход
                                        game_data = game.get_battle_next_step(battle_status)
                                    case 3:  # выйти из битвы
                                        flag_exit_battle = True
                                    case _:
                                        print('Некорректный ввод!')
                                print('', *list(map(lambda x: '□' if x == None else x, game_data.enemy_area)), '\n',
                                      *list(map(lambda x: '□' if x == None else x, game_data.player_area)), '\n',
                                      *list(map(lambda x: '□' if x == None else x, game_data.player_data.activ_cards)), '\n',
                                      game_data.player_data.hp, game_data.remaining_player_energy)
                                '''except ValueError:
                                    print("Ошибка ввода: введите число!")
                                except Exception as e:
                                    print(f"Ошибка битвы: {str(e)}")'''
                        case 2:  # магазин
                            print("Магазин пока не реализован.")
                        case 3:  # инвентарь
                            print("Инвентарь пока не реализован.")
                        case 0:  # выход из игры
                            flag_exit_game = True
                        case _:
                            print('Некорректный ввод!')
                    '''except ValueError:
                        print("Ошибка ввода: введите число!")
                    except Exception as e:
                        print(f"Ошибка в меню битвы: {str(e)}")'''
            case 2:  # обновление данных пользователя
                nickname = input('Введите новый никнейм: ')
                login = input('Введите новый логин: ')
                password = input('Введите новый пароль: ')
                first_name = input('Введите новое имя: ')
                surname = input('Введите фамилию: ') or ''
                last_name = input('Введите отчество: ') or ''
                email = input('Введите свою почту: ') or ''
                phone_number = input('Введите номер телефона: ') or ''

                # Обновляем аккаунт
                account_result = game.update_account(nickname, login, password)
                print(account_result)

                # Обновляем пользовательские данные
                person_result = game.update_person(first_name, surname, last_name, email, phone_number)
                print(person_result)
            case 3:  # удаление пользователя
                confirm = input("Вы уверены, что хотите удалить аккаунт? (да/нет): ")
                if confirm.lower() == 'да':
                    delete_result = game.delete_user()
                    print('\n' + delete_result + '\n')
                    flag_registration_authentication = False
            case 4:  # просмотр текущего пользователя
                current_user = game.get_current_user()
                if current_user[0] and current_user[1]:
                    print("Аккаунт:", current_user[0])
                    print("Персональные данные:", current_user[1])
                else:
                    print("Нет авторизованного пользователя.")
            case 5:  # просмотр всех пользователей
                all_users = game.get_all_users()
                persons, accounts = all_users
                print("\n--- Все пользователи ---")
                for i, (person, account) in enumerate(zip(persons, accounts), 1):
                    print(f"{i}. Персональные данные: {person}, Аккаунт: {account}")
                    print('-' * 30)
            case 0:  # выход
                print('\nДо свидания!')
                flag_exit_menu = True
            case _:
                print('Некорректный ввод!')
    elif not flag_exit_menu:
        print("Необходимо авторизоваться перед использованием основного меню!")
