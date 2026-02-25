import sys
import os

from services.owner_service import OwnerService

# Добавляем путь, чтобы импорты работали
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.account_service import AccountService
from services.person_service import PersonService
from repositories.settings_db_repository import SettingsDbRepository
from repositories.card_db_repository import CardDbRepository
from services.owner_service import OwnerService

class Game:
    def __init__(self):
        # Инициализируем сервисы внутри класса
        self.person_service = PersonService()
        self.account_service = AccountService()
        self.settings_db_storage = SettingsDbRepository()
        self.cards_db_storage = CardDbRepository()
        self.owner_service = OwnerService()

    # ================== РЕГИСТРАЦИЯ ==================
    def register(self, user_data):
        try:
            # 1. создаём персонажа
            person_id = self.person_service.create_person(user_data.first_name)
            if not person_id:
                return False, "Ошибка создания персонажа"

            # 2. создаём аккаунт
            account_id = self.account_service.create_account(user_data, person_id)
            if isinstance(account_id, str):
                return False, account_id

            # 3. связываем персонажа с аккаунтом
            self.person_service.update_account_id(person_id, account_id)

            return True, "✅ Регистрация прошла успешно"
        except Exception as e:
            return False, f"❌ Ошибка БД: {e}"

    # ================== ЛОГИН ==================
    def login(self, login, password):
        login_result = self.account_service.login(login, password)
        if isinstance(login_result, str):
            return False, login_result

        account_data = self.account_service.get_account_by_login(login)
        if not account_data:
            return False, "Аккаунт не найден"

        person_id = account_data.person_id
        self.person_service.login(person_id)

        return True, "✅ Успешный вход"

    # ================== ТЕКУЩИЙ ПОЛЬЗОВАТЕЛЬ ==================
    def get_current_user(self):
        account = self.account_service.get_account_by_id()
        person = self.person_service.get_person_by_id()

        if not account and not person:
            return "❌ Пользователь не найден"

        return f"Аккаунт: {account}\nПерсонаж: {person}"

    # ================== ВСЕ ПОЛЬЗОВАТЕЛИ ==================
    def get_all_users(self):
        persons = self.person_service.get_all_persons()
        accounts = self.account_service.get_all_accounts()
        return persons, accounts

    # ================== УДАЛЕНИЕ ==================
    def delete_user(self):
        person_result = self.person_service.delete_person()
        account_result = self.account_service.delete_account()

        return (
            "🗑 Персонаж удалён" if person_result else "❌ Персонаж не удалён",
            "🗑 Аккаунт удалён" if account_result else "❌ Аккаунт не удалён"
        )

    # ================== ПРОВЕРКА АВТОРИЗАЦИИ ==================
    def verification(self):
        return self.account_service.verification()
    
    def get_inventory_info(self):
        """Метод для получения текстового состава инвентаря"""
        if self.account_service.verification():
            acc_id = self.account_service.current_account_id
            # Теперь self.owner_service существует и метод сработает
            return self.owner_service.get_inventory_text(acc_id)
        return "❌ Ошибка: пользователь не авторизован."