import sqlite3

class PersonsDbRepository:
    def __init__(self, db_path='persons.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.__create_table()
        
    def __create_table(self):
            self.cursor.execute('''
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
            self.conn.commit()
            
    def add_person(self, person):
        self.cursor.execute('''
            INSERT INTO persons (first_name, surname, last_name, email, phone_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (person.first_name, person.surname, person.last_name, person.email, person.phone_number))
        self.conn.commit()
        
        self.cursor.execute("SELECT last_insert_rowid()")
        person_id = self.cursor.fetchone()[0]
        return person_id

    def get_person_by_id(self, person_id):
        self.cursor.execute('''SELECT * From persons WHERE id = ?''', (person_id, ))
        person = self.cursor.fetchone()
        return person
    
    def get_persons(self):
        self.cursor.execute('''SELECT * From persons''')
        persons = self.cursor.fetchall()
        return persons
        
    def update_person(self, person_id, account_id=None, **kwargs):
        if account_id == None:
            account_id = self.cursor.fetchone()[6]
        self.cursor.execute('''UPDATE persons
                            SET first_name = ?,
                            surname = ?,
                            last_name = ?,
                            email = ?,
                            phone_number = ?,
                            account_id = ?,
                            WHERE id = ?''', (kwargs['first_name'], kwargs['surname'], kwargs['last_name'], kwargs['email'], kwargs['phone_number'], account_id, person_id))
        self.conn.commit()
        
    def delete_person(self, person_id):
        self.cursor.execute('DELETE FROM persons WHERE id = ?', (person_id, ))
        self.conn.commit()
    
    def close(self):
        self.conn.close()
