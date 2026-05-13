class BattleStatus:
    def __init__(self, player_data, remaining_player_energy,
                 enemy_data, remaining_enemy_energy,
                 player_area=None, enemy_area=None, result=None):
        self.player_data = player_data
        self.player_area = player_area if player_area is not None else [None] * 5
        self.remaining_player_energy = remaining_player_energy
        self.enemy_data = enemy_data  # Исправлено: было ememy_data
        self.enemy_area = enemy_area if enemy_area is not None else [None] * 5
        self.remaining_enemy_energy = remaining_enemy_energy
        self.result = result if result is not None else [False, False]

        # Добавляем активные карты для игрока и врага
        self.player_data.activ_cards = []
        self.enemy_data.activ_cards = []        
