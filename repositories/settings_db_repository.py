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
                account_id INTEGER UNIQUE,
                card1_id INTEGER,
                card2_id INTEGER,
                card3_id INTEGER,
                card4_id INTEGER,
                card5_id INTEGER
                )
        ''')
        self.conn.commit()

    def add_cards_id(self, account_id, card1_id, card2_id, card3_id, card4_id, card5_id):
        self.cursor.execute('''
            INSERT INTO settings (account_id, card1_id, card2_id,
            card3_id, card4_id, card5_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (account_id, card1_id, card2_id, card3_id, card4_id, card5_id))
        self.conn.commit()
        return self.cursor.lastrowid 

    def get_settings_by_id(self, account_id):
        self.cursor.execute('SELECT * FROM settings WHERE account_id = ?', (account_id,))
        return self.cursor.fetchone()
    
    def update_cards(self, **kwargs):
        self.cursor.execute('''
            UPDATE settings
            SET card1_id = ?,
                card2_id = ?,
                card3_id = ?,
                card4_id = ?,
                card5_id = ?,
            WHERE account_id = ?
        ''', (
            kwargs['card1_id'],
            kwargs['card2_id'],
            kwargs['card3_id'],
            kwargs['card4_id'],
            kwargs['card5_id'],
            kwargs['account_id'],
        ))
        self.conn.commit()
    
    def delete_card(self, account_id):
        self.cursor.execute('DELETE FROM settings WHERE accont_id = ?', (account_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
           
