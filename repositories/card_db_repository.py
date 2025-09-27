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
                price INTEGER NOT NULL,
                link_of_picture TEXT)''')
        self.conn.commit()

    def add_card(self, card):
        try:
            self.cursor.execute('''
                INSERT INTO cards (id, rarity, type, name, count, price, link_of_picture)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (card.id, card.rarity, card.type, card.name, card.count, card.price,card.link_of_picture))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('u already have this card')


    def update_card(self, card_id, card):
        try:
            self.cursor.execute('''UPDATE cards
                                SET id = ?,
                                SET rarity = ?,
                                SET type = ?,
                                SET name = ?,
                                SET count = ?,
                                SET price = ?,
                                SET link_of_picture = ?,
                                WHERE id = ?''', (card.rarity, card.type,card.name, card.count, card.price,
                                                        card.link_of_picture, card.id)))

            print('card updated')
        except:
            print("card update failed")

    def get_card(self, card_id):
        self.cursor.execute('''SELECT * FROM cards WHERE id = ?''', (card_id,))
        card = self.cursor.fetchone()
        if card:
            return card
        else:
            return None

    def delete_card(self, card_id):
        self.cursor.execute('DELETE card FROM cards WHERE id = ?', (card_id,))
        self.conn.commit()
        print(f'Card with id {id} deleted')
        

    def close(self):
        self.conn.close()
