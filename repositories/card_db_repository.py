import sqlite3
import os

class CardDbRepository:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "cards.db")
        self.__create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=20)

    def __create_table(self):
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rarity TEXT, type TEXT, name TEXT, count INTEGER,
                    hp INTEGER, damage INTEGER, energy INTEGER,
                    price INTEGER, link_of_picture TEXT
                )
            ''')

    def get_card_by_id(self, card_id):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
            return cursor.fetchone()

cards_db_storage = CardDbRepository() # Создаем объект сразу
