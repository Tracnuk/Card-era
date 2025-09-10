from Game import Game
from const import *
from user_regestration import UserRegistrationDTO

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
            
        case 3:
            
        case 0:
            