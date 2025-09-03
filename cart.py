class Card:
    def __init__(self, card_id, rarty, card_type, name, count, price,
                 link_of_picture, use_for_battle=False):
        self.id = card_id
        self.rarty = rarty
        self.type = card_type
        self.name = name
        self.count = count
        self.price = price
        self.link_of_picture = link_of_picture
        self.use_for_battle = use_for_battle
        
    def __str__(self):
        return '''редкость: {self.rarty}
тип: {self.type}
имя: {self.name}
параметр: {self.count}
цена: {self.price}
иконка: {self.link_of_picture}
есть ли в калоде: {self.use_for_battle}
'''
