import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.settings_db_repository import SettingsDbRepository
from models.deck import Deck

settings_db_storage = SettingsDbRepository()

class SettingsService:
    def add_cards_in_settings(account_id):
        cards = list(range(1, 6))
        settings_db_storage.add_cards_id(account_id, Deck(cards[0], cards[1], cards[2], cards[3], cards[4])) 
        
    def get_settings_by_id(account_id):
        return settings_db_storage.get_settings_by_id(account_id)

    def update_cards(card1, card2, card3, card4, card5):
        settings_db_storage.update_cards(account_id, Deck(card1, card2, card3, card4, card5))

    def delete_settings(account_id):
        settings_db_storage.delete_cards(account_id)
