class Area:
    def __init__(self):
        self.user_activ_cards = []
        self.enemy_activ_cards = []
        
    def get_all(self):
        return {'user_activ_cards':self.user_place, 'enemy_activ_cards':self.enemy_place}

    def set_activ_user_card(self, card_id):
        self.user_activ_cards.append(card_id) 

    def set_activ_enemy_card(self, card_id):
        self.enemy_activ_cards.append(card_id)
