import sqlite3

class CardDbRepository:
    def __init__(self, db_path="cards.db", ):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                idd INTEGER PRIMARY KEY AUTOINCREMENT,
                rarity TEXT NOT NULL,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                count INTEGER,
                price INTEGER NOT NULL,
                link_of_picture TEXT,
                use_for_battle BOOL)''')
        self.conn.commit()

    def add_card(self, card):
        try:
            self.cursor.execute('''
                INSERT INTO cards (idd, rarity, type, name, count, price,link_of_picture,use_for_battle)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (card.idd, card.rarity, card.type, card.name, card.count, card.price,card.link_of_picture,card.use_for_battle))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('u already have this card')


    def update_card(self, idd, card):
        try:
            self.cursor.execute('''UPDATE cards
                                SET idd = ?,
                                SET rarity = ?,
                                SET type = ?,
                                SET name = ?,
                                SET count = ?,
                                SET price = ?,
                                SET link_of_picture = ?,
                                SET use_for_battle = ?,
                                WHERE card_idd = ?''', (card.idd, card.rarity,card.type,card.name ,card.count,card.price,card.link_of_picture,card.use_for_battle))

            print('card updated')
        except:
            print("card update failed")

    def get_card(self, idd):
        self.cursor.execute('''SELECT * FROM cards WHERE idd = ?''', (idd,))
        card = self.cursor.fetchone()
        if card:
            return card
        else:
            return None

    def delete_card(self, idd):
        self.cursor.execute('DELETE card FROM cards WHERE idd = ?', (idd,))
        self.conn.commit()
        print(f'Card with idd{idd}deleted')
        

    def close(self):
        self.conn.close()
