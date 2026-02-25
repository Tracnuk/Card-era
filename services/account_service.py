import sys
import os
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.account_db_repository import AccountsDbRepository
from repositories.person_db_repository import PersonsDbRepository
from repositories.settings_db_repository import SettingsDbRepository
from repositories.card_db_repository import CardDbRepository
from services.owner_service import OwnerService # Подключаем инвентарь

from models.account import Account
from models.person import Person

# Инициализация хранилищ
settings_db_storage = SettingsDbRepository()
cards_db_storage = CardDbRepository()
person_db_storage = PersonsDbRepository()
account_db_storage = AccountsDbRepository()
owner_service = OwnerService() # Создаем объект инвентаря

class AccountService:
    def __init__(self):
        self.current_account_id = None
        
    def create_account(self, user_data, person_id):
        """Регистрация: создание аккаунта + стартовая колода + карты в инвентарь"""
        try:
            account = Account(user_data.nickname, user_data.login, user_data.password, person_id)
            account_id = account_db_storage.add_account(account)
            
            if not account_id:
                return "Ошибка: БД не вернула ID аккаунта"
                
            self.current_account_id = account_id
            
            # 1. Собираем стартовую колоду для настроек (чтобы сразу можно было в бой)
            cards = []
            for card_id in range(1, 6):
                card_data = cards_db_storage.get_card_by_id(card_id)
                cards.append(card_data[0] if card_data else 0)

            settings_db_storage.add_cards_id(
                self.current_account_id,
                cards[0], cards[1], cards[2], cards[3], cards[4]
            )

            # 2. ВАЖНО: Добавляем эти же карты в инвентарь владельца
            # Это связывает AccountService и OwnerService
            owner_service.give_starter_pack(self.current_account_id)
            
            return account_id

        except sqlite3.IntegrityError:
            return 'Пользователь с таким логином уже существует!'
        except Exception as e:
            print(f"DEBUG ERROR: {e}") 
            return f'Ошибка создания аккаунта: {str(e)}'
        
    def login(self, login, password):
        """Вход в аккаунт"""
        if account_db_storage.verification(login, password):
            account = account_db_storage.get_account_by_login(login)
            self.current_account_id = account[0]
            return f'Добро пожаловать {account[2]}'
        else:
            return 'Неправильный логин или пароль!'

    def delete_account(self):
        """Удаление аккаунта и связанных карт"""
        if self.current_account_id is not None:
            # Сначала чистим карты в инвентаре
            owner_service.delete_all_cards(self.current_account_id)
            # Потом удаляем аккаунт
            account_db_storage.delete_account(self.current_account_id)
            self.current_account_id = None
            return 'Аккаунт и инвентарь был удалён.'
        return 'Вы не вошли в аккаунт!'

    def update_account(self, new_nickname, new_login, new_password):
        """Обновление данных текущего игрока"""
        if self.current_account_id is not None:
            account_db_storage.update_account(
                account_id=self.current_account_id, 
                nickname=new_nickname, 
                login=new_login, 
                password=new_password
            )
            return 'Данные обновлены.'
        return 'Вы не вошли в аккаунт!'

    def verification(self):
        """Проверка авторизации"""
        return self.current_account_id is not None
    
    def get_account_by_id(self, account_id=None):
        target_id = account_id if account_id is not None else self.current_account_id
        if target_id is not None:
            return account_db_storage.get_account_by_id(target_id)
        return "Вы не вошли в аккаунт!"

    def import_deck_of_cards(self):
        """Загрузка текущей колоды из настроек"""
        if self.current_account_id:
            return settings_db_storage.get_settings_by_id(self.current_account_id)
        return None

    def get_all_accounts(self):
        """Для админ-панели: список всех игроков"""
        result = account_db_storage.get_all_accounts()
        if result and len(result) > 0:
            accounts = [Account(
                account_id = data[0],
                person_id = data[1],
                nickname = data[2],
                login = data[3],
                password = data[4] if data[4] else '-',
                cash = data[5] if data[5] else '-',
                level = data[6] if data[6] else '-'
            ) for data in result]
            return accounts
        return ['Нет данных']