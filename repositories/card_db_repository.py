import sqlite3

class CardDbRepository:
    def __init__(self, db_path="cards.db"):
        self.db_path = db_path
        self.__create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=20)

    def __create_table(self):
        try:
            with self._get_conn() as conn:
                conn.execute('''
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
                conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы карт: {e}")

    def add_card(self, card):
        try:
            with self._get_conn() as conn:
                conn.execute('''
                    INSERT INTO cards (rarity, type, name, count, hp, damage, energy, price, link_of_picture)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    card.rarity, card.type, card.name, card.count, 
                    card.hp, card.damage, card.energy, card.price, 
                    card.link_of_picture
                ))
                conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Ошибка при добавлении карты: {e}")

    def update_card(self, card_id, card):
        try:
            with self._get_conn() as conn:
                conn.execute('''
                    UPDATE cards
                    SET rarity = ?, type = ?, name = ?, count = ?, 
                        hp = ?, damage = ?, energy = ?, price = ?, 
                        link_of_picture = ?
                    WHERE id = ?
                ''', (
                    card.rarity, card.type, card.name, card.count, 
                    card.hp, card.damage, card.energy, card.price, 
                    card.link_of_picture, card_id
                ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении карты: {e}")

    def get_card_by_id(self, card_id):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
            return cursor.fetchone()

    def get_all_cards(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cards')
            return cursor.fetchall()

    def delete_card(self, card_id):
        try:
            with self._get_conn() as conn:
                conn.execute('DELETE FROM cards WHERE id = ?', (card_id,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении карты: {e}")