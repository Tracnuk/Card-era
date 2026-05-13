import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.account import Account
from services.account_service import AccountService
from services.person_service import PersonService
from services.settings_service import SettingsService

class Register:
    def register(user_data):
        person_id = PersonService.create_person(user_data.first_name)
        account_id = AccountService.create_account(user_data, person_id)
        if isinstance(person_id, int) and isinstance(account_id, int):
            PersonService.update_person(person_id, user_data.first_name, account_id)
            SettingsService.add_cards_in_settings(account_id)
        elif isinstance(person_id, int):
            PersonService.delete_person(person_id)
        else:
            AccountService.delete_account(account_id)
        return (account_id, person_id)
