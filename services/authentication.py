import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.account import Account
from services.account_service import AccountService
from services.person_service import PersonService

account = AccountService()
person = PersonService()

class Authentication:
    def authentication(self, login, password):
        asnwer = account.authentication(login, password)
        account_data = account.get_account_by_login(login)
        if not isinstance((account_data), str):
            person.authentication(account_data[1])
            return asnwer
        else:
            return account_data
