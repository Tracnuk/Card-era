import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.account import Account
from services.account_service import AccountService
from services.person_service import PersonService
from services.settings_service import SettingsService

class Register:
    def register(self, user_data):
        person_id = person.create_person(user_data.first_name)
        account_id = account.create_account(user_data, person_id)
        #сделать выдачу базовых карт
        if not isinstance(account_id, str):
            return (True, 'Добро пожаловать')
        return (False, account_id)
