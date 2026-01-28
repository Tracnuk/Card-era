import sqlite3


class PersonsDbRepository:
    def __init__(self, db_path='game.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute("""
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
        self.conn.commit()

    def add_person(self, person):
        self.cursor.execute("""
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
        self.conn.commit()
        return self.cursor.lastrowid

    def update_account_id(self, person_id, account_id):
        self.cursor.execute("""
            UPDATE persons
            SET account_id = ?
            WHERE id = ?
        """, (account_id, person_id))
        self.conn.commit()

    def get_person_by_id(self, person_id):
        self.cursor.execute("SELECT * FROM persons WHERE id = ?", (person_id,))
        return self.cursor.fetchone()

    def get_persons(self):
        self.cursor.execute("SELECT * FROM persons")
        return self.cursor.fetchall()

    def delete_person(self, person_id):
        self.cursor.execute("DELETE FROM persons WHERE id = ?", (person_id,))
        self.conn.commit()
