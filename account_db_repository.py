import sqlite3
from const import connection_string


class AccountDbRepository:
    def __init__(self, db_path=connection_string):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Account (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    Account_id INTEGER,
                    cash INTEGER,
                    level INTEGER,
                    mana INTEGER,
                    health INTEGER
                )
            ''')
            self.conn.commit()

    def add_Account(self, user):
        self.cursor.execute('''
            INSERT INTO Account (login, password, Account_id, cash, level, mana, health)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (Account.login, Account.password, Account.Account_id, Account.cash, Account.level, Account.mana, Account.health))
        self.conn.commit()

    def get_account_by_login(self, login):
        self.cursor.execute('SELECT * FROM Account WHERE login = ?', (login,))
        return self.cursor.fetchone()

    def get_account_by_id(self, account_id):
        self.cursor.execute('SELECT * FROM Account WHERE id = ?', (account_id,))
        return self.cursor.fetchone()

    def get_all_accounts(self):
        self.cursor.execute('SELECT * FROM Account')
        return self.cursor.fetchall()

    def update_account(self, account_id, **kwargs):
        self.cursor.execute('''
            UPDATE Account
            SET login = ?,
                password = ?,
                Account_id = ?,
                cash = ?,
                level = ?,
                mana = ?,
                health = ?
            WHERE id = ?
        ''', (
            kwargs['login'],
            kwargs['password'],
            kwargs['Account_id'],
            kwargs['cash'],
            kwargs['level'],
            kwargs['mana'],
            kwargs['health'],
            account_id
        ))
        self.conn.commit()

    def delete_account(self, account_id):
        self.cursor.execute('DELETE FROM Account WHERE id = ?', (account_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
           