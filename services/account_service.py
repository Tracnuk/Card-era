import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.account_db_repository import AccountsDbRepository
from repositories.person_db_repository import PersonsDbRepository
from models.account import Account
from models.person import Person

person_db_storage = PersonsDbRepository()
account_db_storage = AccountsDbRepository()

class AccountService:
    def create_account(self, user_data):
        global auth_account
        try:
            account_db_storage.add_account(Account(user_data.nickname, user_data.login, user_data.password))
            auth_account = account_db_storage.get_account_by_login(user_data.login)[0]
            return auth_account
        except Exception:
            return 'Пользователь с таким логином уже сущестыует!'
        
    def delete_account(self):
        try:
            account_db_storage.delete_account(auth_account)
            return 'Аккаунт был удалён.'
        except:
            return 'Вы не вошли в аккаунт!'

    def update_account(self, new_nickname, new_login, new_password):
        try:
            account_db_storage.update_account(account_id = auth_account, nickname = new_nickname, login = new_login, password = new_password)
            return 'Данные обновлены.'
        except:
            return 'Вы не вошли в аккаунт!'
        
    def get_account_by_id(self, account_id=None):
        if account_id != None:
            return account_db_storage.get_account_by_id(person_id)
        else:
            return account_db_storage.get_account_by_id(auth_account)

    def get_account_by_login(self, login):
        try:
            return account_db_storage.get_account_by_id(login)
        except:
            return 'Такого логина не существует!'
