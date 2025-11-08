import sqlite3

class CardDbRepository:
    def __init__(self, db_path="cards.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rarity TEXT NOT NULL,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    count INTEGER,
                    hp INTEGER,
                    damage INTEGER,
                    energy INTEGER,
                    price INTEGER NOT NULL,
                    link_of_picture TEXT
                )
            ''')
            self.conn.commit()
            
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    def add_card(self, card):
        try:
            self.cursor.execute('''
                INSERT INTO cards (rarity, type, name, count, hp, damage, energy, price, link_of_picture)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                card.rarity, card.type, card.name, card.count, 
                card.hp, card.damage, card.energy, card.price, 
                card.link_of_picture
            ))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Ошибка при создании карты: {e}")

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
                    energy = ?,
                    price = ?,
                    link_of_picture = ?
                WHERE id = ?
            ''', (
                card.rarity, card.type, card.name, card.count, 
                card.hp, card.damage, card.energy, card.price, 
                card.link_of_picture, card_id
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении карты: {e}")

    def get_card_by_id(self, card_id):
        self.cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
        card = self.cursor.fetchone()
        return card if card else None

    def get_all_cards(self):
        self.cursor.execute('SELECT * FROM cards')
        cards = self.cursor.fetchall()
        return cards

    def delete_card(self, card_id):
        try:
            self.cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении карты: {e}")

    def close(self):
        self.conn.close()
