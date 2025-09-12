import sqlite3
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.person import Person

class AccountsDbRepository:
    def __init__(self, db_path='accounts.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER
                nickname TEXT UNIQUE NOT NULL,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                cash INTEGER,
                level INTEGER,
                FOREIGN KEY (person_id) REFERENCES Persons(id)
                )
        ''')
        self.conn.commit()

    def add_account(self, Account):
        self.cursor.execute('''
            INSERT INTO account (nickname, login, password, cash, level)
            VALUES (?, ?, ?, ?, ?)
        ''', (Account.nickname, Account.login, Account.password, Account.cash, Account.level))
        self.conn.commit()

    def get_account_by_login(self, login):
        self.cursor.execute('SELECT * FROM account WHERE login = ?', (login,))
        return self.cursor.fetchone()

    def get_account_by_id(self, account_id):
        self.cursor.execute('SELECT * FROM account WHERE id = ?', (account_id,))
        return self.cursor.fetchone()

    def get_all_accounts(self):
        self.cursor.execute('SELECT * FROM account')
        return self.cursor.fetchall()

    def update_account(self, **kwargs):
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
           
