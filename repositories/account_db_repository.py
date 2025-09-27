import sqlite3
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.person import Person

class AccountsDbRepository:
    def __init__(self, db_path='game.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                nickname TEXT UNIQUE NOT NULL,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                cash INTEGER,
                level INTEGER,
                FOREIGN KEY (person_id) REFERENCES persons(id)
                )
        ''')
        self.conn.commit()

    def add_account(self, account):
        self.cursor.execute('''
            INSERT INTO account (person_id, nickname, login, password, cash, level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (account.person_id, account.nickname, account.login, account.password, account.cash, account.level))
        self.conn.commit()
        return self.cursor.lastrowid 

    def get_account_by_login(self, login):
        self.cursor.execute('SELECT * FROM account WHERE login = ?', (login,))
        return self.cursor.fetchone()

    def get_account_by_id(self, account_id):
        self.cursor.execute('SELECT * FROM account WHERE id = ?', (account_id,))
        return self.cursor.fetchone()

    def get_all_accounts(self):
        self.cursor.execute('SELECT * FROM account')
        return self.cursor.fetchall()

    def verification(self, login, password):
        self.cursor.execute('SELECT password FROM account WHERE login = ?', (login,))
        row = self.cursor.fetchone()
        if row and row[0] == password:
            return True
        return False

    def update_accounts(self, **kwargs):
        self.cursor.execute('''
            UPDATE account
            SET nickname = ?,
                login = ?,
                password = ?,
            WHERE id = ?
        ''', (
            kwargs['nickname'],
            kwargs['login'],
            kwargs['password'],
            kwargs['account_id'],
        ))
        self.conn.commit()

    def delete_account(self, account_id):
        self.cursor.execute('DELETE FROM account WHERE id = ?', (account_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
           
