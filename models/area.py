class Area:
    def __init__(self):
        self.user_place = (0, 0, 0, 0, 0)
        self.enemy_place = (0, 0, 0, 0, 0)
        
    def get_all(self):
        return {'user_place':self.user_place, 'enemy_place':self.enemy_place}

    def set_user_place(self, area_position, card_id):
        self.user_place[area_position] = card_id 

    def set_enemy_place(self, area_position, card_id):
        self.enemy_place[area_position] = card_id 
