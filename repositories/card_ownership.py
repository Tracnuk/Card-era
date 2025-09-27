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
                id_card INTEGER ,
                id_account NTEGER ,
               )''')
        self.conn.commit()

    def add_card(self, card):
        try:
            self.cursor.execute('''
                INSERT INTO CardOwnership (id_card,id_account)
                VALUES (?, ?, ?)''',
                (CardOwnership.id,CardOwnership.id_card,CardOwnership.id_account))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('card already exists on account')

    
    def get_card(self, id_account):
        self.cursor.execute('''SELECT * FROM CardOwnerships WHERE  = ?''', (id_account,))
        CardOwnership = self.cursor.fetchone()
        if CardOwnership:
            return CardOwnership
        else:
            return None

    

    def delete_card(self, id):
        self.cursor.execute('DELETE CardOwnership FROM CardOwnerships WHERE id = ?', (id,))
        self.conn.commit()
        print(f'Card with id{id}deleted')

    def close(self):
        self.conn.close()
