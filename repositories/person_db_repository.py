import sqlite3

class PersonsDbRepository:
    def __init__(self, db_path='game.db'):
        self.db_path = db_path
        self.__create_table()

    def _get_conn(self):
        # Добавляем таймаут и проверку потоков для стабильности
        return sqlite3.connect(self.db_path, timeout=20, check_same_thread=False)

    def __create_table(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    surname TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone_number TEXT,
                    account_id INTEGER
                )
            """)
            conn.commit()

    def add_person(self, person):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO persons (first_name, surname, last_name, email, phone_number, account_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                person.first_name,
                person.surname,
                person.last_name,
                person.email,
                person.phone_number,
                None
            ))
            conn.commit()
            return cursor.lastrowid

    def update_account_id(self, person_id, account_id):
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE persons
                SET account_id = ?
                WHERE id = ?
            """, (account_id, person_id))
            conn.commit()
            return True

    def get_person_by_id(self, person_id):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM persons WHERE id = ?", (person_id,))
            return cursor.fetchone()

    def get_persons(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM persons")
            return cursor.fetchall()

    def delete_person(self, person_id):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM persons WHERE id = ?", (person_id,))
            conn.commit()
            return True