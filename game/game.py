import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.arena import Arena
from services.register_service import Register
from services.authentication_service import Authentication
from services.account_service import AccountService
from services.person_service import PersonService
from services.settings_service import SettingsService

class Game:
    def __init__(self):
        self.current_account_id = None
        self.current_person_id = None

    def register(self, user_data):
        """Регистрирует нового пользователя. Возвращает ID аккаунта."""
        answer = Register.register(user_data)
        if isinstance(answer[0], str):
            self.current_account_id = answer[0]
            self.current_person_id = answer[1]
        SettingsService.add_cards_in_settings(answer[0])
        return answer[0]

    def authentication(self, login, password):
        """Аутентифицирует пользователя. Возвращает (сообщение, успех, person_id)."""
        message, success, person_id = Authentication.authentication(login, password)
        if success:
            self.current_account_id = AccountService.get_account_by_login(login).id
            self.current_person_id = person_id
        return (message, success)

    def get_current_user(self):
        """Получает данные текущего пользователя. Возвращает (аккаунт, человек) или (None, None)."""
        if not self.current_account_id or not self.current_person_id:
            return (None, None)
        user_account = AccountService.get_account_by_id(self.current_account_id)
        user_person = PersonService.get_person_by_id(self.current_person_id)
        return (user_account, user_person)

    def start_battle(self):
        """Запускает арену для битвы."""
        player_deck = SettingsService.get_settings_by_id(self.current_account_id)
        enemy_deck = player_deck #Костыль, потом переделать!!
        self.arena = Arena(player_deck, enemy_deck)
        return self.arena.start_buttle()

    def get_battle_next_step(self, status, position_in_activ_cards='', position_in_field=''):
        """Получает следующий шаг битвы. Возвращает данные арены или сообщение об ошибке."""
        battle_data = self.arena.status_action(status, position_in_activ_cards, position_in_field)
        return battle_data

    def get_all_users(self):
        """Получает всех пользователей системы. Возвращает (люди, аккаунты)."""
        users_persons = PersonService.get_all_persons()
        users_accounts = AccountService.get_all_accounts()
        return (users_persons, users_accounts)
    
    def update_account(self, nickname, login, password, cash=0, level=1):
        """Обновляет данные аккаунта текущего пользователя."""
        if not self.current_account_id:
            return 'Пользователь не авторизован!'
        # Получаем person_id из текущего аккаунта
        current_account = AccountService.get_account_by_id(self.current_account_id)
        if not current_account:
            return 'Аккаунт не найден!'
        result = AccountService.update_account(
            self.current_account_id,
            nickname,
            login,
            password,
            cash,
            level
        )
        return result

    def update_person(self, first_name, new_surname='', new_last_name='',
                      new_email='', new_phone_number=''):
        """Обновляет данные человека текущего пользователя."""
        if not self.current_person_id:
            return 'Пользователь не авторизован!'
        result = PersonService.update_person(
            self.current_person_id,
            first_name,
            self.current_account_id,  # account_id для связи
            new_surname,
            new_last_name,
            new_email,
            new_phone_number
        )
        return result

    def delete_user(self):
        person_answer = PersonService.delete_person(self.current_person_id)
        account_answer = AccountService.delete_account(self.current_account_id)
        SettingsService.delete_settings(self.current_account_id)
        if person_answer[0] and account_answer[0]:
            # Сброс идентификаторов после удаления
            self.current_account_id = None
            self.current_person_id = None
            return account_answer[1]
        elif person_answer[0] or account_answer[0]:
            if person_answer[0]:
                return person_answer[1]
            else:
                return account_answer[1]
        else:
            return (account_answer[1], person_answer[1])

    def verification(self):
        """Проверяет авторизацию пользователя. Возвращает True/False."""
        return bool(self.current_account_id and self.current_person_id)
