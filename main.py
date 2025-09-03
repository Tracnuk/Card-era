from Game import Game
from const import *

game = Game()

while True:
    status = int(input(menu))
    match(status):
        case 1:
            nickname = input('Введите никнэйм: ')
            login = input('Введите логин: ')
            password = input('Введите пророль: ')
            first_name = input('Введите своё имя: ')
            data = {'nickname': nickname, 'login': login, 'password': password, 'firt_name': first_name}
            game.(data)
        case 2:
            
        case 3:
            
        case 0:
            
