import sqlite3

class CardOwnership:
    def __init__(self, db_path="cardownership.db", ):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CardOwnerships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_card INTEGER,
                id_account NTEGER
               )''')
        self.conn.commit()

    def add_card_and_account(self, card_id, account_id):
        try:
            self.cursor.execute('''
                INSERT INTO CardOwnership (id_card, id_account)
                VALUES (?, ?)''',
                (card_id, account_id))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Ошибка при создании связи')
    
    def get_cards_in_account(self, id_account):
        self.cursor.execute('''SELECT * FROM CardOwnerships WHERE id_account = ?''', (id_account,))
        CardOwnership = self.cursor.fetchone()
        if CardOwnership:
            return CardOwnership
        else:
            return None

    def delete_card_and_account(self, id_account):
        self.cursor.execute('DELETE CardOwnership FROM CardOwnerships WHERE id_account = ?', (id_account,))
        self.conn.commit()
        return f'Катра по id {id_account} удалена!'

    def close(self):
        self.conn.close()
