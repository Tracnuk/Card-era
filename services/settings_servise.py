
class Settings_servise():
    def __init__(self)
        
        
    def add_cards_in_settings(self, account_id):
        cards = []
        for card_id in range(1, 6):
            cards.append(cards_db_storage.get_card_by_id(card_id)[0])
        settings_db_storage.add_cards_id(account_id,
                                         cards[0],
                                         cards[1],
                                         cards[2],
                                         cards[3],
                                         cards[4])
        
    def get_settings_by_id(self, account_id):
        
