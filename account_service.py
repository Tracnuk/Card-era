from account_db_repository import AccountDbRepository
from person_db_repository import PersonDbRepository
from account import Account
from person import Person

account_db_storage = AccountDbRepository()

class AccountService:
    def create_account(self, user_data):
        global auth_account
        try:
            account_db_storage.add_account(Account(user_data.nickname, user_data.login, user_data.password))
            auth_account = account_db_storage.get_account_by_login(login)[0]
        except Exception:
            return 'Пользователь с таким логином уже сущестыует!'
        
    def delete_account(self):
        if auth_user != None:
            account_db_storage.delete_account(aurh_user)
            return 'Аккаунт был удалён.'
        else:
            return 'Вы не вошли в аккаунт!'

    def update_account(self, nickname, login, password, first_name):
        try:
            account_id = auth_account
            account_db_storage.update_account(account_id, login = new_login, password = new_password, first_name = new_first_name)
            return 'Данные обновлены.'
        except:
            return 'Вы не вошли в аккаунт!'
            
