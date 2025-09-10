from account_db_repository import AccountDbRepository
from persom_db_repository import PersonDbRepository
from account import Account
from person import Person

person_db_storage = PersonDbRepository()
account_db_storage = AccountDbRepository()

class AccountService:
    def create_account(self, nickname, login, password):
        global auth_account
        try:
            account_db_storage.add_account(Account(nickname, login, password))
            auth_account = account_db_storage.get_account_by_login(login)[0]
            return auth_account
        except Exception:
            return 'Пользователь с таким логином уже сущестыует!'
        
    def delete_account(self):
        if auth_user != None:
            account_db_storage.delete_account(aurh_user)
            return 'Аккаунт был удалён.'
        else:
            return 'Вы не вошли в аккаунт!'

    def update_account(self, new_nickname, new_login, new_password):
        try:
            account_id = auth_account
            account_db_storage.update_account(account_id, nickname = new_nickname, login = new_login, password = new_password)
            return 'Данные обновлены.'
        except:
            return 'Вы не вошли в аккаунт!'
        
    #get_account_by_login
