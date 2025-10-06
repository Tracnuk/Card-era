import sqlite3

class CardDbRepository:
    def __init__(self, db_path="cards.db", ):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rarity TEXT NOT NULL,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                count INTEGER,
                hp INTEGER,
                damage INTEGER,
                price INTEGER NOT NULL,
                link_of_picture TEXT)''')
        self.conn.commit()

    def add_card(self, card):
        try:
            self.cursor.execute('''
                INSERT INTO cards (rarity, type, name, count, hp, damage, price, link_of_picture)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (card.rarity, card.type, card.name, card.count, card.hp, card.damage, card.price, card.link_of_picture))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Ошибка при создании карты')


    def update_card(self, card_id, card):
        try:
            self.cursor.execute('''
                UPDATE cards
                SET rarity = ?,
                    type = ?,
                    name = ?,
                    count = ?,
                    hp = ?,
                    damage = ?,
                    price = ?,
                    link_of_picture = ?
                WHERE id = ?''', (card.rarity, card.type, card.name, card.count, card.hp, card.damage, card.price,
                                        card.link_of_picture, card_id))
            self.conn.commit()
        except:
            print("Ошибка при обновление карты")

    def get_card_by_id(self, card_id):
        self.cursor.execute('''SELECT * FROM cards WHERE id = ?''', (card_id,))
        card = self.cursor.fetchone()
        if card:
            return card
        else:
            return None
        
    def get_all_cards(self):
        self.cursor.execute('''SELECT * From cards''')
        cards = self.cursor.fetchall()
        self.conn.commit()
        return cards
    
    def delete_card(self, card_id):
        self.cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
        self.conn.commit()
        

    def close(self):
        self.conn.close()
