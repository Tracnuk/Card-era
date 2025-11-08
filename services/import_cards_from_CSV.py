import csv
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.card_db_repository import CardDbRepository
from models.card import Card

card_db_storage = CardDbRepository()

class ImportCSVService:
    def import_data(self):
        with open('cards.csv', mode='r', newline='') as csv_file:  
            card_list = csv.reader(csv_file)
            next(card_list)
            for card in card_list:
                card_object = Card(rarity = card[0],
                               card_type = card[1],
                               name = card[2],
                               count = card[3],
                               hp = card[4],
                               damage = card[5],
                               energy = card[6],
                               price = card[7],
                               link_of_picture = card[8])
                card_db_storage.add_card(card)
    
