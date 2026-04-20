import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.arena import Arena
from services.register import Register
from services.Authentication import authentication
from services.account_service import AccountService
from services.person_service import PersonService

person = PersonService()
account = AccountService()

class Game:
    def __init__(self):
        self.user = []

    def register(self, user_data):
        return Register.register(user_data)

    def authentication(self, login, password):
        return Authentication.authentication(login, password)
        
    def get_current_user(self):
        user_account = account.get_account_by_id()
        user_person = person.get_person_by_id()
        return [user_account, user_person]

    def start_battle(self):
        self.arena = Arena()

    def get_battle_next_step(self, status, position_in_activ_cards='', position_in_field=''):
        buttle_data = self.arena.status_action(status, position_in_activ_cards, position_in_field)
        return buttle_data
    
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
