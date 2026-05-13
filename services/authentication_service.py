import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.account import Account
from services.account_service import AccountService
from services.person_service import PersonService

class Authentication:
    @staticmethod
    def authentication(login, password):
        """Аутентифицирует пользователя по логину и паролю.
        Возвращает (сообщение, успех, person_id) или (сообщение, False, None)."""
        # Аутентификация аккаунта
        message, success = AccountService.authentication(login, password)
        if success:
            # Получаем данные аккаунта по логину
            account_data = AccountService.get_account_by_login(login)
            if not account_data:
                return ('Аккаунт найден при аутентификации, но не найден в БД!', False, None)

            # Извлекаем person_id из данных аккаунта
            person_id = account_data.person_id

            # Проверяем существование человека с этим person_id
            is_person_valid = PersonService.authenticate_person(person_id)
            if is_person_valid:
                return (message, True, person_id)
            else:
                return ('Человек, связанный с аккаунтом, не найден!', False, None)
        else:
            return (message, False, None)
