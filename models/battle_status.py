class BattleStatus():
    def __init__(self, player_data, remaining_player_energy,
                 enemy_data, remaining_enemy_energy,
                 player_area=[0, 0, 0, 0, 0], enemy_area=[0, 0, 0, 0, 0], ):
        
        self.player_data = player_data
        self.player_area = player_area
        self.remaining_player_energy = remaining_player_energy
        self.ememy_data = enemy_data
        self.enemy_area = enemy_area
        self.remaining_enemy_energy = remaining_enemy_energy
        
        
