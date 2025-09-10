import sqlite3

class AccountsDbRepository:
    def __init__(self, db_path=connection_string):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Account (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER FOREIGN KEY REFERENCES Persons(id)
                    nickname TEXT UNIQUE NOT NULL,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    cash INTEGER,
                    level INTEGER,
                    )
            ''')
            self.conn.commit()

    def add_account(self, Account):
        self.cursor.execute('''
            INSERT INTO Account (nickname, login, password, cash, level,)
            VALUES (?, ?, ?, ?, ?)
        ''', (Account.nickname, Account.login, Account.password, Account.cash, Account.level))
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

    def update_account(self, **kwargs):
        self.cursor.execute('''
            UPDATE Account
            SET nickname = ?
                login = ?,
                password = ?,
            WHERE id = ?
        ''', (
            kwargs['nickname'],
            kwargs['login'],
            kwargs['password']
        ))
        self.conn.commit()

    def delete_account(self, account_id):
        self.cursor.execute('DELETE FROM Account WHERE id = ?', (account_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
           
