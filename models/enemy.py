import random

class Enemy:
    def __init__(self, deck_of_cards, hp=40, energy=2, activ_cards=[], wasted_energy=0):
        self.deck_of_cards = deck_of_cards
        self.hp = hp
        self.energy = energy
        self.activ_cards = activ_cards
        self.wasted_energy = wasted_energy

    def enemy_move(self, buttle_data):
        activ_card = None
        place = None
        correct_move = True
        if None in buttle_data.enemy_area:
            for card in self.activ_cards:
                if self.energy - self.wasted_energy > card.energy:
                    correct_move = False
        while not correct_move:
            activ_card = random.randint(1, 5)
            place = random.randint(1, 5)
            if self.activ_cards[activ_card] and not buttle_data.enemy_area[place]:
                correct_move = True
                turn = True
        return (activ_card, place), turn
