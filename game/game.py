from services.owner_service import OwnerService
from repositories.user_repository import user_storage

class Game:
    def __init__(self):
        self.current_user = None
        self.owner_service = OwnerService()

    def register(self, user_dto):
        success, message = user_storage.create_user(user_dto)
        if success:
            user = user_storage.auth_user(user_dto.login, user_dto.password)
            if user:
                from repositories.card_ownership import card_ownership_storage
                # Выдаём 5 воробьёв (ID 5)
                for _ in range(5):
                    card_ownership_storage.add_card_and_account(5, user[0])
                return True, "✅ Регистрация успешна! 5 воробьёв уже в инвентаре."
        return success, message

    def login(self, login, password):
        from repositories.user_repository import user_storage
        user = user_storage.auth_user(login, password)
        if user:
            self.current_user = user
            return True
        return False

    def verification(self):
        return self.current_user is not None

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
        return self.owner_service.get_inventory_text(account_id)

    def logout(self):
        self.current_user = None
        return True