class Card:
    def __init__(self, rarity, type_card, name,
                 count, hp, damage, energy, price,
                 link_of_picture, card_id=-1):
        self.id = card_id
        self.rarity = rarity
        self.type = type_card
        self.name = name
        self.count = count
        self.hp = hp
        self.damage = damage
        self.energy = energy
        self.price = price
        self.link_of_picture = link_of_picture
        
    def __str__(self):
        return f'''id: {self.id}
редкость: {self.rarity}
тип: {self.type}
имя: {self.name}
параметр: {self.count}
здоровье: {self.hp}
урон: {self.damage}
энергия: {self.energy}
цена: {self.price}
иконка: {self.link_of_picture}
'''
