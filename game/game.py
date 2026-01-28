import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.account_service import AccountService
from services.person_service import PersonService
from repositories.settings_db_repository import SettingsDbRepository
from repositories.card_db_repository import CardDbRepository

settings_db_storage = SettingsDbRepository()
cards_db_storage = CardDbRepository()

person_service = PersonService()
account_service = AccountService()


class Game:
    def __init__(self):
        pass

    # ================== РЕГИСТРАЦИЯ ==================
    def register(self, user_data):
        # 1. создаём персонажа
        person_id = person_service.create_person(user_data.first_name)
        if not person_id:
            return False, "Ошибка создания персонажа"

        # 2. создаём аккаунт
        account_id = account_service.create_account(user_data, person_id)
        if isinstance(account_id, str):
            return False, account_id

        # 3. ЖЁСТКО связываем персонажа с аккаунтом
        person_service.update_account_id(person_id, account_id)

        return True, "✅ Регистрация прошла успешно"

    # ================== ЛОГИН ==================
    def login(self, login, password):
        login_result = account_service.login(login, password)
        if isinstance(login_result, str):
            return False, login_result

        account_data = account_service.get_account_by_login(login)
        if not account_data:
            return False, "Аккаунт не найден"

        person_id = account_data.person_id
        person_service.login(person_id)

        return True, "✅ Успешный вход"

    # ================== ТЕКУЩИЙ ПОЛЬЗОВАТЕЛЬ ==================
    def get_current_user(self):
        account = account_service.get_account_by_id()
        person = person_service.get_person_by_id()

        if not account and not person:
            return "❌ Пользователь не найден"

        return [account, person]

    # ================== ВСЕ ПОЛЬЗОВАТЕЛИ ==================
    def get_all_users(self):
        persons = person_service.get_all_persons()
        accounts = account_service.get_all_accounts()
        return persons, accounts

    # ================== УДАЛЕНИЕ ==================
    def delete_user(self):
        person_result = person_service.delete_person()
        account_result = account_service.delete_account()

        return (
            "🗑 Персонаж удалён" if person_result else "❌ Персонаж не удалён",
            "🗑 Аккаунт удалён" if account_result else "❌ Аккаунт не удалён"
        )

    # ================== ПРОВЕРКА АВТОРИЗАЦИИ ==================
    def verification(self):
        return account_service.verification()
