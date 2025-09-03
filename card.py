class Card:
    def __init__(self, card_id = -1, 
                rarity, 
                type, 
                name_parametr, 
                count_parametr, 
                price, 
                picture):

    def __str__(self):
        return f'''Редкость : {self.rarity}
        Тип : {self.type}
        Параметр : {self.name_parametr} - {self.count_parametr}
        Цена : {self.price}
        Карта : {self.picture}'''
