
import sys
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.player_DTO import Player
from models.enemy import Enemy
from models.battle_status import BattleStatus
from services.card_service import CardService

class Battle:
    def __init__(self, player_deck, enemy_deck):
        '''self.player_deck = player_deck  # Сохраняем колоду игрока
        self.enemy_deck = enemy_deck    # Сохраняем колоду врага'''
        self.player_deck = list(map(CardService.get_card_by_id, player_deck))  # Сохраняем колоду игрока
        self.enemy_deck = list(map(CardService.get_card_by_id, enemy_deck))    # Сохраняем колоду врага'''
        enemy = Enemy(enemy_deck)
        player = Player(player_deck)

        # Инициализируем BattleStatus с пустыми списками активных карт
        self.battle = BattleStatus(
            player_data=player,
            remaining_player_energy=player.energy,
            enemy_data=enemy,
            remaining_enemy_energy=enemy.energy,
            player_area=[None] * 5,
            enemy_area=[None] * 5,
            result=[False, False]
        )

    def get_battle_data(self):
        return self.battle

    def attak_cards(self):
        for position in range(5):
            player_card = self.battle.player_area[position]
            enemy_card = self.battle.enemy_area[position]

            if player_card is None and enemy_card is None:
                continue
            elif player_card is None:
                self.battle.player_data.hp -= enemy_card.damage
                if self.battle.player_data.hp <= 0:
                    self.battle.result[0] = True
            elif enemy_card is None:
                self.battle.enemy_data.hp -= player_card.damage
                if self.battle.enemy_data.hp <= 0:
                    self.battle.result[1] = True  # исправленный отступ
            else:
                player_card.hp -= enemy_card.damage
                enemy_card.hp -= player_card.damage

                # Проверяем уничтожение карт после атаки
                if enemy_card.hp <= 0:
                    self.battle.enemy_area[position] = None
                if player_card.hp <= 0:
                    self.battle.player_area[position] = None
        return self.battle

    def player_plant_card(self, position_in_field, position_in_activ_cards):
        if (position_in_activ_cards >= len(self.battle.player_data.activ_cards) or
                self.battle.player_data.activ_cards[position_in_activ_cards] is None):
            return "Выбрана несуществующая карта"
        elif self.battle.player_area[position_in_field] is not None:
            return "Поле занято"
        else:
            card = self.battle.player_data.activ_cards.pop(position_in_activ_cards)
            #self.battle.remaining_player_energy -= card.energy
            self.battle.player_area[position_in_field] = card
            return True
        '''        elif (self.battle.remaining_player_energy -
                self.battle.player_data.activ_cards[position_in_activ_cards].energy < 0):
            return "Не хватает энергии"'''

    def enemy_plant_card(self, position_in_field, position_in_activ_cards):
        if (position_in_activ_cards >= len(self.battle.enemy_data.activ_cards) or
                self.battle.enemy_data.activ_cards[position_in_activ_cards] is None):
            return "Выбрана несуществующая карта врага"

        card = self.battle.enemy_data.activ_cards.pop(position_in_activ_cards)
        self.battle.remaining_enemy_energy -= card.energy
        self.battle.enemy_area[position_in_field] = card
        return self.battle

    def giv_activ_cards(self, count_player_cards, count_enemy_cards):
        # Раздаём карты из колод
        for _ in range(count_player_cards):
            if self.player_deck:  # Проверяем, что колода не пуста
                card_index = random.randint(0, len(self.player_deck) - 1)
                card = self.player_deck[card_index]
                self.battle.player_data.activ_cards.append(card)

        for _ in range(count_enemy_cards):
            if self.enemy_deck:  # Проверяем, что колода не пуста
                card_index = random.randint(0, len(self.enemy_deck) - 1)
                card = self.enemy_deck[card_index]
                self.battle.enemy_data.activ_cards.append(card)
