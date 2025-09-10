from ..game.battle import *


while True:
    n = int(input('1 - Выйти на арену\n2 - Войти в инвентарь\n3 - Настройки аккаунта\тВыберете один из пунктов'))
    if n == 1:
        buttle()
    elif n == 2:
        inventory()
    elif n == 3:
        settings()
    elif n == 4:
        print('Досидания!')
        break
    else:
        print('Команда не распознана')
