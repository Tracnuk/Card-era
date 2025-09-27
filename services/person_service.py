import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.account_db_repository import AccountsDbRepository
from repositories.person_db_repository import PersonsDbRepository
from models.account import Account
from models.person import Person

person_db_storage = PersonsDbRepository()
account_db_storage = AccountsDbRepository()

class PersonService:
    def __init__(self):
        self.current_person_id = None
        
    def create_person(self, first_name):
        person = Person(first_name)
        self.current_person_id = person_db_storage.add_person(person)
        return self.current_person_id
        
    def delete_person(self):
        if self.current_person_id != None:
            person_db_storage.delete_person(self.current_person_id)
            return 'Пользователь был удалён.'
        else:
            return 'Вы не вошли в аккаунт!'

    def login(self, person_id):
        self.current_person_id = person_id

    def update_person(self, new_first_name, account_id, new_surname='', new_last_name='', new_email='', new_phone_number=''):
        if self.current_person_id != None:
            person_id = self.current_person_id
            person_db_storage.update_person(person_id, new_first_name, new_surname, new_last_name, new_email, new_phone_number, account_id)
            return 'Данные обновлены.'
        else:
            return 'Вы не вошли в аккаунт!'
    
    def get_person_by_id(self, person_id=None):
        if person_id != None:
            return person_db_storage.get_person_by_id(person_id)
        elif self.current_person_id != None:
            return person_db_storage.get_person_by_id(self.current_person_id)
        else:
            return "Вы не вошли в аккаунт!"
            
    def get_all_persons(self):
        result = person_db_storage.get_persons()
        if result and len(result) > 0:
            person = [Person(person_id = data[0],
            first_name = data[1] if data[1] else '-',
            surname = data[2] if data[2] else '-',
            last_name = data[3] if data[3] else '-',
            email = data[4] if data[4] else '-',
            phone_number = data[5],
            account_id = data[6]) for data in result]
            return person
        return ['Нет данных']
