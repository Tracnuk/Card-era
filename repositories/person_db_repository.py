import sqlite3

class PersonsDbRepository:
    def __init__(self, db_path='game.db'):
        self.db_path = db_path
        self.__create_table()
        
    def __create_table(self):
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    surname TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone_number TEXT,
                    account_id INTEGER
                )
            ''')
            conn.commit()
        finally:
            conn.close()
            
    def add_person(self, person):
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO persons (first_name, surname, last_name, email, phone_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (person.first_name, person.surname, person.last_name, person.email, person.phone_number))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def get_person_by_id(self, person_id):
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM persons WHERE id = ?', (person_id,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    def get_persons(self):
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM persons')
            return cursor.fetchall()
        finally:
            conn.close()
        
    def update_person(self, person_id, first_name, surname, last_name, email, phone_number, account_id=None):
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE persons
                SET first_name = ?,
                    surname = ?,
                    last_name = ?,
                    email = ?,
                    phone_number = ?,
                    account_id = ?
                WHERE id = ?
            ''', (
                first_name,
                surname,
                last_name,
                email,
                phone_number,
                account_id,
                person_id
            ))
            conn.commit()
        finally:
            conn.close()
        
    def delete_person(self, person_id):
        conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM persons WHERE id = ?', (person_id,))
            conn.commit()
        finally:
            conn.close()
