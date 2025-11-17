import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.account_service import AccountService
from services.person_service import PersonService
from repositories.settings_db_repositoty import SettingsDbRepository
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
            return account_id
        else:
            person.update_person(user_data.first_name, account_id)
            cards = []
            for card_id in range(1, 6):
                cards.append(cards_db_storage.get_card_by_id(card_id)[0])
            settings_db_storage.add_cards_id(cards[0],
                                             cards[1],
                                             cards[2],
                                             cards[3],
                                             cards[4])
            return 'Добро пожаловать'

    def login(self, login, password):
        asnwer = account.login(login, password)
        account_data = account.get_account_by_login(login)
        if not isinstance((account_data), str):
            person_id = account_data[1]
            person.login(person_id)
            return asnwer
        else:
            return account_data
        
    def get_current_user(self):
        user_account = account.get_account_by_id()
        user_person = person.get_person_by_id()
        if user_account == user_person:
            return [user_account]
        return [user_account, user_person]

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
