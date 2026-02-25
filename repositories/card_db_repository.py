import sqlite3
import os

class CardDbRepository:
    def __init__(self):
        # Находим путь к папке, где лежит этот скрипт
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Привязываем базу к этой папке, чтобы не создавались пустые копии
        self.db_path = os.path.join(current_dir, "cards.db")
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