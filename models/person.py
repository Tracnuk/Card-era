from repositories.person_db_repository import PersonsDbRepository
from models.person import Person

person_db = PersonsDbRepository()


class PersonService:
    def __init__(self):
        self.current_person_id = None

    def create_person(self, first_name):
        person = Person(first_name=first_name)
        self.current_person_id = person_db.add_person(person)
        return self.current_person_id

    def update_account_id(self, person_id, account_id):
        person_db.update_account_id(person_id, account_id)

    def login(self, person_id):
        self.current_person_id = person_id

    def get_person_by_id(self):
        if not self.current_person_id:
            return None
        return person_db.get_person_by_id(self.current_person_id)

    def get_all_persons(self):
        return person_db.get_persons()

    def delete_person(self):
        if not self.current_person_id:
            return False
        person_db.delete_person(self.current_person_id)
        self.current_person_id = None
        return True
