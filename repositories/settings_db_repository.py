import sqlite3
import sys
import os

# Если нужно оставить привязку к корню для импорта моделей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.person import Person
class SettingsDbRepository:
    def __init__(self, db_path='game.db'):
        self.db_path = db_path
        self.__create_table()

    def _get_conn(self):
        # timeout решает проблему "database is locked"
        return sqlite3.connect(self.db_path, timeout=20)

    def __create_table(self):
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    account_id INTEGER UNIQUE,
                    card1_id INTEGER,
                    card2_id INTEGER,
                    card3_id INTEGER,
                    card4_id INTEGER,
                    card5_id INTEGER
                )
            ''')
            conn.commit()

    def add_cards_id(self, account_id, card1_id, card2_id, card3_id, card4_id, card5_id):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO settings (account_id, card1_id, card2_id,
                card3_id, card4_id, card5_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_id, card1_id, card2_id, card3_id, card4_id, card5_id))
            conn.commit()
            return cursor.lastrowid 

    def get_settings_by_id(self, account_id):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM settings WHERE account_id = ?', (account_id,))
            return cursor.fetchone()
    
    def update_cards(self, **kwargs):
        with self._get_conn() as conn:
            conn.execute('''
                UPDATE settings
                SET card1_id = ?,
                    card2_id = ?,
                    card3_id = ?,
                    card4_id = ?,
                    card5_id = ?
                WHERE account_id = ?
            ''', (
                kwargs.get('card1_id'),
                kwargs.get('card2_id'),
                kwargs.get('card3_id'),
                kwargs.get('card4_id'),
                kwargs.get('card5_id'),
                kwargs.get('account_id'),
            ))
            conn.commit()
    
    def delete_card(self, account_id):
        with self._get_conn() as conn:
            # Исправлена опечатка в имени колонки
            conn.execute('DELETE FROM settings WHERE account_id = ?', (account_id,))
            conn.commit()