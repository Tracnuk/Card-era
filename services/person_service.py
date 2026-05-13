import sys
import os
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.account_db_repository import AccountsDbRepository
from repositories.person_db_repository import PersonsDbRepository
from models.account import Account
from models.person import Person

person_db_storage = PersonsDbRepository()
account_db_storage = AccountsDbRepository()

class PersonService:
    @staticmethod
    def create_person(first_name):
        """Создаёт новые персональные данные. Возвращает ID человека или сообщение об ошибке."""
        try:
            person = Person(first_name)
            person_id = person_db_storage.add_person(person)
            return person_id
        except Exception as e:
            return f'Ошибка создания прсональных данных: {str(e)}'

    @staticmethod
    def delete_person(person_id):
        """Удаляет человека по ID. Возвращает сообщение об успехе или ошибке."""
        if not person_id:
            return 'ID человека не указан!'
        try:
            person_db_storage.delete_person(person_id)
            return (True, 'Персональные данные были удалёны.')
        except sqlite3.Error as e:
            return (False, f'Ошибка удаления персональных данных: {str(e)}')

    @staticmethod
    def update_person(person_id, new_first_name, account_id,
                     new_surname='', new_last_name='', new_email='', new_phone_number=''):
        """Обновляет данные человека. Возвращает сообщение об успехе или ошибке."""
        if not person_id:
            return 'ID человека не указан!'
        try:
            updated_person = Person(
                new_first_name,
                new_surname,
                new_last_name,
                new_email,
                new_phone_number,
                account_id
            )
            updated_person.id = person_id
            person_db_storage.update_person(updated_person)
            return 'Данные обновлены.'
        except Exception as e:
            return f'Ошибка обновления данных человека: {str(e)}'

    @staticmethod
    def get_person_by_id(person_id):
        """Получает человека по ID. Возвращает объект Person или None."""
        if not person_id:
            return None
        person_data = person_db_storage.get_person_by_id(person_id)
        if person_data:
            return Person(
                id=person_data[0],
                first_name=person_data[1] if person_data[1] else '-',
                surname=person_data[2] if person_data[2] else '-',
                last_name=person_data[3] if person_data[3] else '-',
                email=person_data[4] if person_data[4] else '-',
                phone_number=person_data[5],
                account_id=person_data[6]
            )
        return None

    @staticmethod
    def get_all_persons():
        """Получает всех людей. Возвращает список объектов Person или пустой список."""
        result = person_db_storage.get_persons()
        if result:
            persons = [
                Person(
                    id=data[0],
                    first_name=data[1] if data[1] else '-',
                    surname=data[2] if data[2] else '-',
            last_name=data[3] if data[3] else '-',
            email=data[4] if data[4] else '-',
            phone_number=data[5],
            account_id=data[6]
                ) for data in result
            ]
            return persons
        return []

    @staticmethod
    def authenticate_person(person_id):
        """Аутентифицирует человека по ID. Возвращает True/False."""
        try:
            person_data = person_db_storage.get_person_by_id(person_id)
            if person_data:
                return True
            else:
                return False
        except sqlite3.Error:
            return False
