from ..game.game import Game
from ..helpers.const import *
from ..helpers.user_regestration import UserRegistrationDTO

game = Game()

while True:
    status = int(input(menu))
    match(status):
        case 1:
            nickname = input('Введите никнэйм: ')
            login = input('Введите логин: ')
            password = input('Введите пророль: ')
            first_name = input('Введите своё имя: ')
            data = UserRegistrationDTO(nickname, login, password, first_name)
            game.register(data)
        case 2:
            pass
        case 3:
            pass
        case 0:
            pass