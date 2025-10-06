import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.card_service import *

cards = CardService()

while True:
    n = int(input('1-создание\n2-удаление\n3-обновление\n4-по id\n5-получить все\n'))
    print()
    match(n):
        case 1:
            rarty = input('Редкость: ')
            type_card = input('Тип: ')
            name = input('Имя: ')
            count = input('Сила: ')
            hp = input('Здоровье: ')
            damage = input('Урон: ')
            price = input('Цена: ')
            link_of_picture = input('Картинка: ')
            cards.create_card(rarty, type_card, name, count, hp, damage, price, link_of_picture)
            print()
        case 2:
            print(cards.delete_card(input('id: ')))
            print()
        case 3:
            card_id = input('id: ')
            rarty = input('Редкость: ')
            type_card = input('Тип: ')
            name = input('Имя: ')
            count = input('Сила: ')
            hp = input('Здоровье: ')
            damage = input('Урон: ')
            price = input('Цена: ')
            link_of_picture = input('Картинка: ')
            print(cards.update_card(card_id, rarty, type_card, name, count, hp, damage, price, link_of_picture), '\n')
        case 4:
            print(cards.get_card_by_id(input('id: ')), '\n')
        case 5:
            for card_object in cards.get_all_cards():
                print(card_object)
            print()
        case 0:
            break
        case _:
            print('Некорректный ввод')
