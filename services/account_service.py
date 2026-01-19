import sys
import os
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.account_db_repository import AccountsDbRepository
from repositories.person_db_repository import PersonsDbRepository
from repositories.settings_db_repository import SettingsDbRepository
from repositories.card_db_repository import CardDbRepository
from models.account import Account
from models.person import Person

settings_db_storage = SettingsDbRepository()
cards_db_storage = CardDbRepository()
person_db_storage = PersonsDbRepository()
account_db_storage = AccountsDbRepository()

class AccountService:
    def __init__(self):
        self.current_account_id = None
        
    def create_account(self, user_data, person_id):
        try:
            account = Account(user_data.nickname, user_data.login, user_data.password, person_id)
            account_id = account_db_storage.add_account(account)
            self.current_account_id = account_id
            cards = []
            for card_id in range(1, 6):
                cards.append(cards_db_storage.get_card_by_id(card_id)[0])
            settings_db_storage.add_cards_id(self.current_account_id,
                                             cards[0],
                                             cards[1],
                                             cards[2],
                                             cards[3],
                                             cards[4])
            return account_id
        except sqlite3.IntegrityError:
            return 'Пользователь с таким логином уже существует!'
        except Exception as e:
            return f'Ошибка создания аккаунта: {str(e)}'
        
    def delete_account(self):
        if self.current_account_id != None:
            account_db_storage.delete_account(self.current_account_id)
            self.current_account_id = None
            return 'Аккаунт был удалён.'
        else:
            return 'Вы не вошли в аккаунт!'

    def update_account(self, new_nickname, new_login, new_password): #доделать левл и т.д.
        if self.current_account_id != None:
            account_db_storage.update_account(account_id = self.current_account_id, nickname = new_nickname, login = new_login, password = new_password)
            return 'Данные обновлены.'
        else:
            return 'Вы не вошли в аккаунт!'

    def verification(self):
        return self.current_account_id != None
        
    def login(self, login, password):
        if account_db_storage.verification(login, password):
            account = account_db_storage.get_account_by_login(login)
            self.current_account_id = account[0]
            return f'Добро пожаловать {account[2]}'
        else:
            return 'Неправильный логин или пароль!'
    
    def get_account_by_id(self, account_id=None):
        if account_id != None:
            return account_db_storage.get_account_by_id(account_id)
        elif self.current_account_id != None:
            return account_db_storage.get_account_by_id(self.current_account_id)
        else:
            return "Вы не вошли в аккаунт!"

    def import_deck_of_cards(self):
        return settings_db_storage.get_settings_by_id(self.current_account_id)

    def get_all_accounts(self):
        result = account_db_storage.get_all_accounts()
        if result and len(result) > 0:
            accounts = [Account(account_id = data[0],
                person_id = data[1],
                nickname = data[2],
                login = data[3],
                password = data[4] if data[4] else '-',
                cash = data[5] if data[5] else '-',
                level = data[6] if data[6] else '-') for data in result]
            return accounts
        return ['Нет данных']
                
    def get_account_by_login(self, login):
        try:
            return account_db_storage.get_account_by_login(login)
        except:
            return 'Такого логина не существует!'
