from account_service import AccountService
from person import Person
from person_service import PersonService


class Game:
    def __init__(self):
        self.users = []

    def register(self, user_data):
        person = PersonService()
        person_id = person.create_person(user_data.first_name)
        account = AccountService()
        account.create_account(user_data)
        

n = int(input())