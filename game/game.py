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
        if isinstance((account_id := account.create_account(user_data)), str):
            return account_id
        else:
            user = person.get_person_by_id(person_id)
            person.update_person(user[user_data.first_name], account_id)
            return 'Добро пожаловать'
