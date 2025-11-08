import sqlite3
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.person import Person

class SettingsDbRepository:
    def __init__(self, db_path='game.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                account_id INTEGER,
                card1 INTEGER,
                card2 INTEGER,
                card3 INTEGER,
                card4 INTEGER,
                card5 INTEGER
                )
        ''')
        self.conn.commit()

    def add_cards(self, card1, card2, card3, card4, card5):
        self.cursor.execute('''
            INSERT INTO settings (card1, card2, card3, card4, card5)
            VALUES (?, ?, ?, ?, ?)
        ''', (card1, card2, card3, card4, card5))
        self.conn.commit()
        return self.cursor.lastrowid 

    def get_settings_by_id(self, account_id):
        self.cursor.execute('SELECT * FROM account WHERE account_id = ?', (account_id,))
        return self.cursor.fetchone()
    
    def update_cards(self, **kwargs):
        self.cursor.execute('''
            UPDATE settings
            SET card1 = ?,
                card2 = ?,
                card3 = ?,
                card4 = ?,
                card5 = ?,
            WHERE account_id = ?
        ''', (
            kwargs['card1'],
            kwargs['card2'],
            kwargs['card3'],
            kwargs['card4'],
            kwargs['card5'],
            kwargs['account_id'],
        ))
        self.conn.commit()

    def delete_card(self, account_id):
        self.cursor.execute('DELETE FROM settings WHERE accont_id = ?', (account_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
           
