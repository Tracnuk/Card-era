class Enemy:
    def __init__(self, deck_of_cards, hp=40, energy=2, activ_cards=[], wasted_energy=0):
        self.deck_of_cards = deck_of_cards
        self.hp = hp
        self.energy = energy
        self.activ_card = activ_cards
        self.wasted_energy = wasted_energy

