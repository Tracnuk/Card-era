import sqlite3

class CardOwnership:
    def __init__(self, db_path="game.db"):
        self.db_path = db_path
        self._create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=20)

    def _create_table(self):
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS CardOwnerships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_card INTEGER,
                    id_account INTEGER
                )''')
            conn.commit()

    def add_card_and_account(self, card_id, account_id):
        try:
            with self._get_conn() as conn:
                conn.execute('''
                    INSERT INTO CardOwnerships (id_card, id_account)
                    VALUES (?, ?)''', (card_id, account_id))
                conn.commit()
        except sqlite3.Error as e:
            print(f'Ошибка при создании связи: {e}')
    
    def get_cards_in_account(self, id_account):
        """Возвращает список всех ID карт игрока"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id_card FROM CardOwnerships WHERE id_account = ?', (id_account,))
            return cursor.fetchall() # Возвращает список кортежей [(5,), (5,), ...]

    def delete_all_user_cards(self, id_account):
        with self._get_conn() as conn:
            conn.execute('DELETE FROM CardOwnerships WHERE id_account = ?', (id_account,))
            conn.commit()
            return f'Все карты аккаунта {id_account} удалены!'