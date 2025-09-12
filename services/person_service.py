import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.account_db_repository import AccountsDbRepository
from repositories.person_db_repository import PersonsDbRepository
from models.account import Account
from models.person import Person

person_db_storage = PersonsDbRepository()
acount_db_storage = AccountsDbRepository()

class PersonService:
    def create_person(self, first_name):
        global auth_person
        auth_person = person_db_storage.add_person(Person(first_name))
        return auth_person
        
    def delete_person(self):
        if auth_user != None:
            person_db_storage.delete_person(aurh_person)
            return 'Пользователь был удалён.'
        else:
            return 'Вы не вошли в аккаунт!'

    def update_person(self, new_first_name, account_id, new_surname='', new_last_name='', new_email='', new_phone_number=''):
        try:
            person_id = auth_person
            person_db_storage.update_person(person_id, first_name = new_first_name, surname = new_surname, last_name = new_last_name, email = new_email, phone_number = new_phone_number)
            return 'Данные обновлены.'
        except:
            return 'Вы не вошли в аккаунт!'
        
    def get_person_by_id(self, person_id=None):
        if person_id != None:
            return person_db_storage.get_person_by_id(person_id)
        else:
            return person_db_storage.get_person_by_id(auth_person)

    def get_persons(self):
        result = person_db_storage.get_persons()
        if result and len(result) > 0:
            persons = [__convert_data_from_user_model(data) for data in result]
            return persons
        return ['Нет данных']
