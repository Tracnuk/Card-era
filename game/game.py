import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.account_service import AccountService
from services.person_service import PersonService

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
            return 'Добро пожаловать'

    def login(self, login, password):
        asnwer = account.login(login, password)
        person_id = account.get_account_by_login(login)[1]
        person.login(person_id)
        return asnwer
        
    def get_user(self):
        user_account = account.get_account_by_id()
        user_person = person.get_person_by_id()
        return [user_account, user_person]

    def get_all_users(self):
        users_persons = person.get_all_persons()
        users_accounts = account.get_all_accounts()
        return (users_persons, users_accounts)
