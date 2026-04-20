import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.dekc import Deck

class SettingsServise():
    def add_cards_in_settings(self, account_id):
        cards = []
        for card_id in range(1, 6):
            cards.append(cards_db_storage.get_card_by_id(card_id)[0])
        settings_db_storage.add_cards_id(account_id, Deck(cards[0], cards[1], cards[2], cards[3], cards[4])) 
        
    def get_settings_by_id(self, account_id):
        return get_settings_by_id(account_id)

    def update_cards(card1, card2, card3, card4, card5):
        update_cards(Deck(card1, card2, card3, card4, card5), account_id)

    def import_deck_of_cards(self, current_account_id):
        return settings_db_storage.get_settings_by_id(current_account_id)
