import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.card_db_repository import CardDbRepository
from models.card import Card

card_db_storage = CardDbRepository()

class cardService:
    def create_card(self, rarty, type_card, name, count, price, link_of_picture):
        card = Card(rarty, card_type, name, count, price, link_of_picture)
        card_db_storage.add_card(card)
        
    def delete_card(self, card_id):
        card_db_storage.delete_card(card_id)
        return 'Карта была удалена.'

    def update_card(self, card_id, rarity, type_card, name, count, price, link_of_picture):
        card_db_storage.update_card(card_id, new_first_name, new_surname, new_last_name, new_email, new_phone_number, account_id)
        return 'Данные обновлены.'
    
    def get_card_by_id(self, card_id=None):
        return card_db_storage.get_card_by_id(card_id)
            
    def get_all_cards(self):
        result = card_db_storage.get_cards()
        if result and len(result) > 0:
            card = [card(card_id = data[0],
            rarity = data[1],
            type_card = data[2],
            count = data[3],
            price = data[4],
            link_of_picture = data[5]) for data in result]
            return card
        return ['Нет данных']
