from ..repositories.account_db_repository import AccountDbRepository
from ..repositories.person_db_repository import PersonDbRepository
from ..models.account import Account
from ..models.person import Person

person_db_storage = PersonDbRepository()
acount_db_storage = AccountDbRepository()

class PersonService:
    def create_person(self, first_name):
        global auth_person
        account_id = account_db_storage.get_account_by_login(login)[0]
        person_db_storage.add_person(Person(first_name, account_id = account_db_storage.get_account_by_login(login)[0]))
        auth_person = person_db_storage.get_person_by_id(login)[0]
        return auth_person
        
    def delete_person(self):
        if auth_user != None:
            person_db_storage.delete_person(aurh_person)
            return 'Пользователь был удалён.'
        else:
            return 'Вы не вошли в аккаунт!'

    def update_person(self, nickname, login, password, first_name):
        try:
            person_id = auth_person
            person_db_storage.update_person(person_id, login = new_login, password = new_password, first_name = new_first_name)
            return 'Данные обновлены.'
        except:
            return 'Вы не вошли в аккаунт!'
        
    #get_person_by_id
