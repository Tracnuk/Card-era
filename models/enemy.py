class Enemy:
    def __init__(self, hp=40, energy=2, activ_cards=[], wasted_energy=0):
        self.hp = hp
        self.energy = energy
        self.activ_card = activ_cards
        self.wasted_energy = wasted_energy

