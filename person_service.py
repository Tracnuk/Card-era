from person import Person
from person_db_repository import PersonDbRepository
from account_db_repository import AccountDbRepository
from account import Account


person_db_storage = PersonDbRepository()

class PersonService():
    def create_person(self, user_data):
        try:
            person_id = person_db_storage.add_person(Person(user_data.first_name, user_data.last_name, user_data.email, user_data.phone))
            return person_id
        except Exception:
            return 'Ошибка при создании пользователя!'
        
    def delete_person(self):
        if auth_user != None:
            person_db_storage.delete_person(auth_user)
            return 'Пользователь был удалён.'
        else:
            return 'Вы не вошли в аккаунт!'
        
    def update_person(self, first_name, last_name, email, phone):
        try:
            person_id = auth_user
            person_db_storage.update_person(person_id, first_name = new_first_name, last_name = new_last_name, email = new_email, phone = new_phone)
            return 'Данные обновлены.'
        except:
            return 'Вы не вошли в аккаунт!'