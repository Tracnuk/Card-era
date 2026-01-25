import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.battle import Battle
from services.account_service import AccountService
from services.person_service import PersonService
from repositories.settings_db_repository import SettingsDbRepository
from repositories.card_db_repository import CardDbRepository

settings_db_storage = SettingsDbRepository()
cards_db_storage = CardDbRepository()
person = PersonService()
account = AccountService()

class Game:
    def __init__(self):
        self.users = []

    def register(self, user_data):
        person_id = person.create_person(user_data.first_name)
        account_id = account.create_account(user_data, person_id)
        if isinstance((account_id), str):
            return (False, account_id)
        else:
            person.update_person(user_data.first_name, account_id)
        return (True, 'Добро пожаловать')

    def login(self, login, password):
        asnwer = account.login(login, password)
        account_data = account.get_account_by_login(login)
        if not isinstance((account_data), str):
            person_id = account_data[1]
            person.login(person_id)
            return asnwer
        else:
            return account_data

    def import_deck_of_cards(self):
        return list(map(cards_db_storage.get_card_by_id, account.import_deck_of_cards()[1:]))
        
    def get_current_user(self):
        user_account = account.get_account_by_id()
        user_person = person.get_person_by_id()
        if user_account == user_person:
            return [user_account]
        return [user_account, user_person]

    def get_buttle_data(self):
        current_account = account.get_account_by_id()
        result = check_result_buttle()
        if result[0]:
            current_account.cash += 10 * (0.2 * current_account.level)
        elif result[1]:
            current_account.cash += 30 * (0.2 * current_account.level)
            level += 1
        data = buttle_data()
        return data
    
    def get_all_users(self):
        users_persons = person.get_all_persons()
        users_accounts = account.get_all_accounts()
        return (users_persons, users_accounts)

    def delete_user(self):
        person_answer = person.delete_person()
        account_answer = account.delete_account()
        return (person_answer, account_answer)

    def verification(self):
        return account.verification()
