import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.account_service import AccountService
from services.person_service import PersonService
from repositories.settings_db_repository import SettingsDbRepository
from repositories.card_db_repository import CardDbRepository
from models.user_registration import UserRegistrationDTO

# === Сервисы и репозитории ===
settings_db_storage = SettingsDbRepository()
cards_db_storage = CardDbRepository()
person = PersonService()
account = AccountService()


class Game:
    def __init__(self):
        self.users = []

    # === Регистрация нового пользователя ===
    def register(self, user_data: UserRegistrationDTO):
        person_id = person.create_person(user_data.first_name)

        account_id = account.create_account(user_data, person_id)

        if account_id is None:
            return "❌ Ошибка создания аккаунта!"
        elif isinstance(account_id, str):  # если вернулась ошибка
            return account_id
        else:
            # Обновляем персонажа с привязкой к аккаунту
            person.update_person(user_data.first_name, account_id)
            return f"✅ Добро пожаловать, {user_data.first_name}!"

    # === Вход в аккаунт ===
    def login(self, login: str, password: str):
        answer = account.login(login, password)
        account_data = account.get_account_by_login(login)

        if account_data is None:
            return "❌ Аккаунт не найден!"
        else:
            person_id = account_data[1]  # безопасно
            person.login(person_id)
            return f"✅ {answer}"

    # === Получить текущего пользователя ===
    def get_current_user(self):
        user_account = account.get_account_by_id()
        user_person = person.get_person_by_id()

        text_account = str(user_account) if user_account else "Нет аккаунта"
        text_person = str(user_person) if user_person else "Нет персонажа"

        return f"👤 Текущий пользователь:\nАккаунт: {text_account}\nПерсона: {text_person}"

    # === Получить всех пользователей ===
    def get_all_users(self):
        users_persons = person.get_all_persons()
        users_accounts = account.get_all_accounts()

        text_persons = "\n".join([str(u) for u in users_persons]) if users_persons else "Нет персонажей"
        text_accounts = "\n".join([str(a) for a in users_accounts]) if users_accounts else "Нет аккаунтов"

        return f"👥 Все пользователи:\nПерсонажи:\n{text_persons}\nАккаунты:\n{text_accounts}"

    # === Удаление текущего пользователя ===
    def delete_user(self):
        person_answer = person.delete_person()
        account_answer = account.delete_account()

        # Возвращаем строку, чтобы Telegram не ругался
        return f"🗑️ {person_answer}\n🗑️ {account_answer}"

    # === Проверка авторизации ===
    def verification(self):
        return account.verification()

