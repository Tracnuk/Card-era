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

class AccountService:
    @staticmethod
    def create_account(user_data, person_id):
        """Создаёт новый аккаунт. Возвращает ID аккаунта или сообщение об ошибке."""
        try:
            # Проверяем, существует ли аккаунт с таким логином
            existing_account = account_db_storage.get_account_by_login(user_data.login)
            if existing_account:
                return '\nПользователь с таким логином уже существует!\n'

            account = Account(user_data.nickname, user_data.login, user_data.password, person_id)
            account_id = account_db_storage.add_account(account)
            return account_id
        except sqlite3.IntegrityError as e:
            return f'Ошибка целостности данных: {str(e)}'
        except Exception as e:
            return f'Неожиданная ошибка создания аккаунта: {str(e)}'

    @staticmethod
    def delete_account(account_id):
        """Удаляет аккаунт по ID. Возвращает сообщение об успехе или ошибке."""
        try:
            account_db_storage.delete_account(account_id)
            return (True, 'Аккаунт был удалён.')
        except sqlite3.Error as e:
            return (False, f'Ошибка удаления аккаунта: {str(e)}')

    @staticmethod
    def update_account(account_id, new_nickname, new_login, new_password, cash, level):
        """Обновляет данные аккаунта. Возвращает сообщение об успехе или ошибке."""
        # Проверяем, не занят ли новый логин другим аккаунтом (кроме текущего)
        existing_account = account_db_storage.get_account_by_login(new_login)
        if existing_account and existing_account[0] != account_id:
            return 'Логин уже занят другим пользователем!'

        updated_account = Account(
            new_nickname,
            new_login,
            new_password,
            existing_account[1],  # person_id из существующей записи
            cash,
            level
        )
        updated_account.id = account_id
        account_db_storage.update_accounts(updated_account)
        return 'Данные обновлены.'

    @staticmethod
    def authentication(login, password):
        """Аутентифицирует пользователя. Возвращает кортеж (сообщение, успех)."""
        if account_db_storage.authentication(login, password):
            name = account_db_storage.get_account_by_login(login)[2]
            return (f'\nДобро пожаловать, {name}!\n', True)
        else:
            return ('\nНеправильный логин или пароль!\n', False)

    @staticmethod
    def get_account_by_id(account_id):
        """Получает аккаунт по ID. Возвращает объект Account или None."""
        if not account_id:
            return None
        account_data = account_db_storage.get_account_by_id(account_id)
        if account_data:
            return Account(
                account_id=account_data[0],
                person_id=account_data[1],
                nickname=account_data[2],
                login=account_data[3],
                password=account_data[4] if account_data[4] else '-',
                cash=account_data[5] if account_data[5] else '-',
                level=account_data[6] if account_data[6] else '-'
            )
        return None

    @staticmethod
    def get_all_accounts():
        """Получает все аккаунты. Возвращает список объектов Account или пустой список."""
        result = account_db_storage.get_all_accounts()
        if result:
            accounts = [
                Account(
                    account_id=data[0],
                    person_id=data[1],
                    nickname=data[2],
                    login=data[3],
                    password=data[4] if data[4] else '-',
                    cash=data[5] if data[5] else '-',
            level=data[6] if data[6] else '-'
                ) for data in result
            ]
            return accounts
        return []

    @staticmethod
    def get_account_by_login(login):
        """Получает аккаунт по логину. Возвращает объект Account или None."""
        try:
            account_data = account_db_storage.get_account_by_login(login)
            if account_data:
                return Account(
                    account_id=account_data[0],
                    person_id=account_data[1],
                    nickname=account_data[2],
                    login=account_data[3],
                    password=account_data[4] if account_data[4] else '-',
                    cash=account_data[5] if account_data[5] else '-',
                    level=account_data[6] if account_data[6] else '-'
                )
            else:
                return None
        except sqlite3.Error as e:
            print(f'Ошибка базы данных в get_account_by_login: {str(e)}')
            return None

    @staticmethod
    def verify_credentials(login, password):
        """Проверяет учётные данные без вывода приветствия. Возвращает True/False."""
        return bool(account_db_storage.authentication(login, password))
