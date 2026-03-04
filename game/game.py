from services.owner_service import OwnerService
# Импортируем созданный выше объект
from repositories.user_repository import user_storage

class Game:
    def __init__(self):
        self.current_user = None
        self.owner_service = OwnerService()

    def register(self, user_dto):
        success, message = user_storage.create_user(user_dto)
        if success:
            # 1. Сначала логинимся, чтобы получить ID нового игрока
            user = user_storage.auth_user(user_dto.login, user_dto.password)
            if user:
                # 2. Выдаем карту (ID карты 1 — твой воробей)
                from repositories.card_ownership import card_ownership_storage
                card_ownership_storage.add_card_and_account(2, user[0])  # user[0] — это ID аккаунта
                return True, "✅ Регистрация успешна! Воробей уже в инвентаре."
        return success, message

    def login(self, login, password):
        user = user_storage.auth_user(login, password)
        if user:
            self.current_user = user
            return True
        return False

    def verification(self):
        return self.current_user is not None

    def login(self, login, password):
        from repositories.user_repository import user_storage
        from repositories.card_ownership import card_ownership_storage
        
        user = user_storage.auth_user(login, password)
        if user:
            self.current_user = user
            uid = user[0]
            
            # ПРОВЕРКА: Если у игрока вообще нет карт, выдаем стартовую карту №1
            user_cards = card_ownership_storage.get_cards_in_account(uid)
            if not user_cards:
                # Дарим карту №1 (Воробей) сразу в базу данных
                card_ownership_storage.add_card_and_account(1, uid)
            
            return True
        return False

    def get_current_user(self):
        if not self.current_user:
            return "❌ Вы не вошли в аккаунт!"
        u = self.current_user
        return (
            f"👤 <b>Профиль игрока</b>\n"
            f"Ник: <b>{u[1]}</b>\n"
            f"Имя героя: <b>{u[4]}</b>\n"
            f"💰 Золото: <code>{u[5]}</code>\n"
            f"🏆 Уровень: <code>{u[6]}</code>"
        )

    def get_inventory_info(self):
        if not self.verification():
            return "❌ Сначала войдите в аккаунт!"
        
        account_id = self.current_user[0]
        
        # Проверяем, есть ли карты
        cards = self.owner_service.get_inventory_text(account_id)
        
        # Если карт нет (текст содержит "пуст"), выдаем стартовную карту
        if "пуст" in cards.lower():
            from repositories.card_ownership import card_ownership_storage
            # Выдаем карту №1 (Воробей) текущему игроку
            card_ownership_storage.add_card_and_account(4, account_id)
            # Запрашиваем текст инвентаря снова
            cards = self.owner_service.get_inventory_text(account_id)
            
        return cards
    
    def logout(self):
        """Сбрасывает сессию текущего пользователя"""
        self.current_user = None
        return True